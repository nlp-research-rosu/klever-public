#!/usr/bin/env python3
"""Bounded extraction of provenance claims from untrusted candidate records."""

from __future__ import annotations

import collections
import glob
import json
from pathlib import Path


def bounded(text: str, limit: int = 1200) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...[truncated; original chars={len(text)}]"


print("RUN_INPUT_JSON")
print(json.dumps(json.loads(Path("/candidate/run-input.json").read_text()), indent=2))
print("METRICS_JSON")
print(json.dumps(json.loads(Path("/candidate/metrics.json").read_text()), indent=2))
print("CODEX_LAST")
print(Path("/candidate/codex-last.txt").read_text())

for trace_path in glob.glob("/candidate/codex-trace/**/*.jsonl", recursive=True):
    records = [json.loads(line) for line in Path(trace_path).read_text().splitlines()]
    print(f"TRACE {trace_path}")
    print("TOP_LEVEL_TYPES", dict(collections.Counter(r.get("type") for r in records)))
    print(
        "PAYLOAD_TYPES",
        dict(collections.Counter(r.get("payload", {}).get("type") for r in records)),
    )
    for record in records:
        payload = record.get("payload", {})
        payload_type = payload.get("type")
        if payload_type == "agent_message":
            print("AGENT_MESSAGE", bounded(payload.get("message", "")))
        elif payload_type == "task_complete":
            print("TASK_COMPLETE", bounded(payload.get("last_agent_message", "")))
        elif payload_type in {"custom_tool_call", "function_call"}:
            raw = payload.get("input", "") or payload.get("arguments", "")
            if any(term in raw for term in ("kompile", "krun", "kprove", "prove.sh")):
                print("TOOL_CALL", bounded(raw))
        elif payload_type in {"custom_tool_call_output", "function_call_output"}:
            output = payload.get("output", [])
            texts = [
                item.get("text", "")
                for item in output
                if isinstance(item, dict) and item.get("type") == "input_text"
            ]
            combined = "\n".join(texts)
            if any(term in combined for term in ("#Top", "WarnStuck", "<k>")):
                print("TOOL_OUTPUT", bounded(combined))

generation_log = Path("/candidate/codex-output.log").read_text().splitlines()
needles = ("#Top", "WarnStuckClaimState", "RESULT:", "kprove spec.k")
print("CODEX_OUTPUT_RELEVANT_LINES")
for number, line in enumerate(generation_log, 1):
    if any(needle in line for needle in needles):
        print(f"{number}:{line}")
