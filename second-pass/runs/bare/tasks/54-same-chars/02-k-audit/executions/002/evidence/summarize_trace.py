#!/usr/bin/env python3
"""Parse every untrusted structured trace record and summarize its substance."""

from __future__ import annotations

import collections
import json
from pathlib import Path


root = Path("/generation-evidence/codex-trace")
counts: collections.Counter[tuple[str, str]] = collections.Counter()
records = 0

for path in sorted(root.rglob("*.jsonl")):
    print(f"FILE {path}")
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            obj = json.loads(line)
            records += 1
            top_type = obj.get("type", "")
            payload = obj.get("payload", {})
            payload_type = payload.get("type", "") if isinstance(payload, dict) else ""
            counts[(top_type, payload_type)] += 1

            if top_type != "response_item" or not isinstance(payload, dict):
                continue

            if payload_type == "message":
                role = payload.get("role")
                texts = [
                    item.get("text", "")
                    for item in payload.get("content", [])
                    if isinstance(item, dict) and "text" in item
                ]
                if role in {"user", "assistant"}:
                    joined = "\n".join(texts)
                    print(
                        f"LINE {line_number} MESSAGE role={role} "
                        f"chars={len(joined)}\n{joined}"
                    )
            elif payload_type == "custom_tool_call":
                print(
                    f"LINE {line_number} TOOL_CALL "
                    f"name={payload.get('name')} input={payload.get('input')}"
                )
            elif payload_type == "custom_tool_call_output":
                output = str(payload.get("output", ""))
                print(
                    f"LINE {line_number} TOOL_OUTPUT chars={len(output)}\n"
                    f"{output}"
                )

print(f"RECORDS {records}")
for (top_type, payload_type), count in sorted(counts.items()):
    print(f"COUNT {top_type}/{payload_type or '-'} {count}")
