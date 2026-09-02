#!/usr/bin/env python3
"""Parse every structured trace line and summarize untrusted generation claims."""

from __future__ import annotations

from collections import Counter
import glob
import json
from pathlib import Path


trace_paths = glob.glob("/generation-evidence/codex-trace/**/*.jsonl", recursive=True)
assert len(trace_paths) == 1, trace_paths
trace = Path(trace_paths[0])
top_types: Counter[str] = Counter()
subtypes: Counter[str] = Counter()
calls: Counter[str] = Counter()
exec_commands: list[tuple[int, str]] = []
agent_messages: list[tuple[int, str]] = []

line_count = 0
with trace.open() as stream:
    for line_count, line in enumerate(stream, 1):
        record = json.loads(line)
        top = record["type"]
        top_types[top] += 1
        payload = record.get("payload", {})
        subtype = payload.get("type") or payload.get("role") or "-"
        subtypes[f"{top}/{subtype}"] += 1
        if top == "response_item" and subtype in (
            "function_call",
            "custom_tool_call",
        ):
            name = payload.get("name", "custom")
            calls[name] += 1
            if name == "exec_command":
                arguments = json.loads(payload["arguments"])
                exec_commands.append((line_count, arguments["cmd"]))
        if top == "event_msg" and subtype == "agent_message":
            agent_messages.append((line_count, payload["message"]))

print(f"trace={trace}")
print(f"trace_json_lines_parsed={line_count}")
print(f"top_types={json.dumps(top_types, sort_keys=True)}")
print(f"subtypes={json.dumps(subtypes, sort_keys=True)}")
print(f"tool_calls={json.dumps(calls, sort_keys=True)}")
for line_number, command in exec_commands:
    print(
        f"exec_line={line_number}\t"
        + command.replace("\r", "\\r").replace("\n", "\\n")
    )
for line_number, message in agent_messages:
    print(
        f"agent_message_line={line_number}\t"
        + message.replace("\r", "\\r").replace("\n", "\\n")
    )

raw_output = Path("/generation-evidence/codex-output.log").read_text(
    errors="replace"
)
print(
    "codex_output_counts="
    + json.dumps(
        {
            "bytes": len(raw_output.encode(errors="replace")),
            "lines": raw_output.count("\n") + 1,
            "#Top": raw_output.count("#Top"),
            "WarnStuckClaimState": raw_output.count("WarnStuckClaimState"),
            "[Error]": raw_output.count("[Error]"),
        },
        sort_keys=True,
    )
)
print("STAGE1_GENERATION_RECORDS_PARSED")
