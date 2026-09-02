#!/usr/bin/env python3
"""Independent provenance/type/hash checks for audit 67-fruit-distribution."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Independently reproduce the pipeline-v2 length-delimited tree digest."""
    assert stat.S_ISDIR(root.lstat().st_mode) and not root.is_symlink()
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


audit = json.loads(Path("/audit-input.json").read_text())
lock = json.loads(Path("/audit-campaign-lock.json").read_text())
assert audit["record_layout"] == "legacy-selected-stage1"
assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
assert audit["audit_campaign"] == lock

required = [
    Path("/audit-input.json"),
    Path("/audit-campaign-lock.json"),
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
required += [
    Path("/reference/canonical.py"),
    Path("/reference/prompt.py"),
    Path("/reference/py2mpy.py"),
]
for path in required:
    require_regular(path)

trace_root = Path("/generation-evidence/codex-trace")
assert stat.S_ISDIR(trace_root.lstat().st_mode) and not trace_root.is_symlink()
trace_files = sorted(p for p in trace_root.rglob("*") if p.is_file())
assert trace_files
for path in trace_files:
    require_regular(path)

assert not Path("/reference/reference-semantics").exists()
assert not Path("/candidate/reference-semantics").exists()
assert Path("/candidate").is_dir() and not Path("/candidate").is_symlink()
for path in Path("/candidate").rglob("*"):
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode) or stat.S_ISREG(mode), f"bad candidate type: {path}"
    assert not path.is_symlink(), f"candidate symlink: {path}"

expected_file_hashes = {
    "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
    "/reference/canonical.py": "canonical_sha256",
    "/reference/prompt.py": "trusted_prompt_sha256",
    "/reference/py2mpy.py": "trusted_translator_sha256",
    "/candidate/prompt.py": "candidate_prompt_sha256",
    "/candidate/py2mpy.py": "candidate_translator_sha256",
    "/run.json": "run_manifest_sha256",
    "/task.json": "task_manifest_sha256",
    "/generation-result.json": "stage1_result_sha256",
    "/generation-evidence/invocation.json": "stage1_invocation_sha256",
    "/generation-evidence/metrics.json": "generation_metrics_sha256",
    "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
    "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
}
if usage.exists():
    expected_file_hashes[str(usage)] = "generation_usage_sha256"

print("record_layout=legacy-selected-stage1")
print("campaign_structural_match=true")
for file_name, hash_key in expected_file_hashes.items():
    actual = file_hash(Path(file_name))
    expected = audit["hashes"][hash_key]
    assert actual == expected, (file_name, actual, expected)
    print(f"OK {hash_key} {actual} {file_name}")

trace_actual = pipeline_tree_hash(trace_root)
usage_doc = json.loads(usage.read_text())
assert trace_actual == usage_doc["source_trace_sha256"]
print(f"OK trace_tree_pipeline_sha256 {trace_actual}")

candidate_actual = pipeline_tree_hash(Path("/candidate"))
result = json.loads(Path("/generation-result.json").read_text())
invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
assert candidate_actual == result["outputs"]["workspace_sha256"]
assert candidate_actual == invocation["retained_workspace_sha256"]
print(f"OK candidate_pipeline_tree_sha256 {candidate_actual}")
print(
    "NOTE audit_input_candidate_tree_sha256 "
    f"{audit['hashes']['candidate_tree_sha256']} "
    "(launcher uses a separately recorded candidate-tree digest)"
)
print("OK no symlinked or mistyped required/candidate/trace entries")
print("OK generated-semantics boundary: no trusted or candidate reference-semantics")
