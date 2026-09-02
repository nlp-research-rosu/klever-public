#!/usr/bin/env python3
"""Read and summarize the complete untrusted generation record."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path("/generation-evidence")
RECORDS = [
    Path("/run.json"),
    Path("/task.json"),
    Path("/generation-result.json"),
    ROOT / "invocation.json",
    ROOT / "metrics.json",
    ROOT / "usage.json",
    ROOT / "codex-last.txt",
    ROOT / "codex-output.log",
    ROOT / "prompt.txt",
    ROOT / "legacy-run-input.json",
    ROOT / "legacy-metrics.json",
]
KEYWORDS = (
    "kompile",
    "kprove",
    "krun",
    "#Top",
    "WarnStuck",
    "oracle",
    "RESULT:",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)


def main() -> int:
    for path in RECORDS:
        data = path.read_bytes()
        print(f"record {path}: bytes={len(data)} sha256={sha256(path)}")
        if path.suffix == ".json":
            json.loads(data)

    output_text = (ROOT / "codex-output.log").read_text(
        encoding="utf-8", errors="strict"
    )
    print(f"codex_output_lines={len(output_text.splitlines())}")
    for keyword in KEYWORDS:
        print(f"codex_output_occurrences {keyword!r}={output_text.count(keyword)}")
    print("codex_output_final_nonempty_lines:")
    for line in [line for line in output_text.splitlines() if line.strip()][-12:]:
        print("  " + line[:800])

    trace_types: Counter[str] = Counter()
    payload_types: Counter[str] = Counter()
    commands: list[str] = []
    assistant_messages: list[str] = []
    keyword_leaf_count: Counter[str] = Counter()
    trace_lines = 0
    for path in sorted((ROOT / "codex-trace").rglob("*.jsonl")):
        with path.open(encoding="utf-8") as stream:
            for raw_line in stream:
                trace_lines += 1
                event = json.loads(raw_line)
                trace_types[str(event.get("type"))] += 1
                payload = event.get("payload", {})
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type", "<missing>"))] += 1
                    if payload.get("type") in {"function_call", "custom_tool_call"}:
                        name = payload.get("name", "<unnamed>")
                        arguments = payload.get("arguments") or payload.get("input")
                        commands.append(f"{name}: {str(arguments)[:1200]}")
                    if payload.get("type") == "message" and payload.get("role") == "assistant":
                        for leaf in strings(payload.get("content", [])):
                            assistant_messages.append(leaf)
                for leaf in strings(event):
                    for keyword in KEYWORDS:
                        if keyword in leaf:
                            keyword_leaf_count[keyword] += 1

    print(f"trace_lines={trace_lines}")
    print("trace_types=" + json.dumps(dict(sorted(trace_types.items()))))
    print("trace_payload_types=" + json.dumps(dict(sorted(payload_types.items()))))
    print("trace_keyword_leaf_count=" + json.dumps(dict(sorted(keyword_leaf_count.items()))))
    print(f"trace_tool_call_count={len(commands)}")
    for index, command in enumerate(commands, 1):
        print(f"tool_call_{index:03d}: {command}")
    print(f"assistant_message_count={len(assistant_messages)}")
    print("assistant_final_message:")
    print(assistant_messages[-1] if assistant_messages else "<none>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
