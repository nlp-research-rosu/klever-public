#!/usr/bin/env python3
"""Summarize all claim-bearing records in the untrusted generation trace."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def text_content(content: object) -> str:
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        value = item.get("text", item.get("output_text", item.get("input_text", "")))
        if isinstance(value, str):
            parts.append(value)
    return "\n".join(parts)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    event_counts: collections.Counter[tuple[str, str, str]] = collections.Counter()
    records: list[str] = []

    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            event_type = str(record.get("type", ""))
            payload = record.get("payload")
            if not isinstance(payload, dict):
                payload = {}
            payload_type = str(payload.get("type", ""))
            role = str(payload.get("role", ""))
            event_counts[(event_type, payload_type, role)] += 1

            if event_type != "response_item":
                continue
            prefix = f"line={line_number} timestamp={record.get('timestamp')} type={payload_type}"
            if payload_type == "message":
                body = text_content(payload.get("content"))
                # System/developer/user prompts are provenance, not candidate claims.
                # Include their hashes/lengths while printing candidate-authored messages.
                if role == "assistant":
                    records.append(f"{prefix} role={role}\n{body}")
                else:
                    records.append(
                        f"{prefix} role={role} content_chars={len(body)}"
                    )
            elif payload_type == "function_call":
                records.append(
                    f"{prefix} name={payload.get('name')} arguments={payload.get('arguments')}"
                )
            elif payload_type == "function_call_output":
                output = str(payload.get("output", ""))
                records.append(
                    f"{prefix} output_chars={len(output)}\n{output[-6000:]}"
                )

    print("TRACE_EVENT_HISTOGRAM")
    for key, count in sorted(event_counts.items()):
        print(count, *key, sep="\t")
    print("CLAIM_BEARING_RECORDS")
    for record in records:
        print(record)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
