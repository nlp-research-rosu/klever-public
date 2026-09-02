#!/usr/bin/env python3
"""Print the frozen source slices used for the semantic judgment."""

from __future__ import annotations

from pathlib import Path


def show(path: str, start: int, end: int) -> None:
    source = Path(path)
    print(f"### {source}:{start}-{end}")
    lines = source.read_text().splitlines()
    for number in range(start, min(end, len(lines)) + 1):
        print(f"{number:5d}\t{lines[number - 1]}")


def main() -> None:
    show("/reference/k-proof/verification.k", 1, 102)
    show("/reference/k-proof/shape-connection.k", 1, 5)
    show("/reference/k-proof/shape-connection-spec.k", 1, 10)
    show("/reference/k-proof/prove.sh", 34, 48)
    show("/reference/k-proof/reference-semantics/semantics/controls.k", 62, 74)
    show("/reference/k-proof/reference-semantics/semantics/list.k", 8, 20)
    show("/reference/k-proof/reference-semantics/semantics/list.k", 52, 66)
    show("/reference/k-proof/reference-semantics/semantics/tuple.k", 9, 21)
    show("/reference/k-proof/spec.k", 6, 125)
    show("/reference/k-proof/solution.py", 1, 25)
    show("/reference/klean-generation/generated/Klean87GetRow/Lemmas.lean", 1, 9)


if __name__ == "__main__":
    main()
