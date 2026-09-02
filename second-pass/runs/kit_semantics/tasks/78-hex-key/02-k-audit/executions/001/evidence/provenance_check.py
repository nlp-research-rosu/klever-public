#!/usr/bin/env python3
"""Independent structural and hash checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Launcher-compatible tree hash, independently reimplemented here."""
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise AssertionError(f"tree root is not a real directory: {root}")
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(
                    f"tree contains symlink or unsupported entry: {path}"
                )
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode) or stat.S_ISLNK(mode):
        raise AssertionError(f"not a regular non-symlink file: {path}")
    if not os.access(path, os.R_OK):
        raise AssertionError(f"not readable: {path}")


def compare_trees(trusted: Path, candidate: Path) -> None:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        entries: dict[str, tuple[str, str | None]] = {}
        for path in sorted(root.rglob("*")):
            rel = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                entries[rel] = ("symlink", os.readlink(path))
            elif stat.S_ISDIR(mode):
                entries[rel] = ("directory", None)
            elif stat.S_ISREG(mode):
                entries[rel] = ("file", sha256(path))
            else:
                entries[rel] = ("other", f"{mode:o}")
        return entries

    trusted_entries = inventory(trusted)
    candidate_entries = inventory(candidate)
    if trusted_entries != candidate_entries:
        trusted_only = sorted(trusted_entries.keys() - candidate_entries.keys())
        candidate_only = sorted(candidate_entries.keys() - trusted_entries.keys())
        changed = sorted(
            key
            for key in trusted_entries.keys() & candidate_entries.keys()
            if trusted_entries[key] != candidate_entries[key]
        )
        raise AssertionError(
            "semantics tree mismatch: "
            f"trusted_only={trusted_only}, candidate_only={candidate_only}, "
            f"changed_or_mistyped={changed}"
        )
    symlinks = [
        rel for rel, (kind, _) in candidate_entries.items() if kind == "symlink"
    ]
    if symlinks:
        raise AssertionError(f"candidate semantics contains symlinks: {symlinks}")
    print(
        "REFERENCE_SEMANTICS_TREE: exact recursive type/content match; "
        f"{len(candidate_entries)} entries; no symlinks"
    )


audit_input_path = Path("/audit-input.json")
campaign_lock_path = Path("/audit-campaign-lock.json")
require_regular(audit_input_path)
require_regular(campaign_lock_path)
audit_input = json.loads(audit_input_path.read_text())
campaign_lock = json.loads(campaign_lock_path.read_text())

assert audit_input["record_layout"] == "pipeline-v3"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert audit_input["mount_reference_semantics"] is True
assert audit_input["audit_campaign"] == campaign_lock
assert (
    sha256(campaign_lock_path)
    == audit_input["hashes"]["audit_campaign_lock_sha256"]
)
print("CAMPAIGN_LOCK: block equality and recorded SHA-256 match")

container_paths = audit_input["container_paths"]
declared_mounts = {
    "audit_campaign_lock",
    "candidate",
    "canonical",
    "generation_last",
    "generation_manifest",
    "generation_metrics",
    "generation_output",
    "generation_root",
    "generation_trace",
    "run_manifest",
    "stage1_result",
    "task_manifest",
    "translator",
    "trusted_prompt",
}
assert declared_mounts <= container_paths.keys()
for key in sorted(declared_mounts):
    path = Path(container_paths[key])
    if not path.exists():
        raise AssertionError(f"missing launcher-declared mount {key}: {path}")
    print(f"MOUNT {key}: {path}")

required_pipeline_files = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]
for path in required_pipeline_files:
    require_regular(path)
print(f"PIPELINE_V3_REQUIRED_RECORDS: {len(required_pipeline_files)} regular files")

recorded_file_hashes = {
    Path("/audit-campaign-lock.json"): "audit_campaign_lock_sha256",
    Path("/reference/canonical.py"): "canonical_sha256",
    Path("/reference/prompt.py"): "trusted_prompt_sha256",
    Path("/reference/py2mpy.py"): "trusted_translator_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
    Path("/run.json"): "run_manifest_sha256",
    Path("/task.json"): "task_manifest_sha256",
    Path("/generation-result.json"): "stage1_result_sha256",
    Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
    Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
    Path("/generation-evidence/runtime-metrics.json"):
        "generation_runtime_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
    Path("/generation-evidence/codex-output.log"):
        "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
}
for path, key in recorded_file_hashes.items():
    require_regular(path)
    actual = sha256(path)
    expected = audit_input["hashes"][key]
    if actual != expected:
        raise AssertionError(
            f"hash mismatch for {path}: expected={expected} actual={actual}"
        )
    print(f"SHA256 {path}: {actual} MATCH")

