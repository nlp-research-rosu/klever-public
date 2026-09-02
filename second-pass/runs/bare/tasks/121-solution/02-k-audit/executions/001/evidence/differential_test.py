#!/usr/bin/env python3
"""Independent differential test for HumanEval 121.

The oracle and generated modules are loaded from distinct, explicit paths.
The test data are declared in differential_inputs.json; short-list coverage is
exhaustive and the larger sample is deterministic.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "differential_inputs.json"
CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/candidate-src/solution.py")


def load_solution(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


def main() -> int:
    config = json.loads(MANIFEST.read_text(encoding="utf-8"))
    canonical = load_solution("trusted_humaneval_121", CANONICAL_PATH)
    generated = load_solution("candidate_humaneval_121", CANDIDATE_PATH)

    cases: list[list[int]] = [list(case) for case in config["explicit_cases"]]
    alphabet = config["exhaustive_alphabet"]
    for length in range(config["exhaustive_max_length"] + 1):
        cases.extend(map(list, itertools.product(alphabet, repeat=length)))

    rng = random.Random(config["random_seed"])
    for _ in range(config["random_case_count"]):
        length = rng.randint(0, config["random_max_length"])
        cases.append(
            [
                rng.randint(
                    config["random_value_min"], config["random_value_max"]
                )
                for _ in range(length)
            ]
        )

    mismatches = []
    digest = hashlib.sha256()
    for index, values in enumerate(cases):
        expected = canonical(values)
        actual = generated(values)
        digest.update(
            json.dumps(
                [values, expected, actual], separators=(",", ":")
            ).encode("utf-8")
        )
        if actual != expected:
            mismatches.append(
                {"index": index, "input": values, "canonical": expected, "candidate": actual}
            )
            if len(mismatches) >= 20:
                break

    documented = [
        ([5, 8, 7, 1], 12),
        ([3, 3, 3, 3, 3], 9),
        ([30, 13, 24, 321], 0),
    ]
    documented_results = [
        {
            "input": values,
            "expected": expected,
            "canonical": canonical(values),
            "candidate": generated(values),
        }
        for values, expected in documented
    ]
    print(
        json.dumps(
            {
                "canonical_path": str(CANONICAL_PATH),
                "candidate_path": str(CANDIDATE_PATH),
                "manifest": str(MANIFEST),
                "case_count": len(cases),
                "documented_results": documented_results,
                "mismatch_count": len(mismatches),
                "mismatches": mismatches,
                "result_digest_sha256": digest.hexdigest(),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
