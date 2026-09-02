#!/usr/bin/env python3
"""Ground witnesses for each entry shape and its result formula."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


def load(name: str, path: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def change_range(values: list[int], left: int, right: int) -> int:
    count = 0
    while left < right:
        count += int(values[left] != values[right])
        left += 1
        right -= 1
    return count


def helper_valid(values: list[int], left: int, right: int) -> bool:
    return 0 <= left <= len(values) and -1 <= right < len(values)


def main() -> int:
    canonical = load("trusted_canonical_witness", "/reference/canonical.py")
    generated = load("generated_witness", "/tmp/audit-work/audit73/solution.py")

    public_arr = [1, 2]
    public_answer = change_range(public_arr, 0, len(public_arr) - 1)
    print("PUBLIC_ENTRY_BRIDGE_WITNESS:")
    print("  k = #applyK(toCall(#mainClosure), (ref(0), .Vals)) ~> .K")
    print("  heap = 0 |-> list(vCons(1, vCons(2, .ValSeq)))")
    print("  explicit_requires = none (therefore satisfiable)")
    print(f"  targetAnswer(mainCall, ...) = {public_answer}")
    print(f"  trusted_canonical.smallest_change = {canonical.smallest_change(public_arr)}")
    print(f"  generated.smallest_change = {generated.smallest_change(public_arr)}")

    helper_arr = [1, 2, 3, 4]
    left, right = 1, 2
    helper_answer = change_range(helper_arr, left, right)
    print("HELPER_ENTRY_BRIDGE_WITNESS:")
    print("  k = #applyK(toCall(#helperClosure), (ref(0), 1, 2, .Vals)) ~> .K")
    print("  heap = 0 |-> list(vCons(1, vCons(2, vCons(3, vCons(4, .ValSeq)))))")
    print("  explicit_requires = none (therefore satisfiable)")
    print(f"  targetValid(helperCall, ...) = {helper_valid(helper_arr, left, right)}")
    print(f"  targetAnswer(helperCall, ...) = {helper_answer}")
    print(
        "  trusted_canonical.smallest_change(arr[left:right+1]) = "
        f"{canonical.smallest_change(helper_arr[left : right + 1])}"
    )
    print(
        "  generated._smallest_change(arr,left,right) = "
        f"{generated._smallest_change(helper_arr, left, right)}"
    )

    print("CORRECTNESS_MAIN_WITNESS:")
    print("  k = #targetCall(mainCall, ref(0), 123, -99) ~> .K")
    print("  targetValid(mainCall, [1,2], 123, -99) = true")
    print(f"  claimed result = {public_answer}")
    print("CORRECTNESS_HELPER_WITNESS:")
    print("  k = #targetCall(helperCall, ref(0), 1, 2) ~> .K")
    print(f"  targetValid = {helper_valid(helper_arr, left, right)}")
    print(f"  claimed result = {helper_answer}")

    checks = [
        public_answer == canonical.smallest_change(public_arr),
        public_answer == generated.smallest_change(public_arr),
        helper_valid(helper_arr, left, right),
        helper_answer == canonical.smallest_change(helper_arr[left : right + 1]),
        helper_answer == generated._smallest_change(helper_arr, left, right),
    ]
    print(f"ALL_GROUND_CHECKS_PASS: {all(checks)}")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
