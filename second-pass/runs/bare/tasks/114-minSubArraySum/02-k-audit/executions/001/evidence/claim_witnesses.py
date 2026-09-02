#!/usr/bin/env python3
"""Ground witnesses for all three reachability-claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def min_prefix(nums: list[int]) -> int:
    return min(sum(nums[:end]) for end in range(1, len(nums) + 1))


def min_subarray(nums: list[int]) -> int:
    return min(
        sum(nums[start:end])
        for start in range(len(nums))
        for end in range(start + 1, len(nums) + 1)
    )


def main() -> int:
    nums = [4, -6, 2, -5, 7]
    canonical = load(Path("/reference/canonical.py"), "witness_canonical")
    candidate = load(
        Path("/tmp/audit-work/114-minSubArraySum-audit/solution.py"),
        "witness_candidate",
    )

    prefix_result = min_prefix(nums)
    subarray_result = min_subarray(nums)
    canonical_result = canonical.minSubArraySum(nums.copy())
    candidate_prefix = candidate.min_prefix_sum(nums.copy())
    candidate_result = candidate.minSubArraySum(nums.copy())

    assert prefix_result == candidate_prefix == -5
    assert subarray_result == canonical_result == candidate_result == -9

    tail_term = "cons(-6, cons(2, cons(-5, cons(7, nil))))"
    print(
        "PREFIX CLAIM WITNESS: "
        f"H=4 T={tail_term} K=.K D=z ENTRY=\"unused\" "
        "ARGS=.Values RHO=.Map STACK=.List; result=pyInt(-5)"
    )
    print(
        "TARGET-CALL CLAIM WITNESS: "
        f"H=4 T={tail_term} K=.K D=z ENTRY=\"unused\" "
        "ARGS=.Values RHO=.Map STACK=.List; result=pyInt(-9)"
    )
    print(
        "ENTRY CLAIM WITNESS: "
        f"H=4 T={tail_term}; initial functions=.Map env=.Map "
        "callStack=.List callDepth=z; result=pyInt(-9)"
    )
    print(
        "GROUND COMPARISON: "
        f"candidate_prefix={candidate_prefix} direct_prefix={prefix_result} "
        f"candidate={candidate_result} canonical={canonical_result} "
        f"direct_subarray={subarray_result}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
