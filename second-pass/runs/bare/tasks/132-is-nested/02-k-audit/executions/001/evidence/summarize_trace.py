#!/usr/bin/env python3
import collections
import json
import sys

path = sys.argv[1]
counts = collections.Counter()
final_messages = []
with open(path, "r", encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        item = json.loads(line)
        counts[item.get("type")] += 1
        payload = item.get("payload", {})
        if (
            item.get("type") == "event_msg"
            and payload.get("type") in {"agent_message", "task_complete"}
        ):
            final_messages.append(
                {
                    "line": line_number,
                    "timestamp": item.get("timestamp"),
                    "event": payload.get("type"),
                    "message": payload.get("message")
                    or payload.get("last_agent_message"),
                }
            )

print("TYPE_COUNTS")
print(json.dumps(dict(sorted(counts.items())), indent=2))
print("FINAL_MESSAGES")
print(json.dumps(final_messages, indent=2))
