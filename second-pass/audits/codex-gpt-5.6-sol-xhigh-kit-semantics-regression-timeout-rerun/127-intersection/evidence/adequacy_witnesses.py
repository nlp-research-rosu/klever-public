#!/usr/bin/env python3
"""Concrete witnesses for every candidate claim precondition."""

import importlib.util
import json


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def overlap_length(a, b, c, d):
    return min(b, d) - max(a, c)


def scan_prime_by_loop(length, divisor, prime):
    while divisor < length:
        if length % divisor == 0:
            prime = False
        divisor += 1
    return divisor, prime


def entry_witness(label, first, second, expected_summary):
    a, b = first
    c, d = second
    length = overlap_length(a, b, c, d)
    final_divisor, summary = scan_prime_by_loop(length, 2, length > 1)
    return {
        "claim": label,
        "interval1": first,
        "interval2": second,
        "A_le_B": a <= b,
        "C_le_D": c <= d,
        "overlapLength": length,
        "scanPrime": summary,
        "expected_scanPrime": expected_summary,
        "loop_final_divisor": final_divisor,
    }


def main():
    canonical = load_module("trusted_canonical", "/reference/canonical.py")
    candidate = load_module(
        "scratch_generated_solution", "/tmp/audit-work/scratch/solution.py"
    )

    loop_divisor, loop_prime = scan_prime_by_loop(4, 2, True)
    loop_witness = {
        "claim": "divisor-loop",
        "N": 4,
        "I": 2,
        "P": True,
        "requires_I_ge_2": True,
        "post_divisor": loop_divisor,
        "expected_maxInt_I_N": max(2, 4),
        "post_prime": loop_prime,
        "expected_scanPrime": False,
        "realized_by": [[0, 4], [0, 4]],
    }

    entry_witnesses = [
        entry_witness(
            "intersection-prime",
            (-3, -1),
            (-5, 5),
            True,
        ),
        entry_witness(
            "intersection-not-prime",
            (0, 4),
            (0, 4),
            False,
        ),
    ]
    for witness in entry_witnesses:
        first = tuple(witness["interval1"])
        second = tuple(witness["interval2"])
        witness["canonical_result"] = canonical.intersection(first, second)
        witness["candidate_result"] = candidate.intersection(first, second)
        witness["formal_postcondition"] = (
            "YES" if witness["scanPrime"] else "NO"
        )

    if (
        loop_witness["post_divisor"] != loop_witness["expected_maxInt_I_N"]
        or loop_witness["post_prime"] != loop_witness["expected_scanPrime"]
    ):
        raise SystemExit("loop witness failed")

    for witness in entry_witnesses:
        if not (witness["A_le_B"] and witness["C_le_D"]):
            raise SystemExit("entry domain witness is malformed")
        if witness["scanPrime"] != witness["expected_scanPrime"]:
            raise SystemExit("entry summary precondition mismatch")
        if witness["canonical_result"] != witness["formal_postcondition"]:
            raise SystemExit("canonical/postcondition mismatch")
        if witness["candidate_result"] != witness["formal_postcondition"]:
            raise SystemExit("candidate/postcondition mismatch")

    print(json.dumps(loop_witness, sort_keys=True))
    for witness in entry_witnesses:
        print(json.dumps(witness, sort_keys=True))
    print("ADEQUACY_WITNESSES=PASS")


if __name__ == "__main__":
    main()
