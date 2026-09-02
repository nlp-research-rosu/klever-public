#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs.

This script deliberately reimplements the launcher tree-hash algorithm used by
the pipeline-v3 records instead of importing candidate or benchmark helpers.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys


AUDIT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> tuple[str, int]:
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
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
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest(), len(entries)


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    next(os.scandir(path), None)


def compare_trees(left: Path, right: Path) -> None:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        pending = [root]
        while pending:
            directory = pending.pop()
            for child in os.scandir(directory):
                path = Path(child.path)
                mode = child.stat(follow_symlinks=False).st_mode
                relative = path.relative_to(root).as_posix()
                if stat.S_ISDIR(mode):
                    result[relative] = ("directory", None)
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    result[relative] = ("file", sha256_file(path))
                else:
                    result[relative] = ("UNSUPPORTED", None)
        return result

    li = inventory(left)
    ri = inventory(right)
    assert li == ri, "semantics inventories differ"
    print(f"semantics_recursive_inventory_equal=True entries={len(li)}")


def main() -> int:
    audit = json.loads(AUDIT.read_text())
    lock = json.loads(Path("/audit-campaign-lock.json").read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    lock_hash = sha256_file(Path("/audit-campaign-lock.json"))
    assert lock_hash == audit["hashes"]["audit_campaign_lock_sha256"]
    print(f"campaign_object_equal=True lock_sha256={lock_hash}")

    required_files = [
        Path("/audit-input.json"),
        Path("/audit-campaign-lock.json"),
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/runtime-metrics.json"),
        Path("/generation-evidence/usage.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_directories:
        require_directory(path)
    print(
        f"required_regular_files={len(required_files)} "
        f"required_real_directories={len(required_directories)}"
    )

    declared_file_hashes = {
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
        "/generation-evidence/runtime-metrics.json":
            "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt":
            "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log":
            "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
    }
    for raw_path, field in declared_file_hashes.items():
        path = Path(raw_path)
        require_regular(path)
        actual = sha256_file(path)
        expected = audit["hashes"][field]
        assert actual == expected, f"{field}: {actual} != {expected}"
        print(f"{field}={actual} MATCH")

    assert Path("/candidate/prompt.py").read_bytes() == (
        Path("/reference/prompt.py").read_bytes()
    )
    assert Path("/candidate/py2mpy.py").read_bytes() == (
        Path("/reference/py2mpy.py").read_bytes()
    )
    print("candidate_prompt_byte_equal=True candidate_translator_byte_equal=True")

    trusted_semantics = Path("/reference/reference-semantics")
    candidate_semantics = Path("/candidate/reference-semantics")
    require_directory(candidate_semantics)
    compare_trees(trusted_semantics, candidate_semantics)
    trusted_sem_hash, trusted_count = pipeline_tree_hash(trusted_semantics)
    candidate_sem_hash, candidate_count = pipeline_tree_hash(candidate_semantics)
    expected_sem_hash = audit["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    assert trusted_sem_hash == expected_sem_hash
    assert candidate_sem_hash == expected_sem_hash
    print(
        f"semantics_pipeline_tree_hash={trusted_sem_hash} MATCH "
        f"trusted_entries={trusted_count} candidate_entries={candidate_count}"
    )

    result = json.loads(Path("/generation-result.json").read_text())
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text()
    )
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    candidate_tree_hash, candidate_entries = pipeline_tree_hash(
        Path("/candidate")
    )
    assert candidate_tree_hash == result["outputs"]["workspace_sha256"]
    assert candidate_tree_hash == invocation["outputs"]["workspace_sha256"]
    print(
        f"candidate_pipeline_tree_hash={candidate_tree_hash} MATCH "
        f"entries={candidate_entries}"
    )

    trace_root = Path("/generation-evidence/codex-trace")
    trace_tree_hash, trace_entries = pipeline_tree_hash(trace_root)
    assert trace_tree_hash == usage["source_trace_sha256"]
    print(
        f"trace_pipeline_tree_hash={trace_tree_hash} MATCH "
        f"entries={trace_entries}"
    )

    for relative, expected in result["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, f"evidence hash mismatch: {relative}"
        print(f"generation_result_evidence={relative} sha256={actual} MATCH")

    print("STAGE1_INTEGRITY_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
