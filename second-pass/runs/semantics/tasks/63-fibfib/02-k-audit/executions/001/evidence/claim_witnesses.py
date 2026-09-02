#!/usr/bin/env python3
"""Concrete witnesses for the main and loop claims."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def shift(a: int, b: int, c: int, count: int) -> tuple[int, int, int]:
    for _ in range(count):
        a, b, c = b, c, a + b + c
    return a, b, c


def run_remaining(
    a: int, b: int, c: int, d: int, i: int, n: int
) -> tuple[int, int, int, int, int]:
    while i < n:
        d = a + b + c
        a = b
        b = c
        c = d
        i += 1
    return a, b, c, d, i


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL SOLUTION")
        return 64
    canonical = load("witness_canonical", Path(sys.argv[1]))
    solution = load("witness_solution", Path(sys.argv[2]))

    entry_rows = []
    for n in (0, 1, 2, 3, 5, 8):
        summary = shift(0, 0, 1, n)[0]
        entry_rows.append(
            {
                "N": n,
                "precondition_N_ge_0": n >= 0,
                "claimed_fibFrom": summary,
                "trusted_python": canonical.fibfib(n),
                "candidate_python": solution.fibfib(n),
            }
        )

    # This is the actual state after two iterations of solution.py for n = 5.
    n, i = 5, 2
    a, b, c = shift(0, 0, 1, i)
    d = 2
    remaining_summary = shift(a, b, c, n - i)[0]
    final_state = run_remaining(a, b, c, d, i, n)
    loop_witness = {
        "cells": {
            "env": 1,
            "a": a,
            "b": b,
            "c": c,
            "d": d,
            "i": i,
            "n": n,
            "parent": "parent(0)",
        },
        "precondition_0_le_I_le_N": 0 <= i <= n,
        "claimed_final_a_fibFrom_A_B_C_N_minus_I": remaining_summary,
        "actual_remaining_loop_final": {
            "a": final_state[0],
            "b": final_state[1],
            "c": final_state[2],
            "d": final_state[3],
            "i": final_state[4],
        },
        "trusted_python_n_5": canonical.fibfib(n),
        "candidate_python_n_5": solution.fibfib(n),
    }

    print(json.dumps({"entry_witnesses": entry_rows, "loop_witness": loop_witness}, indent=2))
    entry_matches = all(
        row["claimed_fibFrom"]
        == row["trusted_python"]
        == row["candidate_python"]
        for row in entry_rows
    )
    return 0 if entry_matches and remaining_summary == final_state[0] else 1


if __name__ == "__main__":
    raise SystemExit(main())
