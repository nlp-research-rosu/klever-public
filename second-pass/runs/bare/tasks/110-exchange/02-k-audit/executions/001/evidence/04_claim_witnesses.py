#!/usr/bin/env python3
"""Ground witnesses for the three reachability-claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Callable


def load_exchange(path: Path, name: str) -> Callable[[list[int], list[int]], str]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


def count_even(values: list[int]) -> int:
    return sum(value % 2 == 0 for value in values)


def last_value(values: list[int], default: int) -> int:
    return values[-1] if values else default


def show_entry(
    label: str,
    left: list[int],
    right: list[int],
    oracle: Callable[[list[int], list[int]], str],
    candidate: Callable[[list[int], list[int]], str],
) -> None:
    total = count_even(left) + count_even(right)
    boundary = len(left)
    final_value = last_value(right, last_value(left, 0))
    print(f"CLAIM: {label}")
    print(f"L1={left!r}")
    print(f"L2={right!r}")
    print(f"countEven(L1)+countEven(L2)={total}")
    print(f"length(L1)={boundary}")
    print(f"yes_precondition={total >= boundary}")
    print(f"no_precondition={total < boundary}")
    print(f"claimed_final_even={total}")
    print(f"claimed_final_value={final_value}")
    print(f"canonical_result={oracle(list(left), list(right))!r}")
    print(f"candidate_result={candidate(list(left), list(right))!r}")
    print("---")


def main() -> None:
    oracle = load_exchange(Path("/reference/canonical.py"), "witness_oracle")
    candidate = load_exchange(
        Path("/tmp/audit-work/110-exchange/solution.py"), "witness_candidate"
    )

    # Satisfies exchange-yes and the prompt's non-empty-list assumption.
    show_entry("exchange-yes", [0], [1], oracle, candidate)

    # Satisfies exchange-no and the prompt's non-empty-list assumption.
    show_entry("exchange-no", [-4, -3, -2, -1], [-8, -7], oracle, candidate)

    # A complete ground instance of the loop claim's implicit precondition.
    loop_list = [2, 1]
    initial_even = 5
    old_value = 9
    print("CLAIM: loop-counts-even")
    print("L=Cons(2, Cons(1, Nil)); N=5; OLD=9; CONT=.K")
    print('env={"lst1": Nil, "lst2": Nil, "even": 5, "value": 9}')
    print("result=noResult")
    print(f"claimed_final_even={initial_even + count_even(loop_list)}")
    print(f"claimed_final_value={last_value(loop_list, old_value)}")


if __name__ == "__main__":
    main()
