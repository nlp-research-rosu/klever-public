#!/usr/bin/env python3
"""Independent exhaustive comparison of trusted canonical and candidate Python."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


ROOT = Path("/audit-output/evidence")
INPUTS = json.loads((ROOT / "differential_inputs.json").read_text())
CANONICAL_PATH = Path("/tmp/audit-work/reconstruction/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/candidate/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.int_to_mini_roman


def main() -> None:
    canonical = load_function("trusted_canonical", CANONICAL_PATH)
    candidate = load_function("candidate_solution", CANDIDATE_PATH)

    examples = {int(key): value for key, value in INPUTS["documented_examples"].items()}
    for number, expected in examples.items():
        got_canonical = canonical(number)
        got_candidate = candidate(number)
        assert got_canonical == expected, (number, got_canonical, expected)
        assert got_candidate == expected, (number, got_candidate, expected)

    boundaries = INPUTS["digit_and_subtractive_boundaries"]
    boundary_rows = [
        (number, canonical(number), candidate(number)) for number in boundaries
    ]
    assert all(left == right for _, left, right in boundary_rows)

    generator = INPUTS["representative_generation"]
    representative = random.Random(generator["seed"]).sample(
        range(
            INPUTS["contract_domain"]["minimum"],
            INPUTS["contract_domain"]["maximum"] + 1,
        ),
        generator["count"],
    )
    assert all(canonical(number) == candidate(number) for number in representative)

    mismatches = []
    rows = []
    for number in range(
        INPUTS["contract_domain"]["minimum"],
        INPUTS["contract_domain"]["maximum"] + 1,
    ):
        expected = canonical(number)
        actual = candidate(number)
        rows.append([number, expected, actual])
        if expected != actual:
            mismatches.append([number, expected, actual])
        assert isinstance(actual, str)
        assert actual == actual.lower()

    excluded_rows = [
        [number, canonical(number), candidate(number)]
        for number in INPUTS["excluded_domain_diagnostics"]
    ]
    encoded = json.dumps(rows, separators=(",", ":"), ensure_ascii=True).encode()
    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print("empty_case=NOT_APPLICABLE (contract input is an integer)")
    print(f"examples={json.dumps(examples, sort_keys=True)}")
    print(f"branch_boundaries={json.dumps(boundary_rows)}")
    print(f"representative_seed={generator['seed']} count={len(representative)}")
    print(f"representative_inputs={json.dumps(representative)}")
    print(f"exhaustive_domain=1..1000 cases={len(rows)}")
    print(f"mismatches={len(mismatches)}")
    print(f"mapping_sha256={hashlib.sha256(encoded).hexdigest()}")
    print(f"excluded_domain_diagnostics={json.dumps(excluded_rows)}")
    if mismatches:
        print(f"mismatch_rows={json.dumps(mismatches)}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
