#!/usr/bin/env python3
import collections
import json
from pathlib import Path

trace_path = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T04-16-12-019f891c-7928-74e1-8f32-d57a688478a9.jsonl"
)
output_path = Path("/generation-evidence/codex-output.log")

rows = [json.loads(line) for line in trace_path.read_text().splitlines()]
print(f"TRACE_LINES {len(rows)}")
print("TRACE_TYPES", dict(collections.Counter(row["type"] for row in rows)))

payload_types = collections.Counter(
    row.get("payload", {}).get("type") for row in rows if isinstance(row.get("payload"), dict)
)
print("PAYLOAD_TYPES", dict(payload_types))

tool_calls = []
tool_outputs = 0
assistant_messages = []
for line_number, row in enumerate(rows, 1):
    payload = row.get("payload", {})
    if payload.get("type") == "custom_tool_call":
        tool_calls.append((line_number, payload.get("name"), payload.get("input", "")))
    elif payload.get("type") == "custom_tool_call_output":
        tool_outputs += 1
    elif payload.get("type") == "message" and payload.get("role") == "assistant":
        content = payload.get("content", [])
        texts = [item.get("text", "") for item in content if isinstance(item, dict)]
        assistant_messages.append((line_number, "\n".join(texts)))

print(f"TOOL_CALLS {len(tool_calls)}")
print(f"TOOL_OUTPUTS {tool_outputs}")
for line_number, name, tool_input in tool_calls:
    flattened = " ".join(str(tool_input).split())
    if any(token in flattened for token in ("kompile", "krun", "kprove", "prove.sh")):
        print(f"PROOF_TOOL_CALL line={line_number} name={name} input={flattened[:900]}")

print(f"ASSISTANT_MESSAGES {len(assistant_messages)}")
for line_number, message in assistant_messages:
    if "KPROVE_PASSED" in message or "#Top" in message:
        print(f"UNTRUSTED_FINAL_CLAIM line={line_number} text={' '.join(message.split())[:900]}")

output_text = output_path.read_text()
print(f"CODEX_OUTPUT_LINES {len(output_text.splitlines())}")
print(f"CODEX_OUTPUT_CHARS {len(output_text)}")
for needle in ["#Top", "KPROVE_PASSED", "intVal ( 3 )", "Backend crashed"]:
    print(f"CODEX_OUTPUT_OCCURRENCES {needle!r} {output_text.count(needle)}")

usage = json.loads(Path("/generation-evidence/usage.json").read_text())
print("USAGE_SELECTED_EVENT", usage["selected_event"])
print("USAGE_STATUS", usage["status"])
print("GENERATION_RECORD_SUMMARY_OK")
