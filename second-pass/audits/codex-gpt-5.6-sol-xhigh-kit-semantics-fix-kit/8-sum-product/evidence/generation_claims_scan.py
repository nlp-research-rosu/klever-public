#!/usr/bin/env python3
"""Bounded full-file scan of untrusted generation prose and structured trace."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


FILES = (
    Path("/candidate/run-input.json"),
    Path("/candidate/metrics.json"),
    Path("/candidate/codex-last.txt"),
    Path("/candidate/codex-output.log"),
)
PATTERN = re.compile(
    r"#Top|WarnStuckClaimState|KPROVE_PASSED|VALIDATED|mismatch|EXPECTED FAILURE|"
    r"exit(?:ed|_status|_code)?\s*[=: ]\s*[0-9]+|\b(?:error|failed|timeout)\b",
    re.IGNORECASE,
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    for path in FILES:
        data = path.read_bytes()
        text = data.decode("utf-8", errors="replace")
        lines = text.splitlines()
        hits = [(number, line) for number, line in enumerate(lines, 1) if PATTERN.search(line)]
        print(
            f"FILE {path} bytes={len(data)} lines={len(lines)} sha256={digest(data)} "
            f"claim_hits={len(hits)}"
        )
        selected = hits if len(hits) <= 80 else hits[:40] + hits[-40:]
        for number, line in selected:
            print(f"  {number}: {line[:500]}")
        if len(hits) > len(selected):
            print(f"  OMITTED_MIDDLE_HITS={len(hits) - len(selected)}")

    trace_paths = sorted(Path("/candidate/codex-trace").rglob("*.jsonl"))
    for path in trace_paths:
        data = path.read_bytes()
        lines = data.decode("utf-8", errors="replace").splitlines()
        outer_types: Counter[str] = Counter()
        payload_types: Counter[str] = Counter()
        parse_failures = 0
        assistant_messages: list[str] = []
        command_claims: list[str] = []
        for line in lines:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                parse_failures += 1
                continue
            outer_types[str(record.get("type"))] += 1
            payload = record.get("payload")
            if isinstance(payload, dict):
                payload_types[str(payload.get("type"))] += 1
                if payload.get("type") == "message" and payload.get("role") == "assistant":
                    for content in payload.get("content", []):
                        if isinstance(content, dict) and isinstance(content.get("text"), str):
                            assistant_messages.append(content["text"])
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    command_claims.append(json.dumps(payload, sort_keys=True)[:1000])
        print(
            f"TRACE {path} bytes={len(data)} lines={len(lines)} sha256={digest(data)} "
            f"parse_failures={parse_failures}"
        )
        print(f"  outer_types={dict(sorted(outer_types.items()))}")
        print(f"  payload_types={dict(sorted(payload_types.items()))}")
        print(f"  assistant_message_count={len(assistant_messages)} command_record_count={len(command_claims)}")
        for message in assistant_messages[-5:]:
            print(f"  assistant_tail={message[:1000]}")
        for command in command_claims[-10:]:
            print(f"  command_tail={command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
