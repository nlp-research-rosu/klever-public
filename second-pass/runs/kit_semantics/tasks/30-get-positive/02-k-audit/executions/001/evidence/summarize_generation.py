#!/usr/bin/env python3
"""Read and summarize every structured generation event and the text output."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


TRACE_ROOT = Path("/generation-evidence/codex-trace")
OUTPUT = Path("/generation-evidence/codex-output.log")


def walk(value: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, path + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, path + (str(index),))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    type_counts: collections.Counter[str] = collections.Counter()
    payload_type_counts: collections.Counter[str] = collections.Counter()
    interesting: list[tuple[str, int, str, str]] = []
    parse_failures: list[str] = []
    total_lines = 0

    for trace in sorted(TRACE_ROOT.rglob("*")):
        if not trace.is_file():
            continue
        print(f"TRACE {trace.relative_to(TRACE_ROOT)} sha256={sha256(trace)}")
        with trace.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                total_lines += 1
                try:
                    event = json.loads(line)
                except Exception as error:
                    parse_failures.append(f"{trace}:{line_number}:{error}")
                    continue
                type_counts[str(event.get("type", "<none>"))] += 1
                payload = event.get("payload")
                if isinstance(payload, dict):
                    payload_type_counts[str(payload.get("type", "<none>"))] += 1
                for path, value in walk(event):
                    if not isinstance(value, str):
                        continue
                    key = path[-1] if path else ""
                    if key in {
                        "arguments", "command", "cmd", "input", "message",
                        "output", "text", "tool_name",
                    } and value.strip():
                        clipped = value.replace("\x1b", "<ESC>")
                        if len(clipped) > 4000:
                            clipped = clipped[:4000] + f"...<clipped {len(value) - 4000} chars>"
                        interesting.append((
                            trace.relative_to(TRACE_ROOT).as_posix(),
                            line_number,
                            ".".join(path),
                            clipped,
                        ))

    output_bytes = OUTPUT.read_bytes()
    output_text = output_bytes.decode("utf-8", errors="replace")
    output_lines = output_text.splitlines()
    markers = [
        line for line in output_lines
        if any(token in line for token in (
            "#Top", "WarnStuckClaimState", "[Error]", "RESULT:",
            "kompile", "kprove", "krun", "python3", "apply_patch",
        ))
    ]
    print(f"TOTAL_TRACE_LINES={total_lines}")
    print(f"TRACE_PARSE_FAILURES={len(parse_failures)}")
    for failure in parse_failures:
        print(f"PARSE_FAILURE {failure}")
    print(f"EVENT_TYPES={dict(sorted(type_counts.items()))}")
    print(f"PAYLOAD_TYPES={dict(sorted(payload_type_counts.items()))}")
    print(f"INTERESTING_FIELD_COUNT={len(interesting)}")
    for rel, line_number, field, value in interesting:
        print(f"EVENT {rel}:{line_number} FIELD={field}")
        print(value)
    print(f"CODEX_OUTPUT_SHA256={sha256(OUTPUT)}")
    print(f"CODEX_OUTPUT_BYTES={len(output_bytes)}")
    print(f"CODEX_OUTPUT_LINES={len(output_lines)}")
    print(f"CODEX_OUTPUT_MARKERS={len(markers)}")
    for marker in markers:
        print(f"OUTPUT_MARKER {marker[:4000]}")
    return int(bool(parse_failures))


if __name__ == "__main__":
    raise SystemExit(main())
