#!/usr/bin/env python3
"""Parse every generation trace record and summarize untrusted generation actions."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


trace_paths = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
line_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_names: Counter[str] = Counter()
call_count = 0
output_count = 0
task_complete_count = 0
parse_errors: list[tuple[str, int, str]] = []
command_heads: list[str] = []

for path in trace_paths:
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            try:
                record = json.loads(line)
            except Exception as err:  # pragma: no cover - audit diagnostic
                parse_errors.append((str(path), line_number, repr(err)))
                continue
            line_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                payload_types[payload_type] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    call_count += 1
                    tool_name = str(payload.get("name"))
                    tool_names[tool_name] += 1
                    raw = payload.get("arguments", payload.get("input", ""))
                    if tool_name in {"exec", "exec_command"} and isinstance(raw, str):
                        normalized = " ".join(raw.split())
                        command_heads.append(normalized[:240])
                if payload_type in {
                    "function_call_output",
                    "custom_tool_call_output",
                }:
                    output_count += 1
                if payload_type == "task_complete":
                    task_complete_count += 1

print(f"trace_file_count={len(trace_paths)}")
print(f"trace_record_count={sum(line_types.values())}")
print(f"trace_parse_error_count={len(parse_errors)}")
print(f"top_level_types={dict(sorted(line_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"tool_names={dict(sorted(tool_names.items()))}")
print(f"tool_call_count={call_count}")
print(f"tool_output_count={output_count}")
print(f"task_complete_count={task_complete_count}")
print(f"captured_exec_command_count={len(command_heads)}")
for index, command in enumerate(command_heads, 1):
    print(f"EXEC_CALL_{index:03d}={command}")
for error in parse_errors:
    print(f"PARSE_ERROR={error}")
print("TRACE_INVENTORY_COMPLETE")
