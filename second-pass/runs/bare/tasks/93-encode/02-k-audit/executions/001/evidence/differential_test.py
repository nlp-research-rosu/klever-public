#!/usr/bin/env python3
"""Independent differential checks for HumanEval 93.

The oracle is the trusted, mounted canonical.py.  The implementation under
test is the clean scratch copy of the submitted solution.py.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
import string
from pathlib import Path


def load_encode(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--inputs-json", type=Path, required=True)
    args = parser.parse_args()

    canonical_encode = load_encode(args.canonical, "trusted_canonical")
    candidate_encode = load_encode(args.candidate, "scratch_candidate")

    named_cases = [
        ("example-test", "test"),
        ("example-message", "This is a message"),
        ("empty", ""),
        ("single-lower-vowels", "aeiou"),
        ("single-upper-vowels", "AEIOU"),
        ("nonvowel-boundaries", "bBzZ"),
        ("alphabet-lower", string.ascii_lowercase),
        ("alphabet-upper", string.ascii_uppercase),
        ("spaces-from-example", "   "),
        ("alternating-branches", "aBaEbIcOdUf"),
        ("long-boundary", ("aZ eI" * 820)[:4096]),
    ]

    cases: list[tuple[str, str]] = list(named_cases)
    domain_alphabet = string.ascii_letters + " "
    cases.extend(
        (f"single-{ord(value):03d}", value) for value in domain_alphabet
    )
    cases.extend(
        (f"pair-{index:04d}", "".join(chars))
        for index, chars in enumerate(itertools.product(domain_alphabet, repeat=2))
    )

    rng = random.Random(930093)
    for index in range(1000):
        length = rng.randrange(0, 65)
        value = "".join(rng.choice(domain_alphabet) for _ in range(length))
        cases.append((f"generated-{index:04d}", value))

    args.inputs_json.write_text(
        json.dumps(
            {
                "domain": "ASCII letters plus space (space included because the prompt example uses it)",
                "seed": 930093,
                "cases": [{"name": name, "input": value} for name, value in cases],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    selected_results = {}
    for name, value in cases:
        expected = canonical_encode(value)
        actual = candidate_encode(value)
        if name in {item[0] for item in named_cases}:
            def bounded(value_to_report: str):
                if len(value_to_report) <= 120:
                    return value_to_report
                return {
                    "length": len(value_to_report),
                    "prefix": value_to_report[:80],
                    "sha256": hashlib.sha256(value_to_report.encode()).hexdigest(),
                }

            selected_results[name] = {
                "input_length": len(value),
                "expected": bounded(expected),
                "actual": bounded(actual),
            }
        if expected != actual:
            mismatches.append(
                {"name": name, "input": value, "expected": expected, "actual": actual}
            )

    print(f"oracle={args.canonical}")
    print(f"candidate={args.candidate}")
    print(f"case_count={len(cases)}")
    print(f"mismatch_count={len(mismatches)}")
    print("selected_results=" + json.dumps(selected_results, ensure_ascii=False, sort_keys=True))
    if mismatches:
        print("first_mismatches=" + json.dumps(mismatches[:10], ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
