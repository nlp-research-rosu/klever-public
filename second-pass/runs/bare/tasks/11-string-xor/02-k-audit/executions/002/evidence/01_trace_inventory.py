#!/usr/bin/env python3
"""Parse the complete generation trace and summarize its untrusted claims."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_path = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T04-00-45-019f890e-53e2-7f21-9e88-38401bd1ffa8.jsonl"
)
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
function_calls = []
custom_tool_calls = []
agent_messages = []

with trace_path.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        record = json.loads(line)
        top_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1
            if payload.get("type") == "function_call":
                function_calls.append(
                    (
                        line_number,
                        str(payload.get("name")),
                        str(payload.get("arguments")),
                    )
                )
            elif payload.get("type") == "custom_tool_call":
                custom_tool_calls.append(
                    (
                        line_number,
                        str(payload.get("name")),
                        str(payload.get("input")),
                    )
                )
            elif payload.get("type") == "agent_message":
                agent_messages.append(
                    (line_number, str(payload.get("phase")), str(payload.get("message")))
                )

print(f"jsonl_records={sum(top_types.values())}")
print(f"top_level_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"function_calls={len(function_calls)}")
for line_number, name, arguments in function_calls:
    collapsed = " ".join(arguments.split())
    print(f"TRACE_CALL line={line_number} name={name} args={collapsed[:600]}")
print(f"custom_tool_calls={len(custom_tool_calls)}")
for line_number, name, tool_input in custom_tool_calls:
    collapsed = " ".join(tool_input.split())
    print(f"TRACE_CUSTOM_CALL line={line_number} name={name} input={collapsed[:1000]}")
print(f"agent_messages={len(agent_messages)}")
for line_number, phase, message in agent_messages:
    collapsed = " ".join(message.split())
    print(f"TRACE_MESSAGE line={line_number} phase={phase} text={collapsed[:600]}")

output_log = Path("/generation-evidence/codex-output.log").read_text(
    encoding="utf-8", errors="replace"
)
last = Path("/generation-evidence/codex-last.txt").read_text(
    encoding="utf-8", errors="replace"
)
prompt = Path("/generation-evidence/prompt.txt").read_text(
    encoding="utf-8", errors="replace"
)
print(f"codex_output_chars={len(output_log)}")
print(f"codex_output_lines={output_log.count(chr(10))}")
print(f"codex_last_chars={len(last)}")
print(f"generation_prompt_chars={len(prompt)}")
print(f"output_contains_final_marker={'RESULT: KPROVE_PASSED' in output_log}")
print(f"last_contains_final_marker={'RESULT: KPROVE_PASSED' in last}")
