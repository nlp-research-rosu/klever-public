#!/usr/bin/env python3
"""Concrete satisfying witnesses for each symbolic entry claim."""

from __future__ import annotations

import importlib.util
import sys


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 3:
        return 2
    canonical = load(sys.argv[1], "canonical_witness")
    candidate = load(sys.argv[2], "candidate_witness")
    witnesses = [
        ("need<=remaining", (5, 6, 10), [5 + 6, 10 - 6]),
        ("remaining<need", (2, 11, 5), [2 + 5, 0]),
    ]
    for branch, case, claimed in witnesses:
        oracle = canonical.eat(*case)
        actual = candidate.eat(*case)
        if oracle != claimed or actual != claimed:
            raise AssertionError((branch, case, oracle, actual, claimed))
        print(
            f"branch={branch} input={case} "
            f"precondition_satisfied=true canonical={oracle} "
            f"candidate={actual} claimed_heap_list={claimed}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
