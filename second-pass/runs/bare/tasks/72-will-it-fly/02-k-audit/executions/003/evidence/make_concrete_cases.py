#!/usr/bin/env python3
"""Wrap the regenerated submitted module in concrete audit invocations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/72-will-it-fly-audit/candidate")
MODULE = (WORK / "regenerated-solution.mpy").read_text(encoding="utf-8").strip()

CASES = {
    "empty-at-bound": ([], 0, True),
    "empty-overweight": ([], -1, False),
    "singleton-at-bound": ([3], 3, True),
    "unbalanced-underweight": ([1, 2], 5, False),
    "palindrome-overweight": ([3, 2, 3], 1, False),
    "palindrome-at-bound": ([3, 2, 3], 8, True),
    "negative-at-bound": ([-3, 1, -3], -5, True),
    "negative-overweight": ([-3, 1, -3], -6, False),
    "longer-palindrome": ([1, 2, 3, 2, 1], 9, True),
}


def int_list(values: list[int]) -> str:
    result = "nil"
    for value in reversed(values):
        result = f"cons({value}, {result})"
    return result


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.will_it_fly


canonical = load_function(WORK.parent / "reference/canonical.py", "case_canonical")
generated = load_function(WORK / "solution.py", "case_generated")

for name, (q, w, expected) in CASES.items():
    canonical_result = canonical(list(q), w)
    generated_result = generated(list(q), w)
    assert canonical_result is expected
    assert generated_result is expected
    target = WORK / f"audit-{name}.mpy"
    target.write_text(
        f"run(\n{MODULE},\n"
        f"  pyList({int_list(q)}),\n"
        f"  pyInt({w}))\n",
        encoding="utf-8",
    )
    print(
        f"{target.name} canonical={canonical_result} "
        f"generated={generated_result} expected=pyBool({str(expected).lower()})"
    )
