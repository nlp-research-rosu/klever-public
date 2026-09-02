#!/usr/bin/env python3
"""Ground witnesses for each claim family and its result expression."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/reconstruction")


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bracket_seq_spec(text: str, depth: int) -> bool:
    """Mathematical reading of candidate bracketSeqSpec equations."""
    for character in text:
        if character == "<":
            depth += 1
        elif character == ">":
            depth -= 1
            if depth < 0:
                return False
        else:
            raise ValueError("outside BracketSeq alphabet")
    return depth == 0


def main() -> int:
    canonical = load(
        "trusted_canonical", ROOT / "reference/canonical.py"
    ).correct_bracketing
    candidate = load(
        "generated_solution", ROOT / "candidate-src/solution.py"
    ).correct_bracketing
    witnesses = [
        ("loop-zero", "", 0),
        ("loop-positive", ">", 1),
        ("universal-empty", "", 0),
        ("universal-open", "<", 0),
        ("universal-pair", "<>", 0),
        ("universal-negative-prefix", "><", 0),
        ("example-open", "<", 0),
        ("example-pair", "<>", 0),
        ("example-nested", "<<><>>", 0),
        ("example-negative-prefix", "><<>", 0),
    ]
    mismatches = 0
    print(
        "state schema: functions=.Map; result=noResult(); universal/examples "
        "env=emptyStore(); loop env=bind('depth',IVal(D),emptyStore())"
    )
    for name, text, depth in witnesses:
        claimed = bracket_seq_spec(text, depth)
        if depth == 0:
            oracle = canonical(text)
            subject = candidate(text)
            equal = claimed == oracle == subject
        else:
            # This loop-helper witness describes execution from an internal
            # positive-depth state, so no Python entry call has that state.
            oracle = subject = None
            equal = True
        mismatches += int(not equal)
        print(
            f"claim={name} text={text!r} D={depth} claimed={claimed!r} "
            f"canonical_entry={oracle!r} candidate_entry={subject!r} "
            f"entry_values_equal={equal}"
        )
    print(f"witnesses={len(witnesses)} mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
