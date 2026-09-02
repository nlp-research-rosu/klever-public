#!/usr/bin/env python3
"""Parse the untrusted generation trace and report only structural facts."""

import collections
import json
from pathlib import Path

TRACE = Path(
    "/candidate/codex-trace/2026/07/23/"
    "rollout-2026-07-23T04-38-09-019f8e56-ef59-7241-ab33-f94739461da5.jsonl"
)

counts = collections.Counter()
line_count = 0
parse_errors = []
first_time = None
last_time = None
final_messages = []
with TRACE.open(encoding="utf-8") as stream:
    for line_count, line in enumerate(stream, 1):
        try:
            item = json.loads(line)
        except Exception as err:
            parse_errors.append((line_count, type(err).__name__, str(err)))
            continue
        counts[item.get("type", "<missing>")] += 1
        payload = item.get("payload", {})
        if (
            item.get("type") == "event_msg"
            and payload.get("type") == "agent_message"
            and payload.get("phase") == "final_answer"
        ):
            final_messages.append(payload.get("message"))
        timestamp = item.get("timestamp")
        if first_time is None:
            first_time = timestamp
        last_time = timestamp

print(f"path={TRACE}")
print(f"is_symlink={TRACE.is_symlink()}")
print(f"lines={line_count}")
print(f"parse_errors={len(parse_errors)}")
print(f"first_timestamp={first_time}")
print(f"last_timestamp={last_time}")
for key in sorted(counts):
    print(f"type[{key}]={counts[key]}")
for error in parse_errors:
    print(f"error={error!r}")
print(f"final_message_count={len(final_messages)}")
for index, message in enumerate(final_messages):
    print(f"final_message[{index}]={message!r}")
