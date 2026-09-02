#!/usr/bin/env python3
"""Ground satisfying witnesses for the two entry-claim preconditions."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


sys.dont_write_bytecode = True


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_nums


def count_nums_spec_under_decimal_contract(values: list[int]) -> int:
    result = 0
    for value in values:
        codes = [ord(char) for char in str(abs(value))]
        digit_sum = sum(code - 48 for code in codes)
        first_nonzero = next((code - 48 for code in codes if code != 48), 0)
        signed = digit_sum - 2 * first_nonzero if value < 0 else digit_sum
        result += signed > 0
    return result


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "canonical_witness")
    generated = load(
        Path("/tmp/audit-work/108-count-nums-audit/solution.py"),
        "generated_witness",
    )
    witnesses = [
        [],
        [11],
        [-11],
        [-12],
        [-12, 0, 11],
        [-101, -102, 999],
    ]
    ok = True
    for values in witnesses:
        precondition = all(isinstance(value, int) and not isinstance(value, bool) for value in values)
        expected = count_nums_spec_under_decimal_contract(values)
        canonical_result = canonical(values)
        generated_result = generated(values)
        item_ok = (
            precondition
            and expected == canonical_result
            and expected == generated_result
        )
        ok &= item_ok
        print(
            json.dumps(
                {
                    "input": values,
                    "entry": "empty" if not values else "nonempty",
                    "precondition_satisfied": precondition,
                    "claim_result_under_named_decimal_contract": expected,
                    "canonical": canonical_result,
                    "generated": generated_result,
                    "match": item_ok,
                },
                sort_keys=True,
            )
        )
    print(f"CLAIM_WITNESSES={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
