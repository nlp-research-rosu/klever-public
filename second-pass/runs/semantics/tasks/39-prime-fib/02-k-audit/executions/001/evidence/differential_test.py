#!/usr/bin/env python3
"""Independent differential checks for HumanEval 39-prime-fib."""

from __future__ import annotations

import importlib.util
import math
import multiprocessing
import time
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/candidate/solution.py")
DOCUMENTED_INPUTS = [1, 2, 3, 4, 5]
GENERATED_POSITIVE_INPUTS = [6, 7, 8, 9, 10, 11]
OUTSIDE_INTENDED_INPUTS = [0, -1]
CACHED_PRIMES = [
    2,
    3,
    5,
    13,
    89,
    233,
    1597,
    28657,
    514229,
    433494437,
    2971215073,
]
CACHED_COMPOSITES = [
    17711,
    121393,
    1346269,
    5702887,
    165580141,
    1836311903,
]
HELPER_INPUTS = sorted(
    set(
        list(range(-10, 501))
        + CACHED_PRIMES
        + CACHED_COMPOSITES
        + [v - 1 for v in CACHED_PRIMES + CACHED_COMPOSITES]
        + [v + 1 for v in CACHED_PRIMES + CACHED_COMPOSITES]
    )
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_is_prime(value: int) -> bool:
    if value < 2:
        return False
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def run_in_child(path: str, n: int, queue) -> None:
    module = load(f"child_{n}_{Path(path).stem}", Path(path))
    queue.put(module.prime_fib(n))


def bounded_call(path: Path, n: int, timeout: float = 0.5):
    queue = multiprocessing.Queue()
    process = multiprocessing.Process(
        target=run_in_child, args=(str(path), n, queue)
    )
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        return ("timeout", None)
    if process.exitcode != 0:
        return ("error", process.exitcode)
    return ("returned", queue.get(timeout=0.1))


def main() -> int:
    canonical = load("trusted_canonical", CANONICAL_PATH)
    generated = load("submitted_generated", GENERATED_PATH)
    mismatches = []

    print("DOCUMENTED_AND_POSITIVE_DOMAIN")
    for n in DOCUMENTED_INPUTS + GENERATED_POSITIVE_INPUTS:
        start = time.monotonic()
        expected = canonical.prime_fib(n)
        actual = generated.prime_fib(n)
        elapsed = time.monotonic() - start
        print(
            f"n={n} canonical={expected} generated={actual} "
            f"match={expected == actual} elapsed={elapsed:.6f}s"
        )
        if expected != actual:
            mismatches.append(("prime_fib", n, expected, actual))

    print("OUTSIDE_INTENDED_POSITIVE_DOMAIN")
    for n in OUTSIDE_INTENDED_INPUTS:
        expected = bounded_call(CANONICAL_PATH, n)
        actual = bounded_call(GENERATED_PATH, n)
        print(f"n={n} canonical={expected} generated={actual} match={expected == actual}")

    helper_mismatches = []
    for value in HELPER_INPUTS:
        expected = independent_is_prime(value)
        actual = generated._is_prime(value)
        if expected != actual:
            helper_mismatches.append((value, expected, actual))
    print(
        "HELPER_SCOPE "
        f"count={len(HELPER_INPUTS)} min={min(HELPER_INPUTS)} "
        f"max={max(HELPER_INPUTS)} cache_primes={CACHED_PRIMES} "
        f"cache_composites={CACHED_COMPOSITES}"
    )
    print(f"HELPER_MISMATCHES count={len(helper_mismatches)} values={helper_mismatches}")
    mismatches.extend(("is_prime",) + item for item in helper_mismatches)
    print(f"TOTAL_MISMATCHES={len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
