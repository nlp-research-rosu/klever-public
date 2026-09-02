#!/usr/bin/env python3
"""Parse every record in the untrusted generation trace and print a bounded summary."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 2

    path = pathlib.Path(sys.argv[1])
    rows: list[dict] = []
    for line_number, line in enumerate(path.open(encoding="utf-8"), 1):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as err:
            print(f"invalid JSON at line {line_number}: {err}", file=sys.stderr)
            return 1

    record_types = collections.Counter(row.get("type", "<missing>") for row in rows)
    payload_types = collections.Counter(
        (row.get("type", "<missing>"), row.get("payload", {}).get("type", "<missing>"))
        for row in rows
    )
    print(f"path={path}")
    print(f"valid_json_records={len(rows)}")
    print(f"record_types={dict(sorted(record_types.items()))}")
    print("payload_types:")
    for key, count in sorted(payload_types.items()):
        print(f"  {key}: {count}")

    custom_calls = [
        row
        for row in rows
        if row.get("type") == "response_item"
        and row.get("payload", {}).get("type") == "custom_tool_call"
    ]
    function_calls = [
        row
        for row in rows
        if row.get("type") == "response_item"
        and row.get("payload", {}).get("type") == "function_call"
    ]
    print(f"custom_tool_calls={len(custom_calls)}")
    print(f"function_calls={len(function_calls)}")
    print("custom_call_names:")
    print(
        dict(
            sorted(
                collections.Counter(
                    row["payload"].get("name", "<missing>") for row in custom_calls
                ).items()
            )
        )
    )
    print("function_call_names:")
    print(
        dict(
            sorted(
                collections.Counter(
                    row["payload"].get("name", "<missing>") for row in function_calls
                ).items()
            )
        )
    )

    assistant_texts: list[str] = []
    for row in rows:
        payload = row.get("payload", {})
        if (
            row.get("type") == "response_item"
            and payload.get("type") == "message"
            and payload.get("role") == "assistant"
        ):
            for content in payload.get("content", []):
                if content.get("type") == "output_text":
                    assistant_texts.append(content.get("text", ""))
    print(f"assistant_output_messages={len(assistant_texts)}")
    if assistant_texts:
        print("final_untrusted_assistant_claim:")
        print(assistant_texts[-1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
