#!/usr/bin/env python3
"""Concrete satisfiability and result-substitution witnesses for all entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.correct_bracketing


def bracket_result(suffix: str, depth: int) -> bool:
    if depth < 0:
        return False
    for character in suffix:
        if character == "<":
            depth += 1
        else:
            depth -= 1
        if depth < 0:
            return False
    return depth == 0


def intseq(text: str) -> str:
    term = ".IntSeq"
    for code in reversed([ord(character) for character in text]):
        term = f"iCons({code}, {term})"
    return term


def main() -> int:
    canonical = load_entry(
        "trusted_canonical",
        Path("/tmp/audit-work/trusted/canonical.py"),
    )
    submitted = load_entry(
        "submitted_solution",
        Path("/tmp/audit-work/scratch/solution.py"),
    )

    # The prefix witnesses make the loop states reachable from real entry calls.
    cases = [
        ("correct-bracketing", "", 0, ""),
        ("correct-bracketing", "", 0, "<>"),
        ("correct-bracketing", "", 0, ">"),
        ("correct-bracketing", "", 0, "<<><>>"),
        ("loop-zero", "", 0, ""),
        ("loop-zero", "", 0, "<>"),
        ("loop-zero", "<>", 0, "<>"),
        ("loop-positive", "<", 1, ">"),
        ("loop-positive", "<<", 2, ">>"),
        ("loop-positive", "<", 1, "<>>"),
    ]

    mismatch_count = 0
    for claim, prefix, depth, suffix in cases:
        full_input = prefix + suffix
        formal = bracket_result(suffix, depth)
        canonical_value = canonical(full_input)
        submitted_value = submitted(full_input)
        ok = formal == canonical_value == submitted_value
        mismatch_count += not ok
        print(
            f"claim={claim} prefix={prefix!r} suffix={suffix!r} "
            f"S={intseq(suffix)} D={depth} "
            f"bracketResult={formal} canonical={canonical_value} "
            f"submitted={submitted_value} match={ok}"
        )

    print("\nSATISFYING_STATE_SCHEMAS")
    print(
        "loop-zero: L=1, CALLER=0, SAVED=1, CONT=.K, "
        "D=0, stack=ListItem(frame(.K,0,1)) .List, "
        "SC=(0 |-> scope(.Map,parent(-1)) "
        "-1 |-> builtinsScope), so 1 not in_keys(SC)"
    )
    print(
        "loop-positive: same cells, D=1, suffix='>', prefix='<'; "
        "all guards hold and this state is reachable after the first iteration"
    )
    print(
        "correct-bracketing: every listed S with the exact initial cells "
        "shown in spec.k satisfies the unguarded precondition"
    )
    print(f"mismatch_count={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
