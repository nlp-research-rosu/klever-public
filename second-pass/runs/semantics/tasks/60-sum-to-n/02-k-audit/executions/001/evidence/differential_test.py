#!/usr/bin/env python3
"""Independent differential test for HumanEval 60 and the submitted solution."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUTS = HERE / "differential_inputs.json"
CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/reconstruction/solution.py")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generated_values(cfg: dict[str, int]) -> list[int]:
    rng = random.Random(cfg["seed"])
    return [
        rng.randint(cfg["minimum"], cfg["maximum"])
        for _ in range(cfg["count"])
    ]


def digest(values: list[int]) -> str:
    payload = json.dumps(values, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def compare(canonical, generated, values: list[int]):
    mismatches = []
    for n in values:
        expected = canonical.sum_to_n(n)
        actual = generated.sum_to_n(n)
        if expected != actual:
            mismatches.append((n, expected, actual))
    return mismatches


def main() -> int:
    config = json.loads(INPUTS.read_text())
    canonical = load_module("trusted_canonical", CANONICAL)
    generated = load_module("submitted_solution", GENERATED)

    examples = config["documented_examples"]
    example_values = [n for n, _ in examples]
    for n, stated in examples:
        canonical_value = canonical.sum_to_n(n)
        generated_value = generated.sum_to_n(n)
        if canonical_value != stated or generated_value != stated:
            print(
                "DOCUMENTED EXAMPLE FAILURE",
                n,
                stated,
                canonical_value,
                generated_value,
            )
            return 1

    boundaries = config["boundary_and_empty_cases"]
    exhaustive_cfg = config["intended_domain_exhaustive"]
    exhaustive = list(
        range(exhaustive_cfg["start"], exhaustive_cfg["stop_inclusive"] + 1)
    )
    generated_in = generated_values(config["intended_domain_generated"])
    intended = sorted(set(example_values + [n for n in boundaries if n >= 0] + exhaustive + generated_in))
    intended_mismatches = compare(canonical, generated, intended)

    generated_out = generated_values(config["outside_formal_domain_generated"])
    outside = sorted(set([n for n in boundaries if n < 0] + generated_out))
    outside_mismatches = compare(canonical, generated, outside)

    print(f"canonical={CANONICAL}")
    print(f"generated={GENERATED}")
    print(f"documented_examples={len(examples)} status=PASS")
    print(
        f"intended_nonnegative_cases={len(intended)} "
        f"sha256={digest(intended)} mismatches={len(intended_mismatches)}"
    )
    print(
        f"outside_formal_domain_negative_cases={len(outside)} "
        f"sha256={digest(outside)} mismatches={len(outside_mismatches)}"
    )
    print(f"boundary_results={[(n, canonical.sum_to_n(n), generated.sum_to_n(n)) for n in boundaries]}")
    print(f"outside_mismatch_sample={outside_mismatches[:10]}")

    if intended_mismatches:
        print(f"intended_mismatch_sample={intended_mismatches[:10]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
