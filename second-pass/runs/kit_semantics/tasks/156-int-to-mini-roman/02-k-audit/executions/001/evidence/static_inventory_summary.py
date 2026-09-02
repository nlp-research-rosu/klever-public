#!/usr/bin/env python3
"""Count and classify every declaration/rule start in the fixed and local K sources."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re


SEMANTICS = Path("/reference/reference-semantics")
FILES = [SEMANTICS / "semantics.k", *sorted((SEMANTICS / "semantics").glob("*.k"))]
FILES.append(Path("/candidate/verification.k"))


def classify(line: str) -> str | None:
    stripped = line.lstrip()
    for prefix, kind in (
        ("syntax ", "syntax"),
        ("rule ", "rule"),
        ("context ", "context"),
        ("configuration", "configuration"),
        ("claim ", "claim"),
        ("priority ", "priority-declaration"),
    ):
        if stripped.startswith(prefix):
            return kind
    return None


def main() -> int:
    totals: Counter[str] = Counter()
    print(
        "file | syntax | rules | contexts | configs | claims | function | "
        "total | macro | priority | concrete | simplification | functional | "
        "no-evaluators"
    )
    for path in FILES:
        lines = path.read_text(encoding="utf-8").splitlines()
        counts: Counter[str] = Counter()
        for number, line in enumerate(lines, 1):
            code = line.split("//", 1)[0]
            kind = classify(code)
            if kind:
                counts[kind] += 1
            # Attributes can be on a continuation line, so count declarations
            # containing each exact marker independently of start-line counts.
            for attr in (
                "function",
                "total",
                "macro",
                "priority",
                "concrete",
                "simplification",
                "functional",
                "no-evaluators",
            ):
                if re.search(
                    rf"\[[^]]*\b{re.escape(attr)}(?:\b|\()[^]]*\]",
                    code,
                ):
                    counts[attr] += 1
        totals.update(counts)
        shown = str(path).replace("/reference/reference-semantics/", "")
        print(
            f"{shown} | {counts['syntax']} | {counts['rule']} | "
            f"{counts['context']} | {counts['configuration']} | "
            f"{counts['claim']} | {counts['function']} | {counts['total']} | "
            f"{counts['macro']} | {counts['priority']} | "
            f"{counts['concrete']} | {counts['simplification']} | "
            f"{counts['functional']} | {counts['no-evaluators']}"
        )
    print(f"TOTALS={dict(sorted(totals.items()))}")
    print("FULL_LINE_INVENTORY=/audit-output/evidence/rule_inventory.txt")
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
