#!/usr/bin/env python3
"""Parse every JSONL record in the untrusted generation trace and summarize it."""

from __future__ import annotations

import collections
import hashlib
import json
import pathlib
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: trace_summary.py TRACE.jsonl", file=sys.stderr)
        return 2

    path = pathlib.Path(sys.argv[1])
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    function_names: collections.Counter[str] = collections.Counter()
    commands: list[str] = []
    invalid: list[tuple[int, str]] = []
    timestamps: list[str] = []
    final_messages: list[str] = []

    digest = hashlib.sha256()
    line_count = 0
    with path.open("rb") as raw:
        for line_count, raw_line in enumerate(raw, 1):
            digest.update(raw_line)
            try:
                record = json.loads(raw_line)
            except Exception as err:  # noqa: BLE001 - audit malformed records
                invalid.append((line_count, repr(err)))
                continue

            top_types[str(record.get("type", "<none>"))] += 1
            timestamp = record.get("timestamp")
            if isinstance(timestamp, str):
                timestamps.append(timestamp)

            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<none>"))
                payload_types[payload_type] += 1
                if payload_type == "function_call":
                    name = str(payload.get("name", "<none>"))
                    function_names[name] += 1
                    arguments = payload.get("arguments")
                    if name == "exec_command" and isinstance(arguments, str):
                        try:
                            args = json.loads(arguments)
                            commands.append(str(args.get("cmd", "<missing cmd>")))
                        except json.JSONDecodeError:
                            commands.append("<malformed exec_command arguments>")
                if payload_type == "agent_message" and payload.get("phase") == "final_answer":
                    final_messages.append(str(payload.get("message", "")))

    print(f"path={path}")
    print(f"sha256={digest.hexdigest()}")
    print(f"lines={line_count}")
    print(f"invalid_json_lines={len(invalid)}")
    for lineno, error in invalid:
        print(f"invalid[{lineno}]={error}")
    if timestamps:
        print(f"first_timestamp={min(timestamps)}")
        print(f"last_timestamp={max(timestamps)}")
    print("top_types=" + json.dumps(dict(sorted(top_types.items())), sort_keys=True))
    print("payload_types=" + json.dumps(dict(sorted(payload_types.items())), sort_keys=True))
    print("function_names=" + json.dumps(dict(sorted(function_names.items())), sort_keys=True))
    print(f"exec_command_count={len(commands)}")
    for index, command in enumerate(commands, 1):
        one_line = " ".join(command.splitlines())
        if len(one_line) > 1000:
            one_line = one_line[:1000] + "...<truncated>"
        print(f"exec_command[{index}]={one_line}")
    print(f"final_message_count={len(final_messages)}")
    for index, message in enumerate(final_messages, 1):
        print(f"final_message[{index}]={message!r}")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
