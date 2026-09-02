#!/usr/bin/env python3
"""Validate and summarize every record in the untrusted generation trace/log."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/23/"
    "rollout-2026-07-23T06-00-25-019f8ea2-3fbc-7e83-b2d2-0c095b02db55.jsonl"
)
OUTPUT = Path("/generation-evidence/codex-output.log")


def bounded(value: object, limit: int = 1200) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x00", "\\0")
    return text if len(text) <= limit else text[:limit] + "...[TRUNCATED]"


outer_types: collections.Counter[str] = collections.Counter()
payload_types: collections.Counter[str] = collections.Counter()
response_types: collections.Counter[str] = collections.Counter()
calls: list[tuple[int, str, object]] = []
function_outputs: list[tuple[int, object]] = []
decode_failures: list[tuple[int, str]] = []

with TRACE.open(encoding="utf-8") as handle:
    for line_number, line in enumerate(handle, 1):
        try:
            record = json.loads(line)
        except Exception as err:  # pragma: no cover - audit diagnostic
            decode_failures.append((line_number, repr(err)))
            continue
        outer_types[str(record.get("type"))] += 1
        payload = record.get("payload")
        if isinstance(payload, dict):
            payload_types[str(payload.get("type"))] += 1
            if record.get("type") == "response_item":
                response_types[str(payload.get("type"))] += 1
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    calls.append(
                        (
                            line_number,
                            str(payload.get("name")),
                            payload.get("arguments", payload.get("input")),
                        )
                    )
                if payload.get("type") in {
                    "function_call_output",
                    "custom_tool_call_output",
                }:
                    function_outputs.append(
                        (line_number, payload.get("output", payload.get("content")))
                    )

log_lines = OUTPUT.read_text(encoding="utf-8", errors="replace").splitlines()
signals = collections.Counter()
patterns = {
    "top": re.compile(r"(?m)^\s*#Top\s*$"),
    "warn_stuck": re.compile(r"WarnStuckClaimState"),
    "error": re.compile(r"\b(?:ERROR|Error|error:|\[Error\])\b"),
    "kprove": re.compile(r"\bkprove\b"),
    "kompile": re.compile(r"\bkompile\b"),
    "krun": re.compile(r"\bkrun\b"),
    "result_marker": re.compile(r"RESULT:\s"),
}
whole_log = "\n".join(log_lines)
for name, pattern in patterns.items():
    signals[name] = len(pattern.findall(whole_log))

print(f"TRACE_LINES={sum(outer_types.values())}")
print(f"TRACE_JSON_DECODE_FAILURES={len(decode_failures)} {decode_failures}")
print(f"TRACE_OUTER_TYPES={dict(sorted(outer_types.items()))}")
print(f"TRACE_PAYLOAD_TYPES={dict(sorted(payload_types.items()))}")
print(f"TRACE_RESPONSE_TYPES={dict(sorted(response_types.items()))}")
print(f"TRACE_TOOL_CALLS={len(calls)}")
for line_number, name, args in calls:
    print(f"CALL line={line_number} name={name} args={bounded(args)}")
print(f"TRACE_TOOL_OUTPUTS={len(function_outputs)}")
for line_number, output in function_outputs:
    output_text = bounded(output, 800)
    interesting = any(
        needle in output_text
        for needle in (
            "Process exited with code",
            "#Top",
            "Error",
            "WarnStuck",
            "timed out",
            "failed",
        )
    )
    if interesting:
        print(f"OUTPUT line={line_number} data={output_text}")
print(f"CODEX_OUTPUT_LINES={len(log_lines)}")
print(f"CODEX_OUTPUT_SIGNALS={dict(sorted(signals.items()))}")
