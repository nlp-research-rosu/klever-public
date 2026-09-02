#!/usr/bin/env python3
"""Independent differential test of trusted canonical and submitted solution."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.car_race_collision


def main() -> int:
    evidence = Path(__file__).resolve().parent
    inputs = json.loads((evidence / "differential_inputs.json").read_text())
    canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_function(
        "submitted_generated", Path("/tmp/audit-work/race41/solution.py")
    )

    cases = list(inputs["documented_examples"])
    cases.extend(inputs["explicit_nonnegative_integers"])
    range_spec = inputs["exhaustive_range"]
    cases.extend(range(range_spec["start"], range_spec["stop_exclusive"]))
    random_spec = inputs["generated_sample"]
    generator = random.Random(random_spec["seed"])
    cases.extend(
        generator.randint(random_spec["minimum"], random_spec["maximum"])
        for _ in range(random_spec["count"])
    )

    mismatches = []
    for index, value in enumerate(cases):
        expected = canonical(value)
        observed = generated(value)
        if observed != expected:
            mismatches.append(
                {
                    "index": index,
                    "input": value,
                    "canonical": expected,
                    "generated": observed,
                }
            )

    unique_cases = len(set(cases))
    print(f"total_cases={len(cases)}")
    print(f"unique_cases={unique_cases}")
    print(
        "scope=explicit boundary 0 and 1; exhaustive 0..200; "
        "1000 deterministic generated nonnegative integers"
    )
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
