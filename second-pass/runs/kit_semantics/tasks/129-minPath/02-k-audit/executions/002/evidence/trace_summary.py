#!/usr/bin/env python3
import collections
import hashlib
import json
from pathlib import Path

files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
print(f"files={len(files)}")
for path in files:
    counts = collections.Counter()
    payload_counts = collections.Counter()
    commands = []
    messages = []
    tool_failures = []
    line_count = 0
    with path.open("rb") as stream:
        raw = stream.read()
    for line_count, line in enumerate(raw.splitlines(), 1):
        event = json.loads(line)
        counts[event.get("type")] += 1
        payload = event.get("payload") or {}
        payload_counts[str(payload.get("type"))] += 1
        if payload.get("type") == "custom_tool_call":
            inp = payload.get("input", "")
            if '"cmd"' in inp or "exec_command" in inp:
                commands.append((line_count, inp[:1000].replace("\n", "\\n")))
        if payload.get("type") in {"agent_message", "message"}:
            msg = payload.get("message")
            if msg:
                messages.append((line_count, msg.replace("\n", "\\n")[:1200]))
        if payload.get("type") == "custom_tool_call_output":
            text = json.dumps(payload.get("output", ""))
            if any(token in text for token in ("exit_code\\\":1", "exit_code\\\":2", "WarnStuckClaimState", "Error")):
                tool_failures.append((line_count, text[:1200].replace("\n", "\\n")))
    print(f"path={path.relative_to('/generation-evidence/codex-trace')} lines={line_count} bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()}")
    print("event_types=" + json.dumps(counts, sort_keys=True))
    print("payload_types=" + json.dumps(payload_counts, sort_keys=True))
    print(f"tool_commands={len(commands)} plain_messages={len(messages)} flagged_tool_outputs={len(tool_failures)}")
    print("COMMANDS_BEGIN")
    for item in commands:
        print(f"line={item[0]} {item[1]}")
    print("COMMANDS_END")
    print("MESSAGES_BEGIN")
    for item in messages:
        print(f"line={item[0]} {item[1]}")
    print("MESSAGES_END")
    print("FLAGGED_OUTPUTS_BEGIN")
    for item in tool_failures:
        print(f"line={item[0]} {item[1]}")
    print("FLAGGED_OUTPUTS_END")
