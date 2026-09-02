#!/usr/bin/env python3
"""Independent provenance and integrity checks for audit 90-next-smallest."""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from pathlib import Path
import stat
import sys


AUDIT_INPUT = Path("/audit-input.json")
CAMPAIGN_LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplement the pipeline-v2 tree digest without trusting its module."""
    root_stat = root.lstat()
    if not stat.S_ISDIR(root_stat.st_mode):
        raise AssertionError(f"not a real directory: {root}")
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
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
    assert stat.S_ISREG(mode), f"required regular file is missing/mistyped: {path}"


def require_directory(path: Path) -> None:
    mode = path.lstat().st_mode
    assert stat.S_ISDIR(mode), f"required directory is missing/mistyped: {path}"


def main() -> int:
    require_regular(AUDIT_INPUT)
    require_regular(CAMPAIGN_LOCK)
    audit = json.loads(AUDIT_INPUT.read_text(encoding="utf-8"))
    campaign = json.loads(CAMPAIGN_LOCK.read_text(encoding="utf-8"))

    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["mount_reference_semantics"] is False
    assert audit["audit_campaign"] == campaign
    actual_campaign_hash = sha256_file(CAMPAIGN_LOCK)
    assert actual_campaign_hash == audit["hashes"]["audit_campaign_lock_sha256"]
    assert not Path("/reference/reference-semantics").exists()
    assert not Path("/reference/reference-semantics").is_symlink()

    required_files = [
        AUDIT_INPUT,
        CAMPAIGN_LOCK,
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
        Path("/generation-evidence/usage.json"),
    ]
    required_dirs = [
        Path("/candidate"),
        Path("/generation-evidence"),
        Path("/generation-evidence/codex-trace"),
    ]
    for path in required_files:
        require_regular(path)
    for path in required_dirs:
        require_directory(path)

    expected_files = {
        Path("/candidate/prompt.py"): "candidate_prompt_sha256",
        Path("/candidate/py2mpy.py"): "candidate_translator_sha256",
        Path("/reference/canonical.py"): "canonical_sha256",
        Path("/reference/prompt.py"): "trusted_prompt_sha256",
        Path("/reference/py2mpy.py"): "trusted_translator_sha256",
        Path("/run.json"): "run_manifest_sha256",
        Path("/task.json"): "task_manifest_sha256",
        Path("/generation-result.json"): "stage1_result_sha256",
        Path("/generation-evidence/invocation.json"): "stage1_invocation_sha256",
        Path("/generation-evidence/metrics.json"): "generation_metrics_sha256",
        Path("/generation-evidence/usage.json"): "generation_usage_sha256",
        Path("/generation-evidence/codex-last.txt"): "generation_codex_last_sha256",
        Path("/generation-evidence/codex-output.log"): "generation_codex_output_sha256",
        Path("/generation-evidence/prompt.txt"): "generation_prompt_sha256",
    }
    for path, key in expected_files.items():
        actual = sha256_file(path)
        expected = audit["hashes"][key]
        assert actual == expected, f"{path}: {actual} != {expected}"
        print(f"HASH_OK {key} {actual} {path}")

    assert Path("/candidate/prompt.py").read_bytes() == Path(
        "/reference/prompt.py"
    ).read_bytes()
    assert Path("/candidate/py2mpy.py").read_bytes() == Path(
        "/reference/py2mpy.py"
    ).read_bytes()
    print("BYTE_IDENTITY_OK candidate prompt == trusted prompt")
    print("BYTE_IDENTITY_OK candidate translator == trusted translator")

    invocation = json.loads(
        Path("/generation-evidence/invocation.json").read_text(encoding="utf-8")
    )
    result = json.loads(Path("/generation-result.json").read_text(encoding="utf-8"))
    output_hashes = invocation["outputs"]["evidence"]
    assert output_hashes == result["outputs"]["evidence"]
    for relative, expected in sorted(output_hashes.items()):
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, f"generation output hash mismatch: {relative}"
        print(f"GENERATION_OUTPUT_HASH_OK {actual} {relative}")

    candidate_tree = pipeline_tree_hash(Path("/candidate"))
    trace_tree = pipeline_tree_hash(Path("/generation-evidence/codex-trace"))
    assert candidate_tree == invocation["retained_workspace_sha256"]
    assert candidate_tree == result["outputs"]["workspace_sha256"]
    usage = json.loads(Path("/generation-evidence/usage.json").read_text())
    assert trace_tree == usage["source_trace_sha256"]
    print(f"PIPELINE_TREE_HASH_OK {candidate_tree} /candidate")
    print(f"PIPELINE_TREE_HASH_OK {trace_tree} /generation-evidence/codex-trace")
    print(
        "LAUNCHER_DIRECTORY_HASH_RECORDED "
        f"{audit['hashes']['candidate_tree_sha256']} /candidate"
    )
    print(
        "LAUNCHER_DIRECTORY_HASH_RECORDED "
        f"{audit['hashes']['generation_codex_trace_sha256']} "
        "/generation-evidence/codex-trace"
    )

    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_files if path.is_file()]
    assert trace_files
    event_counts: Counter[str] = Counter()
    item_counts: Counter[str] = Counter()
    tool_calls: list[tuple[int, str, str]] = []
    line_count = 0
    for trace_file in trace_files:
        with trace_file.open(encoding="utf-8") as stream:
            for line_count_in_file, line in enumerate(stream, start=1):
                line_count += 1
                record = json.loads(line)
                event_counts[record["type"]] += 1
                payload = record.get("payload", {})
                if isinstance(payload, dict):
                    subtype = payload.get("type")
                    if isinstance(subtype, str):
                        item_counts[subtype] += 1
                    if subtype == "custom_tool_call":
                        tool_calls.append(
                            (
                                line_count_in_file,
                                str(payload.get("name")),
                                str(payload.get("input")),
                            )
                        )
    assert line_count > 0
    print(f"TRACE_JSONL_OK files={len(trace_files)} lines={line_count}")
    print(f"TRACE_TOP_LEVEL_COUNTS {dict(sorted(event_counts.items()))}")
    print(f"TRACE_PAYLOAD_COUNTS {dict(sorted(item_counts.items()))}")
    print(f"TRACE_TOOL_CALL_COUNT {len(tool_calls)}")
    for line_number, name, tool_input in tool_calls:
        compact = " ".join(tool_input.split())
        print(f"TRACE_TOOL_CALL line={line_number} name={name} input={compact}")

    # Read every byte of the unstructured log as well; its trusted role is only
    # provenance evidence, not proof evidence.
    generation_log = Path("/generation-evidence/codex-output.log").read_bytes()
    assert generation_log
    print(
        "GENERATION_LOG_READ "
        f"bytes={len(generation_log)} sha256={hashlib.sha256(generation_log).hexdigest()}"
    )
    print("INTEGRITY_STATUS OK")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"INTEGRITY_STATUS ERROR: {error}", file=sys.stderr)
        raise
