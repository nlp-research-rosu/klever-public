#!/usr/bin/env python3
"""Ground witnesses for the formal precondition and result term."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable

WORK = Path("/tmp/audit-work/79-decimal-to-binary")


def load(path: Path, name: str) -> Callable[[int], str]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.decimal_to_binary


def formal_bin_codes(number: int) -> list[int]:
    if number < 0:
        raise ValueError("the K claim requires N >= 0")
    if number == 0:
        return [48]
    acc: list[int] = []
    current = number
    while current > 0:
        current, remainder = divmod(current, 2)
        acc.insert(0, 48 + remainder)
    return acc


candidate = load(WORK / "solution.py", "candidate_witness")
canonical = load(WORK / "canonical.py", "canonical_witness")
witnesses = [0, 1, 2, 15, 32, 103, (1 << 128) - 1, 1 << 128]
records = []
for number in witnesses:
    codepoints = [100, 98] + formal_bin_codes(number) + [100, 98]
    formal_rhs = "".join(map(chr, codepoints))
    independent_math = "db" + format(number, "b") + "db"
    generated_result = candidate(number)
    canonical_result = canonical(number)
    equal = (
        formal_rhs
        == independent_math
        == generated_result
        == canonical_result
    )
    records.append(
        {
            "N": number,
            "precondition_N_ge_0": number >= 0,
            "formal_rhs_codepoints": codepoints,
            "formal_rhs": formal_rhs,
            "independent_math": independent_math,
            "candidate": generated_result,
            "canonical": canonical_result,
            "all_equal": equal,
        }
    )

summary = {
    "witness_count": len(records),
    "mismatch_count": sum(not record["all_equal"] for record in records),
    "records": records,
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(0 if summary["mismatch_count"] == 0 else 1)
