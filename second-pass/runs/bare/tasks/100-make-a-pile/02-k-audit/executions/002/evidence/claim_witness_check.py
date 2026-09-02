#!/usr/bin/env python3
"""Ground witnesses for every submitted claim precondition."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_a_pile


def pile_from(n: int, index: int) -> list[int]:
    return [n + 2 * i for i in range(index, n)]


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 2

    canonical = load(Path(sys.argv[1]), "canonical_witness")
    candidate = load(Path(sys.argv[2]), "candidate_witness")

    n = 3
    preservation_i = 1
    witnesses = {
        "invariant-initialization": {
            "N": n,
            "precondition": n > 0,
            "start_env": {"n": n},
        },
        "invariant-preservation": {
            "N": n,
            "I": preservation_i,
            "precondition": n > 0 and 0 <= preservation_i < n,
            "start_env": {
                "i": preservation_i,
                "n": n,
                "result": pile_from(n, preservation_i + 1),
            },
        },
        "invariant-exit": {
            "N": n,
            "precondition": n > 0,
            "start_env": {"i": -1, "n": n, "result": pile_from(n, 0)},
        },
        "loop-invariant": {
            "N": n,
            "I": n - 1,
            "precondition": n > 0 and -1 <= n - 1 < n,
            "start_env": {"i": n - 1, "n": n, "result": pile_from(n, n)},
        },
        "functional-correctness": {"N": n, "precondition": n > 0},
    }
    claimed = pile_from(n, 0)
    canonical_result = canonical(n)
    candidate_result = candidate(n)

    for label, witness in witnesses.items():
        print(f"{label}: {witness}")
        assert witness["precondition"]
    print(f"CLAIMED_PILE_FROM_3_0={claimed}")
    print(f"CANONICAL_N_3={canonical_result}")
    print(f"CANDIDATE_N_3={candidate_result}")
    assert claimed == canonical_result == candidate_result == [3, 5, 7]
    print("WITNESS_CHECK=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
