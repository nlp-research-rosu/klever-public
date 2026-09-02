#!/usr/bin/env python3
"""Evaluate ground substitutions of verification.k's arrangeResult equations."""

import importlib.util
import json
import sys


sys.dont_write_bytecode = True


def load_entry(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.can_arrange


def arrange_result_equations(values):
    index = 0
    previous = 0
    result = -1
    for current in values:
        result = (
            index
            if index > 0 and current < previous
            else result
        )
        index += 1
        previous = current
    return result


canonical = load_entry("trusted_canonical_ground", "/reference/canonical.py")
generated = load_entry("candidate_solution_ground", "/candidate/solution.py")
inputs = [[], [7], [1, 2], [2, 1], [1, 2, 4, 3, 5], [5, 4, 3, 2, 1]]
rows = []
for values in inputs:
    summary = arrange_result_equations(values)
    expected = canonical(list(values))
    actual = generated(list(values))
    rows.append(
        {
            "input": values,
            "arrangeResult_equations": summary,
            "canonical_python": expected,
            "generated_python": actual,
            "all_equal": summary == expected == actual,
        }
    )

print(json.dumps(rows, indent=2))
raise SystemExit(0 if all(row["all_equal"] for row in rows) else 1)
