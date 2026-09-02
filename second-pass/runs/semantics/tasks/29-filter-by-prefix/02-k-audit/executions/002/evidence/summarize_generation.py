#!/usr/bin/env python3
"""Read every structured-trace record and summarize the untrusted generation log."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


TRACE = Path(
    "/generation-evidence/codex-trace/2026/07/22/"
    "rollout-2026-07-22T22-37-25-019f8d0c-aa5a-7c71-bb49-106b51fa9dd0.jsonl"
)
OUTPUT = Path("/generation-evidence/codex-output.log")


def compact(value: object, limit: int = 1200) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\r", "\\r")
    if len(text) <= limit:
        return text
    digest = hashlib.sha256(text.encode()).hexdigest()
    return f"{text[:600]} ... <sha256={digest} bytes={len(text)}> ... {text[-300:]}"


def main() -> None:
    items = []
    with TRACE.open() as stream:
        for number, line in enumerate(stream, 1):
            items.append((number, json.loads(line)))
    print(f"TRACE: parsed all {len(items)} JSONL records")
    counts = Counter(item["type"] for _, item in items)
    print(f"TRACE outer counts: {dict(counts)}")
    for number, item in items:
        payload = item.get("payload", {})
        outer = item.get("type")
        subtype = payload.get("type")
        if outer == "response_item" and subtype in {
            "function_call",
            "custom_tool_call",
        }:
            argument = payload.get("arguments", payload.get("input", ""))
            print(
                f"TRACE line {number}: CALL {payload.get('name')} "
                f"{compact(argument, 2200)}"
            )
        elif outer == "response_item" and subtype in {
            "function_call_output",
            "custom_tool_call_output",
        }:
            output = payload.get("output", "")
            print(
                f"TRACE line {number}: OUTPUT call_id={payload.get('call_id')} "
                f"{compact(output, 1000)}"
            )
        elif outer == "response_item" and subtype == "message":
            role = payload.get("role")
            if role == "assistant":
                print(
                    f"TRACE line {number}: ASSISTANT "
                    f"{compact(payload.get('content', ''), 1800)}"
                )
        elif outer == "event_msg" and subtype in {
            "agent_message",
            "task_complete",
            "patch_apply_end",
        }:
            print(f"TRACE line {number}: EVENT {subtype} {compact(payload, 1000)}")

    raw = OUTPUT.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    print(
        f"CODEX-OUTPUT: read all bytes={len(raw)} lines={text.count(chr(10)) + 1} "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )
    markers = Counter()
    patterns = {
        "#Top": r"#Top",
        "WarnStuckClaimState": r"WarnStuckClaimState",
        "Error": r"\[Error\]|\bERROR\b",
        "timed out": r"timed out|timeout",
        "KPROVE_PASSED": r"KPROVE_PASSED",
        "PARTIAL": r"\bPARTIAL\b",
        "BLOCKED": r"\bBLOCKED\b",
    }
    for name, pattern in patterns.items():
        markers[name] = len(re.findall(pattern, text, flags=re.IGNORECASE))
    print(f"CODEX-OUTPUT markers={dict(markers)}")
    selected = []
    key_pattern = re.compile(
        r"(kompile|kprove|krun|#Top|WarnStuckClaimState|\[Error\]|"
        r"RESULT:|exit code|Process exited|Script running)",
        re.IGNORECASE,
    )
    for number, line in enumerate(text.splitlines(), 1):
        if key_pattern.search(line):
            selected.append((number, line))
    print(f"CODEX-OUTPUT selected key lines={len(selected)}")
    for number, line in selected:
        print(f"CODEX-OUTPUT line {number}: {compact(line, 1000)}")


if __name__ == "__main__":
    main()
