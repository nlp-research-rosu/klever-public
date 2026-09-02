#!/usr/bin/env python3
"""Read all generation trace/output records and emit a bounded audit summary."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT_LOG = Path("/generation-evidence/codex-output.log")
KEYWORDS = re.compile(
    r"#Top|WarnStuck|\\[Error\\]|\\bkompile\\b|\\bkprove\\b|\\bkrun\\b|"
    r"RESULT:|verification\\.k|spec\\.k|musicCodes|musicIter|split bridge",
    re.IGNORECASE,
)


def bounded(value: object, limit: int = 2600) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True)
    text = text.replace("\x00", "<NUL>")
    if len(text) <= limit:
        return text
    half = limit // 2
    return text[:half] + f"\n...<TRUNCATED {len(text) - limit} CHARS>...\n" + text[-half:]


def main() -> int:
    counts: Counter[tuple[str, str]] = Counter()
    trace_lines = 0
    for path in sorted(TRACE_ROOT.rglob("*.jsonl")):
        print(f"TRACE_FILE {path} size={path.stat().st_size}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                trace_lines += 1
                event = json.loads(line)
                outer = event.get("type", "")
                payload = event.get("payload") or {}
                inner = payload.get("type", "")
                counts[(outer, inner)] += 1
                if outer == "response_item" and inner in {
                    "function_call",
                    "custom_tool_call",
                }:
                    print(
                        f"TRACE_CALL line={line_number} type={inner} "
                        f"name={payload.get('name')} call_id={payload.get('call_id')}"
                    )
                    print(bounded(payload.get("arguments", payload.get("input", ""))))
                elif outer == "response_item" and inner in {
                    "function_call_output",
                    "custom_tool_call_output",
                }:
                    print(
                        f"TRACE_OUTPUT line={line_number} type={inner} "
                        f"call_id={payload.get('call_id')}"
                    )
                    print(bounded(payload.get("output", "")))
                elif outer == "response_item" and inner == "message":
                    role = payload.get("role")
                    pieces = []
                    for item in payload.get("content") or []:
                        if isinstance(item, dict):
                            pieces.append(item.get("text", ""))
                    print(f"TRACE_MESSAGE line={line_number} role={role}")
                    print(bounded("\n".join(pieces), 5000))

    print(f"TRACE_LINES_READ={trace_lines}")
    for key, value in sorted(counts.items()):
        print(f"TRACE_COUNT outer={key[0]} inner={key[1]} count={value}")

    output_lines = 0
    output_matches = 0
    with OUTPUT_LOG.open(errors="replace") as stream:
        for line_number, line in enumerate(stream, 1):
            output_lines += 1
            if KEYWORDS.search(line):
                output_matches += 1
                print(f"OUTPUT_KEYWORD line={line_number}: {bounded(line.rstrip(), 1800)}")
    print(f"OUTPUT_LINES_READ={output_lines}")
    print(f"OUTPUT_KEYWORD_LINES={output_matches}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
