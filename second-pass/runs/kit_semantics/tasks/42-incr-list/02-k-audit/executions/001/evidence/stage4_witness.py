#!/usr/bin/env python3
"""Ground substitutions for the entry theorem's INPUT and incrAcc result."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Callable


def load_entry(path: Path, name: str) -> Callable[[list[int]], list[int]]:
    module_spec = importlib.util.spec_from_file_location(name, path)
    assert module_spec is not None and module_spec.loader is not None
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.incr_list


def val_seq(values: list[int]) -> str:
    term = ".ValSeq"
    for value in reversed(values):
        term = f"vCons({value}, {term})"
    return term


def incr_acc(accumulator: list[int], remaining: list[int]) -> list[int]:
    # Ground Int instance of verification.k's structurally recursive equations:
    # incrAcc(ACC, vCons(V,R)) = incrAcc(valSeqConcat(ACC,[V+1]),R).
    result = list(accumulator)
    for value in remaining:
        result = result + [value + 1]
    return result


def main() -> None:
    canonical = load_entry(Path("/reference/canonical.py"), "stage4_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/42-incr-list-audit/solution.py"),
        "stage4_generated",
    )
    inputs = [
        [],
        [0],
        [-1, 0, 1],
        [1, 2, 3],
        [5, 3, 5, 2, 3, 3, 9, 0, 123],
    ]
    for index, input_value in enumerate(inputs):
        summary = incr_acc([], input_value)
        canonical_result = canonical(list(input_value))
        generated_result = generated(list(input_value))
        assert summary == canonical_result == generated_result
        print(f"witness_{index}_pre_heap=0 |-> list({val_seq(input_value)})")
        print("witness_%d_pre_allNumeric=true" % index)
        print(f"witness_{index}_claimed_result_heap=1 |-> list({val_seq(summary)})")
        print(f"witness_{index}_python_result={generated_result!r}")
    print("STAGE4_WITNESSES_OK")


if __name__ == "__main__":
    main()
