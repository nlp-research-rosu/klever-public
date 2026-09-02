#!/usr/bin/env python3
"""Independent integrity checks for the launcher-owned audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT = Path("/audit-input.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    assert path.exists(), f"missing: {path}"
    assert not path.is_symlink(), f"symlink: {path}"
    assert path.is_file(), f"not a regular file: {path}"
    assert os.access(path, os.R_OK), f"unreadable: {path}"


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v3 length-delimited tree digest."""
    assert root.is_dir() and not root.is_symlink()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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


data = json.loads(AUDIT.read_text())
assert data["record_layout"] == "pipeline-v3"
assert data["semantics_mode"] == "SUPPLIED_SEMANTICS"

paths = data["container_paths"]
declared = {
    "audit_campaign_lock": Path(paths["audit_campaign_lock"]),
    "canonical": Path(paths["canonical"]),
    "generation_last": Path(paths["generation_last"]),
    "generation_manifest": Path(paths["generation_manifest"]),
    "generation_metrics": Path(paths["generation_metrics"]),
    "generation_output": Path(paths["generation_output"]),
    "run_manifest": Path(paths["run_manifest"]),
    "stage1_result": Path(paths["stage1_result"]),
    "task_manifest": Path(paths["task_manifest"]),
    "translator": Path(paths["translator"]),
    "trusted_prompt": Path(paths["trusted_prompt"]),
}
for path in declared.values():
    require_regular(path)

extra_pipeline_records = [
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    Path("/generation-evidence/prompt.txt"),
]
for path in extra_pipeline_records:
    require_regular(path)

trace_root = Path(paths["generation_trace"])
assert trace_root.is_dir() and not trace_root.is_symlink()
trace_files = sorted(path for path in trace_root.rglob("*") if path.is_file())
assert trace_files, "structured trace is empty"
assert not any(path.is_symlink() for path in trace_root.rglob("*"))

lock = json.loads(declared["audit_campaign_lock"].read_text())
assert lock == data["audit_campaign"], "campaign lock content mismatch"
assert sha256(declared["audit_campaign_lock"]) == data["hashes"]["audit_campaign_lock_sha256"]

hash_bindings = {
    "canonical_sha256": declared["canonical"],
    "trusted_prompt_sha256": declared["trusted_prompt"],
    "trusted_translator_sha256": declared["translator"],
    "run_manifest_sha256": declared["run_manifest"],
    "task_manifest_sha256": declared["task_manifest"],
    "stage1_result_sha256": declared["stage1_result"],
    "stage1_invocation_sha256": declared["generation_manifest"],
    "generation_metrics_sha256": declared["generation_metrics"],
    "generation_runtime_metrics_sha256": Path("/generation-evidence/runtime-metrics.json"),
    "generation_usage_sha256": Path("/generation-evidence/usage.json"),
    "generation_prompt_sha256": Path("/generation-evidence/prompt.txt"),
    "generation_codex_last_sha256": declared["generation_last"],
    "generation_codex_output_sha256": declared["generation_output"],
}
for key, path in hash_bindings.items():
    actual = sha256(path)
    expected = data["hashes"][key]
    assert actual == expected, f"{key}: {actual} != {expected}"
    print(f"HASH_OK {key} {actual} {path}")

candidate = Path(paths["candidate"])
assert candidate.is_dir() and not candidate.is_symlink()
for required in (
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
    "prompt.py",
    "py2mpy.py",
):
    require_regular(candidate / required)

assert (candidate / "prompt.py").read_bytes() == declared["trusted_prompt"].read_bytes()
assert (candidate / "py2mpy.py").read_bytes() == declared["translator"].read_bytes()
print("CANDIDATE_PROMPT_BYTE_IDENTICAL")
print("CANDIDATE_TRANSLATOR_BYTE_IDENTICAL")

trusted_semantics = Path("/reference/reference-semantics")
candidate_semantics = candidate / "reference-semantics"
assert trusted_semantics.is_dir() and candidate_semantics.is_dir()
assert not trusted_semantics.is_symlink() and not candidate_semantics.is_symlink()


def tree_manifest(root: Path) -> list[tuple[str, str, str | None]]:
    manifest: list[tuple[str, str, str | None]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            kind, digest = "symlink", os.readlink(path)
        elif path.is_dir():
            kind, digest = "dir", None
        elif path.is_file():
            kind, digest = "file", sha256(path)
        else:
            kind, digest = "other", None
        manifest.append((relative, kind, digest))
    return manifest


trusted_manifest = tree_manifest(trusted_semantics)
candidate_manifest = tree_manifest(candidate_semantics)
assert trusted_manifest == candidate_manifest, "candidate semantics differs from trusted tree"
assert all(kind != "symlink" for _, kind, _ in candidate_manifest)
print(f"SEMANTICS_TREE_BYTE_AND_TYPE_IDENTICAL entries={len(trusted_manifest)}")
for relative, kind, digest in trusted_manifest:
    print(f"SEMANTICS_ENTRY {kind} {digest or '-'} {relative}")

stage_result = json.loads(declared["stage1_result"].read_text())
invocation = json.loads(declared["generation_manifest"].read_text())
task = json.loads(declared["task_manifest"].read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())

candidate_tree_hash = pipeline_tree_sha256(candidate)
assert candidate_tree_hash == stage_result["outputs"]["workspace_sha256"]
assert candidate_tree_hash == invocation["outputs"]["workspace_sha256"]
print(f"CANDIDATE_PIPELINE_TREE_HASH_OK {candidate_tree_hash}")

trusted_semantics_hash = pipeline_tree_sha256(trusted_semantics)
candidate_semantics_hash = pipeline_tree_sha256(candidate_semantics)
assert trusted_semantics_hash == candidate_semantics_hash
assert trusted_semantics_hash == task["inputs"]["reference_semantics_sha256"]
assert trusted_semantics_hash == data["hashes"]["trusted_reference_semantics_manifest_sha256"]
print(f"SEMANTICS_PIPELINE_TREE_HASH_OK {trusted_semantics_hash}")

trace_tree_hash = pipeline_tree_sha256(trace_root)
assert trace_tree_hash == usage["source_trace_sha256"]
print(f"TRACE_PIPELINE_TREE_HASH_OK {trace_tree_hash}")

for record_name, record in (("result", stage_result), ("invocation", invocation)):
    evidence = record["outputs"]["evidence"]
    for relative, expected in sorted(evidence.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256(path)
        assert actual == expected, f"{record_name}:{relative}: {actual} != {expected}"
        print(f"GENERATION_OUTPUT_OK {record_name} {actual} {relative}")

trace_lines = 0
for path in trace_files:
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            json.loads(line)
            trace_lines += 1
    print(f"TRACE_JSONL_OK {path.relative_to(trace_root)} lines={line_number}")

for root in (candidate, Path("/reference"), Path("/generation-evidence")):
    symlinks = list(root.rglob("*"))
    symlinks = [path for path in symlinks if path.is_symlink()]
    assert not symlinks, f"unexpected symlinks below {root}: {symlinks}"

print(f"TRACE_TOTAL_LINES {trace_lines}")
print(f"AUDIT_INPUT_SHA256 {sha256(AUDIT)}")
print("STAGE1_INTEGRITY_PASS")
