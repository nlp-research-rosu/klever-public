#!/usr/bin/env python3
"""Read every generation trace/log record and emit a bounded audit summary."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re


ROOT = Path("/generation-evidence")
TRACE = (
    ROOT
    / "codex-trace/2026/07/23/"
    "rollout-2026-07-23T02-35-02-019f8de6-3522-7992-a411-c8389da4eabd.jsonl"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flattened_strings(value: object):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from flattened_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from flattened_strings(item)


print("$ python3 /audit-output/evidence/stage1_trace_inspect.py")
raw_lines = TRACE.read_text().splitlines()
events = [json.loads(line) for line in raw_lines]
print(f"trace_path={TRACE}")
print(f"trace_sha256={digest(TRACE)}")
print(f"trace_json_lines={len(raw_lines)} valid_json_lines={len(events)}")
print(f"trace_first_timestamp={events[0].get('timestamp')}")
print(f"trace_last_timestamp={events[-1].get('timestamp')}")

top_types = Counter(event.get("type", "<missing>") for event in events)
payload_types = Counter(
    event.get("payload", {}).get("type", "<missing>") for event in events
)
print("top_level_type_counts=" + json.dumps(top_types, sort_keys=True))
print("payload_type_counts=" + json.dumps(payload_types, sort_keys=True))

signals = Counter()
tool_calls: list[tuple[int, str, str]] = []
messages: list[tuple[int, str, str]] = []
for line_number, event in enumerate(events, 1):
    payload = event.get("payload", {})
    payload_type = payload.get("type", "")
    if payload_type in {"function_call", "custom_tool_call"}:
        name = str(payload.get("name", payload.get("tool_name", "<unnamed>")))
        args = str(payload.get("arguments", payload.get("input", "")))
        tool_calls.append((line_number, name, args))
    if payload_type == "message":
        role = str(payload.get("role", ""))
        text = "\n".join(flattened_strings(payload.get("content", "")))
        messages.append((line_number, role, text))
    for text in flattened_strings(payload):
        for label, pattern in {
            "#Top": r"(?m)^#Top$",
            "WarnStuckClaimState": r"WarnStuckClaimState",
            "CompilerError": r"\[Error\] Compiler",
            "ProverError": r"\[Error\] Prover",
            "KPROVE_PASSED": r"KPROVE_PASSED",
        }.items():
            signals[label] += len(re.findall(pattern, text))

print(f"tool_call_count={len(tool_calls)}")
for line_number, name, args in tool_calls:
    one_line = args.replace("\r", "\\r").replace("\n", "\\n")
    if len(one_line) > 1000:
        one_line = one_line[:1000] + "...<truncated>"
    print(f"tool_call trace_line={line_number} name={name} args={one_line}")
print("trace_signal_counts=" + json.dumps(signals, sort_keys=True))

for path in [
    ROOT / "codex-output.log",
    ROOT / "codex-last.txt",
    ROOT / "prompt.txt",
    ROOT / "invocation.json",
    ROOT / "metrics.json",
    ROOT / "usage.json",
    ROOT / "legacy-metrics.json",
    ROOT / "legacy-run-input.json",
]:
    data = path.read_bytes()
    lines = data.count(b"\n")
    print(
        f"fully_read path={path} bytes={len(data)} "
        f"newline_count={lines} sha256={hashlib.sha256(data).hexdigest()}"
    )

log_text = (ROOT / "codex-output.log").read_text(errors="replace")
patterns = {
    "shell_invocation": re.compile(r"^/bin/bash -lc .+ in /work$", re.MULTILINE),
    "top": re.compile(r"^#Top$", re.MULTILINE),
    "stuck": re.compile(r"WarnStuckClaimState"),
    "compiler_error": re.compile(r"\[Error\] Compiler"),
    "prover_error": re.compile(r"\[Error\] Prover"),
}
for name, pattern in patterns.items():
    matches = list(pattern.finditer(log_text))
    print(f"codex_output_{name}_count={len(matches)}")
    if name == "shell_invocation":
        for match in matches:
            line_number = log_text.count("\n", 0, match.start()) + 1
            line = match.group(0)
            if len(line) > 1200:
                line = line[:1200] + "...<truncated>"
            print(f"codex_output_command line={line_number} text={line}")

print("[exit 0]")
