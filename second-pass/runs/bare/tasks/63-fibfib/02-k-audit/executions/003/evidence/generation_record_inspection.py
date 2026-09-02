#!/usr/bin/env python3
"""Parse every structured generation-trace record and scan the full text log."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T05-21-03-019f8957-d850-7863-8a70-b8af8aa93fc1.jsonl"
)
LOG = Path("/generation-evidence/codex-output.log")

outer_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
line_count = 0
final_messages: list[str] = []
for line_count, line in enumerate(TRACE.open(encoding="utf-8"), 1):
    item = json.loads(line)
    outer_types[str(item.get("type"))] += 1
    payload = item.get("payload")
    if isinstance(payload, dict):
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        if payload_type in {"function_call", "custom_tool_call"}:
            tool_names[str(payload.get("name") or payload.get("tool_name"))] += 1
        if payload_type in {"message", "agent_message"}:
            text = payload.get("message") or payload.get("text") or payload.get("content")
            if isinstance(text, str) and "RESULT:" in text:
                final_messages.append(text[-800:])

log_text = LOG.read_text(encoding="utf-8")
patterns = {
    "kompile_mentions": r"\bkompile\b",
    "kprove_mentions": r"\bkprove\b",
    "krun_mentions": r"\bkrun\b",
    "top_mentions": r"#Top",
    "stuck_mentions": r"WarnStuckClaimState",
    "passed_markers": r"RESULT: KPROVE_PASSED",
}

print(f"trace_json_lines={line_count}")
print(f"trace_outer_types={dict(sorted(outer_types.items()))}")
print(f"trace_payload_types={dict(sorted(payload_types.items()))}")
print(f"trace_tool_names={dict(sorted(tool_names.items()))}")
print(f"text_log_chars={len(log_text)} text_log_lines={len(log_text.splitlines())}")
for label, pattern in patterns.items():
    print(f"{label}={len(re.findall(pattern, log_text))}")
print(f"trace_final_message_count={len(final_messages)}")
for index, message in enumerate(final_messages, 1):
    print(f"trace_final_message_{index}={message!r}")
