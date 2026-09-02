#!/usr/bin/env python3
"""Independent differential test for HumanEval 139.

The oracle and candidate modules are loaded from explicit paths and share no
implementation code. Large integers are summarized without decimal conversion.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import random
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def summarize_integer(value: int) -> str:
    if -10**18 <= value <= 10**18:
        return repr(value)
    magnitude = abs(value)
    raw = magnitude.to_bytes((magnitude.bit_length() + 7) // 8, "big")
    digest = hashlib.sha256(raw).hexdigest()[:20]
    sign = "-" if value < 0 else "+"
    return f"Int(sign={sign},bits={magnitude.bit_length()},sha256={digest})"


def evaluate(function: Callable[[int], int], n: int) -> tuple[str, object]:
    try:
        value = function(n)
    except Exception as err:  # Deliberately record observable divergence.
        return ("exception", type(err).__name__)
    if not isinstance(value, int):
        return ("non_int", type(value).__name__)
    return ("value", value)


def printable(outcome: tuple[str, object]) -> str:
    kind, payload = outcome
    if kind == "value":
        return summarize_integer(payload)  # type: ignore[arg-type]
    return f"{kind}({payload})"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module("trusted_canonical_139", args.canonical)
    candidate = load_module("audited_candidate_139", args.candidate)
    oracle = canonical.special_factorial
    generated = candidate.special_factorial

    rng = random.Random(139)
    groups = [
        ("documented_example", [4]),
        ("empty_product_and_branch_boundaries", [-1, 0, 1, 2]),
        ("small_positive_exhaustive", list(range(1, 26))),
        ("representative_generated", [rng.randint(1, 40) for _ in range(32)]),
        ("positive_resource_boundary", [1000]),
    ]

    mismatch_count = 0
    case_count = 0
    print(f"python={sys.version.split()[0]} recursion_limit={sys.getrecursionlimit()}")
    print("formal intended domain from prompt: integer n > 0")
    print("note: -1 and 0 are explicit out-of-contract empty-product probes")
    for group_name, inputs in groups:
        print(f"GROUP {group_name} inputs={inputs}")
        for n in inputs:
            expected = evaluate(oracle, n)
            actual = evaluate(generated, n)
            same = (
                expected[0] == actual[0]
                and (
                    expected[1] == actual[1]
                    if expected[0] != "value"
                    else expected[1] == actual[1]
                )
            )
            case_count += 1
            mismatch_count += int(not same)
            marker = "MATCH" if same else "MISMATCH"
            print(
                f"{marker} n={n} canonical={printable(expected)} "
                f"candidate={printable(actual)}"
            )

    # The helper is not the required entry point, but these probes ensure both
    # sides of its <= 1 branch and its recursive branch are exercised.
    helper = candidate.factorial
    helper_cases = [(0, 1), (1, 1), (2, 2), (5, 120)]
    print(f"GROUP candidate_helper_boundaries inputs={[n for n, _ in helper_cases]}")
    for n, expected in helper_cases:
        actual = evaluate(helper, n)
        same = actual == ("value", expected)
        case_count += 1
        mismatch_count += int(not same)
        marker = "MATCH" if same else "MISMATCH"
        print(
            f"{marker} factorial({n}) expected={expected} "
            f"candidate={printable(actual)}"
        )

    print(f"SUMMARY cases={case_count} mismatches={mismatch_count}")
    return 1 if mismatch_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
