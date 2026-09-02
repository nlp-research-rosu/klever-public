#!/usr/bin/env python3
"""Produce a bounded chronological inventory of the untrusted generation trace."""

from __future__ import annotations

import collections
import json
from pathlib import Path


trace_path = next(Path("/generation-evidence/codex-trace").rglob("*.jsonl"))
top_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
actions: list[str] = []
line_count = 0

with trace_path.open() as stream:
    for line_count, line in enumerate(stream, 1):
        item = json.loads(line)
        top_types[item.get("type", "<none>")] += 1
        payload = item.get("payload", {})
        payload_type = payload.get("type", "<none>")
        payload_types[payload_type] += 1
        if payload_type == "function_call":
            arguments = str(payload.get("arguments", "")).replace("\n", " ")
            actions.append(
                f"line {line_count}: function {payload.get('name')} {arguments[:700]}"
            )
        elif payload_type == "custom_tool_call":
            tool_input = str(payload.get("input", "")).replace("\n", " ")
            actions.append(
                f"line {line_count}: custom {payload.get('name')} {tool_input[:700]}"
            )
        elif payload_type == "message" and payload.get("role") == "assistant":
            text = " ".join(
                str(part.get("text", ""))
                for part in payload.get("content", [])
                if isinstance(part, dict)
            ).replace("\n", " ")
            if text:
                actions.append(f"line {line_count}: assistant {text[:700]}")

print(f"trace={trace_path}")
print(f"jsonl_lines={line_count}")
print(f"top_level_types={dict(sorted(top_types.items()))}")
print(f"payload_types={dict(sorted(payload_types.items()))}")
print(f"chronological_action_count={len(actions)}")
for action in actions:
    print(action)

output_log = Path("/generation-evidence/codex-output.log")
lines = output_log.read_text(errors="replace").splitlines()
print(f"codex_output_lines={len(lines)}")
print(f"codex_output_bytes={output_log.stat().st_size}")
for needle in (
    "RESULT: KPROVE_PASSED",
    "#Top",
    "prompt_examples=6 exhaustive_pairs=14641 mismatches=0",
    "EXPECTED_FAILURE: spec-vacuity.k exited 1",
    "EXPECTED_FAILURE: spec-body-mutation.k exited 1",
):
    matching = [index + 1 for index, line in enumerate(lines) if needle in line]
    print(f"codex_output_occurrences[{needle!r}]={matching}")
