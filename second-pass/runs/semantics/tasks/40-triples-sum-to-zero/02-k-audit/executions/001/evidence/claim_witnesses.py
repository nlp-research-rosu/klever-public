#!/usr/bin/env python3
"""Concrete satisfying witnesses for every submitted entry-claim precondition."""

from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_contract(values: list[int]) -> bool:
    return any(sum(values[i] for i in triple) == 0
               for triple in itertools.combinations(range(len(values)), 3))


def main() -> int:
    root = Path("/tmp/audit-work/forty-triples-audit")
    canonical = load(root / "trusted/canonical.py", "claim_trusted")
    candidate = load(root / "candidate-src/solution.py", "claim_candidate")
    witnesses = [
        ("empty", []),
        ("length-one", [0]),
        ("length-two", [0, 0]),
        ("length-three", [0, 0, 0]),
        ("length-four", [1, 2, 3, 7]),
        ("length-five", [50, 60, -3, 1, 2]),
        ("length-six", [2, 4, -5, 3, 9, 7]),
    ]
    failures = 0
    for label, values in witnesses:
        formal_summary = independent_contract(values)
        trusted_result = canonical.triples_sum_to_zero(list(values))
        candidate_result = candidate.triples_sum_to_zero(list(values))
        ok = (
            len(values) == witnesses.index((label, values))
            and type(trusted_result) is bool
            and type(candidate_result) is bool
            and formal_summary == trusted_result == candidate_result
        )
        print(
            f"WITNESS {label} input={values!r} "
            f"hasZeroTriple={formal_summary} canonical={trusted_result} "
            f"candidate={candidate_result} precondition_satisfied={ok}"
        )
        failures += not ok
    print(f"WITNESS_FAILURE_COUNT {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
