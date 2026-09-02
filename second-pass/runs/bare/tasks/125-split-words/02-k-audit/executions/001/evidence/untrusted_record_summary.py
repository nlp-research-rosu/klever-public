#!/usr/bin/env python3
"""Parse the complete untrusted generation records and emit a bounded summary."""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path
from typing import Any, Iterable


LOG = Path("/candidate/codex-output.log")
TRACE_ROOT = Path("/candidate/codex-trace")
SIGNAL_RE = re.compile(
    r"(?:^|\b)(?:kompile|krun|kprove)\b|#Top|WarnStuckClaimState|"
    r"KPROVE_PASSED|RESULT:|exit code|timed out",
    re.IGNORECASE,
)


def strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for nested in value.values():
            yield from strings(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from strings(nested)


def clip(value: str, limit: int = 320) -> str:
    flattened = " ".join(value.split())
    return flattened if len(flattened) <= limit else flattened[:limit] + "..."


def main() -> int:
    log_signals: list[tuple[int, str]] = []
    log_line_count = 0
    with LOG.open(encoding="utf-8", errors="replace") as handle:
        for line_number, line in enumerate(handle, 1):
            log_line_count = line_number
            if SIGNAL_RE.search(line):
                log_signals.append((line_number, clip(line)))

    trace_files = sorted(TRACE_ROOT.rglob("*.jsonl"))
    trace_line_count = 0
    event_types: collections.Counter[str] = collections.Counter()
    trace_signals: list[tuple[str, int, str]] = []
    for path in trace_files:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                trace_line_count += 1
                record = json.loads(line)
                event_types[str(record.get("type", "<missing>"))] += 1
                for value in strings(record):
                    if SIGNAL_RE.search(value):
                        trace_signals.append(
                            (str(path), line_number, clip(value))
                        )

    print("UNTRUSTED_LOG:", LOG)
    print("LOG_LINES_PARSED:", log_line_count)
    print("LOG_SIGNAL_COUNT:", len(log_signals))
    print("TRACE_FILES:", len(trace_files))
    print("TRACE_JSON_LINES_PARSED:", trace_line_count)
    print("TRACE_EVENT_TYPES:", dict(sorted(event_types.items())))
    print("TRACE_SIGNAL_COUNT:", len(trace_signals))
    print("LAST_80_LOG_SIGNALS:")
    for line_number, value in log_signals[-80:]:
        print(f"{line_number}: {value}")
    print("LAST_40_TRACE_SIGNALS:")
    for path, line_number, value in trace_signals[-40:]:
        print(f"{path}:{line_number}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
