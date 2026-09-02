#!/usr/bin/env python3
"""Ground witnesses for every formal precondition and claimed result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/110-exchange")


def load_exchange(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.exchange


canonical = load_exchange("witness_canonical", ROOT / "trusted/canonical.py")
generated = load_exchange("witness_generated", ROOT / "candidate/solution.py")


def count_even(values: list[int]) -> int:
    return sum(1 for value in values if value % 2 == 0)


def last_value(values: list[int], default: int) -> int:
    return values[-1] if values else default


# loop-counts-even precondition witness:
# L=[2,3], L1=[1], L2=[2], N=7, OLD=9, CONT=.K, result=noResult.
loop_l = [2, 3]
loop_n = 7
loop_old = 9
loop_final_even = loop_n + count_even(loop_l)
loop_final_value = last_value(loop_l, loop_old)
assert loop_final_even == 8
assert loop_final_value == 3
print(
    "LOOP_WITNESS "
    "L=[2,3] L1=[1] L2=[2] N=7 OLD=9 CONT=.K result=noResult "
    f"post_even={loop_final_even} post_value={loop_final_value}"
)

# exchange-yes precondition witness: 1 total even >= length 1.
yes_l1 = [1]
yes_l2 = [2]
yes_count = count_even(yes_l1) + count_even(yes_l2)
assert yes_count >= len(yes_l1)
yes_canonical = canonical(yes_l1, yes_l2)
yes_generated = generated(yes_l1, yes_l2)
assert yes_canonical == yes_generated == "YES"
print(
    f"YES_WITNESS L1={yes_l1} L2={yes_l2} "
    f"countEvenSum={yes_count} lengthL1={len(yes_l1)} "
    f"canonical={yes_canonical} generated={yes_generated} "
    f"post_even={yes_count} post_value={last_value(yes_l2, last_value(yes_l1, 0))}"
)

# exchange-no precondition witness: 0 total even < length 1.
no_l1 = [1]
no_l2 = [3]
no_count = count_even(no_l1) + count_even(no_l2)
assert no_count < len(no_l1)
no_canonical = canonical(no_l1, no_l2)
no_generated = generated(no_l1, no_l2)
assert no_canonical == no_generated == "NO"
print(
    f"NO_WITNESS L1={no_l1} L2={no_l2} "
    f"countEvenSum={no_count} lengthL1={len(no_l1)} "
    f"canonical={no_canonical} generated={no_generated} "
    f"post_even={no_count} post_value={last_value(no_l2, last_value(no_l1, 0))}"
)

print("CLAIM_WITNESSES_OK all_preconditions_satisfiable=true")
