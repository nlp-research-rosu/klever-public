#!/usr/bin/env python3
import collections
import json
from pathlib import Path

trace = Path(
    "/generation-evidence/codex-trace/2026/07/30/"
    "rollout-2026-07-30T02-20-25-019fb1e5-574a-7a01-9912-7e04dde6ea3c.jsonl"
)

top_types = collections.Counter()
payload_types = collections.Counter()
response_roles = collections.Counter()
tool_calls = []
tool_outputs = []
messages = []
malformed = []

for line_no, raw in enumerate(trace.open(), 1):
    try:
        item = json.loads(raw)
    except Exception as err:
        malformed.append((line_no, str(err)))
        continue
    top_types[item.get("type")] += 1
    payload = item.get("payload", {})
    payload_types[payload.get("type")] += 1
    if item.get("type") == "response_item":
        ptype = payload.get("type")
        if ptype == "message":
            role = payload.get("role")
            response_roles[role] += 1
            texts = [
                c.get("text", "")
                for c in payload.get("content", [])
                if c.get("type") in {"input_text", "output_text"}
            ]
            messages.append((line_no, role, "\n".join(texts)))
        elif ptype in {"function_call", "custom_tool_call"}:
            tool_calls.append(
                (
                    line_no,
                    payload.get("name"),
                    payload.get("arguments", payload.get("input", "")),
                )
            )
        elif ptype in {"function_call_output", "custom_tool_call_output"}:
            tool_outputs.append(
                (
                    line_no,
                    payload.get("call_id"),
                    payload.get("output", ""),
                )
            )

print("trace", trace)
print("line_count", sum(top_types.values()))
print("malformed_count", len(malformed))
print("top_types", dict(sorted(top_types.items(), key=lambda x: str(x[0]))))
print("payload_types", dict(sorted(payload_types.items(), key=lambda x: str(x[0]))))
print("response_roles", dict(sorted(response_roles.items(), key=lambda x: str(x[0]))))
print("tool_call_count", len(tool_calls))
print("tool_output_count", len(tool_outputs))

print("tool_calls")
for line_no, name, args in tool_calls:
    flat = str(args).replace("\n", "\\n")
    if len(flat) > 1800:
        flat = flat[:1800] + "...[truncated]"
    print(f"  line={line_no} tool={name} args={flat}")

print("assistant_messages")
for line_no, role, msg in messages:
    if role != "assistant":
        continue
    flat = msg.replace("\n", "\\n")
    if len(flat) > 3000:
        flat = flat[:3000] + "...[truncated]"
    print(f"  line={line_no} role={role} text={flat}")

print("tool_outputs_status_summary")
for line_no, call_id, output in tool_outputs:
    text = str(output)
    markers = []
    for needle in (
        '"exit_code":0',
        '"exit_code": 0',
        '"exit_code":1',
        '"exit_code": 1',
        "#Top",
        "WarnStuckClaimState",
        "timed out",
        "Traceback",
    ):
        if needle in text:
            markers.append(needle)
    print(
        f"  line={line_no} call_id={call_id} chars={len(text)} "
        f"markers={markers}"
    )
