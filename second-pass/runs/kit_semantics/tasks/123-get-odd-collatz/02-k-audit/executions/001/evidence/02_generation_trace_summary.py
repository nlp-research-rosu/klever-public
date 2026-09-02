"""Validate and summarize every record in the launcher-owned generation trace."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/25/"
    "rollout-2026-07-25T02-26-36-019f982b-3454-72a0-9280-99e7bcf6de86.jsonl"
)


def main() -> None:
    outer_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    response_types: Counter[str] = Counter()
    tool_names: Counter[str] = Counter()
    parsed = []

    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            parsed.append(record)
            outer = str(record.get("type", "<missing>"))
            payload = record.get("payload")
            payload_type = (
                str(payload.get("type", "<missing>"))
                if isinstance(payload, dict)
                else type(payload).__name__
            )
            outer_types[outer] += 1
            payload_types[payload_type] += 1

            if isinstance(payload, dict):
                response = payload.get("response")
                if isinstance(response, dict):
                    response_types[str(response.get("type", "<missing>"))] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    tool_names[str(payload.get("name", "<missing>"))] += 1

            print(
                f"line={line_number} outer={outer} payload={payload_type} "
                f"timestamp={record.get('timestamp', '<missing>')}"
            )

    print(f"valid_json_records={len(parsed)}")
    print("outer_types=", dict(sorted(outer_types.items())))
    print("payload_types=", dict(sorted(payload_types.items())))
    print("response_types=", dict(sorted(response_types.items())))
    print("tool_names=", dict(sorted(tool_names.items())))
    if parsed:
        print("first_record=", json.dumps(parsed[0], sort_keys=True)[:4000])
        print("last_record=", json.dumps(parsed[-1], sort_keys=True)[:12000])


if __name__ == "__main__":
    main()

