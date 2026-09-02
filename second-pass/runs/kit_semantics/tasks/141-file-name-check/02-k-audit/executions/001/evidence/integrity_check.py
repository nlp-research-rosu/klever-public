#!/usr/bin/env python3
"""Independent integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")
GENERATION = Path("/generation-evidence")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Independent implementation of pipeline-v3's length-delimited tree hash."""
    if root.is_symlink() or not root.is_dir():
        raise AssertionError(f"tree root is not a real directory: {root}")
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
    return digest.hexdigest()


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    if not stat.S_ISREG(mode):
        raise AssertionError(f"required path is not a regular file: {path}")


def compare_trees(left: Path, right: Path) -> tuple[int, int]:
    def inventory(root: Path) -> dict[str, tuple[str, str | None]]:
        result: dict[str, tuple[str, str | None]] = {}
        for current, directories, files in os.walk(root, followlinks=False):
            current_path = Path(current)
            for name in directories:
                path = current_path / name
                if path.is_symlink():
                    raise AssertionError(f"symlinked directory: {path}")
                result[path.relative_to(root).as_posix()] = ("directory", None)
            for name in files:
                path = current_path / name
                if path.is_symlink() or not path.is_file():
                    raise AssertionError(f"non-regular file: {path}")
                result[path.relative_to(root).as_posix()] = (
                    "file",
                    sha256_file(path),
                )
        return result

    left_inventory = inventory(left)
    right_inventory = inventory(right)
    if left_inventory != right_inventory:
        left_only = sorted(left_inventory.keys() - right_inventory.keys())
        right_only = sorted(right_inventory.keys() - left_inventory.keys())
        changed = sorted(
            key
            for key in left_inventory.keys() & right_inventory.keys()
            if left_inventory[key] != right_inventory[key]
        )
        raise AssertionError(
            f"tree mismatch left_only={left_only} right_only={right_only} "
            f"changed={changed}"
        )
    file_count = sum(kind == "file" for kind, _ in left_inventory.values())
    return len(left_inventory), file_count


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True
    assert audit["audit_campaign"] == lock
    assert (
        sha256_file(LOCK)
        == audit["hashes"]["audit_campaign_lock_sha256"]
    )

    required = [
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GENERATION / "invocation.json",
        GENERATION / "metrics.json",
        GENERATION / "runtime-metrics.json",
        GENERATION / "usage.json",
        GENERATION / "codex-last.txt",
        GENERATION / "codex-output.log",
        GENERATION / "prompt.txt",
        REFERENCE / "canonical.py",
        REFERENCE / "prompt.py",
        REFERENCE / "py2mpy.py",
        CANDIDATE / "prompt.py",
        CANDIDATE / "py2mpy.py",
    ]
    for path in required:
        require_regular(path)

    declared_file_hashes = {
        LOCK: "audit_campaign_lock_sha256",
        REFERENCE / "canonical.py": "canonical_sha256",
        REFERENCE / "prompt.py": "trusted_prompt_sha256",
        REFERENCE / "py2mpy.py": "trusted_translator_sha256",
        CANDIDATE / "prompt.py": "candidate_prompt_sha256",
        CANDIDATE / "py2mpy.py": "candidate_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        GENERATION / "invocation.json": "stage1_invocation_sha256",
        GENERATION / "metrics.json": "generation_metrics_sha256",
        GENERATION / "runtime-metrics.json": "generation_runtime_metrics_sha256",
        GENERATION / "usage.json": "generation_usage_sha256",
        GENERATION / "codex-last.txt": "generation_codex_last_sha256",
        GENERATION / "codex-output.log": "generation_codex_output_sha256",
        GENERATION / "prompt.txt": "generation_prompt_sha256",
    }
    for path, key in declared_file_hashes.items():
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        assert actual == expected, (path, actual, expected)

    assert (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()

    entry_count, semantics_files = compare_trees(
        CANDIDATE / "reference-semantics",
        REFERENCE / "reference-semantics",
    )
    semantics_hash = pipeline_tree_hash(REFERENCE / "reference-semantics")
    assert semantics_hash == audit["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    assert semantics_hash == audit["manifest"]["inputs"][
        "reference_semantics_sha256"
    ]

    result = json.loads(Path("/generation-result.json").read_text())
    candidate_hash = pipeline_tree_hash(CANDIDATE)
    assert candidate_hash == result["outputs"]["workspace_sha256"]

    invocation = json.loads((GENERATION / "invocation.json").read_text())
    for relative, expected in invocation["outputs"]["evidence"].items():
        path = GENERATION / relative
        require_regular(path)
        assert sha256_file(path) == expected, relative

    trace_root = GENERATION / "codex-trace"
    trace_hash = pipeline_tree_hash(trace_root)
    usage = json.loads((GENERATION / "usage.json").read_text())
    assert trace_hash == usage["source_trace_sha256"]
    trace_files = sorted(trace_root.rglob("*.jsonl"))
    assert trace_files
    trace_lines = 0
    for trace_file in trace_files:
        require_regular(trace_file)
        for line_number, line in enumerate(
            trace_file.read_text().splitlines(), start=1
        ):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                raise AssertionError(
                    f"malformed trace line {trace_file}:{line_number}"
                ) from error
            assert isinstance(record, dict) and "type" in record
            trace_lines += 1

    integrity = audit["integrity"]
    assert all(value is True for value in integrity.values())
    print("record_layout=pipeline-v3")
    print("semantics_mode=SUPPLIED_SEMANTICS")
    print("campaign_block_match=true")
    print(
        "declared_regular_file_hashes="
        f"{len(declared_file_hashes)}/{len(declared_file_hashes)} matched"
    )
    print("candidate_prompt_matches_trusted=true")
    print("candidate_translator_matches_trusted=true")
    print(
        f"reference_semantics_exact_match=true entries={entry_count} "
        f"files={semantics_files}"
    )
    print(f"reference_semantics_pipeline_tree_sha256={semantics_hash}")
    print(f"candidate_pipeline_tree_sha256={candidate_hash}")
    print(f"structured_trace_pipeline_tree_sha256={trace_hash}")
    print(f"structured_trace_files={len(trace_files)} lines={trace_lines}")
    print("integrity_fields_all_true=true")
    print("INTEGRITY_CHECK=PASS")


if __name__ == "__main__":
    main()
