#!/usr/bin/env python3
"""Print a bounded metadata-only view of the untrusted generation trace."""

from __future__ import annotations

import json
import sys
from collections import Counter, deque
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        return 2
    counts: Counter[tuple[str, str]] = Counter()
    tail: deque[tuple[str, str, str, str, str]] = deque(maxlen=80)
    for raw in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
        item = json.loads(raw)
        payload = item.get("payload", {})
        row = (
            str(item.get("timestamp", "")),
            str(item.get("type", "")),
            str(payload.get("type", "")),
            str(payload.get("name", "")),
            str(payload.get("phase", "")),
        )
        counts[(row[1], row[2])] += 1
        tail.append(row)
    for key, count in sorted(counts.items()):
        print(f"COUNT outer={key[0]} payload={key[1]} count={count}")
    for row in tail:
        print("\t".join(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
