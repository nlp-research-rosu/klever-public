#!/usr/bin/env python3
"""Ground witnesses for each semantic shape used by the submitted claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.longest


def fold(best: str | None, remaining: list[str]) -> str | None:
    for current in remaining:
        if best is None or len(current) > len(best):
            best = current
    return best


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: claim_witnesses.py CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 2
    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical_witness")
    solution = load_entry(Path(sys.argv[2]), "generated_solution_witness")

    witnesses = [
        ("loop-init-empty/call-empty", None, [], []),
        ("loop-init-cons", "a", ["bbb"], ["a", "bbb"]),
        ("loop-empty", "x", [], ["x"]),
        ("loop-longer", "yy", [], ["x", "yy"]),
        ("loop-retain-shorter", "xx", [], ["xx", "y"]),
        ("loop-retain-tie", "first", [], ["first", "later"]),
        ("call-cons-dispatch", "a", ["bbb", "cc"], ["a", "bbb", "cc"]),
    ]
    failures = 0
    for label, after_first, rest, whole_input in witnesses:
        formal_summary = fold(after_first, rest)
        canonical_result = canonical(list(whole_input))
        solution_result = solution(list(whole_input))
        print(
            f"{label}: input={whole_input!r} "
            f"formal_summary={formal_summary!r} "
            f"canonical={canonical_result!r} solution={solution_result!r}"
        )
        if label != "call-cons-dispatch" and not (
            formal_summary == canonical_result == solution_result
        ):
            failures += 1
    print(
        "NOTE call-cons-dispatch has no terminal-result postcondition; "
        "the displayed formal_summary is the omitted obligation."
    )
    print(f"witness_failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
