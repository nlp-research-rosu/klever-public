#!/usr/bin/env python3
"""Bounded summary of the untrusted generation records read during Stage 1."""

from __future__ import annotations

import collections
import json
from pathlib import Path


ROOT = Path("/generation-evidence")
TRACE = next((ROOT / "codex-trace").rglob("*.jsonl"))


outer_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
function_names: collections.Counter[str] = collections.Counter()
assistant_messages: list[str] = []

with TRACE.open(encoding="utf-8") as handle:
    for line in handle:
        record = json.loads(line)
        outer_types[record.get("type", "<missing>")] += 1
        payload = record.get("payload", {})
        if isinstance(payload, dict):
            payload_types[str(payload.get("type", "<missing>"))] += 1
            if "role" in payload:
                roles[str(payload["role"])] += 1
            if payload.get("type") in {"function_call", "custom_tool_call"}:
                function_names[str(payload.get("name", "<missing>"))] += 1
            if payload.get("type") == "message" and payload.get("role") == "assistant":
                pieces = payload.get("content", [])
                text = "\n".join(
                    piece.get("text", "")
                    for piece in pieces
                    if isinstance(piece, dict)
                    and piece.get("type") in {"output_text", "input_text"}
                )
                if text:
                    assistant_messages.append(text)

print(f"TRACE path={TRACE} records={sum(outer_types.values())}")
for key, value in sorted(outer_types.items()):
    print(f"OUTER_TYPE {key} count={value}")
for key, value in sorted(payload_types.items()):
    print(f"PAYLOAD_TYPE {key} count={value}")
for key, value in sorted(roles.items()):
    print(f"ROLE {key} count={value}")
for key, value in sorted(function_names.items()):
    print(f"FUNCTION {key} count={value}")

output_log = (ROOT / "codex-output.log").read_text(errors="replace")
last = (ROOT / "codex-last.txt").read_text(errors="replace").strip()
prompt = (ROOT / "prompt.txt").read_text(errors="replace")
print(
    "GENERATION_TEXT"
    f" output_chars={len(output_log)}"
    f" prompt_chars={len(prompt)}"
    f" last_chars={len(last)}"
    f" top_mentions={output_log.count('#Top')}"
    f" validated_mentions={output_log.count('VALIDATED')}"
    f" expected_failure_mentions={output_log.count('EXPECTED FAILURE')}"
)
trace_final = assistant_messages[-1].strip() if assistant_messages else ""
print(f"FINAL_MATCH codex_last_equals_trace_final={str(last == trace_final).lower()}")
print("UNTRUSTED_FINAL_BEGIN")
print(last)
print("UNTRUSTED_FINAL_END")
