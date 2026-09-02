#!/usr/bin/env python3
"""Ground witnesses for the formal entry precondition and postcondition."""

from __future__ import annotations

import ast
import importlib.util
import json
from collections import Counter
from pathlib import Path


CASES = {
    "result_empty": [],
    "result_two_duplicates": [0, 0],
    "result_three_duplicates": [0, 0, 0],
    "result_unsorted": [1, 0],
    "result_large": [0, 10**40],
}


def load_entry(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem + "_ground", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def first_function_dump(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return ast.dump(tree.body[0], include_attributes=False)


def intended(values: list[int]) -> bool:
    # Ground interpretation of intendedSorted for ordinary integer lists:
    # equality with ascending sort, then the scan's >2 update.
    result = values == sorted(values)
    counts = Counter(values)
    for value in values:
        if counts[value] > 2:
            result = False
    return result


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"))
    generated = load_entry(Path("/tmp/audit-work/scratch/solution.py"))
    concrete_source = Path("/audit-output/evidence/stage4_concrete.py")

    source_identity = (
        first_function_dump(concrete_source)
        == first_function_dump(Path("/tmp/audit-work/scratch/solution.py"))
    )
    print(f"CONCRETE_FUNCTION_AST_IDENTICAL={str(source_identity).lower()}")

    failures = 0
    for name, values in CASES.items():
        row = {
            "name": name,
            "input": values,
            "precondition_nonnegative_ints": all(
                type(value) is int and value >= 0 for value in values
            ),
            "formal_ground_result": intended(values),
            "canonical": canonical(values.copy()),
            "generated": generated(values.copy()),
        }
        row["all_equal"] = (
            row["precondition_nonnegative_ints"]
            and row["formal_ground_result"]
            == row["canonical"]
            == row["generated"]
        )
        failures += not row["all_equal"]
        print(json.dumps(row, sort_keys=True))
    print(f"GROUND_FAILURES={failures}")
    return 0 if source_identity and failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
