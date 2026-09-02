#!/usr/bin/env python3
"""Concrete satisfying states for both reachability-claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.f


def expected_completion(
    i: int, n: int, factorial: int, total: int, prefix: list[int]
) -> list[int]:
    output = list(prefix)
    while i <= n:
        factorial *= i
        total += i
        output.append(factorial if i % 2 == 0 else total)
        i += 1
    return output


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "witness_canonical")
    candidate = load_entry(
        Path("/tmp/audit-work/reconstruction/solution.py"),
        "witness_candidate",
    )

    main_n = 5
    main_precondition = main_n >= 0
    main_expected = expected_completion(1, main_n, 1, 0, [])
    print(
        "main witness: <input> 5 </input>, <env> .Map </env>, "
        "<result> noResult </result>"
    )
    print(f"main precondition N >= 0: {main_precondition}")
    print(
        f"main substituted expected(5)={main_expected} "
        f"canonical={canonical(main_n)} candidate={candidate(main_n)}"
    )

    loop_n = 5
    loop_i = 3
    loop_factorial = 2
    loop_total = 3
    loop_prefix = [1, 2]
    loop_precondition = loop_n >= 0 and loop_i >= 1
    loop_expected = expected_completion(
        loop_i,
        loop_n,
        loop_factorial,
        loop_total,
        loop_prefix,
    )
    print(
        "loop witness: N=5, I=3, F=2, T=3, L=[1,2], "
        "the reachable state after iterations 1 and 2"
    )
    print(f"loop precondition N >= 0 and I >= 1: {loop_precondition}")
    print(
        "loop substituted expectedCompletion(3,5,2,3,[1,2])="
        f"{loop_expected} canonical={canonical(loop_n)} "
        f"candidate={candidate(loop_n)}"
    )

    conditions = [
        main_precondition,
        loop_precondition,
        main_expected == canonical(main_n) == candidate(main_n),
        loop_expected == canonical(loop_n) == candidate(loop_n),
    ]
    status = 0 if all(conditions) else 1
    print(f"CLAIM_WITNESS_STATUS={status}")
    return status


if __name__ == "__main__":
    sys.exit(main())
