#!/usr/bin/env python3
"""Independent differential check for HumanEval problem 26."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


EVIDENCE_DIR = Path(__file__).resolve().parent
MANIFEST = EVIDENCE_DIR / "03-differential-inputs.json"
TRUSTED = Path("/tmp/audit-work/26-remove-duplicates/trusted/canonical.py")
GENERATED = Path("/tmp/audit-work/26-remove-duplicates/candidate/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_duplicates


def direct_contract_oracle(numbers: list[int]) -> list[int]:
    """Independent statement of the prompt: retain values occurring exactly once."""
    return [value for value in numbers if sum(item == value for item in numbers) == 1]


def generated_cases(config: dict):
    for case in config["documented_and_targeted_cases"]:
        yield "targeted", case

    exhaustive = config["exhaustive"]
    for length in exhaustive["lengths"]:
        for case in itertools.product(exhaustive["alphabet"], repeat=length):
            yield "exhaustive", list(case)

    random_spec = config["random"]
    rng = random.Random(random_spec["seed"])
    for _ in range(random_spec["case_count"]):
        length = rng.randint(random_spec["min_length"], random_spec["max_length"])
        case: list[int] = []
        for _ in range(length):
            if case and rng.random() < random_spec["duplicate_injection_probability"]:
                case.append(rng.choice(case))
            else:
                case.append(
                    rng.randint(random_spec["min_value"], random_spec["max_value"])
                )
        yield "random", case


def main() -> int:
    config = json.loads(MANIFEST.read_text())
    canonical = load_function("trusted_canonical_26", TRUSTED)
    candidate = load_function("generated_solution_26", GENERATED)
    counts = {"targeted": 0, "exhaustive": 0, "random": 0}
    mismatches: list[dict] = []

    for group, case in generated_cases(config):
        counts[group] += 1
        expected = direct_contract_oracle(case)
        canonical_result = canonical(list(case))
        candidate_result = candidate(list(case))
        if canonical_result != expected or candidate_result != expected:
            mismatches.append(
                {
                    "group": group,
                    "input": case,
                    "oracle": expected,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                }
            )
            if len(mismatches) >= 20:
                break

    print(f"trusted_module={TRUSTED}")
    print(f"candidate_module={GENERATED}")
    print(f"counts={json.dumps(counts, sort_keys=True)}")
    print(f"total_cases={sum(counts.values())}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2, sort_keys=True))
        return 1
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
