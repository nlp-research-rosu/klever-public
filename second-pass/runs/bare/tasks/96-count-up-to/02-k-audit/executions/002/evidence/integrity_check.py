#!/usr/bin/env python3
"""Independent audit-input and legacy-selected-stage1 integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    assert os.access(path, os.R_OK), f"not readable: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    assert os.access(path, os.R_OK | os.X_OK), f"not readable: {path}"


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the stage-1 workspace hash documented by pipeline-v2."""
    digest = hashlib.sha256()
    entries: list[tuple[str, str, Path]] = []
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            entries.append((relative, "directory", path))
        elif stat.S_ISREG(mode):
            entries.append((relative, "file", path))
        else:
            raise AssertionError(f"unsupported tree node: {path}")
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.lstat().st_size
            digest.update(size.to_bytes(8, "big"))
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


document = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
assert document["record_layout"] == "legacy-selected-stage1"
assert document["semantics_mode"] == "GENERATED_SEMANTICS"

paths = document["container_paths"]
required = [
    AUDIT_INPUT,
    Path(paths["audit_campaign_lock"]),
    Path(paths["canonical"]),
    Path(paths["generation_manifest"]),
    Path(paths["generation_metrics"]),
    Path(paths["generation_last"]),
    Path(paths["generation_output"]),
    Path(paths["run_manifest"]),
    Path(paths["stage1_result"]),
    Path(paths["task_manifest"]),
    Path(paths["translator"]),
    Path(paths["trusted_prompt"]),
    Path(paths["generation_root"]) / "prompt.txt",
]
usage = Path(paths["generation_root"]) / "usage.json"
if usage.exists() or usage.is_symlink():
    required.append(usage)
for path in required:
    require_regular(path)

require_directory(Path(paths["candidate"]))
require_directory(Path(paths["generation_root"]))
require_directory(Path(paths["generation_trace"]))

for root in (
    Path(paths["candidate"]),
    Path(paths["generation_root"]),
    Path(paths["generation_trace"]),
):
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        assert stat.S_ISREG(mode) or stat.S_ISDIR(mode), (
            f"linked or unsupported entry: {path}"
        )

campaign_path = Path(paths["audit_campaign_lock"])
campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
assert campaign == document["audit_campaign"]
assert sha256(campaign_path) == document["hashes"]["audit_campaign_lock_sha256"]

hash_map = {
    "canonical_sha256": Path(paths["canonical"]),
    "trusted_prompt_sha256": Path(paths["trusted_prompt"]),
    "trusted_translator_sha256": Path(paths["translator"]),
    "candidate_prompt_sha256": Path(paths["candidate"]) / "prompt.py",
    "candidate_translator_sha256": Path(paths["candidate"]) / "py2mpy.py",
    "run_manifest_sha256": Path(paths["run_manifest"]),
    "task_manifest_sha256": Path(paths["task_manifest"]),
    "manifest_sha256": Path(paths["task_manifest"]),
    "stage1_result_sha256": Path(paths["stage1_result"]),
    "stage1_invocation_sha256": Path(paths["generation_manifest"]),
    "generation_metrics_sha256": Path(paths["generation_metrics"]),
    "generation_codex_last_sha256": Path(paths["generation_last"]),
    "generation_codex_output_sha256": Path(paths["generation_output"]),
    "generation_prompt_sha256": Path(paths["generation_root"]) / "prompt.txt",
    "generation_usage_sha256": usage,
}
for key, path in hash_map.items():
    actual = sha256(path)
    expected = document["hashes"][key]
    assert actual == expected, f"{key}: expected {expected}, got {actual}"
    print(f"HASH_OK {key} {actual} {path}")

candidate = Path(paths["candidate"])
assert (candidate / "prompt.py").read_bytes() == Path(
    paths["trusted_prompt"]
).read_bytes()
assert (candidate / "py2mpy.py").read_bytes() == Path(
    paths["translator"]
).read_bytes()
print("BYTE_IDENTITY_OK candidate/prompt.py reference/prompt.py")
print("BYTE_IDENTITY_OK candidate/py2mpy.py reference/py2mpy.py")

reference_semantics = Path("/reference/reference-semantics")
assert not reference_semantics.exists() and not reference_semantics.is_symlink()
print("GENERATED_SEMANTICS_BOUNDARY_OK reference/reference-semantics absent")

generation_result = json.loads(
    Path(paths["stage1_result"]).read_text(encoding="utf-8")
)
invocation = json.loads(
    Path(paths["generation_manifest"]).read_text(encoding="utf-8")
)
candidate_pipeline_hash = pipeline_tree_sha256(candidate)
assert candidate_pipeline_hash == generation_result["outputs"]["workspace_sha256"]
assert candidate_pipeline_hash == invocation["retained_workspace_sha256"]
print(f"STAGE1_WORKSPACE_TREE_HASH_OK {candidate_pipeline_hash}")

for relative, expected in generation_result["outputs"]["evidence"].items():
    evidence_path = Path(paths["generation_root"]) / relative
    require_regular(evidence_path)
    actual = sha256(evidence_path)
    assert actual == expected, (
        f"generation-result evidence mismatch {relative}: "
        f"expected {expected}, got {actual}"
    )
    assert invocation["outputs"]["evidence"][relative] == expected
    print(f"STAGE1_EVIDENCE_HASH_OK {actual} {evidence_path}")

trace_files = sorted(Path(paths["generation_trace"]).rglob("*.jsonl"))
assert trace_files, "structured trace has no JSONL files"
trace_lines = 0
for trace_file in trace_files:
    require_regular(trace_file)
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            json.loads(line)
            trace_lines += 1
print(f"STRUCTURED_TRACE_JSON_OK files={len(trace_files)} lines={trace_lines}")

print("CAMPAIGN_LOCK_EQUALITY_OK")
print("REQUIRED_RECORDS_OK legacy-selected-stage1")
