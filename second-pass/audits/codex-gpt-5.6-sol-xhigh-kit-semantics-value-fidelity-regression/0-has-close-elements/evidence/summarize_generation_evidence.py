#!/usr/bin/env python3
"""Read every byte/record of the untrusted generation reports and summarize claims."""

from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path


CANDIDATE = Path("/candidate")
ANSI = re.compile(rb"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_from_content(content: object) -> str:
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        text = item.get("text")
        if isinstance(text, str):
            parts.append(text)
    return "\n".join(parts)


def main() -> int:
    for name in [
        "run-input.json",
        "metrics.json",
        "codex-last.txt",
        "codex-output.log",
    ]:
        data = (CANDIDATE / name).read_bytes()
        print(
            f"READ {name}: bytes={len(data)} lines={data.count(bytes([10]))} "
            f"sha256={sha256(data)}"
        )

    output_bytes = (CANDIDATE / "codex-output.log").read_bytes()
    cleaned = ANSI.sub(b"", output_bytes).decode("utf-8", errors="replace")
    relevant_pattern = re.compile(
        r"(?:#Top|WarnStuckClaimState|EXPECTED FAILURE|RESULT:|"
        r"Incomplete work|Gate [ABC]|kompile |kprove |krun |"
        r"differential|mutation|bridge)",
        re.IGNORECASE,
    )
    relevant: list[str] = []
    seen: set[str] = set()
    for line in cleaned.splitlines():
        line = "".join(
            character for character in line if character == "\t" or ord(character) >= 32
        ).strip()
        if relevant_pattern.search(line) and line not in seen:
            seen.add(line)
            relevant.append(line)
    print(f"codex_output_unique_relevant_lines={len(relevant)}")
    for line in relevant[:120]:
        print(f"  OUTPUT_CLAIM {line[:1000]}")
    if len(relevant) > 120:
        print(f"  OUTPUT_CLAIM [... {len(relevant) - 120} more omitted ...]")

    trace_paths = sorted((CANDIDATE / "codex-trace").glob("**/*.jsonl"))
    print(f"trace_files={len(trace_paths)}")
    for trace_path in trace_paths:
        raw = trace_path.read_bytes()
        type_counts: collections.Counter[str] = collections.Counter()
        payload_counts: collections.Counter[str] = collections.Counter()
        call_counts: collections.Counter[str] = collections.Counter()
        assistant_messages: list[str] = []
        invalid_records = 0
        record_count = 0
        for line in raw.splitlines():
            record_count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                invalid_records += 1
                continue
            outer_type = str(record.get("type"))
            payload = record.get("payload")
            payload = payload if isinstance(payload, dict) else {}
            payload_type = str(payload.get("type"))
            type_counts[outer_type] += 1
            payload_counts[payload_type] += 1
            if outer_type == "response_item" and payload_type in {
                "function_call",
                "custom_tool_call",
            }:
                call_counts[str(payload.get("name"))] += 1
            if (
                outer_type == "response_item"
                and payload_type == "message"
                and payload.get("role") == "assistant"
            ):
                assistant_messages.append(text_from_content(payload.get("content")))
        print(
            f"TRACE {trace_path.relative_to(CANDIDATE)}: bytes={len(raw)} "
            f"sha256={sha256(raw)} records={record_count} invalid={invalid_records}"
        )
        print(f"  outer_types={dict(type_counts)}")
        print(f"  payload_types={dict(payload_counts)}")
        print(f"  tool_calls={dict(call_counts)}")
        print(f"  assistant_messages={len(assistant_messages)}")
        for message in assistant_messages[-6:]:
            one_line = " ".join(message.split())
            print(f"  ASSISTANT_CLAIM {one_line[:2000]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
