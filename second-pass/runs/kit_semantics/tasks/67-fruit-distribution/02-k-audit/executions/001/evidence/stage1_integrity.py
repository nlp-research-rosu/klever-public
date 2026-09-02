#!/usr/bin/env python3
"""Independent provenance and mounted-input integrity checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_digest(root: Path) -> str:
    """Reimplementation of the pipeline-v3 length-delimited tree digest."""
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise AssertionError(f"tree root is not a real directory: {root}")
    digest = hashlib.sha256()
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required regular file is missing/mistyped/symlinked: {path}")
    with path.open("rb") as stream:
        stream.read(1)


def require_real_directory(path: Path) -> None:
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise AssertionError(f"required real directory is missing/mistyped/symlinked: {path}")
    list(path.iterdir())


def tree_entries(root: Path) -> dict[str, tuple[str, str | None]]:
    result: dict[str, tuple[str, str | None]] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                result[relative] = ("directory", None)
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[relative] = ("file", sha256_file(path))
            else:
                result[relative] = ("unsupported", None)
    return result


audit = json.loads(AUDIT_INPUT.read_text())
assert audit["record_layout"] == "pipeline-v3"
assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
paths = {name: Path(value) for name, value in audit["container_paths"].items()}

required_regular = [
    AUDIT_INPUT,
    paths["audit_campaign_lock"],
    paths["canonical"],
    paths["translator"],
    paths["trusted_prompt"],
    paths["run_manifest"],
    paths["task_manifest"],
    paths["stage1_result"],
    paths["generation_manifest"],
    paths["generation_metrics"],
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
    paths["generation_last"],
    paths["generation_output"],
    Path("/generation-evidence/prompt.txt"),
]
for required in required_regular:
    require_regular(required)
for required in [
    paths["candidate"],
    paths["generation_root"],
    paths["generation_trace"],
    Path("/reference/reference-semantics"),
    Path("/candidate/reference-semantics"),
]:
    require_real_directory(required)

lock = json.loads(paths["audit_campaign_lock"].read_text())
assert lock == audit["audit_campaign"], "campaign lock differs from audit campaign block"

hash_checks = {
    paths["audit_campaign_lock"]: "audit_campaign_lock_sha256",
    paths["canonical"]: "canonical_sha256",
    paths["translator"]: "trusted_translator_sha256",
    paths["trusted_prompt"]: "trusted_prompt_sha256",
    paths["run_manifest"]: "run_manifest_sha256",
    paths["task_manifest"]: "task_manifest_sha256",
    paths["stage1_result"]: "stage1_result_sha256",
    paths["generation_manifest"]: "stage1_invocation_sha256",
    paths["generation_metrics"]: "generation_metrics_sha256",
    Path("/generation-evidence/runtime-metrics.json"): "generation_runtime_metrics_sha256",
    Path("/generation-evidence/usage.json"): "generation_usage_sha256",
    paths["generation_last"]: "generation_codex_last_sha256",
    paths["generation_output"]: "generation_codex_output_sha256",
    Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    Path("/candidate/prompt.py"): "candidate_prompt_sha256",
    Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
}
for path, key in hash_checks.items():
    actual = sha256_file(path)
    expected = audit["hashes"][key]
    assert actual == expected, f"{key}: {actual} != {expected}"
    print(f"FILE_HASH_OK {key} {actual} {path}")

assert Path("/candidate/prompt.py").read_bytes() == paths["trusted_prompt"].read_bytes()
assert Path("/candidate/py2mpy.py").read_bytes() == paths["translator"].read_bytes()
trusted_semantics = tree_entries(Path("/reference/reference-semantics"))
candidate_semantics = tree_entries(Path("/candidate/reference-semantics"))
assert candidate_semantics == trusted_semantics
assert all(kind in {"file", "directory"} for kind, _ in trusted_semantics.values())
print(f"SEMANTICS_RECURSIVE_IDENTITY_OK entries={len(trusted_semantics)}")

run = json.loads(paths["run_manifest"].read_text())
task = json.loads(paths["task_manifest"].read_text())
result = json.loads(paths["stage1_result"].read_text())
invocation = json.loads(paths["generation_manifest"].read_text())
usage = json.loads(Path("/generation-evidence/usage.json").read_text())
assert run["condition"]["name"] == audit["condition"]
for key, value in task.items():
    assert audit["manifest"][key] == value
assert audit["manifest"]["config"] == audit["config"]
assert result["invocation"] == invocation["name"]
assert result["outputs"] == invocation["outputs"]

candidate_digest = pipeline_tree_digest(paths["candidate"])
trusted_semantics_digest = pipeline_tree_digest(Path("/reference/reference-semantics"))
candidate_semantics_digest = pipeline_tree_digest(Path("/candidate/reference-semantics"))
trace_digest = pipeline_tree_digest(paths["generation_trace"])
assert candidate_digest == result["outputs"]["workspace_sha256"]
assert candidate_digest == invocation["outputs"]["workspace_sha256"]
assert trusted_semantics_digest == task["inputs"]["reference_semantics_sha256"]
assert candidate_semantics_digest == trusted_semantics_digest
assert trace_digest == usage["source_trace_sha256"]
print(f"PIPELINE_TREE_HASH_OK candidate {candidate_digest}")
print(f"PIPELINE_TREE_HASH_OK trusted_semantics {trusted_semantics_digest}")
print(f"PIPELINE_TREE_HASH_OK candidate_semantics {candidate_semantics_digest}")
print(f"PIPELINE_TREE_HASH_OK generation_trace {trace_digest}")

trace_outputs = {
    key: value
    for key, value in result["outputs"]["evidence"].items()
    if key.startswith("codex-trace/")
}
actual_trace_files = sorted(paths["generation_trace"].rglob("*"))
actual_trace_files = [path for path in actual_trace_files if path.is_file()]
assert len(trace_outputs) == len(actual_trace_files)
for path in actual_trace_files:
    relative = path.relative_to(paths["generation_root"]).as_posix()
    assert relative in trace_outputs
    actual = sha256_file(path)
    assert actual == trace_outputs[relative]
    print(f"TRACE_FILE_HASH_OK {actual} {relative}")

candidate_entries = tree_entries(paths["candidate"])
unsupported = [path for path, (kind, _) in candidate_entries.items() if kind == "unsupported"]
assert not unsupported, f"candidate contains symlink/special entries: {unsupported}"
for name in [
    "solution.py",
    "solution.mpy",
    "verification.k",
    "spec.k",
    "prove.sh",
    "PROOF.md",
]:
    assert candidate_entries.get(name, (None,))[0] == "file", f"missing proof artifact: {name}"
print(f"CANDIDATE_ENTRY_TYPES_OK entries={len(candidate_entries)}")
print("STAGE1_INTEGRITY=PASS")