assert Path("/candidate/prompt.py").read_bytes() == Path(
    "/reference/prompt.py"
).read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path(
    "/reference/py2mpy.py"
).read_bytes()
print("PROMPT_AND_TRANSLATOR: byte-identical to trusted mounts")

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = Path("/candidate/reference-semantics")
if not trusted_semantics.is_dir():
    raise AssertionError("SUPPLIED_SEMANTICS trusted tree is absent")
if not candidate_semantics.is_dir():
    raise AssertionError("candidate reference-semantics tree is absent")
compare_trees(trusted_semantics, candidate_semantics)

manifest_tree_hashes = {
    candidate_semantics:
        audit_input["hashes"]["trusted_reference_semantics_manifest_sha256"],
    trusted_semantics:
        audit_input["hashes"]["trusted_reference_semantics_manifest_sha256"],
}
for path, expected in manifest_tree_hashes.items():
    actual = sha256_tree(path)
    if actual != expected:
        raise AssertionError(
            f"manifest tree hash mismatch for {path}: "
            f"expected={expected} actual={actual}"
        )
    print(f"MANIFEST_TREE_SHA256 {path}: {actual} MATCH")

# Record independently computed whole-tree hashes as additional evidence. The
# audit-input aggregate fields use a separate launcher digest scheme; their
# security-relevant contents are checked above by exact recursive comparison
# and below by every recorded regular-file/trace hash.
candidate_pipeline_tree_sha256 = sha256_tree(Path("/candidate"))
trace_pipeline_tree_sha256 = sha256_tree(
    Path("/generation-evidence/codex-trace")
)
print(
    f"INDEPENDENT_TREE_SHA256 /candidate: "
    f"{candidate_pipeline_tree_sha256}"
)
print(
    f"INDEPENDENT_TREE_SHA256 /generation-evidence/codex-trace: "
    f"{trace_pipeline_tree_sha256}"
)
assert (
    audit_input["hashes"]["candidate_reference_semantics_sha256"]
    == audit_input["hashes"]["trusted_reference_semantics_sha256"]
)
print(
    "AUDIT_AGGREGATE_SEMANTICS_HASHES: candidate/trusted recorded values agree"
)

candidate_deliverables = [
    Path("/candidate/solution.py"),
    Path("/candidate/solution.mpy"),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
    Path("/candidate/prove.sh"),
    Path("/candidate/PROOF.md"),
]
for path in candidate_deliverables:
    require_regular(path)
print(f"CANDIDATE_REQUIRED_DELIVERABLES: {len(candidate_deliverables)} regular files")

generation_result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(
    Path("/generation-evidence/invocation.json").read_text()
)
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
assert (
    candidate_pipeline_tree_sha256
    == generation_result["outputs"]["workspace_sha256"]
    == invocation["outputs"]["workspace_sha256"]
)
assert trace_pipeline_tree_sha256 == usage["source_trace_sha256"]
print("INDEPENDENT_TREE_HASHES: match generation-result/invocation/usage records")
for record_name, record in [
    ("generation-result", generation_result),
    ("invocation", invocation),
]:
    for relative, expected in record["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256(path)
        if actual != expected:
            raise AssertionError(
                f"{record_name} evidence mismatch {relative}: "
                f"expected={expected} actual={actual}"
            )
        print(f"{record_name.upper()} EVIDENCE {relative}: {actual} MATCH")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
if not trace_files:
    raise AssertionError("structured trace contains no regular file")
trace_counts: Counter[str] = Counter()
line_count = 0
for path in trace_files:
    require_regular(path)
    with path.open() as handle:
        for line_number, line in enumerate(handle, start=1):
            line_count += 1
            event = json.loads(line)
            trace_counts[str(event.get("type", "<missing>"))] += 1
print(
    "STRUCTURED_TRACE: "
    f"{len(trace_files)} files, {line_count} parseable JSONL records, "
    f"top-level types={dict(trace_counts)}"
)

print("PROVENANCE_CHECK: PASS")
