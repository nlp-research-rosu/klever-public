#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks for the audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Reproduce the length-delimited pipeline-v3 tree digest."""
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise ValueError(f"tree root is not a real directory: {root}")
    digest = hashlib.sha256()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            child_path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = child_path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", child_path))
                pending.append(child_path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", child_path))
            else:
                raise ValueError(f"linked or unsupported tree entry: {child_path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def kind(path: Path) -> str:
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        return "file"
    if stat.S_ISDIR(mode):
        return "directory"
    if stat.S_ISLNK(mode):
        return "symlink"
    return "unsupported"


def require(path: Path, expected_kind: str) -> None:
    actual = kind(path)
    if actual != expected_kind:
        raise AssertionError(f"{path}: expected {expected_kind}, found {actual}")
    print(f"OK type {expected_kind}: {path}")


def compare_hash(label: str, actual: str, expected: str, *, required: bool = True) -> None:
    if actual == expected:
        status = "MATCH"
    elif required:
        status = "MISMATCH"
    else:
        status = "DIFFERENT-ENCODING"
    print(f"{status} {label}: actual={actual} expected={expected}")
    if required and actual != expected:
        raise AssertionError(f"{label} hash mismatch")


def tree_manifest(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            rel = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                result[rel] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[rel] = ("file", sha256_file(path))
            elif stat.S_ISLNK(mode):
                result[rel] = ("symlink", os.readlink(path))
            else:
                result[rel] = ("unsupported", None)
    return result


audit_input = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
lock = json.loads(LOCK.read_text(encoding="utf-8"))
hashes = audit_input["hashes"]

print(f"record_layout={audit_input['record_layout']}")
print(f"semantics_mode={audit_input['semantics_mode']}")
assert audit_input["record_layout"] == "legacy-selected-stage1"
assert audit_input["semantics_mode"] == "SUPPLIED_SEMANTICS"

required_files = [
    AUDIT_INPUT,
    LOCK,
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
    Path("/generation-evidence/legacy-metrics.json"),
    Path("/generation-evidence/legacy-run-input.json"),
]
if Path("/generation-evidence/usage.json").exists():
    required_files.append(Path("/generation-evidence/usage.json"))
for path in required_files:
    require(path, "file")

required_dirs = [
    Path("/candidate"),
    Path("/reference/reference-semantics"),
    Path("/generation-evidence"),
    Path("/generation-evidence/codex-trace"),
]
for path in required_dirs:
    require(path, "directory")

for label, mounted in audit_input["container_paths"].items():
    path = Path(mounted)
    if not path.exists():
        raise AssertionError(f"container_paths[{label}] missing: {path}")
    if path.is_symlink():
        raise AssertionError(f"container_paths[{label}] is a symlink: {path}")
    print(f"OK container_paths[{label}]={path} kind={kind(path)}")

assert lock == audit_input["audit_campaign"]
print("MATCH campaign lock object and audit_input.audit_campaign")

file_expectations = [
    ("audit campaign lock", LOCK, hashes["audit_campaign_lock_sha256"]),
    ("canonical", Path("/reference/canonical.py"), hashes["canonical_sha256"]),
    ("trusted prompt", Path("/reference/prompt.py"), hashes["trusted_prompt_sha256"]),
    ("trusted translator", Path("/reference/py2mpy.py"), hashes["trusted_translator_sha256"]),
    ("candidate prompt", Path("/candidate/prompt.py"), hashes["candidate_prompt_sha256"]),
    ("candidate translator", Path("/candidate/py2mpy.py"), hashes["candidate_translator_sha256"]),
    ("run manifest", Path("/run.json"), hashes["run_manifest_sha256"]),
    ("task manifest", Path("/task.json"), hashes["task_manifest_sha256"]),
    ("manifest alias", Path("/task.json"), hashes["manifest_sha256"]),
    ("stage1 result", Path("/generation-result.json"), hashes["stage1_result_sha256"]),
    (
        "stage1 invocation",
        Path("/generation-evidence/invocation.json"),
        hashes["stage1_invocation_sha256"],
    ),
    (
        "generation metrics",
        Path("/generation-evidence/metrics.json"),
        hashes["generation_metrics_sha256"],
    ),
    (
        "generation last",
        Path("/generation-evidence/codex-last.txt"),
        hashes["generation_codex_last_sha256"],
    ),
    (
        "generation output",
        Path("/generation-evidence/codex-output.log"),
        hashes["generation_codex_output_sha256"],
    ),
    (
        "generation prompt",
        Path("/generation-evidence/prompt.txt"),
        hashes["generation_prompt_sha256"],
    ),
]
if Path("/generation-evidence/usage.json").exists():
    file_expectations.append(
        (
            "generation usage",
            Path("/generation-evidence/usage.json"),
            hashes["generation_usage_sha256"],
        )
    )
for label, path, expected in file_expectations:
    require(path, "file")
    compare_hash(label, sha256_file(path), expected)

result_document = json.loads(
    Path("/generation-result.json").read_text(encoding="utf-8")
)
for relative, expected in sorted(result_document["outputs"]["evidence"].items()):
    evidence_path = Path("/generation-evidence") / relative
    require(evidence_path, "file")
    compare_hash(
        f"generation-result declared evidence {relative}",
        sha256_file(evidence_path),
        expected,
    )

candidate_tree_digest = sha256_tree(Path("/candidate"))
candidate_semantics_digest = sha256_tree(Path("/candidate/reference-semantics"))
trusted_semantics_digest = sha256_tree(Path("/reference/reference-semantics"))
trace_tree_digest = sha256_tree(Path("/generation-evidence/codex-trace"))

# The audit-input schema records both a current audit digest and, where
# applicable, the length-delimited pipeline digest. The current digest's
# implementation is launcher-side and not exposed in the container; record the
# independent length-delimited digest against its separately recorded field and
# retain the current values explicitly rather than falsely equating encodings.
compare_hash(
    "candidate tree current audit digest (different encoding)",
    candidate_tree_digest,
    hashes["candidate_tree_sha256"],
    required=False,
)
invocation_document = json.loads(
    Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
)
compare_hash(
    "candidate tree legacy pipeline digest",
    candidate_tree_digest,
    invocation_document["retained_workspace_sha256"],
)
compare_hash(
    "candidate reference semantics current audit digest (different encoding)",
    candidate_semantics_digest,
    hashes["candidate_reference_semantics_sha256"],
    required=False,
)
compare_hash(
    "candidate reference semantics manifest digest",
    candidate_semantics_digest,
    hashes["trusted_reference_semantics_manifest_sha256"],
)
compare_hash(
    "trusted reference semantics current audit digest (different encoding)",
    trusted_semantics_digest,
    hashes["trusted_reference_semantics_sha256"],
    required=False,
)
compare_hash(
    "trusted reference semantics manifest digest",
    trusted_semantics_digest,
    hashes["trusted_reference_semantics_manifest_sha256"],
)
compare_hash(
    "generation trace current audit digest (different encoding)",
    trace_tree_digest,
    hashes["generation_codex_trace_sha256"],
    required=False,
)
usage_document = json.loads(
    Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
)
compare_hash(
    "generation trace pipeline digest",
    trace_tree_digest,
    usage_document["source_trace_sha256"],
)

assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == Path("/reference/py2mpy.py").read_bytes()
print("BYTE-IDENTICAL candidate prompt.py and trusted prompt.py")
print("BYTE-IDENTICAL candidate py2mpy.py and trusted py2mpy.py")

candidate_semantics = tree_manifest(Path("/candidate/reference-semantics"))
trusted_semantics = tree_manifest(Path("/reference/reference-semantics"))
if candidate_semantics != trusted_semantics:
    only_candidate = sorted(candidate_semantics.keys() - trusted_semantics.keys())
    only_trusted = sorted(trusted_semantics.keys() - candidate_semantics.keys())
    changed = sorted(
        key
        for key in candidate_semantics.keys() & trusted_semantics.keys()
        if candidate_semantics[key] != trusted_semantics[key]
    )
    print(f"SEMANTICS only_candidate={only_candidate}")
    print(f"SEMANTICS only_trusted={only_trusted}")
    print(f"SEMANTICS changed_or_mistyped={changed}")
    raise AssertionError("candidate semantics differs recursively from trusted semantics")
print(
    "BYTE/TYPE-IDENTICAL recursive semantics trees: "
    f"{sum(value[0] == 'file' for value in candidate_semantics.values())} files, "
    f"{sum(value[0] == 'directory' for value in candidate_semantics.values())} directories"
)

for name in ("solution.py", "solution.mpy", "verification.k", "spec.k", "prove.sh"):
    require(Path("/candidate") / name, "file")

json_files = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/legacy-metrics.json"),
    Path("/generation-evidence/legacy-run-input.json"),
]
if Path("/generation-evidence/usage.json").exists():
    json_files.append(Path("/generation-evidence/usage.json"))
for path in json_files:
    json.loads(path.read_text(encoding="utf-8"))
    print(f"OK JSON parse: {path}")

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
trace_files = [path for path in trace_files if path.is_file()]
assert trace_files
trace_lines = 0
trace_types: dict[str, int] = {}
for path in trace_files:
    expected = (
        json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
        ["outputs"]["evidence"]
        .get(path.relative_to("/generation-evidence").as_posix())
    )
    if expected:
        compare_hash(f"declared trace file {path}", sha256_file(path), expected)
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            trace_lines += 1
            record_type = str(record.get("type", "<none>"))
            trace_types[record_type] = trace_types.get(record_type, 0) + 1
    print(f"OK JSONL parse: {path} lines={line_number}")
print(f"trace total lines={trace_lines} top-level types={trace_types}")

output_text = Path("/generation-evidence/codex-output.log").read_text(encoding="utf-8")
last_text = Path("/generation-evidence/codex-last.txt").read_text(encoding="utf-8")
prompt_text = Path("/generation-evidence/prompt.txt").read_text(encoding="utf-8")
print(
    "OK full UTF-8 reads: "
    f"codex-output chars={len(output_text)} lines={len(output_text.splitlines())}; "
    f"codex-last chars={len(last_text)} lines={len(last_text.splitlines())}; "
    f"prompt chars={len(prompt_text)} lines={len(prompt_text.splitlines())}"
)

print("STAGE1_INTEGRITY_OK")
