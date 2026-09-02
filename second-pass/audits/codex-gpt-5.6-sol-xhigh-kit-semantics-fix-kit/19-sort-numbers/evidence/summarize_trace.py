#!/usr/bin/env python3
"""Render the untrusted generation trace into a bounded, auditable event index."""

import json
import pathlib
import sys


def compact(value: object, limit: int = 1000) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit] + " ...[truncated]"


def main() -> int:
    path = pathlib.Path(sys.argv[1])
    counts: dict[str, int] = {}
    rows: list[str] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            payload = event.get("payload", {})
            event_type = event.get("type", "")
            payload_type = payload.get("type", "") if isinstance(payload, dict) else ""
            key = f"{event_type}/{payload_type}"
            counts[key] = counts.get(key, 0) + 1

            if event_type != "response_item" or not isinstance(payload, dict):
                continue
            if payload_type == "message":
                content = payload.get("content", [])
                texts = [item.get("text", "") for item in content if isinstance(item, dict)]
                rows.append(
                    f"{line_number}\tMESSAGE/{payload.get('role', '')}\t{compact(' '.join(texts))}"
                )
            elif payload_type == "function_call":
                rows.append(
                    f"{line_number}\tCALL/{payload.get('name', '')}\t{compact(payload.get('arguments', ''))}"
                )
            elif payload_type == "function_call_output":
                rows.append(
                    f"{line_number}\tOUTPUT\t{compact(payload.get('output', ''))}"
                )
            elif payload_type == "custom_tool_call":
                rows.append(
                    f"{line_number}\tCUSTOM-CALL/{payload.get('name', '')}\t{compact(payload.get('input', ''))}"
                )
            elif payload_type == "custom_tool_call_output":
                rows.append(
                    f"{line_number}\tCUSTOM-OUTPUT\t{compact(payload.get('output', ''))}"
                )

    print("EVENT COUNTS")
    for key in sorted(counts):
        print(f"{counts[key]:4d} {key}")
    print("\nMESSAGES, CALLS, AND OUTPUTS")
    print("\n".join(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
