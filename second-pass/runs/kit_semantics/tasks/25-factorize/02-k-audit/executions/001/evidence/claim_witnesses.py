#!/usr/bin/env python3
"""Ground evaluation of the claim's factorAcc postcondition."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def factor_acc(accumulator: list[int], n: int, divisor: int) -> list[int]:
    result = list(accumulator)
    while True:
        if n < divisor:
            return result
        if n % divisor == 0:
            result.append(divisor)
            n = n // divisor
        else:
            divisor += 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", required=True)
    parser.add_argument("--generated", required=True)
    args = parser.parse_args()
    canonical = load_module("witness_canonical", Path(args.canonical))
    generated = load_module("witness_generated", Path(args.generated))

    print(
        "factor_loop_satisfying_state="
        "N=1,D=2,A=.ValSeq,env=1,heap[0]=list(.ValSeq),NoExc"
    )
    print(
        "factorize_satisfying_state="
        "N=8,env=0,exact closure binding,empty heap,NoExc"
    )
    for value in [1, 2, 8, 25, 70, 97]:
        claimed = factor_acc([], value, 2)
        trusted = canonical.factorize(value)
        actual = generated.factorize(value)
        print(
            f"N={value} claimed_factorAcc={claimed} "
            f"canonical={trusted} generated={actual} "
            f"all_equal={claimed == trusted == actual}"
        )
        assert claimed == trusted == actual
    helper_claimed = factor_acc([11], 8, 2)
    print(
        "helper_nonempty_accumulator="
        f"A=[11],N=8,D=2 claimed_factorAcc={helper_claimed}"
    )
    assert helper_claimed == [11, 2, 2, 2]


if __name__ == "__main__":
    main()
