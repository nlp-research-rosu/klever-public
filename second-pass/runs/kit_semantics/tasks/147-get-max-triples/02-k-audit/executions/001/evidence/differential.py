#!/usr/bin/env python3
"""Reviewer-authored differential check for HumanEval/147."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if len(sys.argv) != 3:
    raise SystemExit("usage: differential.py CANONICAL.py SOLUTION.py")

canonical = load(sys.argv[1], "trusted_canonical")
generated = load(sys.argv[2], "generated_solution")

rng = random.Random(147)
documented = [5]
empty_boundary = [0]
branch_boundaries = list(range(1, 19))
representative_generated = [rng.randint(1, 120) for _ in range(120)]
intended_inputs = sorted(set(documented + branch_boundaries + representative_generated))

rows = []
for n in intended_inputs:
    expected = canonical.get_max_triples(n)
    actual = generated.get_max_triples(n)
    rows.append({"n": n, "canonical": expected, "generated": actual})

mismatches = [row for row in rows if row["canonical"] != row["generated"]]
assert not mismatches, mismatches

outside_rows = []
for n in empty_boundary + [-1]:
    outside_rows.append(
        {
            "n": n,
            "canonical": canonical.get_max_triples(n),
            "generated": generated.get_max_triples(n),
            "contract_status": "outside positive-integer precondition",
        }
    )

print(
    json.dumps(
        {
            "oracle": str(Path(sys.argv[1]).resolve()),
            "implementation": str(Path(sys.argv[2]).resolve()),
            "documented": documented,
            "branch_boundaries": branch_boundaries,
            "generated_seed": 147,
            "generated_draw_count": len(representative_generated),
            "intended_unique_input_count": len(intended_inputs),
            "intended_inputs": intended_inputs,
            "intended_results": rows,
            "intended_mismatch_count": len(mismatches),
            "outside_contract_probes": outside_rows,
        },
        indent=2,
        sort_keys=True,
    )
)
