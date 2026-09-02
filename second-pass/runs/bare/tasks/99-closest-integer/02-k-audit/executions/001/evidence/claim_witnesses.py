#!/usr/bin/env python3
"""Ground satisfying witnesses for all eleven target claims."""

from __future__ import annotations

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
from typing import Callable


def load_function(name: str, path: Path) -> Callable[[str], int]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.closest_integer


CANONICAL = load_function(
    "witness_canonical",
    Path("/tmp/audit-work/99-closest-integer/trusted/canonical.py"),
)
CANDIDATE = load_function(
    "witness_candidate",
    Path("/tmp/audit-work/99-closest-integer/source/solution.py"),
)

# claim, substitution, numeric input string, claimed pyInt payload
WITNESSES = [
    ("audit-01", {"N": 3, "D": 2}, "1.5", 2),
    ("audit-02", {"I": 0}, "0.5", 1),
    ("audit-03", {"I": 0}, "-0.5", -1),
    ("audit-04", {"I": 0}, "0.25", 0),
    ("audit-05", {"I": 0}, "0.75", 1),
    ("audit-06", {"I": 0}, "-0.25", 0),
    ("audit-07", {"I": 0}, "-0.75", -1),
    ("audit-08", {}, "10", 10),
    ("audit-09", {}, "15.3", 15),
    ("audit-10", {}, "14.5", 15),
    ("audit-11", {}, "-14.5", -15),
]


def round_nearest_away(numerator: int, denominator: int) -> int:
    value = Fraction(numerator, denominator)
    shifted = value + Fraction(1, 2) if value >= 0 else value - Fraction(1, 2)
    return int(shifted)


def main() -> None:
    mismatch_count = 0
    for claim, substitution, value, claimed in WITNESSES:
        canonical = CANONICAL(value)
        candidate = CANDIDATE(value)
        record = {
            "claim": claim,
            "substitution": substitution,
            "input": value,
            "claimed": claimed,
            "canonical": canonical,
            "candidate": candidate,
            "all_equal": claimed == canonical == candidate,
        }
        if claim == "audit-01":
            record["independent_fraction_oracle"] = round_nearest_away(
                substitution["N"], substitution["D"]
            )
            record["all_equal"] = (
                record["all_equal"]
                and record["independent_fraction_oracle"] == claimed
            )
        mismatch_count += not record["all_equal"]
        print(json.dumps(record, sort_keys=True))
    print(
        "SUMMARY "
        + json.dumps(
            {"claims": len(WITNESSES), "mismatches": mismatch_count},
            sort_keys=True,
        )
    )
    raise SystemExit(1 if mismatch_count else 0)


if __name__ == "__main__":
    main()
