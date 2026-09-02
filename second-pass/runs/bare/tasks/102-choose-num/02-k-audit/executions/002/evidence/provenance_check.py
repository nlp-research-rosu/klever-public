#!/usr/bin/env python3
"""Independent integrity checks for the launcher-provided audit mounts."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from collections import Counter
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
LOCK = Path("/audit-campaign-lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_tree(root: Path) -> str:
    """Reimplement the pipeline-v2 length-delimited tree digest."""
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
    assert stat.S_ISREG(mode), f"not a real regular file: {path}"
    assert not path.is_symlink(), f"symlinked file: {path}"


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    lock = json.loads(LOCK.read_text())
    assert audit["record_layout"] == "legacy-selected-stage1"
    assert audit["semantics_mode"] == "GENERATED_SEMANTICS"
    assert audit["audit_campaign"] == lock
    assert sha256_file(LOCK) == audit["hashes"]["audit_campaign_lock_sha256"]

    required = [
        AUDIT_INPUT,
        LOCK,
        Path("/run.json"),
        Path("/task.json"),
        Path("/generation-result.json"),
        Path("/generation-evidence/invocation.json"),
        Path("/generation-evidence/metrics.json"),
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/codex-output.log"),
        Path("/generation-evidence/prompt.txt"),
        Path("/reference/canonical.py"),
        Path("/reference/prompt.py"),
        Path("/reference/py2mpy.py"),
    ]
    for path in required:
        require_regular(path)
    assert Path("/generation-evidence/codex-trace").is_dir()
    assert not Path("/generation-evidence/codex-trace").is_symlink()
    usage = Path("/generation-evidence/usage.json")
    if usage.exists():
        require_regular(usage)
    assert not Path("/reference/reference-semantics").exists()

    for root in (Path("/candidate"), Path("/generation-evidence"), Path("/reference")):
        for path in root.rglob("*"):
            assert not path.is_symlink(), f"symlinked mounted entry: {path}"
            assert path.is_dir() or path.is_file(), f"unsupported mounted entry: {path}"

    hashes = audit["hashes"]
    direct_checks = {
        "/reference/canonical.py": hashes["canonical_sha256"],
        "/reference/prompt.py": hashes["trusted_prompt_sha256"],
        "/reference/py2mpy.py": hashes["trusted_translator_sha256"],
        "/candidate/prompt.py": hashes["candidate_prompt_sha256"],
        "/candidate/py2mpy.py": hashes["candidate_translator_sha256"],
        "/generation-evidence/invocation.json": hashes["stage1_invocation_sha256"],
        "/generation-evidence/metrics.json": hashes["generation_metrics_sha256"],
        "/generation-evidence/codex-last.txt": hashes["generation_codex_last_sha256"],
        "/generation-evidence/codex-output.log": hashes["generation_codex_output_sha256"],
        "/generation-evidence/prompt.txt": hashes["generation_prompt_sha256"],
        "/run.json": hashes["run_manifest_sha256"],
        "/task.json": hashes["task_manifest_sha256"],
        "/generation-result.json": hashes["stage1_result_sha256"],
    }
    if usage.exists():
        direct_checks[str(usage)] = hashes["generation_usage_sha256"]
    for raw_path, expected in direct_checks.items():
        actual = sha256_file(Path(raw_path))
        assert actual == expected, (raw_path, expected, actual)
        print(f"FILE_HASH_OK {raw_path} {actual}")

    assert Path("/candidate/prompt.py").read_bytes() == Path("/reference/prompt.py").read_bytes()
    assert (
        Path("/candidate/py2mpy.py").read_bytes()
        == Path("/reference/py2mpy.py").read_bytes()
    )
    print("TRUSTED_COPY_OK prompt.py")
    print("TRUSTED_COPY_OK py2mpy.py")
    print("SEMANTICS_BOUNDARY_OK no /reference/reference-semantics")

    result = json.loads(Path("/generation-result.json").read_text())
    for relative, expected in result["outputs"]["evidence"].items():
        path = Path("/generation-evidence") / relative
        require_regular(path)
        actual = sha256_file(path)
        assert actual == expected, (path, expected, actual)
        print(f"RESULT_EVIDENCE_HASH_OK {relative} {actual}")

    candidate_digest = sha256_tree(Path("/candidate"))
    trace_digest = sha256_tree(Path("/generation-evidence/codex-trace"))
    invocation = json.loads(Path("/generation-evidence/invocation.json").read_text())
    assert candidate_digest == invocation["outputs"]["workspace_sha256"]
    assert candidate_digest == result["outputs"]["workspace_sha256"]
    print(f"PIPELINE_TREE_HASH_OK /candidate {candidate_digest}")
    if usage.exists():
        usage_doc = json.loads(usage.read_text())
        assert trace_digest == usage_doc["source_trace_sha256"]
        print(f"PIPELINE_TREE_HASH_OK /generation-evidence/codex-trace {trace_digest}")

    # Parse every trace record and summarize the untrusted generation claims.
    trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    assert trace_files
    outer_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    tool_calls = 0
    tool_outputs = 0
    task_complete = 0
    lines = 0
    for trace_file in trace_files:
        for line_number, line in enumerate(trace_file.read_text().splitlines(), 1):
            record = json.loads(line)
            assert isinstance(record, dict), (trace_file, line_number)
            lines += 1
            outer_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                payload_types[payload_type] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    tool_calls += 1
                if payload_type in {"function_call_output", "custom_tool_call_output"}:
                    tool_outputs += 1
                if payload_type == "task_complete":
                    task_complete += 1
    print(f"TRACE_PARSED files={len(trace_files)} lines={lines}")
    print(f"TRACE_OUTER_TYPES {dict(sorted(outer_types.items()))}")
    print(f"TRACE_PAYLOAD_TYPES {dict(sorted(payload_types.items()))}")
    print(
        "TRACE_COMPLETION_COUNTS "
        f"tool_calls={tool_calls} tool_outputs={tool_outputs} task_complete={task_complete}"
    )

    generation_log = Path("/generation-evidence/codex-output.log").read_text()
    print(
        "GENERATION_LOG_SCAN "
        f"bytes={len(generation_log.encode())} "
        f"kprove_mentions={generation_log.count('kprove')} "
        f"top_mentions={generation_log.count('#Top')} "
        f"stuck_mentions={generation_log.count('WarnStuckClaimState')} "
        f"error_mentions={generation_log.count('[Error]')} "
        f"result_markers={generation_log.count('RESULT: KPROVE_PASSED')}"
    )
    print("PROVENANCE_CHECK_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
