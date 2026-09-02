#!/usr/bin/env python3
"""Independent differential testing of canonical.py and the candidate program."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_module(
        "scratch_generated", Path("/tmp/audit-work/candidate/solution.py")
    )

    # The prompt has no explicit input/output examples. These cases cover the
    # empty traversal, both modulo wrap boundaries, all single characters, all
    # pairs, and all triples over the alphabet (18,279 strings).
    cases = ["", "a", "e", "f", "z", "abc", "xyz", "helloworld"]
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for length in range(1, 4):
        cases.extend("".join(chars) for chars in itertools.product(alphabet, repeat=length))

    rng = random.Random(50050)
    cases.extend(
        "".join(rng.choice(alphabet) for _ in range(length))
        for length in (4, 5, 8, 16, 31, 64, 127)
        for _ in range(100)
    )
    cases.append(alphabet)
    cases.append(alphabet[::-1])

    mismatches = []
    inverse_failures = []
    for value in cases:
        expected = canonical.decode_shift(value)
        actual = generated.decode_shift(value)
        if actual != expected:
            mismatches.append((value, expected, actual))
        if generated.decode_shift(canonical.encode_shift(value)) != value:
            inverse_failures.append(value)

    print(f"case_count={len(cases)}")
    print(f"unique_case_count={len(set(cases))}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"inverse_failure_count={len(inverse_failures)}")
    print(
        "boundary_results="
        + repr(
            {
                value: generated.decode_shift(value)
                for value in ("", "a", "e", "f", "z", "abc", "xyz")
            }
        )
    )
    if mismatches:
        print(f"first_mismatch={mismatches[0]!r}")
    if inverse_failures:
        print(f"first_inverse_failure={inverse_failures[0]!r}")
    assert not mismatches
    assert not inverse_failures
    print("DIFFERENTIAL_TEST=PASS")


if __name__ == "__main__":
    main()
