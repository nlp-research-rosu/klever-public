#!/usr/bin/env python3
"""Independent integrity checks over launcher-owned and mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def regular_nonsymlink(path: Path) -> bool:
    mode = path.lstat().st_mode
    return stat.S_ISREG(mode) and not stat.S_ISLNK(mode)


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    for current, directories, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        for name in sorted(directories + files):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[relative] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", digest(path))
            else:
                result[relative] = ("other", oct(mode))
    return result


def manifest_digest(manifest: dict[str, tuple[str, str | None]]) -> str:
    encoded = json.dumps(
        manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reproduce the length/type/size-delimited launcher tree hash."""
    manifest = tree_manifest(root)
    hasher = hashlib.sha256()
    for relative, (kind, value) in sorted(manifest.items()):
        encoded = relative.encode()
        hasher.update(len(encoded).to_bytes(4, "big"))
        hasher.update(encoded)
        hasher.update(kind.encode() + b"\0")
        if kind == "file":
            path = root / relative
            size = path.stat(follow_symlinks=False).st_size
            hasher.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    hasher.update(chunk)
        elif kind not in {"directory"}:
            raise RuntimeError(f"unsupported tree entry for pipeline digest: {relative}")
    return hasher.hexdigest()


def legacy_tree_digest(root: Path) -> str:
    """Reproduce the legacy path-NUL-kind-NUL-content tree hash."""
    manifest = tree_manifest(root)
    hasher = hashlib.sha256()
    for relative, (kind, value) in sorted(manifest.items()):
        hasher.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            with (root / relative).open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    hasher.update(chunk)
        elif kind not in {"directory"}:
            raise RuntimeError(f"unsupported tree entry for legacy digest: {relative}")
    return hasher.hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
campaign = json.loads(CAMPAIGN_LOCK.read_text())
failures: list[str] = []

print(f"audit-input regular non-symlink: {regular_nonsymlink(AUDIT_INPUT)}")
print(f"campaign-lock regular non-symlink: {regular_nonsymlink(CAMPAIGN_LOCK)}")
actual_lock_digest = digest(CAMPAIGN_LOCK)
recorded_lock_digest = audit["hashes"]["audit_campaign_lock_sha256"]
print(f"campaign lock sha256 actual:   {actual_lock_digest}")
print(f"campaign lock sha256 recorded: {recorded_lock_digest}")
if actual_lock_digest != recorded_lock_digest:
    failures.append("campaign lock byte hash mismatch")
if campaign != audit["audit_campaign"]:
    failures.append("campaign lock JSON differs from audit_campaign block")
print(f"campaign block structural match: {campaign == audit['audit_campaign']}")

expected_layout = "legacy-selected-stage1"
print(f"record layout: {audit.get('record_layout')}")
if audit.get("record_layout") != expected_layout:
    failures.append(f"unexpected record layout, wanted {expected_layout}")

print(f"semantics mode: {audit.get('semantics_mode')}")
if audit.get("semantics_mode") != "SUPPLIED_SEMANTICS":
    failures.append("semantics mode is not SUPPLIED_SEMANTICS")
if not Path("/reference/reference-semantics").is_dir():
    failures.append("trusted supplied semantics tree missing")

print("container path mounts:")
for name, value in sorted(audit["container_paths"].items()):
    path = Path(value)
    readable = os.access(path, os.R_OK)
    print(
        f"  {name}: {path} exists={path.exists()} readable={readable} "
        f"symlink={path.is_symlink()}"
    )
    if not path.exists() or not readable or path.is_symlink():
        failures.append(f"bad launcher-declared provenance mount: {name}")

required = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
usage = Path("/generation-evidence/usage.json")
if usage.exists():
    required.append(usage)
trace_root = Path("/generation-evidence/codex-trace")
required.append(trace_root)

print("required record types:")
for path in required:
    if path == trace_root:
        okay = path.is_dir() and not path.is_symlink() and os.access(path, os.R_OK)
        kind = "directory"
    else:
        okay = path.exists() and regular_nonsymlink(path) and os.access(path, os.R_OK)
        kind = "regular file"
    print(f"  {path}: expected={kind} okay={okay}")
    if not okay:
        failures.append(f"missing, unreadable, mistyped, or symlinked record: {path}")

trace_files = sorted(trace_root.rglob("*"))
print("trace entries:")
for path in trace_files:
    print(
        f"  {path.relative_to(trace_root)} "
        f"type={'symlink' if path.is_symlink() else 'dir' if path.is_dir() else 'file'}"
    )
    if path.is_symlink() or (not path.is_dir() and not regular_nonsymlink(path)):
        failures.append(f"bad trace entry type: {path}")
if not any(path.is_file() and not path.is_symlink() for path in trace_files):
    failures.append("structured trace contains no regular file")

