#!/usr/bin/env python3
"""Static source-body identity plus boundary/counterfactual semantic checks."""

from __future__ import annotations

import ast
import json
from pathlib import Path


solution_path = Path("/reference/k-proof/solution.py")
expected_source = """\
def choose_num(x, y):
    if y % 2 == 0:
        if y >= x:
            return y
        return -1
    if y - 1 >= x:
        return y - 1
    return -1
"""
observed_ast = ast.dump(
    ast.parse(solution_path.read_text()), include_attributes=False
)
expected_ast = ast.dump(
    ast.parse(expected_source), include_attributes=False
)


def audited_operational_model(x: int, y: int) -> int:
    """Local evaluator for the statically checked frozen source AST."""

    if y % 2 == 0:
        if y >= x:
            return y
        return -1
    if y - 1 >= x:
        return y - 1
    return -1


def summary(x: int, y: int) -> int:
    upper = y - (y % 2)
    return upper if x <= upper else -1


def parity_flipped_mutant(x: int, y: int) -> int:
    if y % 2 == 1:
        if y >= x:
            return y
        return -1
    if y - 1 >= x:
        return y - 1
    return -1


cases = [
    (12, 15),
    (13, 12),
    (2, 2),
    (3, 3),
    (4, 5),
    (5, 5),
    (6, 5),
    (1, 1),
    (1, 2),
    (1, 3),
    (99, 100),
    (101, 100),
]
results = [
    {
        "x": x,
        "y": y,
        "audited_operational_model": audited_operational_model(x, y),
        "summary": summary(x, y),
        "match": audited_operational_model(x, y) == summary(x, y),
        "parity_flipped_mutant": parity_flipped_mutant(x, y),
        "mutant_differs": (
            parity_flipped_mutant(x, y) != audited_operational_model(x, y)
        ),
    }
    for x, y in cases
]
failures = [item for item in results if not item["match"]]
mutant_witnesses = [item for item in results if item["mutant_differs"]]
print(
    json.dumps(
        {
            "frozen_source_ast_matches_audited_model": (
                observed_ast == expected_ast
            ),
            "cases": results,
            "all_source_summary_matches": not failures,
            "counterfactual_mutant_witness_count": len(mutant_witnesses),
            "counterfactual_mutant_witnesses": mutant_witnesses,
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(
    1
    if observed_ast != expected_ast or failures or not mutant_witnesses
    else 0
)
