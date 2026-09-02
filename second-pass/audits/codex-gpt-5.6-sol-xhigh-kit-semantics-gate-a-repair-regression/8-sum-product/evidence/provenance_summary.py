#!/usr/bin/env python3
"""Bounded extraction of the untrusted generation/provenance claims."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


candidate = Path("/candidate")
for name in ("run-input.json", "metrics.json"):
    value = json.loads((candidate / name).read_text(encoding="utf-8"))
    print(f"## {name}")
    print(json.dumps(value, indent=2, sort_keys=True))

for name in ("codex-last.txt", "codex-output.log"):
    path = candidate / name
    data = path.read_bytes()
    print(f"## {name}")
    print(
        json.dumps(
            {
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "first_200_utf8": data[:200].decode("utf-8", errors="replace"),
                "last_200_utf8": data[-200:].decode("utf-8", errors="replace"),
            },
            indent=2,
            sort_keys=True,
        )
    )

traces = sorted((candidate / "codex-trace").rglob("*.jsonl"))
print("## structured trace")
print(f"files={len(traces)}")
for path in traces:
    counts: Counter[str] = Counter()
    invalid = 0
    lines = 0
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            lines += 1
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                invalid += 1
            else:
                counts[str(event.get("type", "<none>"))] += 1
    print(
        json.dumps(
            {
                "path": str(path),
                "bytes": path.stat().st_size,
                "lines": lines,
                "invalid_json_lines": invalid,
                "event_types": dict(sorted(counts.items())),
            },
            indent=2,
            sort_keys=True,
        )
    )
