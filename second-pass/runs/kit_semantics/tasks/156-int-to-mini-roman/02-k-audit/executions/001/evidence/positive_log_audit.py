#!/usr/bin/env python3
"""Check fresh positive logs for exact claim coverage and success signals."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


def main() -> int:
    seen: Counter[int] = Counter()
    for batch in range(1, 11):
        path = Path(f"/audit-output/evidence/kprove_positive_{batch:02d}.log")
        text = path.read_text(encoding="utf-8")
        labels = [
            int(value)
            for value in re.findall(r"SPEC\.roman-(\d{4})", text.splitlines()[0])
        ]
        top_count = sum(line == "#Top" for line in text.splitlines())
        exit_statuses = re.findall(r"^EXIT_STATUS: (\d+)$", text, re.MULTILINE)
        expected = list(range((batch - 1) * 100 + 1, batch * 100 + 1))
        print(
            f"batch={batch:02d} label_count={len(labels)} "
            f"range={labels[0] if labels else None}.."
            f"{labels[-1] if labels else None} top_count={top_count} "
            f"exit_statuses={exit_statuses}"
        )
        if labels != expected or top_count != 1 or exit_statuses != ["0"]:
            print("RESULT=FAIL")
            return 1
        seen.update(labels)

    if set(seen) != set(range(1, 1001)) or any(
        count != 1 for count in seen.values()
    ):
        print("RESULT=FAIL coverage or uniqueness")
        return 1
    print("coverage=every claim 1..1000 exactly once")
    print("success_signal=one #Top and exit 0 per batch")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
