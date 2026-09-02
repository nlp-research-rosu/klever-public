#!/usr/bin/env python3
"""Emit a line-addressed inventory of local K declarations and program constructors."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


def selected_lines(path: Path) -> None:
    print(f"FILE {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    for number, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if (
            stripped.startswith(("requires ", "module ", "imports ", "configuration", "syntax ", "rule ", "claim "))
            or "[function" in line
            or "[total" in line
            or "[functional" in line
            or "[simplification" in line
            or "[priority" in line
        ):
            print(f"{number:4d}: {line}")
    print(f"rule_count={sum(line.lstrip().startswith('rule ') for line in lines)}")
    print(f"claim_count={sum(line.lstrip().startswith('claim ') for line in lines)}")
    print()


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: static_inventory.py SEMANTIC VERIFICATION SOLUTION_MPY", file=sys.stderr)
        return 64
    semantic, verification, solution = map(Path, sys.argv[1:])
    selected_lines(semantic)
    selected_lines(verification)

    solution_text = solution.read_text(encoding="utf-8")
    constructors = Counter(re.findall(r"\b([A-Z][A-Za-z0-9]*)\s*\(", solution_text))
    print(f"PROGRAM {solution}")
    print("constructors=" + ", ".join(f"{name}:{constructors[name]}" for name in sorted(constructors)))
    print("runtime operations=module entry, sequencing, docstring discard, assignment, empty list,")
    print("for iteration, name lookup/update, if/elif, == and > comparison, string literals,")
    print("list.append mutation, and final return")

    combined = semantic.read_text(encoding="utf-8") + verification.read_text(encoding="utf-8")
    for attribute in ("functional", "simplification", "priority", "concrete", "opaque"):
        print(f"{attribute}_occurrences={len(re.findall(attribute, combined, flags=re.IGNORECASE))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
