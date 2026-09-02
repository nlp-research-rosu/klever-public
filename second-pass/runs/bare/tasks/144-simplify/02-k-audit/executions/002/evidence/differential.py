#!/usr/bin/env python3
"""Independent differential audit for HumanEval 144.

Input scope:
* the three prompt examples;
* explicit minimum, divisibility-boundary, leading-zero, and large-integer cases;
* every positive a,b,c,d in 1..20 for x=a/b and n=c/d;
* 10,000 deterministic pseudo-random positive quadruples in 1..10**9;
* three out-of-contract malformed/zero-denominator diagnostics.

The exact-integer oracle is independently restated from the natural-language
contract.  The trusted canonical implementation is also imported and compared.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


def exact_oracle(x: str, n: str) -> bool:
    a_text, b_text = x.split("/")
    c_text, d_text = n.split("/")
    a, b, c, d = map(int, (a_text, b_text, c_text, d_text))
    return (a * c) % (b * d) == 0


def outcome(function, x: str, n: str):
    try:
        return ("value", function(x, n))
    except Exception as error:  # Diagnostics intentionally include invalid cases.
        return ("exception", type(error).__name__, str(error))


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: differential.py TRUSTED_CANONICAL GENERATED_SOLUTION")

    canonical = load_entry(Path(sys.argv[1]), "audit_trusted_canonical")
    generated = load_entry(Path(sys.argv[2]), "audit_generated_solution")

    cases: list[tuple[str, str, str]] = [
        ("example", "1/5", "5/1"),
        ("example", "1/6", "2/1"),
        ("example", "7/10", "10/2"),
        ("minimum-true", "1/1", "1/1"),
        ("minimum-false", "1/2", "1/1"),
        ("cross-cancel-true", "5/6", "6/5"),
        ("product-boundary-below", "5/6", "1/1"),
        ("product-boundary-equal", "2/3", "3/2"),
        ("remainder-one", "7/3", "1/2"),
        ("multi-integer-true", "9/2", "4/1"),
        ("leading-zero-true", "0001/0005", "0005/0001"),
        ("leading-zero-false", "0001/0006", "0002/0001"),
        ("float-rounding-boundary", f"{2**54 + 1}/2", "1/1"),
        ("large-exact-true", f"{10**400}/1", "1/1"),
        ("large-exact-false", f"{10**400 + 1}/2", "1/1"),
    ]

    for a in range(1, 21):
        for b in range(1, 21):
            for c in range(1, 21):
                for d in range(1, 21):
                    cases.append(("exhaustive-1..20", f"{a}/{b}", f"{c}/{d}"))

    rng = random.Random(144)
    for _ in range(10_000):
        a, b, c, d = (rng.randint(1, 10**9) for _ in range(4))
        cases.append(("random-seed-144", f"{a}/{b}", f"{c}/{d}"))

    encoded_cases = json.dumps(cases, separators=(",", ":")).encode()
    generated_oracle_mismatches = []
    canonical_oracle_mismatches = []
    canonical_generated_mismatches = []
    canonical_exceptions = []

    for label, x, n in cases:
        expected = exact_oracle(x, n)
        generated_outcome = outcome(generated, x, n)
        canonical_outcome = outcome(canonical, x, n)
        if generated_outcome != ("value", expected):
            generated_oracle_mismatches.append(
                (label, x, n, expected, generated_outcome)
            )
        if canonical_outcome != ("value", expected):
            canonical_oracle_mismatches.append(
                (label, x, n, expected, canonical_outcome)
            )
        if canonical_outcome != generated_outcome:
            canonical_generated_mismatches.append(
                (label, x, n, canonical_outcome, generated_outcome)
            )
        if canonical_outcome[0] == "exception":
            canonical_exceptions.append((label, x, n, canonical_outcome))

    invalid_cases = [
        ("empty-x", "", "1/1"),
        ("empty-n", "1/1", ""),
        ("zero-denominator", "1/0", "1/1"),
    ]

    print(f"valid_case_count={len(cases)}")
    print(f"valid_cases_sha256={hashlib.sha256(encoded_cases).hexdigest()}")
    print(f"generated_oracle_mismatches={len(generated_oracle_mismatches)}")
    print(f"canonical_oracle_mismatches={len(canonical_oracle_mismatches)}")
    print(f"canonical_generated_mismatches={len(canonical_generated_mismatches)}")
    print(f"canonical_exceptions={len(canonical_exceptions)}")
    print(
        "canonical_mismatch_samples="
        + json.dumps(canonical_oracle_mismatches[:10], separators=(",", ":"))
    )
    print("out_of_contract_diagnostics:")
    for label, x, n in invalid_cases:
        print(
            json.dumps(
                {
                    "label": label,
                    "x": x,
                    "n": n,
                    "canonical": outcome(canonical, x, n),
                    "generated": outcome(generated, x, n),
                },
                separators=(",", ":"),
            )
        )

    if generated_oracle_mismatches:
        print(
            "generated_mismatch_samples="
            + json.dumps(generated_oracle_mismatches[:10], separators=(",", ":"))
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
