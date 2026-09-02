#!/usr/bin/env python3
"""Independent canonical/candidate differential and helper-boundary checks."""

from __future__ import annotations

import importlib.util
import math
import multiprocessing as mp
import random
from pathlib import Path

WORK = Path("/tmp/audit-work/prime-fib-audit")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", WORK / "canonical.py")
candidate = load("generated_candidate", WORK / "solution.py")


def oracle_prime(value: int) -> bool:
    if value < 2:
        return False
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def invoke(queue, which: str, n: int) -> None:
    try:
        func = canonical.prime_fib if which == "canonical" else candidate.prime_fib
        queue.put(("return", func(n)))
    except BaseException as err:  # evidence should record unexpected behavior
        queue.put(("exception", f"{type(err).__name__}: {err}"))


def timed_call(which: str, n: int, timeout: float):
    ctx = mp.get_context("fork")
    queue = ctx.Queue()
    process = ctx.Process(target=invoke, args=(queue, which, n))
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join()
        return ("timeout", None)
    if queue.empty():
        return ("no-result", process.exitcode)
    return queue.get()


entry_mismatches = 0
documented = {1: 2, 2: 3, 3: 5, 4: 13, 5: 89}
print(f"documented examples={documented}")

# The natural source domain is positive integers. Values 1..12 include all
# examples, every result claim, both outer-loop boundary directions, and one
# positive input beyond the submitted theorem.
for n in range(1, 13):
    timeout = 120.0 if n == 12 else 15.0
    can_result = timed_call("canonical", n, timeout)
    cand_result = timed_call("candidate", n, timeout)
    match = can_result == cand_result
    if n in documented:
        match = match and cand_result == ("return", documented[n])
    entry_mismatches += int(not match)
    print(
        f"ENTRY n={n} canonical={can_result} candidate={cand_result} "
        f"match={match}"
    )

# These are explicit boundary observations outside the positive-input
# contract: the canonical search does not terminate, while the rewrite does.
for n in (-1, 0):
    can_result = timed_call("canonical", n, 0.5)
    cand_result = timed_call("candidate", n, 0.5)
    print(
        f"OUTSIDE-DOMAIN n={n} canonical={can_result} "
        f"candidate={cand_result} same_behavior={can_result == cand_result}"
    )

helper_values = {
    *range(-5, 101),
    121,
    169,
    17711,
    121393,
    1346269,
    5702887,
    165580141,
    1836311903,
    233,
    1597,
    28657,
    514229,
    433494437,
    2971215073,
}
random.seed(39039)
helper_values.update(random.randrange(-100, 1_000_001) for _ in range(300))
helper_mismatches = []
for value in sorted(helper_values):
    actual = candidate._is_prime(value)
    expected = oracle_prime(value)
    if actual != expected:
        helper_mismatches.append((value, expected, actual))
print(
    f"HELPER tested={len(helper_values)} range=-100..1000000 plus "
    "all cache entries and branch boundaries"
)
print(f"HELPER mismatches={helper_mismatches}")
print(f"ENTRY mismatch_count={entry_mismatches}")
print(f"TOTAL mismatch_count={entry_mismatches + len(helper_mismatches)}")

raise SystemExit(1 if entry_mismatches or helper_mismatches else 0)
