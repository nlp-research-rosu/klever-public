#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential audit.

The input corpus is deterministically written to the path supplied as argv[1].
It imports the trusted canonical entry point and the scratch-copied candidate
entry point as distinct modules.
"""

import importlib.util
import itertools
import json
import math
import random
import sys
from pathlib import Path


def import_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


def encoded(value):
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if value == math.inf:
            return "+Infinity"
        if value == -math.inf:
            return "-Infinity"
        if value == 0.0 and math.copysign(1.0, value) < 0:
            return "-0.0"
    return value


def record_case(label, numbers, threshold):
    return {
        "label": label,
        "numbers": list(numbers),
        "threshold": threshold,
    }


def outcome(function, numbers, threshold):
    try:
        return ("return", function(list(numbers), threshold))
    except Exception as error:  # compare exceptions without hiding them
        return ("exception", type(error).__name__, str(error))


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: differential_audit.py INPUTS_JSON")

    canonical = import_function(
        "trusted_canonical_audit", Path("/tmp/audit-work/0-has-close-elements/canonical.py")
    )
    candidate = import_function(
        "candidate_solution_audit", Path("/tmp/audit-work/0-has-close-elements/solution.py")
    )

    cases = [
        record_case("prompt-false", [1.0, 2.0, 3.0], 0.5),
        record_case("prompt-true", [1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3),
        record_case("empty", [], 1.0),
        record_case("singleton", [1.0], 1.0),
        record_case("i-less-j-false-only", [7.0], 10.0),
        record_case("distance-equals-threshold", [0.0, 1.0], 1.0),
        record_case("distance-just-inside", [0.0, math.nextafter(1.0, 0.0)], 1.0),
        record_case("distance-just-outside", [0.0, math.nextafter(1.0, math.inf)], 1.0),
        record_case("duplicate-zero-threshold", [1.0, 1.0], 0.0),
        record_case("duplicate-positive-threshold", [1.0, 1.0], 0.01),
        record_case("negative-threshold", [-2.0, -1.9], -0.1),
        record_case("negative-and-positive", [-2.0, 2.0, -1.9], 0.2),
        record_case("negative-zero", [-0.0, 0.0], 0.0),
        record_case("negative-zero-positive-threshold", [-0.0, 0.0], 5e-324),
        record_case("positive-infinities", [math.inf, math.inf], 1.0),
        record_case("opposite-infinities", [-math.inf, math.inf], math.inf),
        record_case("nan-list", [math.nan, 0.0, math.nan], math.inf),
        record_case("nan-threshold", [0.0, 0.0], math.nan),
    ]

    values = [-2.0, -0.5, -0.0, 0.0, 0.5, 2.0]
    thresholds = [-1.0, 0.0, 5e-324, 0.1, 0.5, 1.0, 2.5]
    for length in range(5):
        for numbers in itertools.product(values, repeat=length):
            for threshold in thresholds:
                cases.append(record_case(f"exhaustive-len-{length}", numbers, threshold))

    rng = random.Random(23071983)
    for index in range(2000):
        length = rng.randrange(0, 10)
        numbers = [rng.uniform(-1e6, 1e6) for _ in range(length)]
        threshold = rng.uniform(-100.0, 1e6)
        cases.append(record_case(f"seeded-random-{index}", numbers, threshold))

    serializable_cases = [
        {
            "label": case["label"],
            "numbers": [encoded(value) for value in case["numbers"]],
            "threshold": encoded(case["threshold"]),
        }
        for case in cases
    ]
    Path(sys.argv[1]).write_text(
        json.dumps(serializable_cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    mismatches = []
    branch_results = {"canonical_true": 0, "canonical_false": 0}
    for index, case in enumerate(cases):
        expected = outcome(canonical, case["numbers"], case["threshold"])
        actual = outcome(candidate, case["numbers"], case["threshold"])
        if expected == ("return", True):
            branch_results["canonical_true"] += 1
        if expected == ("return", False):
            branch_results["canonical_false"] += 1
        if expected != actual:
            mismatches.append(
                {
                    "index": index,
                    "case": serializable_cases[index],
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    print("canonical_path=/tmp/audit-work/0-has-close-elements/canonical.py")
    print("candidate_path=/tmp/audit-work/0-has-close-elements/solution.py")
    print(f"documented_and_boundary_cases=18")
    print(f"total_cases={len(cases)}")
    print(f"branch_results={json.dumps(branch_results, sort_keys=True)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:10], indent=2, default=encoded))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
