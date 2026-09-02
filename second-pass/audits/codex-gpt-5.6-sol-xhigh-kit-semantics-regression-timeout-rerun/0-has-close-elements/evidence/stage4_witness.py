#!/usr/bin/env python3
"""Check exact function-body identity and concrete satisfying witnesses."""

import ast
import importlib.util
import json
from pathlib import Path


def load_function(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


def function_ast(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    functions = [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "has_close_elements"
    ]
    if len(functions) != 1:
        raise AssertionError((path, len(functions)))
    return ast.dump(functions[0], include_attributes=False)


scratch = Path("/tmp/audit-work/0-has-close-elements")
evidence = Path("/audit-output/evidence")
solution_path = scratch / "solution.py"
concrete_path = evidence / "concrete_audit.py"

solution_ast = function_ast(solution_path)
concrete_ast = function_ast(concrete_path)
print(f"concrete_harness_function_ast_identity={solution_ast == concrete_ast}")
if solution_ast != concrete_ast:
    raise AssertionError("concrete harness changed the candidate function")

canonical = load_function("stage4_canonical", scratch / "canonical.py")
candidate = load_function("stage4_candidate", solution_path)
witnesses = [
    {
        "name": "empty-satisfying-entry",
        "numbers": [],
        "threshold": 1.0,
        "claimed_pair_formula": False,
    },
    {
        "name": "prompt-true-satisfying-entry",
        "numbers": [1.0, 2.8, 3.0, 4.0, 5.0, 2.0],
        "threshold": 0.3,
        "claimed_pair_formula": True,
    },
    {
        "name": "strict-boundary-satisfying-entry",
        "numbers": [0.0, 1.0],
        "threshold": 1.0,
        "claimed_pair_formula": False,
    },
]

failures = []
for witness in witnesses:
    numbers = witness["numbers"]
    threshold = witness["threshold"]
    independent_pair_formula = any(
        abs(numbers[left] - numbers[right]) < threshold
        for left in range(len(numbers))
        for right in range(left + 1, len(numbers))
    )
    row = {
        **witness,
        "independent_pair_formula": independent_pair_formula,
        "canonical": canonical(numbers, threshold),
        "candidate": candidate(numbers, threshold),
        "formal_precondition_all_float": all(
            isinstance(value, float) for value in numbers
        )
        and isinstance(threshold, float),
    }
    print(json.dumps(row, sort_keys=True))
    if len(set([
        row["claimed_pair_formula"],
        row["independent_pair_formula"],
        row["canonical"],
        row["candidate"],
    ])) != 1 or not row["formal_precondition_all_float"]:
        failures.append(row)

print(f"witness_failures={len(failures)}")
raise SystemExit(1 if failures else 0)
