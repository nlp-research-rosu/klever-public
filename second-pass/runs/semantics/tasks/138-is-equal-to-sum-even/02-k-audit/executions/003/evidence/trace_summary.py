#!/usr/bin/env python3
"""Parse every structured generation trace record and emit a bounded summary."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


trace_files = sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
print(f"trace_file_count={len(trace_files)}")
total = 0
for path in trace_files:
    print(f"FILE {path}")
    for line_number, line in enumerate(path.open(), 1):
        record = json.loads(line)
        total += 1
        payload = record.get("payload", {})
        record_type = record.get("type", "")
        payload_type = payload.get("type", "")
        role = payload.get("role", "")
        name = payload.get("name", "")
        status = payload.get("status", "")
        detail = ""
        if payload_type in {
            "function_call",
            "function_call_output",
            "custom_tool_call",
            "custom_tool_call_output",
        }:
            value = payload.get(
                "arguments",
                payload.get("output", payload.get("input", "")),
            )
            encoded = str(value).encode()
            detail = f" bytes={len(encoded)} sha256={hashlib.sha256(encoded).hexdigest()}"
        elif payload_type == "message" and role == "assistant":
            texts = [
                item["text"]
                for item in payload.get("content", [])
                if isinstance(item, dict) and "text" in item
            ]
            encoded = "\n".join(texts).encode()
            detail = f" assistant_text_bytes={len(encoded)} sha256={hashlib.sha256(encoded).hexdigest()}"
        print(
            f"{line_number:03d} record={record_type} payload={payload_type} "
            f"role={role} name={name} status={status}{detail}"
        )
print(f"parsed_json_record_count={total}")
print("OVERALL: PASS")
sys.exit(0)