hash_pairs = {
    "audit_campaign_lock_sha256": CAMPAIGN_LOCK,
    "candidate_prompt_sha256": Path("/candidate/prompt.py"),
    "candidate_translator_sha256": Path("/candidate/py2mpy.py"),
    "canonical_sha256": Path("/reference/canonical.py"),
    "generation_codex_last_sha256": Path("/generation-evidence/codex-last.txt"),
    "generation_codex_output_sha256": Path("/generation-evidence/codex-output.log"),
    "generation_metrics_sha256": Path("/generation-evidence/metrics.json"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "run_manifest_sha256": Path("/run.json"),
    "stage1_invocation_sha256": Path("/generation-evidence/invocation.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "task_manifest_sha256": Path("/task.json"),
    "trusted_prompt_sha256": Path("/reference/prompt.py"),
    "trusted_translator_sha256": Path("/reference/py2mpy.py"),
}
print("recorded leaf-file hashes:")
for field, path in hash_pairs.items():
    actual = digest(path)
    recorded = audit["hashes"][field]
    match = actual == recorded
    print(f"  {field}: match={match} actual={actual} recorded={recorded}")
    if not match:
        failures.append(f"recorded hash mismatch: {field}")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
declared_evidence = result["outputs"]["evidence"]
print("generation-result evidence hashes:")
for relative, recorded in sorted(declared_evidence.items()):
    path = Path("/generation-evidence") / relative
    okay = path.exists() and regular_nonsymlink(path) and digest(path) == recorded
    print(f"  {relative}: okay={okay}")
    if not okay:
        failures.append(f"generation-result evidence mismatch: {relative}")
print(
    "invocation/result evidence maps match:",
    invocation["outputs"]["evidence"] == declared_evidence,
)
if invocation["outputs"]["evidence"] != declared_evidence:
    failures.append("invocation and result evidence maps differ")

trace_declared = {
    relative: recorded
    for relative, recorded in declared_evidence.items()
    if relative.startswith("codex-trace/")
}
actual_trace_relative = {
    path.relative_to(Path("/generation-evidence")).as_posix()
    for path in trace_root.rglob("*")
    if path.is_file() and not path.is_symlink()
}
print(
    "declared/actual trace file set match:",
    set(trace_declared) == actual_trace_relative,
)
if set(trace_declared) != actual_trace_relative:
    failures.append("declared and actual structured trace sets differ")

candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
print(f"candidate semantics entries: {len(candidate_semantics)}")
print(f"trusted semantics entries:   {len(trusted_semantics)}")
print(
    "candidate semantics manifest digest:",
    manifest_digest(candidate_semantics),
)
print(
    "trusted semantics manifest digest:  ",
    manifest_digest(trusted_semantics),
)
print("semantics trees exact entry/type/byte match:", candidate_semantics == trusted_semantics)
if candidate_semantics != trusted_semantics:
    failures.append("candidate supplied semantics tree differs from trusted tree")
    for key in sorted(set(candidate_semantics) | set(trusted_semantics)):
        if candidate_semantics.get(key) != trusted_semantics.get(key):
            print(
                f"  DIFFERENCE {key}: "
                f"candidate={candidate_semantics.get(key)} "
                f"trusted={trusted_semantics.get(key)}"
            )

generation_result = json.loads(Path("/generation-result.json").read_text())
usage_record = json.loads(Path("/generation-evidence/usage.json").read_text())
tree_hash_checks = [
    (
        "pipeline candidate/workspace tree",
        Path("/candidate"),
        pipeline_tree_digest(Path("/candidate")),
        generation_result["outputs"]["workspace_sha256"],
    ),
    (
        "pipeline candidate semantics tree",
        Path("/candidate/reference-semantics"),
        pipeline_tree_digest(Path("/candidate/reference-semantics")),
        audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    ),
    (
        "pipeline trusted semantics tree",
        Path("/reference/reference-semantics"),
        pipeline_tree_digest(Path("/reference/reference-semantics")),
        audit["hashes"]["trusted_reference_semantics_manifest_sha256"],
    ),
    (
        "pipeline structured-trace tree",
        Path("/generation-evidence/codex-trace"),
        pipeline_tree_digest(Path("/generation-evidence/codex-trace")),
        usage_record["source_trace_sha256"],
    ),
]
print("independent aggregate tree hashes with same-format recorded counterparts:")
for label, path, actual, recorded in tree_hash_checks:
    match = actual == recorded
    print(
        f"  {label}: path={path} match={match} "
        f"actual={actual} recorded={recorded}"
    )
    if not match:
        failures.append(f"recorded aggregate tree hash mismatch: {label}")
print("other launcher-recorded aggregate digests (different declared formats):")
for field in (
    "candidate_tree_sha256",
    "candidate_reference_semantics_sha256",
    "generation_codex_trace_sha256",
    "trusted_reference_semantics_legacy_sha256",
    "trusted_reference_semantics_sha256",
):
    print(f"  {field}={audit['hashes'][field]}")

for candidate_file, trusted_file, label in [
    (Path("/candidate/prompt.py"), Path("/reference/prompt.py"), "prompt"),
    (Path("/candidate/py2mpy.py"), Path("/reference/py2mpy.py"), "translator"),
]:
    same = candidate_file.read_bytes() == trusted_file.read_bytes()
    print(f"candidate/trusted {label} byte match: {same}")
    if not same:
        failures.append(f"candidate {label} differs from trusted")

candidate_manifest = tree_manifest(Path("/candidate"))
print(f"candidate tree entries: {len(candidate_manifest)}")
print(f"candidate independent manifest digest: {manifest_digest(candidate_manifest)}")
bad_candidate_entries = [
    (name, value)
    for name, value in candidate_manifest.items()
    if value[0] in {"symlink", "other"}
]
print(f"candidate symlink/other entries: {bad_candidate_entries}")
if bad_candidate_entries:
    failures.append("candidate contains symlink or special entry")

print(f"FAILURE_COUNT: {len(failures)}")
for failure in failures:
    print(f"FAILURE: {failure}")
raise SystemExit(1 if failures else 0)
