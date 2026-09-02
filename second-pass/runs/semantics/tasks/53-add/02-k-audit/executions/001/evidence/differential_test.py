#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/53."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path
from typing import Callable


WORK = Path("/tmp/audit-work/53-add")
EVIDENCE = Path("/audit-output/evidence")


def load_entry(module_path: Path, module_name: str) -> Callable[[int, int], int]:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add


def make_inputs() -> tuple[list[tuple[int, int]], dict[str, object]]:
    documented = [(2, 3), (5, 7)]
    explicit_boundaries = [
        (0, 0),
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
        (1, -1),
        (-1, 1),
        (-10, 3),
        (3, -10),
        (2**63 - 1, 1),
        (-(2**63), -1),
        (10**100, -(10**100)),
        (10**100, 10**100),
        (-(10**100), -(10**100)),
    ]
    boundary_values = [
        -(2**63),
        -(2**31),
        -1000,
        -2,
        -1,
        0,
        1,
        2,
        1000,
        2**31 - 1,
        2**63 - 1,
    ]
    cartesian = [(x, y) for x in boundary_values for y in boundary_values]

    seed = 530053
    rng = random.Random(seed)
    generated = [
        (rng.randint(-10**12, 10**12), rng.randint(-10**12, 10**12))
        for _ in range(5000)
    ]

    inputs: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for pair in documented + explicit_boundaries + cartesian + generated:
        if pair not in seen:
            seen.add(pair)
            inputs.append(pair)

    scope = {
        "domain": "pairs of Python ints",
        "documented": documented,
        "explicit_boundaries": explicit_boundaries,
        "boundary_values_for_cartesian_product": boundary_values,
        "random_seed": seed,
        "random_pair_count": len(generated),
        "random_component_interval_inclusive": [-10**12, 10**12],
        "deduplicated_total": len(inputs),
    }
    return inputs, scope


def main() -> int:
    canonical = load_entry(WORK / "trusted" / "canonical.py", "trusted_canonical_53")
    candidate = load_entry(WORK / "solution.py", "audited_candidate_53")
    inputs, scope = make_inputs()

    (EVIDENCE / "differential-inputs.json").write_text(
        json.dumps({"scope": scope, "inputs": inputs}, indent=2) + "\n",
        encoding="utf-8",
    )

    mismatches: list[dict[str, object]] = []
    for x, y in inputs:
        try:
            canonical_result: object = canonical(x, y)
            canonical_error = None
        except Exception as err:  # pragma: no cover - retained for audit output
            canonical_result = None
            canonical_error = f"{type(err).__name__}: {err}"
        try:
            candidate_result: object = candidate(x, y)
            candidate_error = None
        except Exception as err:  # pragma: no cover - retained for audit output
            candidate_result = None
            candidate_error = f"{type(err).__name__}: {err}"

        expected = x + y
        if (
            canonical_error != candidate_error
            or canonical_result != candidate_result
            or canonical_error is not None
            or canonical_result != expected
            or type(canonical_result) is not int
            or type(candidate_result) is not int
        ):
            mismatches.append(
                {
                    "input": [x, y],
                    "canonical_result": canonical_result,
                    "canonical_error": canonical_error,
                    "candidate_result": candidate_result,
                    "candidate_error": candidate_error,
                    "mathematical_python_sum": expected,
                }
            )

    result = {
        "oracle": str(WORK / "trusted" / "canonical.py") + ":add",
        "candidate": str(WORK / "solution.py") + ":add",
        "scope": scope,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:20],
    }
    print(json.dumps(result, indent=2))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
