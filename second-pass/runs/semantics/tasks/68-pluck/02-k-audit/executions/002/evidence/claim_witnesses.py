#!/usr/bin/env python3
"""Concrete satisfying states and substitutions for both formal claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_pluck(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pluck


def val_seq(values: list[int]) -> str:
    result = ".ValSeq"
    for value in reversed(values):
        result = f"vCons({value}, {result})"
    return result


def scan_pluck(
    values: list[int], best: int, best_index: int, index: int, last: int
) -> tuple[int, int, int, int]:
    for value in values:
        if value % 2 == 0 and (best == -1 or value < best):
            best = value
            best_index = index
        index += 1
        last = value
    return best, best_index, index, last


def result_seq(values: list[int]) -> str:
    best, best_index, _, _ = scan_pluck(values, -1, -1, 0, 0)
    return ".ValSeq" if best == -1 else val_seq([best, best_index])


def main() -> None:
    canonical = load_pluck(Path("/reference/canonical.py"), "canonical_witness")
    candidate = load_pluck(Path("/candidate/solution.py"), "candidate_witness")
    entry_inputs = [[], [4, 2, 3], [5, 0, 3, 0, 4, 2], [7, 5, 9]]
    for values in entry_inputs:
        precondition = all(isinstance(value, int) and value >= 0 for value in values)
        expected = result_seq(values)
        canonical_result = canonical(list(values))
        candidate_result = candidate(list(values))
        python_as_seq = val_seq(candidate_result)
        print(
            f"ENTRY values={values} VS={val_seq(values)} "
            f"allNonNegative={str(precondition).lower()} "
            f"pluckResult={expected} canonical={canonical_result} "
            f"candidate={candidate_result} python_result_seq={python_as_seq} "
            f"agree={expected == python_as_seq and canonical_result == candidate_result}"
        )
        if not precondition or expected != python_as_seq or canonical_result != candidate_result:
            raise SystemExit(1)

    loop_values = [4, 2, 3]
    loop_initial = (-1, -1, 0, 0)
    loop_final = scan_pluck(loop_values, *loop_initial)
    print(
        "LOOP satisfying_state="
        f"VS:{val_seq(loop_values)} B:{loop_initial[0]} BI:{loop_initial[1]} "
        f"I:{loop_initial[2]} LAST:{loop_initial[3]} "
        "L:1 ARR:ref(7) P:parent(0) K:.K "
        "allNonNegative=true"
    )
    print(
        "LOOP substituted_summary="
        f"pstate({loop_final[0]}, {loop_final[1]}, "
        f"{loop_final[2]}, {loop_final[3]})"
    )
    print("CLAIM_WITNESSES=PASS")


if __name__ == "__main__":
    main()
