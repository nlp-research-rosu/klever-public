#!/usr/bin/env python3
"""Read the complete candidate trace/log and extract its audit-relevant claims."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path


TRACE = Path(
    "/candidate/codex-trace/2026/07/22/"
    "rollout-2026-07-22T06-34-43-019f899b-497c-79f0-a88b-47cd648deece.jsonl"
)
TEXT_LOG = Path("/candidate/codex-output.log")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
commands: list[str] = []
tool_outputs: list[str] = []
agent_messages: list[str] = []
json_lines = 0

with TRACE.open(encoding="utf-8") as stream:
    for json_lines, line in enumerate(stream, 1):
        item = json.loads(line)
        top_types[item.get("type", "<missing>")] += 1
        payload = item.get("payload", {})
        payload_types[payload.get("type", "<missing>")] += 1
        if item.get("type") == "response_item":
            if payload.get("type") == "custom_tool_call":
                commands.append(str(payload.get("input", "")))
            elif payload.get("type") == "custom_tool_call_output":
                fragments = payload.get("output", [])
                text = "".join(
                    str(fragment.get("text", ""))
                    for fragment in fragments
                    if isinstance(fragment, dict)
                )
                tool_outputs.append(text)
        if item.get("type") == "event_msg" and payload.get("type") == "agent_message":
            agent_messages.append(str(payload.get("message", "")))

text_lines = 0
claim_hits: list[tuple[int, str]] = []
needles = (
    "#Top",
    "kprove",
    "krun",
    "5914",
    "mismatch",
    "RESULT:",
    "spec-vacuity",
    "rotation oracle",
)
with TEXT_LOG.open(encoding="utf-8", errors="replace") as stream:
    for text_lines, line in enumerate(stream, 1):
        if any(needle in line for needle in needles):
            claim_hits.append((text_lines, line.rstrip()))

print(f"TRACE={TRACE}")
print(f"TRACE_SHA256={digest(TRACE)}")
print(f"TRACE_JSON_LINES={json_lines}")
print(f"TRACE_TOP_TYPES={dict(sorted(top_types.items()))}")
print(f"TRACE_PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
print(f"TEXT_LOG={TEXT_LOG}")
print(f"TEXT_LOG_SHA256={digest(TEXT_LOG)}")
print(f"TEXT_LOG_LINES={text_lines}")
print(f"COMMAND_RECORDS={len(commands)}")
for index, command in enumerate(commands, 1):
    print(f"COMMAND[{index}]={command}")
print(f"TOOL_OUTPUT_RECORDS={len(tool_outputs)}")
for index, output in enumerate(tool_outputs, 1):
    relevant = [
        line
        for line in output.splitlines()
        if any(needle in line for needle in needles)
    ]
    if relevant:
        print(f"TOOL_OUTPUT_RELEVANT[{index}]=")
        print("\n".join(relevant))
print(f"AGENT_MESSAGES={len(agent_messages)}")
for index, message in enumerate(agent_messages, 1):
    if any(needle in message for needle in needles):
        print(f"AGENT_CLAIM[{index}]={message}")
print(f"TEXT_CLAIM_HITS={len(claim_hits)}")
for line_number, line in claim_hits:
    print(f"TEXT_CLAIM[{line_number}]={line}")

