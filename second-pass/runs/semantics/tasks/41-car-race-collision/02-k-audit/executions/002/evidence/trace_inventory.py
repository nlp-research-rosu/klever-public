#!/usr/bin/env python3
"""Read every structured trace record and print a bounded semantic inventory."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


root = Path("/generation-evidence/codex-trace")
records: list[tuple[Path, int, dict]] = []
for path in sorted(root.rglob("*.jsonl")):
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            records.append((path, line_number, json.loads(line)))

outer_types = Counter(record.get("type", "<missing>") for _, _, record in records)
payload_types = Counter(
    record.get("payload", {}).get("type", "<missing>") for _, _, record in records
)
print(f"records={len(records)}")
print(f"outer_types={dict(sorted(outer_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")

for path, line_number, record in records:
    payload = record.get("payload", {})
    outer_type = record.get("type")
    payload_type = payload.get("type")
    prefix = f"{path.relative_to(root)}:{line_number} {outer_type}/{payload_type}"
    if outer_type == "session_meta":
        print(
            f"{prefix} session_id={payload.get('session_id')} "
            f"cwd={payload.get('cwd')} cli={payload.get('cli_version')}"
        )
    elif payload_type == "function_call":
        arguments = payload.get("arguments", "")
        if len(arguments) > 700:
            arguments = arguments[:700] + "...<bounded>"
        print(
            f"{prefix} name={payload.get('name')} "
            f"call_id={payload.get('call_id')} arguments={arguments!r}"
        )
    elif payload_type == "function_call_output":
        output = payload.get("output", "")
        first = output.replace("\n", "\\n")
        if len(first) > 700:
            first = first[:700] + "...<bounded>"
        print(
            f"{prefix} call_id={payload.get('call_id')} "
            f"output={first!r}"
        )
    elif payload_type in {
        "task_started",
        "task_complete",
        "agent_message",
        "message",
    }:
        text = payload.get("message") or payload.get("last_agent_message")
        if text is None and isinstance(payload.get("content"), list):
            text = " ".join(
                part.get("text", "")
                for part in payload["content"]
                if isinstance(part, dict)
            )
        text = (text or "").replace("\n", "\\n")
        if len(text) > 700:
            text = text[:700] + "...<bounded>"
        print(f"{prefix} text={text!r}")
    elif payload_type == "token_count":
        usage = payload.get("info", {}).get("total_token_usage", {})
        print(f"{prefix} total_usage={usage}")
    elif payload_type == "reasoning":
        print(
            f"{prefix} encrypted={bool(payload.get('encrypted_content'))} "
            f"summary_items={len(payload.get('summary', []))}"
        )
    else:
        print(f"{prefix} keys={sorted(payload)}")
