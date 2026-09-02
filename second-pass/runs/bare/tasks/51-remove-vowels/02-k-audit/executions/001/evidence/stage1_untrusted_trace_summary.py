#!/usr/bin/env python3
"""Read the complete untrusted generation trace and emit a bounded summary."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


trace_files = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
print(f"trace_files={len(trace_files)}")
for path in trace_files:
    digest = hashlib.sha256()
    top_types: collections.Counter[str] = collections.Counter()
    payload_types: collections.Counter[str] = collections.Counter()
    tool_names: collections.Counter[str] = collections.Counter()
    parse_errors = 0
    lines = 0
    claims: list[str] = []
    with path.open("rb") as raw:
        for line_no, raw_line in enumerate(raw, 1):
            lines += 1
            digest.update(raw_line)
            try:
                item = json.loads(raw_line)
            except Exception as error:  # evidence parser only
                parse_errors += 1
                if len(claims) < 20:
                    claims.append(f"line {line_no} JSON_ERROR {error}")
                continue
            top_types[str(item.get("type"))] += 1
            payload = item.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                name = payload.get("name")
                if isinstance(name, str):
                    tool_names[name] += 1
                message = payload.get("message")
                if isinstance(message, str) and (
                    "#Top" in message or "KPROVE" in message or "kprove" in message
                ):
                    claims.append(
                        f"line {line_no} message={message[:500].replace(chr(10), ' ')}"
                    )
                command_input = payload.get("input")
                if isinstance(command_input, str) and (
                    "kprove" in command_input
                    or "kompile" in command_input
                    or "krun" in command_input
                ):
                    claims.append(
                        f"line {line_no} tool_input="
                        f"{command_input[:500].replace(chr(10), ' ')}"
                    )
    print(f"path={path}")
    print(
        f"lines={lines} parse_errors={parse_errors} sha256={digest.hexdigest()}"
    )
    print(f"top_types={dict(top_types)}")
    print(f"payload_types={dict(payload_types)}")
    print(f"tool_names={dict(tool_names)}")
    print(f"selected_untrusted_claims={len(claims)}")
    for claim in claims[:40]:
        print(claim)
