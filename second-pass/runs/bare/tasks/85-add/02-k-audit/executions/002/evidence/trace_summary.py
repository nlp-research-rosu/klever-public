#!/usr/bin/env python3
"""Parse every structured trace record and summarize generation actions."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


ROOT = Path("/generation-evidence/codex-trace")


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)


def main() -> int:
    files = sorted(ROOT.rglob("*.jsonl"))
    print(f"TRACE_FILES={len(files)}")
    total = 0
    bad = 0
    top_types: Counter[str] = Counter()
    action_lines = []
    result_lines = []

    for path in files:
        print(f"TRACE_FILE={path}")
        with path.open() as stream:
            for line_number, line in enumerate(stream, 1):
                total += 1
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError as err:
                    bad += 1
                    print(f"INVALID_JSON {path}:{line_number}: {err}")
                    continue
                top_types[str(obj.get("type", "<missing>"))] += 1
                flat = "\n".join(strings(obj))
                if any(
                    needle in flat
                    for needle in (
                        "kompile ",
                        "kprove ",
                        "krun ",
                        "py2mpy.py",
                        "apply_patch",
                    )
                ):
                    action_lines.append((path.name, line_number, flat))
                if any(
                    needle in flat
                    for needle in (
                        "KPROVE_PASSED",
                        "#Top",
                        "WarnStuckClaimState",
                        "Error",
                    )
                ):
                    result_lines.append((path.name, line_number, flat))

    print(f"TRACE_RECORDS={total}")
    print(f"INVALID_JSON_RECORDS={bad}")
    print("TOP_LEVEL_TYPES=" + json.dumps(top_types, sort_keys=True))
    print(f"ACTION_RECORDS={len(action_lines)}")
    for name, line_number, flat in action_lines:
        bounded = flat.replace("\n", " ")[:1200]
        print(f"ACTION {name}:{line_number}: {bounded}")
    print(f"RESULT_RECORDS={len(result_lines)}")
    for name, line_number, flat in result_lines:
        bounded = flat.replace("\n", " ")[:1200]
        print(f"RESULT {name}:{line_number}: {bounded}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
