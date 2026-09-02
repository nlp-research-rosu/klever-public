#!/usr/bin/env python3
"""Summarize every JSONL record in the untrusted generation trace."""

import json
import pathlib
import sys


def short(value, limit=240):
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[:limit] + "..."


def main():
    path = pathlib.Path(sys.argv[1])
    counts = {}
    records = 0
    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            item = json.loads(line)
            records += 1
            top_type = item.get("type", "")
            payload = item.get("payload") or {}
            payload_type = payload.get("type", "")
            key = (top_type, payload_type)
            counts[key] = counts.get(key, 0) + 1
            fields = [
                item.get("timestamp", ""),
                top_type,
                payload_type,
                payload.get("name", ""),
                payload.get("role", ""),
            ]
            interesting = ""
            if payload_type in {
                "function_call",
                "function_call_output",
                "custom_tool_call",
                "custom_tool_call_output",
                "message",
                "agent_message",
            }:
                interesting = (
                    payload.get("arguments")
                    or payload.get("output")
                    or payload.get("content")
                    or ""
                )
            print(
                f"{line_no:04d}\t"
                + "\t".join(short(field, 120) for field in fields)
                + "\t"
                + short(interesting)
            )
    print(f"RECORDS\t{records}")
    for key, value in sorted(counts.items()):
        print(f"COUNT\t{key[0]}\t{key[1]}\t{value}")


if __name__ == "__main__":
    main()
