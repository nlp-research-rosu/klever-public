#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval/39."""

from __future__ import annotations

import importlib.util
import multiprocessing as mp
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/39-prime-fib/src")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load("audit_candidate_solution", ROOT / "solution.py")
canonical = load("audit_trusted_canonical", ROOT / "trusted-canonical.py")


def traced_candidate(n: int) -> tuple[int, list[int]]:
    visited: set[int] = set()
    target = str((ROOT / "solution.py").resolve())

    def tracer(frame, event, arg):
        if event == "line" and frame.f_code.co_filename == target:
            visited.add(frame.f_lineno)
        return tracer

    sys.settrace(tracer)
    try:
        value = candidate.prime_fib(n)
    finally:
        sys.settrace(None)
    return value, sorted(visited)


def canonical_worker(n: int, queue: mp.Queue) -> None:
    queue.put(canonical.prime_fib(n))


def bounded_canonical(n: int, timeout_s: float = 0.25):
    queue: mp.Queue = mp.Queue()
    process = mp.Process(target=canonical_worker, args=(n, queue))
    process.start()
    process.join(timeout_s)
    if process.is_alive():
        process.terminate()
        process.join()
        return "TIMEOUT_NONTERMINATING"
    if process.exitcode != 0:
        return f"CHILD_EXIT_{process.exitcode}"
    return queue.get()


def main() -> None:
    examples = {1: 2, 2: 3, 3: 5, 4: 13, 5: 89}
    generated = list(range(6, 11))
    compared = list(examples) + generated
    mismatches: list[tuple[int, int, int]] = []

    print("INTENDED_DOMAIN positive integers n >= 1")
    print("EMPTY_CASE not applicable: scalar integer input")
    print(f"COMPARED_INPUTS {compared}")
    for n in compared:
        got, lines = traced_candidate(n)
        want = canonical.prime_fib(n)
        print(f"n={n} candidate={got} canonical={want} candidate_lines={lines}")
        if n in examples:
            assert want == examples[n], (n, want, examples[n])
        if got != want:
            mismatches.append((n, got, want))

    # Candidate line witnesses:
    # 11/12: b < 2 true; 13: divisor loop guard; 14/15: divisible true;
    # 16: divisor increment (also witnesses non-divisor fall-through);
    # 17/18: prime branch true; 19: outer-loop false boundary and return.
    for n, required in {
        1: {11, 12, 13, 17, 18, 19},
        3: {13, 14, 16, 17, 18, 19},
        4: {13, 14, 15, 16, 17, 18, 19},
    }.items():
        _, lines = traced_candidate(n)
        missing = required.difference(lines)
        assert not missing, (n, sorted(missing), lines)
        print(f"BRANCH_WITNESS n={n} required_lines={sorted(required)} PASS")

    # n <= 0 is outside the intended positive-index domain. Both return 1 for
    # zero; for a negative input, the generated implementation returns
    # immediately while the canonical loop keeps decrementing away from zero.
    got_zero = candidate.prime_fib(0)
    want_zero = bounded_canonical(0)
    print(f"OUT_OF_DOMAIN n=0 candidate={got_zero} canonical={want_zero}")
    assert got_zero == want_zero == 1

    got_negative = candidate.prime_fib(-1)
    want_negative = bounded_canonical(-1)
    print(
        "OUT_OF_DOMAIN "
        f"n=-1 candidate={got_negative} canonical={want_negative}"
    )
    assert got_negative == 1
    assert want_negative == "TIMEOUT_NONTERMINATING"

    print(f"MISMATCHES {len(mismatches)}")
    assert not mismatches, mismatches


if __name__ == "__main__":
    main()
