#!/usr/bin/env python3
"""Parse every generation trace record and summarize the untrusted transcript."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T04-51-26-019f8e63-156b-7ea1-86de-c4146950b376.jsonl"
)
LOG = Path("/generation-evidence/codex-output.log")

top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
response_types: collections.Counter[str] = collections.Counter()
function_names: collections.Counter[str] = collections.Counter()
commands: list[tuple[int, str, str]] = []
agent_messages: list[tuple[int, str]] = []
parse_errors: list[tuple[int, str]] = []

raw_lines = TRACE.read_text(encoding="utf-8").splitlines()
for line_number, line in enumerate(raw_lines, 1):
    try:
        row = json.loads(line)
    except Exception as err:
        parse_errors.append((line_number, repr(err)))
        continue
    row_type = str(row.get("type"))
    top_types[row_type] += 1
    payload = row.get("payload")
    if isinstance(payload, dict):
        payload_type = str(payload.get("type"))
        payload_types[payload_type] += 1
        if row_type == "response_item":
            response_types[payload_type] += 1
            if payload_type == "function_call":
                name = str(payload.get("name"))
                function_names[name] += 1
                args = payload.get("arguments", "")
                commands.append((line_number, name, str(args)))
        if payload_type == "agent_message":
            agent_messages.append((line_number, str(payload.get("message", ""))))

log_bytes = LOG.read_bytes()
log_text = log_bytes.decode("utf-8")
patterns = {
    "KPROVE_TOP": r"#Top",
    "STUCK": r"WarnStuckClaimState",
    "KPROVE": r"\bkprove\b",
    "KOMPILE": r"\bkompile\b",
    "KRUN": r"\bkrun\b",
    "PATCH": r"\bapply_patch\b",
    "UNSOUND_WORD": r"\bunsound\b",
    "MUTATION_WORD": r"\bmutation\b",
    "ORACLE_WORD": r"\boracle\b",
}

print(f"trace_path={TRACE}")
print(f"trace_lines={len(raw_lines)}")
print(f"trace_parse_errors={parse_errors}")
print(f"top_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"response_types={dict(sorted(response_types.items()))}")
print(f"function_names={dict(sorted(function_names.items()))}")
print(f"function_call_count={len(commands)}")
for line_number, name, arguments in commands:
    one_line = arguments.replace("\n", "\\n")
    if len(one_line) > 1200:
        one_line = one_line[:1200] + "...[bounded]"
    print(f"CALL trace_line={line_number} name={name} args={one_line}")
print(f"agent_message_count={len(agent_messages)}")
for line_number, message in agent_messages:
    print(f"AGENT trace_line={line_number} message={message!r}")
print(f"log_bytes={len(log_bytes)}")
print(f"log_lines={len(log_text.splitlines())}")
print(f"log_nul_bytes={log_bytes.count(bytes([0]))}")
for name, pattern in patterns.items():
    print(f"log_count_{name}={len(re.findall(pattern, log_text))}")
