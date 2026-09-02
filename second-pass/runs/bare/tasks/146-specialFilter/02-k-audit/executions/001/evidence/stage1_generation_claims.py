#!/usr/bin/env python3
"""Read all candidate generation records and summarize their untrusted claims."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import re


CANDIDATE = Path("/candidate")
TRACE = next((CANDIDATE / "codex-trace").glob("**/*.jsonl"))


def compact(text: str, limit: int = 700) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[:limit] + "…"


def main() -> int:
    for name in ("run-input.json", "metrics.json"):
        payload = json.loads((CANDIDATE / name).read_text(encoding="utf-8"))
        print(f"{name}={json.dumps(payload, sort_keys=True)}")
    for name in ("codex-last.txt",):
        text = (CANDIDATE / name).read_text(encoding="utf-8", errors="replace")
        print(f"{name}={compact(text, 1600)}")

    raw_log = (CANDIDATE / "codex-output.log").read_text(encoding="utf-8", errors="replace")
    print(f"codex-output.log bytes={len(raw_log.encode())} lines={len(raw_log.splitlines())}")
    for pattern in (
        "#Top",
        "WarnStuckClaimState",
        "kprove induction-spec.k",
        "kprove spec.k",
        "RESULT: KPROVE_PASSED",
    ):
        print(f"codex-output.log count {pattern!r}={raw_log.count(pattern)}")
    lines = raw_log.splitlines()
    selected = [
        index
        for index, line in enumerate(lines)
        if "kprove induction-spec.k" in line
        or "All six concrete claims" in line
        or "Together these partition every integer up to" in line
        or "RESULT: KPROVE_PASSED" in line
    ]
    print("codex-output.log selected claim lines:")
    for index in selected:
        print(f"  line={index + 1}: {compact(lines[index], 1000)}")

    outer_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    agent_messages = []
    proof_commands = []
    proof_outputs = []
    with TRACE.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            event = json.loads(line)
            outer_types[event.get("type")] += 1
            payload = event.get("payload", {})
            payload_types[payload.get("type")] += 1
            if payload.get("type") == "agent_message":
                agent_messages.append((line_number, payload.get("phase"), payload.get("message", "")))
            if payload.get("type") == "custom_tool_call":
                tool_input = payload.get("input", "")
                if "kprove" in tool_input or "kompile" in tool_input or "krun" in tool_input:
                    proof_commands.append((line_number, tool_input))
            if payload.get("type") == "custom_tool_call_output":
                output = json.dumps(payload.get("output", ""))
                if "#Top" in output or "WarnStuckClaimState" in output:
                    proof_outputs.append((line_number, output))
    print(f"trace={TRACE} bytes={TRACE.stat().st_size}")
    print(f"trace_outer_types={dict(outer_types)}")
    print(f"trace_payload_types={dict(payload_types)}")
    print("trace_agent_messages:")
    for line_number, phase, message in agent_messages:
        print(f"  jsonl_line={line_number} phase={phase}: {compact(message, 1000)}")
    print("trace_proof_commands:")
    for line_number, command in proof_commands:
        print(f"  jsonl_line={line_number}: {compact(command, 1000)}")
    print("trace_proof_outputs_with_top_or_stuck:")
    for line_number, output in proof_outputs:
        markers = []
        if "#Top" in output:
            markers.append("#Top")
        if "WarnStuckClaimState" in output:
            markers.append("WarnStuckClaimState")
        print(f"  jsonl_line={line_number} markers={','.join(markers)}: {compact(output, 1000)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
