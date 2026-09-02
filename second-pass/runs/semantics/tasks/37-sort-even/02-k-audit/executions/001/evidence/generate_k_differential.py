#!/usr/bin/env python3
"""Generate a bounded concrete-K differential corpus with canonical answers."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path

ROOT = Path("/tmp/audit-work/37-sort-even-audit")
EVIDENCE = Path("/audit-output/evidence")


def load_canonical():
    path = ROOT / "trusted/canonical.py"
    spec = importlib.util.spec_from_file_location("k_diff_canonical", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_even


def main() -> int:
    canonical = load_canonical()
    explicit = [
        [],
        [7],
        [1, 2],
        [3, 2, 1],
        [5, 6, 3, 4],
        [9, -1, 3, -2, 3, -3, 0],
    ]
    alphabet = [-2, -1, 0, 1, 2]
    exhaustive = [
        list(values)
        for length in range(3)
        for values in itertools.product(alphabet, repeat=length)
    ]
    rng = random.Random(370137)
    generated = [
        [rng.randint(-100, 100) for _ in range(rng.randint(0, 15))]
        for _ in range(63)
    ]
    cases = explicit + exhaustive + generated
    assert len(cases) == 100

    inputs_path = EVIDENCE / "k-differential-inputs.json"
    inputs_path.write_text(
        json.dumps(
            {
                "explicit": explicit,
                "exhaustive": {
                    "alphabet": alphabet,
                    "lengths": [0, 1, 2],
                    "cases": exhaustive,
                },
                "generated": {
                    "seed": 370137,
                    "length_range": [0, 15],
                    "value_range": [-100, 100],
                    "cases": generated,
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    source = (ROOT / "source/solution.py").read_text(encoding="utf-8").rstrip()
    assertions = [
        f"assert sort_even({case!r}) == {canonical(list(case))!r}"
        for case in cases
    ]
    program = source + "\n\n" + "\n".join(assertions) + "\n"
    program_path = EVIDENCE / "k-differential-tests.py"
    program_path.write_text(program, encoding="utf-8")
    print(f"cases={len(cases)}")
    print(f"program={program_path}")
    print(f"inputs={inputs_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
