#!/usr/bin/env python3
"""Consume untrusted generation records and emit a bounded claims digest."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path


CANDIDATE = Path("/candidate")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    for name in ("run-input.json", "metrics.json", "codex-last.txt", "codex-output.log"):
        path = CANDIDATE / name
        print(f"FILE={name} SIZE={path.stat().st_size} SHA256={sha256(path)}")

    print("RUN_INPUT_JSON=" + json.dumps(json.loads((CANDIDATE / "run-input.json").read_text())))
    print("METRICS_JSON=" + json.dumps(json.loads((CANDIDATE / "metrics.json").read_text())))
    print("CODEX_LAST_BEGIN")
    print((CANDIDATE / "codex-last.txt").read_text(encoding="utf-8"), end="")
    print("CODEX_LAST_END")

    output_path = CANDIDATE / "codex-output.log"
    output_lines = output_path.read_text(encoding="utf-8", errors="replace").splitlines()
    markers = (
        "#Top",
        "VALIDATED",
        "KPROVE_PASSED",
        "EXPECTED_FAILURE",
        "MISMATCHES=0",
        "FINAL_OK=1",
    )
    print(f"CODEX_OUTPUT_LINES={len(output_lines)}")
    for marker in markers:
        print(f"CODEX_OUTPUT_MARKER {marker!r} COUNT={sum(marker in line for line in output_lines)}")
    print("CODEX_OUTPUT_TAIL_BEGIN")
    for line in output_lines[-40:]:
        print(line)
    print("CODEX_OUTPUT_TAIL_END")

    trace_paths = sorted((CANDIDATE / "codex-trace").rglob("*.jsonl"))
    for trace_path in trace_paths:
        top_types: collections.Counter[str] = collections.Counter()
        payload_types: collections.Counter[str] = collections.Counter()
        assistant_texts: list[str] = []
        parse_failures = 0
        line_count = 0
        with trace_path.open(encoding="utf-8", errors="replace") as stream:
            for line in stream:
                line_count += 1
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    parse_failures += 1
                    continue
                top_types[str(event.get("type"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_types[str(payload.get("type"))] += 1
                    if payload.get("type") == "message" and payload.get("role") == "assistant":
                        for content in payload.get("content", []):
                            if isinstance(content, dict) and isinstance(content.get("text"), str):
                                assistant_texts.append(content["text"])
        print(
            f"TRACE={trace_path.relative_to(CANDIDATE)} SIZE={trace_path.stat().st_size} "
            f"SHA256={sha256(trace_path)} LINES={line_count} PARSE_FAILURES={parse_failures}"
        )
        print("TRACE_TOP_TYPES=" + json.dumps(dict(sorted(top_types.items()))))
        print("TRACE_PAYLOAD_TYPES=" + json.dumps(dict(sorted(payload_types.items()))))
        print(f"TRACE_ASSISTANT_TEXT_ITEMS={len(assistant_texts)}")
        if assistant_texts:
            print("TRACE_LAST_ASSISTANT_TEXT_BEGIN")
            print(assistant_texts[-1])
            print("TRACE_LAST_ASSISTANT_TEXT_END")


if __name__ == "__main__":
    main()
