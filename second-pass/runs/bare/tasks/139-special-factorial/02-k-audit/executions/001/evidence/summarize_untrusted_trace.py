#!/usr/bin/env python3
"""Parse the complete candidate JSONL trace as untrusted provenance evidence."""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()

    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    relevant_commands: list[str] = []
    agent_messages: list[str] = []
    lines = 0

    with args.trace.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            lines += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError as err:
                print(f"INVALID_JSON line={line_number} error={err}")
                return 1
            top_type = str(item.get("type", "<missing>"))
            top_types[top_type] += 1
            payload = item.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type", "<missing>"))
                payload_types[f"{top_type}/{payload_type}"] += 1
                if top_type == "event_msg" and payload_type == "agent_message":
                    message = payload.get("message")
                    if isinstance(message, str):
                        agent_messages.append(message)
                command = payload.get("command")
                if isinstance(command, str) and any(
                    marker in command
                    for marker in ("kompile", "kprove", "krun", "prove.sh")
                ):
                    relevant_commands.append(command)
                arguments = payload.get("arguments")
                if isinstance(arguments, str) and any(
                    marker in arguments
                    for marker in ("kompile", "kprove", "krun", "prove.sh")
                ):
                    relevant_commands.append(arguments)

    print(f"VALID_JSONL lines={lines}")
    print("TOP_TYPES")
    for name, count in sorted(top_types.items()):
        print(f"{count:4d} {name}")
    print("PAYLOAD_TYPES")
    for name, count in sorted(payload_types.items()):
        print(f"{count:4d} {name}")
    print(f"RELEVANT_COMMAND_RECORDS count={len(relevant_commands)}")
    for command in relevant_commands[:100]:
        print(command.replace("\n", "\\n"))
    if len(relevant_commands) > 100:
        print(f"... omitted {len(relevant_commands) - 100} records")
    print(f"AGENT_MESSAGES count={len(agent_messages)}")
    for message in agent_messages[-8:]:
        print(message.replace("\n", "\\n"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
