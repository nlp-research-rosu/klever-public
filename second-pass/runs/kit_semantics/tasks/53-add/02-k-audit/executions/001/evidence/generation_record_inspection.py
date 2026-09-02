#!/usr/bin/env python3
"""Read and summarize every structured generation-trace record."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


trace_root = Path("/generation-evidence/codex-trace")
trace_files = sorted(trace_root.rglob("*"))
jsonl_files = [path for path in trace_files if path.is_file()]

outer_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
roles: collections.Counter[str] = collections.Counter()
tool_names: collections.Counter[str] = collections.Counter()
commands: list[str] = []
parse_failures: list[str] = []
line_count = 0

for path in jsonl_files:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    print(f"TRACE_FILE path={path} bytes={path.stat().st_size} sha256={digest}")
    with path.open() as stream:
        for line_number, line in enumerate(stream, 1):
            line_count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as err:
                parse_failures.append(f"{path}:{line_number}: {err}")
                continue
            outer_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_type = str(payload.get("type"))
                payload_types[payload_type] += 1
                if "role" in payload:
                    roles[str(payload["role"])] += 1
                if payload_type in {"function_call", "custom_tool_call"}:
                    name = str(payload.get("name"))
                    tool_names[name] += 1
                    raw_args = payload.get("arguments") or payload.get("input")
                    if name in {"exec_command", "exec"} and isinstance(raw_args, str):
                        try:
                            args = json.loads(raw_args)
                            commands.append(str(args.get("cmd", raw_args)))
                        except json.JSONDecodeError:
                            commands.append(raw_args)

print(f"TRACE_JSONL_FILES={len(jsonl_files)}")
print(f"TRACE_LINES={line_count}")
print(f"TRACE_PARSE_FAILURES={len(parse_failures)}")
for failure in parse_failures:
    print(f"TRACE_PARSE_FAILURE {failure}")
print(f"OUTER_TYPES={dict(sorted(outer_types.items()))}")
print(f"PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
print(f"ROLES={dict(sorted(roles.items()))}")
print(f"TOOL_NAMES={dict(sorted(tool_names.items()))}")
print(f"EXTRACTED_EXEC_COMMANDS={len(commands)}")
for index, command in enumerate(commands):
    flattened = " ".join(command.splitlines())
    print(f"EXEC_COMMAND_{index:03d}={flattened}")

output_log = Path("/generation-evidence/codex-output.log")
with output_log.open(errors="replace") as stream:
    output_lines = 0
    output_chars = 0
    warning_lines = 0
    error_lines = 0
    top_lines = 0
    for line in stream:
        output_lines += 1
        output_chars += len(line)
        warning_lines += int("Warning" in line)
        error_lines += int("Error" in line or "ERROR" in line)
        top_lines += int(line.strip() == "#Top")

print(f"CODEX_OUTPUT_BYTES={output_log.stat().st_size}")
print(f"CODEX_OUTPUT_LINES={output_lines}")
print(f"CODEX_OUTPUT_DECODED_CHARS={output_chars}")
print(f"CODEX_OUTPUT_WARNING_LINES={warning_lines}")
print(f"CODEX_OUTPUT_ERROR_LINES={error_lines}")
print(f"CODEX_OUTPUT_EXACT_TOP_LINES={top_lines}")

raise SystemExit(1 if parse_failures else 0)
