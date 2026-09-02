#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs submitted solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable

CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/candidate-src/solution.py")
INPUT_MANIFEST = Path("/audit-output/evidence/differential-inputs.json")
SEED = 350035


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element


def outcome(function: Callable[[list[int]], int], values: list[int]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(list(values))}
    except Exception as error:  # The empty diagnostic intentionally records exceptions.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def main() -> None:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    generated = load_entry(GENERATED_PATH, "submitted_generated")

    named_cases: list[tuple[str, list[int]]] = [
        ("documented_example_1", [1, 2, 3]),
        ("documented_example_2", [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]),
        ("empty_outside_intended_domain", []),
        ("singleton_zero", [0]),
        ("singleton_negative", [-9]),
        ("branch_strictly_greater", [2, 3]),
        ("branch_strictly_less", [3, 2]),
        ("branch_equal", [3, 3]),
        ("maximum_first", [8, 7, 6, 5]),
        ("maximum_middle", [-5, 11, -2, 3]),
        ("maximum_last", [-5, -2, 0]),
        ("duplicate_maximum", [4, 9, 1, 9, 2]),
        ("large_python_integers", [-(10**100), 10**200, 10**150]),
    ]

    exhaustive_cases = [
        list(values)
        for length in range(1, 5)
        for values in itertools.product((-2, -1, 0, 1, 2), repeat=length)
    ]
    randomizer = random.Random(SEED)
    random_cases = [
        [
            randomizer.randint(-(10**12), 10**12)
            for _ in range(randomizer.randint(1, 64))
        ]
        for _ in range(500)
    ]

    manifest = {
        "oracle": str(CANONICAL_PATH),
        "generated": str(GENERATED_PATH),
        "intended_domain": "non-empty lists of Python integers",
        "named_cases": [{"name": name, "input": values} for name, values in named_cases],
        "exhaustive_generator": {
            "lengths": [1, 2, 3, 4],
            "values": [-2, -1, 0, 1, 2],
            "count": len(exhaustive_cases),
        },
        "exhaustive_inputs": exhaustive_cases,
        "random_generator": {
            "seed": SEED,
            "count": len(random_cases),
            "length_range": [1, 64],
            "element_range": [-(10**12), 10**12],
        },
        "random_inputs": random_cases,
    }
    INPUT_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    intended_mismatches: list[dict[str, Any]] = []
    named_results: list[dict[str, Any]] = []
    for name, values in named_cases:
        left = outcome(canonical, values)
        right = outcome(generated, values)
        record = {
            "name": name,
            "input": values,
            "canonical": left,
            "generated": right,
            "equal": left == right,
        }
        named_results.append(record)
        if values and left != right:
            intended_mismatches.append(record)

    for family, cases in (("exhaustive", exhaustive_cases), ("random", random_cases)):
        for index, values in enumerate(cases):
            left = outcome(canonical, values)
            right = outcome(generated, values)
            if left != right:
                intended_mismatches.append(
                    {
                        "family": family,
                        "index": index,
                        "input": values,
                        "canonical": left,
                        "generated": right,
                    }
                )

    print(f"canonical_path={CANONICAL_PATH}")
    print(f"generated_path={GENERATED_PATH}")
    print("intended_domain=non-empty lists of Python integers")
    print(f"manifest={INPUT_MANIFEST}")
    print(f"named_case_count={len(named_cases)}")
    print(f"exhaustive_case_count={len(exhaustive_cases)}")
    print(f"random_seed={SEED}")
    print(f"random_case_count={len(random_cases)}")
    print("named_results=" + json.dumps(named_results, sort_keys=True))
    print(f"material_mismatches_intended_domain={len(intended_mismatches)}")
    if intended_mismatches:
        print("mismatch_sample=" + json.dumps(intended_mismatches[:10], sort_keys=True))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
