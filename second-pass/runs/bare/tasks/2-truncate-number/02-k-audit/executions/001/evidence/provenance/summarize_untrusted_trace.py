#!/usr/bin/env python3
"""Summarize candidate generation JSONL as untrusted provenance claims."""

from __future__ import annotations

import collections
import json
import pathlib
import sys


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} TRACE.jsonl", file=sys.stderr)
        return 64

    path = pathlib.Path(sys.argv[1])
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    commands: list[str] = []
    salient: list[str] = []
    line_count = 0

    with path.open(encoding="utf-8") as stream:
        for line_count, line in enumerate(stream, 1):
            record = json.loads(line)
            top_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
            for obj in walk(record):
                command = obj.get("command")
                if isinstance(command, str) and command not in commands:
                    commands.append(command)
                for key in ("text", "output", "last_agent_message"):
                    text = obj.get(key)
                    if not isinstance(text, str):
                        continue
                    if any(
                        needle in text
                        for needle in (
                            "#Top",
                            "WarnStuckClaimState",
                            "RESULT:",
                            "Expected failure",
                            "exited 0",
                        )
                    ):
                        compact = " ".join(text.split())
                        if compact not in salient:
                            salient.append(compact[:600])

    print(f"path: {path}")
    print(f"valid_json_lines: {line_count}")
    print(f"top_level_types: {dict(sorted(top_types.items()))}")
    print(f"payload_types: {dict(sorted(payload_types.items()))}")
    print(f"unique_embedded_commands: {len(commands)}")
    for index, command in enumerate(commands, 1):
        print(f"command[{index}]: {' '.join(command.split())}")
    print(f"salient_untrusted_claims: {len(salient)}")
    for index, claim in enumerate(salient, 1):
        print(f"claim[{index}]: {claim}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
