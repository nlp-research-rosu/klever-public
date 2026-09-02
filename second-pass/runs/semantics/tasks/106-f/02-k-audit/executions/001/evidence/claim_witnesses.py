#!/usr/bin/env python3
"""Ground witnesses for the K claims and their outputOK postcondition."""

import importlib.util
import math
from pathlib import Path


def load_f(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


def output_ok(sequence, i, n, factorial_before, total_before):
    cursor = 0
    factorial = factorial_before
    total = total_before
    while i <= n:
        factorial *= i
        total += i
        if cursor >= len(sequence):
            return False
        expected = factorial if i % 2 == 0 else total
        if sequence[cursor] != expected:
            return False
        cursor += 1
        i += 1
    return cursor == len(sequence)


def main():
    scratch = Path("/tmp/audit-work/fresh")
    canonical = load_f("canonical_witness", scratch / "canonical.py")
    candidate = load_f("candidate_witness", scratch / "solution.py")

    # loop-correct witness:
    # N=5, I=1, F=1, T=0, PREFIX=[99], MODULE=.Map, heap 0=list([99]).
    # It satisfies 1 <= I <= N+1 and the required cells are all concrete.
    n, i, factorial_before, total_before = 5, 1, 1, 0
    prefix = [99]
    suffix = [1, 2, 6, 24, 15]
    print(
        "LOOP_WITNESS:",
        {
            "N": n,
            "I": i,
            "F": factorial_before,
            "T": total_before,
            "PREFIX": prefix,
            "MODULE": {},
        },
    )
    print("LOOP_PRECONDITION:", 1 <= i <= n + 1)
    print("LOOP_POST_OUTPUT_OK:", output_ok(suffix, i, n, factorial_before, total_before))
    print("LOOP_FINAL_HEAP_LIST:", prefix + suffix)
    print("LOOP_FINAL_I:", n + 1)
    print("LOOP_FINAL_FACTORIAL:", math.factorial(n))
    print("LOOP_FINAL_TOTAL:", n * (n + 1) // 2)

    # f-symbolic entry witness: choose N=5; all explicitly pinned initial
    # cells are the literals shown in spec.k, and N >= 0.
    print("F_SYMBOLIC_WITNESS_N:", n)
    print("F_SYMBOLIC_PRECONDITION:", n >= 0)
    print("F_SYMBOLIC_POST_OUTPUT_OK:", output_ok(suffix, 1, n, 1, 0))
    print("TRUSTED_CANONICAL_F5:", canonical(n))
    print("CANDIDATE_F5:", candidate(n))
    print("CLAIM_SUFFIX_F5:", suffix)

    # f-zero and f-five have requires true and the concrete configurations
    # shown in spec.k, so their pinned configurations are satisfying states.
    print("F_ZERO_PRECONDITION:", True)
    print("F_ZERO_EXPECTED:", [])
    print("F_ZERO_CANONICAL:", canonical(0))
    print("F_ZERO_CANDIDATE:", candidate(0))
    print("F_FIVE_PRECONDITION:", True)
    print("F_FIVE_EXPECTED:", suffix)
    print("F_FIVE_CANONICAL:", canonical(5))
    print("F_FIVE_CANDIDATE:", candidate(5))

    checks = [
        output_ok(suffix, 1, 5, 1, 0),
        canonical(5) == suffix,
        candidate(5) == suffix,
        canonical(0) == [],
        candidate(0) == [],
    ]
    print("ALL_WITNESS_CHECKS:", all(checks))
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
