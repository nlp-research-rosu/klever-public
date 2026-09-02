#!/usr/bin/env python3
"""Extract all human-readable generation-trace claims without trusting them."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


def text_content(content: Any) -> str:
    if isinstance(content, list):
        pieces: list[str] = []
        for item in content:
            if isinstance(item, dict):
                pieces.append(str(item.get("text", item)))
            else:
                pieces.append(str(item))
        return "\n".join(pieces)
    return str(content)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    trace_path = Path(sys.argv[1])
    counts: Counter[tuple[str, str]] = Counter()
    records: list[str] = []

    for line_number, raw_line in enumerate(
        trace_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        record = json.loads(raw_line)
        outer_type = str(record.get("type", "-"))
        payload = record.get("payload", {})
        payload_type = str(payload.get("type", "-")) if isinstance(payload, dict) else "-"
        counts[(outer_type, payload_type)] += 1
        prefix = (
            f"LINE {line_number} TIMESTAMP {record.get('timestamp', '-')} "
            f"TYPE {outer_type}/{payload_type}"
        )

        if outer_type == "response_item" and isinstance(payload, dict):
            if payload_type == "message":
                records.append(
                    f"{prefix}\nROLE {payload.get('role', '-')}\n"
                    f"{text_content(payload.get('content', ''))}"
                )
            elif payload_type in {"function_call", "custom_tool_call"}:
                records.append(
                    f"{prefix}\nNAME {payload.get('name', '-')}\n"
                    f"ARGUMENTS {payload.get('arguments', payload.get('input', ''))}"
                )
            elif payload_type in {"function_call_output", "custom_tool_call_output"}:
                records.append(
                    f"{prefix}\nCALL_ID {payload.get('call_id', '-')}\n"
                    f"OUTPUT {text_content(payload.get('output', ''))}"
                )
            elif payload_type == "reasoning":
                encrypted = payload.get("encrypted_content", "")
                records.append(
                    f"{prefix}\nSUMMARY {payload.get('summary', [])}\n"
                    f"ENCRYPTED_CONTENT_LENGTH {len(encrypted)}"
                )
            else:
                records.append(f"{prefix}\nPAYLOAD_KEYS {sorted(payload)}")
        elif outer_type == "event_msg" and isinstance(payload, dict):
            reduced = {
                key: value
                for key, value in payload.items()
                if key not in {"memory_citation"}
            }
            records.append(f"{prefix}\n{json.dumps(reduced, sort_keys=True)}")
        elif outer_type in {"session_meta", "turn_context", "world_state"}:
            keys = sorted(payload) if isinstance(payload, dict) else []
            records.append(f"{prefix}\nPAYLOAD_KEYS {keys}")
        else:
            records.append(f"{prefix}\nPAYLOAD {json.dumps(payload, sort_keys=True)}")

    print("TYPE COUNTS")
    for (outer_type, payload_type), count in sorted(counts.items()):
        print(f"{count:4d} {outer_type}/{payload_type}")
    print("READABLE RECORDS")
    print("\n\n".join(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
