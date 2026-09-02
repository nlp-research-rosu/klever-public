#!/usr/bin/env python3
"""Read every required pipeline-v3 record and summarize untrusted generation claims."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


JSON_RECORDS = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/runtime-metrics.json"),
    Path("/generation-evidence/usage.json"),
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    for path in JSON_RECORDS:
        raw = path.read_bytes()
        parsed = json.loads(raw)
        print(f"===== {path} bytes={len(raw)} sha256={digest(raw)} =====")
        print(json.dumps(parsed, indent=2, sort_keys=True))

    for path in [
        Path("/generation-evidence/codex-last.txt"),
        Path("/generation-evidence/prompt.txt"),
    ]:
        raw = path.read_bytes()
        print(f"===== {path} bytes={len(raw)} sha256={digest(raw)} =====")
        print(raw.decode(errors="replace"))

    log_path = Path("/generation-evidence/codex-output.log")
    log_raw = log_path.read_bytes()
    log_text = log_raw.decode(errors="replace")
    print(
        f"===== {log_path} bytes={len(log_raw)} lines={len(log_text.splitlines())} "
        f"sha256={digest(log_raw)} ====="
    )
    for needle in (
        "RESULT:",
        "#Top",
        "WarnStuckClaimState",
        "VALIDATED",
        "SOUND-BUT-LIMITED",
        "FORMALLY-SOUND-UNVALIDATED",
        "Incomplete work",
    ):
        matches = [line for line in log_text.splitlines() if needle in line]
        print(f"log_pattern={needle!r} count={len(matches)}")
        for line in matches[-5:]:
            print(f"  {line[:500]}")

    trace_paths = sorted(Path("/generation-evidence/codex-trace").rglob("*"))
    trace_files = [path for path in trace_paths if path.is_file() and not path.is_symlink()]
    type_counts: Counter[str] = Counter()
    payload_type_counts: Counter[str] = Counter()
    function_counts: Counter[str] = Counter()
    parse_errors = 0
    total_lines = 0
    trace_hash = hashlib.sha256()
    final_messages: list[str] = []
    for path in trace_files:
        raw = path.read_bytes()
        trace_hash.update(path.relative_to("/generation-evidence/codex-trace").as_posix().encode())
        trace_hash.update(b"\0")
        trace_hash.update(raw)
        for line in raw.splitlines():
            total_lines += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                parse_errors += 1
                continue
            record_type = str(record.get("type"))
            type_counts[record_type] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = payload.get("type")
                if payload_type is not None:
                    payload_type_counts[str(payload_type)] += 1
                if payload_type == "function_call":
                    function_counts[str(payload.get("name"))] += 1
                if payload_type == "agent_message" and payload.get("phase") == "final_answer":
                    final_messages.append(str(payload.get("message")))
    print(
        "===== structured trace "
        f"files={len(trace_files)} lines={total_lines} parse_errors={parse_errors} "
        f"independent_content_sha256={trace_hash.hexdigest()} ====="
    )
    print(f"record_types={dict(sorted(type_counts.items()))}")
    print(f"payload_types={dict(sorted(payload_type_counts.items()))}")
    print(f"function_calls={dict(sorted(function_counts.items()))}")
    for message in final_messages:
        print(f"trace_final_message={message!r}")
    return 1 if parse_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
