#!/usr/bin/env python3
"""Read every structured trace record and emit a bounded tool-call inventory."""

import hashlib
import json
from pathlib import Path


for path in sorted(Path("/generation-evidence/codex-trace").rglob("*.jsonl")):
    print(f"trace={path} sha256={hashlib.sha256(path.read_bytes()).hexdigest()}")
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            item = json.loads(line)
            payload = item.get("payload") or {}
            if (
                item.get("type") == "response_item"
                and payload.get("type") in {"function_call", "custom_tool_call"}
            ):
                arguments = str(
                    payload.get("arguments", payload.get("input", ""))
                ).replace("\n", "\\n")
                if len(arguments) > 500:
                    arguments = arguments[:500] + "...[bounded]"
                print(
                    f"{line_number}\t{payload.get('name')}\t{arguments}"
                )
