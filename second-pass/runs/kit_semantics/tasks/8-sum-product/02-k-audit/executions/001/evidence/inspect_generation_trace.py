#!/usr/bin/env python3
"""Read every generation-trace record and summarize its untrusted claims/actions."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
call_names: collections.Counter[str] = collections.Counter()
commands: list[tuple[int, str]] = []
patch_targets: list[tuple[int, list[str]]] = []
assistant_messages: list[tuple[int, str, str]] = []
errors: list[str] = []
line_count = 0

for trace_file in trace_files:
    with trace_file.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            line_count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"{trace_file}:{line_number}: {error}")
                continue
            record_type = str(record.get("type"))
            top_types[record_type] += 1
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue
            payload_type = str(payload.get("type"))
            payload_types[payload_type] += 1
            if record_type == "response_item" and payload_type == "function_call":
                name = str(payload.get("name"))
                call_names[name] += 1
                raw_arguments = payload.get("arguments", "")
                try:
                    arguments = json.loads(raw_arguments)
                except (TypeError, json.JSONDecodeError):
                    arguments = {}
                if name == "exec_command":
                    commands.append((line_number, str(arguments.get("cmd", ""))))
                elif name == "apply_patch":
                    patch = str(arguments.get("input", raw_arguments))
                    targets = re.findall(
                        r"^\*\*\* (?:Add|Update|Delete) File: (.+)$",
                        patch,
                        flags=re.MULTILINE,
                    )
                    patch_targets.append((line_number, targets))
            if record_type == "response_item" and payload_type == "message":
                if payload.get("role") != "assistant":
                    continue
                phase = str(payload.get("phase", ""))
                texts = []
                for item in payload.get("content", []):
                    if isinstance(item, dict) and isinstance(item.get("text"), str):
                        texts.append(item["text"])
                if texts:
                    assistant_messages.append((line_number, phase, "\n".join(texts)))
            if record_type == "event_msg" and payload_type == "agent_message":
                message = payload.get("message")
                if isinstance(message, str):
                    assistant_messages.append(
                        (line_number, str(payload.get("phase", "")), message)
                    )

print(f"TRACE_FILES={len(trace_files)}")
for trace_file in trace_files:
    print(f"TRACE_FILE={trace_file} bytes={trace_file.stat().st_size}")
print(f"TRACE_LINES={line_count}")
print(f"JSON_ERRORS={len(errors)}")
for error in errors:
    print(f"JSON_ERROR {error}")
print("TOP_LEVEL_TYPES")
for name, count in sorted(top_types.items()):
    print(f"  {name}: {count}")
print("PAYLOAD_TYPES")
for name, count in sorted(payload_types.items()):
    print(f"  {name}: {count}")
print("FUNCTION_CALLS")
for name, count in sorted(call_names.items()):
    print(f"  {name}: {count}")
print("EXEC_COMMAND_INVENTORY")
for line_number, command in commands:
    one_line = command.replace("\n", "\\n")
    print(f"  line={line_number} cmd={one_line}")
print("PATCH_TARGET_INVENTORY")
for line_number, targets in patch_targets:
    print(f"  line={line_number} targets={targets}")
print("ASSISTANT_MESSAGE_INVENTORY")
for line_number, phase, message in assistant_messages:
    bounded = message if len(message) <= 1200 else message[:1200] + "...[truncated]"
    print(f"  line={line_number} phase={phase!r} text={bounded!r}")

output_path = Path("/generation-evidence/codex-output.log")
output_bytes = output_path.read_bytes()
decoded = output_bytes.decode("utf-8", errors="replace")
print(f"CODEX_OUTPUT_BYTES={len(output_bytes)}")
print(f"CODEX_OUTPUT_LINES={decoded.count(chr(10))}")
print(f"CODEX_OUTPUT_REPLACEMENT_CHARS={decoded.count(chr(0xfffd))}")
patterns = [
    r"kprove",
    r"#Top",
    r"WarnStuckClaimState",
    r"verification\.k",
    r"spec(?:-body-mutation|-vacuity)?\.k",
    r"PROOF\.md",
    r"RESULT:",
]
output_lines = decoded.splitlines()
for pattern in patterns:
    regex = re.compile(pattern, re.IGNORECASE)
    hits = [(index + 1, text) for index, text in enumerate(output_lines) if regex.search(text)]
    print(f"CODEX_OUTPUT_PATTERN={pattern!r} HITS={len(hits)}")
    for index, text in hits[:20]:
        bounded = text if len(text) <= 500 else text[:500] + "...[truncated]"
        print(f"  {index}: {bounded}")
    if len(hits) > 20:
        print(f"  ... {len(hits) - 20} additional hits omitted")

raise SystemExit(1 if errors else 0)
