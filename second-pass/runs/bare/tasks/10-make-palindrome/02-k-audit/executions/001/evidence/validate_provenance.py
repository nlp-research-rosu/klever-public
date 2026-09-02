#!/usr/bin/env python3
"""Structural validation only; candidate provenance contents remain untrusted."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def main() -> int:
    candidate = Path("/candidate")
    for name in ("run-input.json", "metrics.json"):
        value = json.loads((candidate / name).read_text(encoding="utf-8"))
        print(f"{name}: valid_json type={type(value).__name__}")
        print(json.dumps(value, sort_keys=True))

    traces = sorted((candidate / "codex-trace").rglob("*.jsonl"))
    print(f"trace_file_count={len(traces)}")
    for trace in traces:
        counts: Counter[str] = Counter()
        line_count = 0
        with trace.open(encoding="utf-8") as source:
            for line_count, line in enumerate(source, 1):
                event = json.loads(line)
                counts[str(event.get("type"))] += 1
        print(
            f"trace={trace} lines={line_count} "
            f"event_types={json.dumps(dict(sorted(counts.items())))}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
