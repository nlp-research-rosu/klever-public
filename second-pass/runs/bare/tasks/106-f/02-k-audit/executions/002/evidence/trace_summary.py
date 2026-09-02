#!/usr/bin/env python3
"""Summarize all structured generation-trace events without trusting them."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


def main() -> None:
    traces = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
    print(f"trace_files={len(traces)}")
    for trace in traces:
        counts: Counter[tuple[object, object, object]] = Counter()
        calls: dict[str, tuple[int, str, str]] = {}
        outputs: dict[str, tuple[int, str]] = {}
        lines = 0
        for line_no, line in enumerate(trace.open(encoding="utf-8"), 1):
            lines = line_no
            record = json.loads(line)
            payload = record.get("payload", {})
            key = (
                record.get("type"),
                payload.get("type"),
                payload.get("role"),
            )
            counts[key] += 1
            event_type = payload.get("type")
            if event_type in {"function_call", "custom_tool_call"}:
                call_id = payload.get("call_id", "")
                body = payload.get("arguments", payload.get("input", ""))
                calls[call_id] = (line_no, payload.get("name", ""), str(body))
            elif event_type in {"function_call_output", "custom_tool_call_output"}:
                call_id = payload.get("call_id", "")
                outputs[call_id] = (line_no, str(payload.get("output", "")))
        print(f"trace={trace} lines={lines}")
        for key, count in sorted(counts.items(), key=lambda item: str(item[0])):
            print(f"event_count {count} {key}")
        for call_id, (line_no, name, body) in calls.items():
            output_line, output = outputs.get(call_id, (-1, "<missing>"))
            compact_body = body.replace("\n", "\\n")
            compact_output = output.replace("\n", "\\n")
            print(
                f"call line={line_no} output_line={output_line} "
                f"name={name} id={call_id}"
            )
            print(f"  input={compact_body[:800]}")
            print(f"  output={compact_output[:800]}")


if __name__ == "__main__":
    main()
