#!/usr/bin/env python3
"""Read and summarize every record required by legacy-selected-stage1."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path


json_records = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    Path("/generation-evidence/invocation.json"),
    Path("/generation-evidence/metrics.json"),
    Path("/generation-evidence/usage.json"),
]
text_records = [
    Path("/generation-evidence/codex-last.txt"),
    Path("/generation-evidence/codex-output.log"),
    Path("/generation-evidence/prompt.txt"),
]

for path in json_records:
    document = json.loads(path.read_text())
    print(
        f"JSON {path}: object keys={sorted(document)} "
        f"status={document.get('status', 'n/a')}"
    )

for path in text_records:
    text = path.read_text()
    print(
        f"TEXT {path}: bytes={len(text.encode())} lines={len(text.splitlines())} "
        f"KPROVE_PASSED={text.count('KPROVE_PASSED')} #Top={text.count('#Top')}"
    )

trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
assert len(trace_files) == 1
top_types: Counter[str] = Counter()
payload_types: Counter[str] = Counter()
tool_calls = []
assistant_messages = []
for line_number, line in enumerate(trace_files[0].read_text().splitlines(), 1):
    record = json.loads(line)
    top_types[record.get("type")] += 1
    payload = record.get("payload", {})
    payload_types[payload.get("type")] += 1
    if record.get("type") == "response_item":
        if payload.get("type") == "custom_tool_call":
            raw = payload.get("input") or payload.get("arguments") or ""
            first_line = str(raw).splitlines()[0][:240]
            tool_calls.append((line_number, payload.get("name"), first_line))
        elif payload.get("type") == "message" and payload.get("role") == "assistant":
            text = "\n".join(
                part.get("text", "")
                for part in payload.get("content", [])
                if isinstance(part, dict)
            )
            if text:
                assistant_messages.append((line_number, text))

print(f"TRACE {trace_files[0]}: lines={sum(top_types.values())}")
print(f"TRACE top-level types: {dict(top_types)}")
print(f"TRACE payload types: {dict(payload_types)}")
for line_number, name, first_line in tool_calls:
    print(f"TRACE CALL line={line_number} tool={name}: {first_line}")
for line_number, message in assistant_messages:
    print(f"TRACE ASSISTANT line={line_number}: {message}")

last = Path("/generation-evidence/codex-last.txt").read_text().strip()
print(f"CODEX-LAST:\n{last}")
