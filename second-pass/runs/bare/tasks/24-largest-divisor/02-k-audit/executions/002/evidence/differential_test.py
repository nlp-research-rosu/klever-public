#!/usr/bin/env python3
"""Differential test of trusted canonical.py against candidate solution.py."""

from __future__ import annotations

import importlib.util
import multiprocessing as mp
from pathlib import Path
from typing import Any


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/src/solution.py")


def outcome(path: Path, module_name: str, n: int) -> tuple[str, Any]:
    try:
        value = load(path, module_name).largest_divisor(n)
        return ("return", value)
    except BaseException as err:  # Deliberately compare observable exceptions.
        return ("raise", type(err).__name__)


def worker(path: str, module_name: str, n: int, queue: mp.Queue) -> None:
    queue.put(outcome(Path(path), module_name, n))


def timed_outcome(path: Path, module_name: str, n: int) -> tuple[str, Any]:
    queue: mp.Queue = mp.Queue()
    proc = mp.Process(target=worker, args=(str(path), module_name, n, queue))
    proc.start()
    proc.join(0.25)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        return ("timeout", None)
    return queue.get() if not queue.empty() else ("exit", proc.exitcode)


documented_and_boundaries = [15, 2, 3, 4, 5, 6, 8, 9, 16, 25, 49, 101]
mismatches: list[tuple[int, tuple[str, Any], tuple[str, Any]]] = []

print("DOCUMENTED_AND_BRANCH_BOUNDARIES")
for n in documented_and_boundaries:
    expected = outcome(CANONICAL_PATH, f"canonical_{n}", n)
    actual = outcome(CANDIDATE_PATH, f"candidate_{n}", n)
    print(f"n={n} canonical={expected!r} candidate={actual!r}")
    if expected != actual:
        mismatches.append((n, expected, actual))

for n in range(2, 2001):
    expected = outcome(CANONICAL_PATH, f"canonical_sweep_{n}", n)
    actual = outcome(CANDIDATE_PATH, f"candidate_sweep_{n}", n)
    if expected != actual:
        mismatches.append((n, expected, actual))

print(f"POSITIVE_SWEEP range=2..2000 mismatches={len(mismatches)}")

print("OUTSIDE_FORMAL_PRECONDITION")
outside_mismatches = 0
for n in [1, 0, -1, -2]:
    expected = timed_outcome(CANONICAL_PATH, f"canonical_outside_{n}", n)
    actual = timed_outcome(CANDIDATE_PATH, f"candidate_outside_{n}", n)
    mismatch = expected != actual
    outside_mismatches += int(mismatch)
    print(
        f"n={n} canonical={expected!r} candidate={actual!r} mismatch={mismatch}"
    )

print(f"FORMAL_DOMAIN_MISMATCHES={len(mismatches)}")
print(f"OUTSIDE_FORMAL_DOMAIN_MISMATCHES={outside_mismatches}")
raise SystemExit(1 if mismatches else 0)
