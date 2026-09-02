#!/usr/bin/env python3
"""Independent launcher-input and provenance integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    root_mode = root.lstat().st_mode
    assert stat.S_ISDIR(root_mode), f"not a real directory: {root}"
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
    return sorted(entries)


def pipeline_tree_sha256(root: Path) -> str:
    """Reimplement the pipeline-v3 length/type/size/content tree digest."""
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


def require_regular(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISREG(mode), f"required path is not a real regular file: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"required path is not a real directory: {path}"


def compare_trees(left: Path, right: Path) -> None:
    left_entries = [(rel, kind) for rel, kind, _ in tree_entries(left)]
    right_entries = [(rel, kind) for rel, kind, _ in tree_entries(right)]
    assert left_entries == right_entries, "tree path/type manifests differ"
    for relative, kind in left_entries:
        if kind == "file":
            assert (left / relative).read_bytes() == (right / relative).read_bytes(), (
                f"tree file differs: {relative}"
            )


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/integrity_check.py")
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    assert audit["record_layout"] == "pipeline-v3"
    assert audit["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert audit["mount_reference_semantics"] is True

    required_files = [
        AUDIT_INPUT,
        Path("/audit-campaign-lock.json"),
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
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
        Path("/candidate/prompt.py"),
        Path("/candidate/py2mpy.py"),
    ]
    required_directories = [
        Path("/candidate"),
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_directories:
        require_directory(path)
    print(f"required_regular_files={len(required_files)}")
    print(f"required_real_directories={len(required_directories)}")

    lock = json.loads(Path("/audit-campaign-lock.json").read_text(encoding="utf-8"))
    assert audit["audit_campaign"] == lock
    print("campaign_block_equals_lock=true")

    expected_hashes = {
        "/audit-campaign-lock.json": "audit_campaign_lock_sha256",
        "/run.json": "run_manifest_sha256",
        "/task.json": "task_manifest_sha256",
        "/generation-result.json": "stage1_result_sha256",
        "/generation-evidence/invocation.json": "stage1_invocation_sha256",
        "/generation-evidence/metrics.json": "generation_metrics_sha256",
        "/generation-evidence/runtime-metrics.json": "generation_runtime_metrics_sha256",
        "/generation-evidence/usage.json": "generation_usage_sha256",
        "/generation-evidence/codex-last.txt": "generation_codex_last_sha256",
        "/generation-evidence/codex-output.log": "generation_codex_output_sha256",
        "/generation-evidence/prompt.txt": "generation_prompt_sha256",
        "/reference/canonical.py": "canonical_sha256",
        "/reference/prompt.py": "trusted_prompt_sha256",
        "/reference/py2mpy.py": "trusted_translator_sha256",
        "/candidate/prompt.py": "candidate_prompt_sha256",
        "/candidate/py2mpy.py": "candidate_translator_sha256",
    }
    for raw_path, hash_key in expected_hashes.items():
        actual = sha256_file(Path(raw_path))
        expected = audit["hashes"][hash_key]
        assert actual == expected, f"{raw_path}: {actual} != {expected}"
        print(f"sha256 {raw_path} {actual} MATCH")

    compare_trees(
        Path("/reference/reference-semantics"),
        Path("/candidate/reference-semantics"),
    )
    trusted_semantics_tree = pipeline_tree_sha256(
        Path("/reference/reference-semantics")
    )
    candidate_semantics_tree = pipeline_tree_sha256(
        Path("/candidate/reference-semantics")
    )
    assert trusted_semantics_tree == candidate_semantics_tree
    assert trusted_semantics_tree == audit["hashes"][
        "trusted_reference_semantics_manifest_sha256"
    ]
    print(
        "supplied_semantics_recursive_identity=true "
        f"pipeline_tree_sha256={trusted_semantics_tree}"
    )

    candidate_tree = pipeline_tree_sha256(Path("/candidate"))
    result = json.loads(
        Path("/generation-result.json").read_text(encoding="utf-8")
    )
    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    assert candidate_tree == invocation["outputs"]["workspace_sha256"]
    print(f"candidate_pipeline_tree_sha256={candidate_tree} MATCH generation records")

    trace_root = Path("/generation-evidence/codex-trace")
    trace_tree = pipeline_tree_sha256(trace_root)
    usage = json.loads(
        Path("/generation-evidence/usage.json").read_text(encoding="utf-8")
    )
    assert trace_tree == usage["source_trace_sha256"]
    print(f"trace_pipeline_tree_sha256={trace_tree} MATCH usage record")

    trace_files = [
        path for relative, kind, path in tree_entries(trace_root) if kind == "file"
    ]
    assert len(trace_files) == 1
    trace_file = trace_files[0]
    expected_trace_file_hash = result["outputs"]["evidence"][
        "codex-trace/2026/07/29/"
        "rollout-2026-07-29T03-10-29-019facec-d1db-7801-97a0-88b8a1f5ac4a.jsonl"
    ]
    assert sha256_file(trace_file) == expected_trace_file_hash

    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    response_types: Counter[str] = Counter()
    first_timestamp = None
    last_timestamp = None
    line_count = 0
    with trace_file.open("r", encoding="utf-8") as stream:
        for line_count, line in enumerate(stream, 1):
            event = json.loads(line)
            top_types[str(event.get("type"))] += 1
            payload = event.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                response = payload.get("response")
                if isinstance(response, dict):
                    response_types[str(response.get("type"))] += 1
            timestamp = event.get("timestamp")
            if timestamp is not None:
                first_timestamp = first_timestamp or timestamp
                last_timestamp = timestamp
    assert line_count > 0
    print(f"trace_file={trace_file}")
    print(f"trace_file_sha256={sha256_file(trace_file)} MATCH invocation/result")
    print(f"trace_json_lines_parsed={line_count}")
    print(f"trace_first_timestamp={first_timestamp}")
    print(f"trace_last_timestamp={last_timestamp}")
    print(f"trace_top_types={dict(sorted(top_types.items()))}")
    print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
    print(f"trace_response_types={dict(sorted(response_types.items()))}")

    print("STATUS: ALL INTEGRITY ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
