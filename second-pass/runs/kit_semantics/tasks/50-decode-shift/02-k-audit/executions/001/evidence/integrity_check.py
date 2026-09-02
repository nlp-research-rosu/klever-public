#!/usr/bin/env python3
"""Independent integrity checks for the 50-decode-shift audit mounts."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")
GEN = Path("/generation-evidence")
CANDIDATE = Path("/candidate")
REFERENCE = Path("/reference")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            mode = child.stat(follow_symlinks=False).st_mode
            path = Path(child.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    return sorted(entries)


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement pipeline_contract.sha256_tree without importing harness code."""
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


def require_file(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    with path.open("rb") as stream:
        stream.read(1)


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"not a real directory: {path}"
    list(os.scandir(path))


def compare_trees(left: Path, right: Path) -> None:
    left_entries = [(r, k) for r, k, _ in tree_entries(left)]
    right_entries = [(r, k) for r, k, _ in tree_entries(right)]
    assert left_entries == right_entries, "tree path/type inventory differs"
    for relative, kind in left_entries:
        if kind == "file":
            assert (left / relative).read_bytes() == (right / relative).read_bytes(), (
                f"tree bytes differ: {relative}"
            )


def check_hash(path: Path, expected: str) -> None:
    actual = file_hash(path)
    print(f"FILE_SHA256 {actual} {path}")
    assert actual == expected, f"hash mismatch: {path}"


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    hashes = audit["hashes"]
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    print("CAMPAIGN_LOCK structural_match=true")

    required_files = [
        AUDIT_INPUT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        GEN / "invocation.json",
        GEN / "metrics.json",
        GEN / "runtime-metrics.json",
        GEN / "usage.json",
        GEN / "codex-last.txt",
        GEN / "codex-output.log",
        GEN / "prompt.txt",
        REFERENCE / "canonical.py",
        REFERENCE / "prompt.py",
        REFERENCE / "py2mpy.py",
    ]
    required_directories = [
        CANDIDATE,
        GEN,
        GEN / "codex-trace",
        REFERENCE / "reference-semantics",
    ]
    for path in required_files:
        require_file(path)
        print(f"REGULAR_READABLE {path}")
    for path in required_directories:
        require_directory(path)
        print(f"REAL_DIRECTORY {path}")

    expected_file_hashes = {
        LOCK: hashes["audit_campaign_lock_sha256"],
        Path("/run.json"): hashes["run_manifest_sha256"],
        Path("/task.json"): hashes["task_manifest_sha256"],
        Path("/generation-result.json"): hashes["stage1_result_sha256"],
        GEN / "invocation.json": hashes["stage1_invocation_sha256"],
        GEN / "metrics.json": hashes["generation_metrics_sha256"],
        GEN / "runtime-metrics.json": hashes["generation_runtime_metrics_sha256"],
        GEN / "usage.json": hashes["generation_usage_sha256"],
        GEN / "codex-last.txt": hashes["generation_codex_last_sha256"],
        GEN / "codex-output.log": hashes["generation_codex_output_sha256"],
        GEN / "prompt.txt": hashes["generation_prompt_sha256"],
        REFERENCE / "canonical.py": hashes["canonical_sha256"],
        REFERENCE / "prompt.py": hashes["trusted_prompt_sha256"],
        REFERENCE / "py2mpy.py": hashes["trusted_translator_sha256"],
        CANDIDATE / "prompt.py": hashes["candidate_prompt_sha256"],
        CANDIDATE / "py2mpy.py": hashes["candidate_translator_sha256"],
    }
    for path, expected in expected_file_hashes.items():
        check_hash(path, expected)

    assert (CANDIDATE / "prompt.py").read_bytes() == (
        REFERENCE / "prompt.py"
    ).read_bytes()
    assert (CANDIDATE / "py2mpy.py").read_bytes() == (
        REFERENCE / "py2mpy.py"
    ).read_bytes()
    compare_trees(
        CANDIDATE / "reference-semantics",
        REFERENCE / "reference-semantics",
    )
    print("CANDIDATE_PROMPT translator supplied_semantics byte_identity=true")

    invocation = json.loads((GEN / "invocation.json").read_text())
    task = json.loads(Path("/task.json").read_text())
    usage = json.loads((GEN / "usage.json").read_text())
    candidate_tree = pipeline_tree_hash(CANDIDATE)
    trusted_semantics_tree = pipeline_tree_hash(REFERENCE / "reference-semantics")
    candidate_semantics_tree = pipeline_tree_hash(CANDIDATE / "reference-semantics")
    trace_tree = pipeline_tree_hash(GEN / "codex-trace")
    print(f"PIPELINE_TREE_SHA256 {candidate_tree} /candidate")
    print(
        f"PIPELINE_TREE_SHA256 {trusted_semantics_tree} "
        "/reference/reference-semantics"
    )
    print(
        f"PIPELINE_TREE_SHA256 {candidate_semantics_tree} "
        "/candidate/reference-semantics"
    )
    print(f"PIPELINE_TREE_SHA256 {trace_tree} /generation-evidence/codex-trace")
    assert candidate_tree == invocation["outputs"]["workspace_sha256"]
    assert trusted_semantics_tree == task["inputs"]["reference_semantics_sha256"]
    assert candidate_semantics_tree == trusted_semantics_tree
    assert trace_tree == usage["source_trace_sha256"]

    trace_files = [
        path
        for relative, kind, path in tree_entries(GEN / "codex-trace")
        if kind == "file"
    ]
    assert len(trace_files) == 1
    trace_relative = trace_files[0].relative_to(GEN).as_posix()
    expected_trace_hash = invocation["outputs"]["evidence"][trace_relative]
    check_hash(trace_files[0], expected_trace_hash)
    rows = []
    with trace_files[0].open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                rows.append(json.loads(line))
            except ValueError as error:
                raise AssertionError(
                    f"malformed JSONL at {trace_files[0]}:{line_number}"
                ) from error
    print(f"TRACE_JSONL parsed_lines={len(rows)}")

    output_bytes = (GEN / "codex-output.log").read_bytes()
    output_bytes.decode("utf-8")
    print(
        "CODEX_OUTPUT "
        f"bytes={len(output_bytes)} lines={output_bytes.count(bytes([10])) + 1} "
        f"nul={output_bytes.count(bytes([0]))}"
    )
    print("INTEGRITY_CHECK PASS")


if __name__ == "__main__":
    main()
