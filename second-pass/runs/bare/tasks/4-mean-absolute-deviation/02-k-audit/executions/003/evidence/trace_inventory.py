#!/usr/bin/env python3
"""Parse every structured-trace record and summarize its evidentiary contents."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")


def squash(text: str, limit: int = 500) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    return compact if len(compact) <= limit else compact[:limit] + "…"


def main() -> int:
    records = []
    outer_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    calls: list[tuple[int, str, str]] = []
    messages: list[tuple[int, str, str, str]] = []
    outputs: list[tuple[int, int, str]] = []

    files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    for path in files:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                record = json.loads(line)
                records.append(record)
                outer = str(record.get("type"))
                outer_types[outer] += 1
                payload = record.get("payload") or {}
                inner = str(payload.get("type", ""))
                if inner:
                    payload_types[inner] += 1
                if inner == "custom_tool_call":
                    calls.append((line_number, str(payload.get("name")), squash(str(payload.get("input")), 1200)))
                elif inner == "custom_tool_call_output":
                    raw = json.dumps(payload.get("output"), ensure_ascii=False)
                    outputs.append((line_number, len(raw), squash(raw)))
                elif inner == "message":
                    content = payload.get("content") or []
                    text = " ".join(str(item.get("text", "")) for item in content if isinstance(item, dict))
                    messages.append((line_number, str(payload.get("role")), str(payload.get("phase", "")), squash(text, 1000)))
                elif outer == "event_msg" and inner == "agent_message":
                    messages.append((line_number, "assistant-event", str(payload.get("phase", "")), squash(str(payload.get("message")), 1000)))

    output_text = OUTPUT_LOG.read_text(encoding="utf-8", errors="replace")
    print(f"trace_files={len(files)} trace_records={len(records)}")
    print(f"outer_types={dict(sorted(outer_types.items()))}")
    print(f"payload_types={dict(sorted(payload_types.items()))}")
    print(f"codex_output_lines={output_text.count(chr(10))} codex_output_bytes={len(output_text.encode())}")
    print(f"codex_output_has_final_marker={'RESULT: KPROVE_PASSED' in output_text}")
    print("MESSAGES")
    for item in messages:
        print(item)
    print("TOOL_CALLS")
    for item in calls:
        print(item)
    print("TOOL_OUTPUT_SUMMARIES")
    for item in outputs:
        print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
