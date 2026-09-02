#!/usr/bin/env python3
"""Independent differential audit for HumanEval 126.

Inputs are finite lists of non-negative Python ints.  The exhaustive and
pseudorandom scopes below are deterministic and part of the evidence.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/126-is-sorted")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


canonical = load_entry("audit_canonical", SCRATCH / "canonical.py")
generated = load_entry("audit_generated", SCRATCH / "solution.py")


DOCUMENTED = [
    [5],
    [1, 2, 3, 4, 5],
    [1, 3, 2, 4, 5],
    [1, 2, 3, 4, 5, 6],
    [1, 2, 3, 4, 5, 6, 7],
    [1, 3, 2, 4, 5, 6, 7],
    [1, 2, 2, 3, 3, 4],
    [1, 2, 2, 2, 3, 4],
]

BOUNDARY_AND_BRANCH = [
    [],                    # zero loop iterations
    [0],                   # sentinel lower boundary, comparison/equality false
    [0, 0],                # equality and increment, duplicate threshold false
    [0, 0, 0],             # duplicate threshold true
    [0, 1],                # strict increase
    [1, 0],                # descent
    [0, 1, 0],             # late descent
    [0, 0, 1, 1],          # reset then exactly two of a new value
    [0, 0, 1, 1, 1],       # reset then triple of a new value
    [10**100],             # unbounded-integer representative
    [0, 10**100],
    [10**100, 0],
]


def compare(case: list[int], label: str, mismatches: list[tuple]):
    left = canonical(case.copy())
    right = generated(case.copy())
    if type(left) is not bool or type(right) is not bool or left != right:
        mismatches.append((label, case, left, right))


def main() -> None:
    mismatches: list[tuple] = []
    counts = {"documented": 0, "boundary_branch": 0, "exhaustive": 0, "random": 0}

    for case in DOCUMENTED:
        compare(case, "documented", mismatches)
        counts["documented"] += 1

    for case in BOUNDARY_AND_BRANCH:
        compare(case, "boundary_branch", mismatches)
        counts["boundary_branch"] += 1

    for length in range(7):
        for values in itertools.product(range(5), repeat=length):
            compare(list(values), "exhaustive", mismatches)
            counts["exhaustive"] += 1

    rng = random.Random(126)
    atoms = [0, 1, 2, 3, 10, 2**63 - 1, 10**100]
    for _ in range(5000):
        case = [rng.choice(atoms) for _ in range(rng.randrange(0, 51))]
        compare(case, "random", mismatches)
        counts["random"] += 1

    print("domain=finite lists of non-negative Python ints")
    print("documented_cases=8")
    print("boundary_branch_cases=12")
    print("exhaustive_scope=all lengths 0..6 over values 0..4")
    print("random_scope=5000 lists; seed=126; lengths 0..50; atoms=0,1,2,3,10,2**63-1,10**100")
    print(f"counts={counts}")
    print(f"total_comparisons={sum(counts.values())}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(f"first_mismatch={mismatches[0]!r}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
