#!/usr/bin/env python3
"""Bounded structural summary of the untrusted generation JSONL."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path


def main(path: Path) -> int:
    top = collections.Counter()
    payload = collections.Counter()
    malformed = []
    final_messages = []
    tool_commands = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                item = json.loads(line)
            except Exception as err:  # evidence parser must keep going
                malformed.append([line_number, str(err)])
                continue
            top[item.get("type")] += 1
            body = item.get("payload")
            if not isinstance(body, dict):
                continue
            payload[body.get("type")] += 1
            if body.get("type") == "agent_message":
                message = body.get("message", "")
                if "RESULT:" in message or body.get("phase") == "final_answer":
                    final_messages.append(message)
            if body.get("type") in {"function_call", "custom_tool_call"}:
                name = body.get("name")
                arguments = body.get("arguments") or body.get("input")
                if name or arguments:
                    tool_commands.append({"name": name, "arguments": arguments})
    summary = {
        "line_count": sum(top.values()),
        "top_level_types": dict(sorted(top.items(), key=lambda x: str(x[0]))),
        "payload_types": {
            str(key): value
            for key, value in sorted(payload.items(), key=lambda x: str(x[0]))
        },
        "malformed": malformed,
        "claimed_final_messages": final_messages[-3:],
        "tool_call_count": len(tool_commands),
        "last_five_tool_calls": tool_commands[-5:],
    }
    json.dump(summary, sys.stdout, indent=2, sort_keys=True)
    print()
    return int(bool(malformed))


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
