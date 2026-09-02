#!/usr/bin/env python3
"""Bounded content inspection of the untrusted generation records."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/generation-evidence")


def compact(value: object, limit: int = 1200) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return text if len(text) <= limit else text[:limit] + "...<bounded>"


def main() -> None:
    for name in [
        "invocation.json",
        "metrics.json",
        "usage.json",
        "legacy-metrics.json",
        "legacy-run-input.json",
    ]:
        path = ROOT / name
        if path.exists():
            obj = json.loads(path.read_text())
            print(f"JSON_RECORD {name}: {compact(obj, 4000)}")

    for name in ["prompt.txt", "codex-last.txt"]:
        text = (ROOT / name).read_text()
        print(f"TEXT_RECORD {name} bytes={len(text.encode())} lines={len(text.splitlines())}")
        print(text)

    output_lines = (ROOT / "codex-output.log").read_text().splitlines()
    interesting = re.compile(
        r"(kompile|kprove|krun|#Top|KPROVE|RESULT:|exit(?:ed| code| status)|"
        r"verification\\.k|spec\\.k|solution\\.mpy)",
        re.IGNORECASE,
    )
    matches = [(index, line) for index, line in enumerate(output_lines, 1) if interesting.search(line)]
    print(
        f"CODEX_OUTPUT lines={len(output_lines)} interesting_lines={len(matches)} "
        "(bounded to the first/last 120 matching lines)"
    )
    selected = matches[:60] + (matches[-60:] if len(matches) > 60 else [])
    for line_number, line in selected:
        print(f"CODEX_OUTPUT_MATCH {line_number}: {line[:2000]}")

    trace_paths = sorted((ROOT / "codex-trace").rglob("*.jsonl"))
    top_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    function_calls: list[tuple[str, str]] = []
    messages: list[str] = []
    for path in trace_paths:
        with path.open() as stream:
            for line in stream:
                obj = json.loads(line)
                top_types[str(obj.get("type"))] += 1
                payload = obj.get("payload")
                if isinstance(payload, dict):
                    payload_type = str(payload.get("type", "<missing>"))
                    payload_types[payload_type] += 1
                    if obj.get("type") == "response_item" and payload_type in {
                        "function_call",
                        "custom_tool_call",
                    }:
                        function_calls.append(
                            (
                                str(payload.get("name", payload.get("call_id", "<unnamed>"))),
                                compact(payload.get("arguments", payload.get("input")), 2500),
                            )
                        )
                    if payload_type in {"agent_message", "message"}:
                        text = payload.get("message", payload.get("content", ""))
                        messages.append(compact(text, 2500))
    print(f"TRACE_TOP_TYPES {dict(top_types)}")
    print(f"TRACE_PAYLOAD_TYPES {dict(payload_types)}")
    print(f"TRACE_FUNCTION_CALL_COUNT {len(function_calls)}")
    for index, (name, arguments) in enumerate(function_calls, 1):
        print(f"TRACE_CALL {index} name={name} args={arguments}")
    print(f"TRACE_MESSAGE_COUNT {len(messages)}")
    for index, message in enumerate(messages, 1):
        print(f"TRACE_MESSAGE {index}: {message}")
    print("GENERATION_RECORD_INSPECTION_OK")


if __name__ == "__main__":
    main()
