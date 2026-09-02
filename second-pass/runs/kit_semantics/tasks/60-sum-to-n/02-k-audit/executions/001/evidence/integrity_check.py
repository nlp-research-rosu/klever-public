#!/usr/bin/env python3
"""Independent mounted-input and pipeline-v3 provenance checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    assert root.is_dir() and not root.is_symlink(), f"not a real directory: {root}"
    result: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                result.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                result.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or special tree entry: {path}")
    return sorted(result)


def framed_tree_sha256(root: Path) -> str:
    """Pipeline-v3 tree hash: path length/path/kind and file size/content."""
    digest = hashlib.sha256()
    for relative, kind, path in tree_entries(root):
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


def compare_trees(left: Path, right: Path) -> int:
    left_entries = [(rel, kind) for rel, kind, _ in tree_entries(left)]
    right_entries = [(rel, kind) for rel, kind, _ in tree_entries(right)]
    assert left_entries == right_entries, "tree layouts differ"
    files = 0
    for relative, kind in left_entries:
        if kind == "file":
            files += 1
            assert (left / relative).read_bytes() == (right / relative).read_bytes(), (
                f"file differs: {relative}"
            )
    return files


require_regular(AUDIT)
audit = json.loads(AUDIT.read_text())
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"

container_paths = audit["container_paths"]
for key, raw_path in container_paths.items():
    path = Path(raw_path)
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), (
        f"launcher-declared mount is linked/special: {key}={path}"
    )
    print(f"CONTAINER_PATH_OK {key} {path}")

required = {
    "audit_campaign_lock_sha256": Path("/audit-campaign-lock.json"),
    "run_manifest_sha256": Path("/run.json"),
    "task_manifest_sha256": Path("/task.json"),
    "stage1_result_sha256": Path("/generation-result.json"),
    "stage1_invocation_sha256": GENERATION / "invocation.json",
    "generation_metrics_sha256": GENERATION / "metrics.json",
    "generation_runtime_metrics_sha256": GENERATION / "runtime-metrics.json",
    "generation_usage_sha256": GENERATION / "usage.json",
    "generation_codex_last_sha256": GENERATION / "codex-last.txt",
    "generation_codex_output_sha256": GENERATION / "codex-output.log",
    "generation_prompt_sha256": GENERATION / "prompt.txt",
    "canonical_sha256": REFERENCE / "canonical.py",
    "trusted_prompt_sha256": REFERENCE / "prompt.py",
    "trusted_translator_sha256": REFERENCE / "py2mpy.py",
}
for key, path in required.items():
    require_regular(path)
    actual = sha256_file(path)
    assert actual == audit["hashes"][key], (key, actual, audit["hashes"][key])
    print(f"HASH_OK {key} {actual} {path}")

lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert lock == audit["audit_campaign"]
task = json.loads(Path("/task.json").read_text())
audit_manifest = dict(audit["manifest"])
manifest_config = audit_manifest.pop("config")
assert task == audit_manifest
assert manifest_config == audit["config"]
print("CAMPAIGN_LOCK_OK exact JSON object match")
print("TASK_MANIFEST_OK exact match after launcher-added config field")

result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads((GENERATION / "invocation.json").read_text())
assert result["outputs"] == invocation["outputs"]
assert result["session_id"] == invocation["session_id"]
assert result["status"] == invocation["status"] == "SUCCEEDED"

trace_root = GENERATION / "codex-trace"
trace_entries = [
    (relative, path)
    for relative, kind, path in tree_entries(trace_root)
    if kind == "file"
]
declared_trace = {
    name.removeprefix("codex-trace/"): digest
    for name, digest in result["outputs"]["evidence"].items()
    if name.startswith("codex-trace/")
}
assert {name for name, _ in trace_entries} == set(declared_trace)
trace_lines = 0
for relative, path in trace_entries:
    actual = sha256_file(path)
    assert actual == declared_trace[relative]
    with path.open() as stream:
        for line in stream:
            json.loads(line)
            trace_lines += 1
    print(f"TRACE_FILE_OK {actual} {relative}")

usage = json.loads((GENERATION / "usage.json").read_text())
trace_tree_hash = framed_tree_sha256(trace_root)
assert trace_tree_hash == usage["source_trace_sha256"]
print(f"TRACE_TREE_OK {trace_tree_hash} jsonl_lines={trace_lines}")

candidate_tree_hash = framed_tree_sha256(CANDIDATE)
assert candidate_tree_hash == result["outputs"]["workspace_sha256"]
print(f"CANDIDATE_PIPELINE_TREE_OK {candidate_tree_hash}")

for name in ("prompt.py", "py2mpy.py"):
    candidate_path = CANDIDATE / name
    trusted_path = REFERENCE / name
    require_regular(candidate_path)
    assert candidate_path.read_bytes() == trusted_path.read_bytes()
    print(f"TRUSTED_FILE_COPY_OK {name} {sha256_file(candidate_path)}")

semantics_files = compare_trees(
    CANDIDATE / "reference-semantics",
    REFERENCE / "reference-semantics",
)
trusted_semantics_hash = framed_tree_sha256(REFERENCE / "reference-semantics")
candidate_semantics_hash = framed_tree_sha256(CANDIDATE / "reference-semantics")
assert trusted_semantics_hash == candidate_semantics_hash
assert trusted_semantics_hash == audit["hashes"][
    "trusted_reference_semantics_manifest_sha256"
]
print(
    "SUPPLIED_SEMANTICS_TREE_OK "
    f"files={semantics_files} framed_hash={trusted_semantics_hash}"
)

for name in (
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
):
    require_regular(CANDIDATE / name)
    print(f"PROOF_ARTIFACT_OK {name} {sha256_file(CANDIDATE / name)}")

print("INTEGRITY_CHECK_PASS")
