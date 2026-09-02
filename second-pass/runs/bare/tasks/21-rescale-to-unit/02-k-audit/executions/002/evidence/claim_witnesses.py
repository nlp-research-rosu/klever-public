#!/usr/bin/env python3
"""Ground satisfying witnesses for each symbolic candidate claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable


def load(path: Path) -> Callable[[list[float]], list[float]]:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


def main() -> int:
    submitted = load(Path("/candidate/solution.py"))
    canonical = load(Path("/reference/canonical.py"))
    witnesses = [
        {
            "claim": 1,
            "precondition": "true",
            "input": [1.0, 2.0, 3.0, 4.0, 5.0],
            "claimed": [0.0, 0.25, 0.5, 0.75, 1.0],
        },
        {
            "claim": 2,
            "precondition": "true",
            "input": [-5.0, 0.0, 5.0, 5.0],
            "claimed": [0.0, 0.5, 1.0, 1.0],
        },
        {
            "claim": 3,
            "precondition": "A < B",
            "binding": {"A": -2.0, "B": 6.0},
            "input": [-2.0, 6.0],
            "claimed": [0.0, 1.0],
        },
        {
            "claim": 4,
            "precondition": "A < B and B < C and A < C",
            "binding": {"A": -2.0, "B": 2.0, "C": 6.0},
            "input": [-2.0, 2.0, 6.0],
            "claimed": [0.0, 0.5, 1.0],
        },
        {
            "claim": 5,
            "precondition": "A < B and B < C and A < C and A != C",
            "binding": {"A": -2.0, "B": 2.0, "C": 6.0},
            "input": [-2.0, 2.0, 6.0],
            "claimed": [0.0, 0.5, 1.0],
        },
        {
            "claim": 6,
            "precondition": "A < B and B < C and A < C",
            "binding": {"A": -2.0, "B": 2.0, "C": 6.0},
            "input": [6.0, 2.0, -2.0],
            "claimed": [1.0, 0.5, 0.0],
        },
        {
            "claim": 7,
            "precondition": "A < B",
            "binding": {"A": -2.0, "B": 6.0},
            "input": [-2.0, -2.0, 6.0, 6.0],
            "claimed": [0.0, 0.0, 1.0, 1.0],
        },
    ]
    mismatches = 0
    for witness in witnesses:
        candidate_value = submitted(witness["input"].copy())
        canonical_value = canonical(witness["input"].copy())
        good = candidate_value == canonical_value == witness["claimed"]
        if not good:
            mismatches += 1
        print(
            json.dumps(
                witness
                | {
                    "submitted": candidate_value,
                    "canonical": canonical_value,
                    "match": good,
                },
                sort_keys=True,
            )
        )
    print(f"witnesses={len(witnesses)} mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
