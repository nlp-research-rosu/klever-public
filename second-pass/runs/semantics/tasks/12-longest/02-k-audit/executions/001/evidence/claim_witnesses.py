#!/usr/bin/env python3
"""Ground witnesses for every submitted claim family."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_witness", Path("/reference/canonical.py"))
generated = load("generated_witness", Path("/candidate/solution.py"))


def fold(best: str | None, remaining: list[str]) -> str | None:
    for current in remaining:
        if best is None or len(current) > len(best):
            best = current
    return best


def report(label: str, original: list[str], best: str | None, rest: list[str]) -> None:
    claimed = fold(best, rest)
    print(
        json.dumps(
            {
                "claim": label,
                "satisfying_original_input": original,
                "substituted_accumulator": best,
                "substituted_remaining": rest,
                "claimed_summary_value": claimed,
                "canonical_value": canonical.longest(original),
                "generated_value": generated.longest(original),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )


report("loop-init-empty / call-empty", [], None, [])
report("loop-init-cons", ["a", "bb"], None, ["a", "bb"])
report("loop-empty", ["aa"], "aa", [])
report("loop-longer", ["a", "bb"], "a", ["bb"])
report("loop-retain-tie", ["aa", "bb"], "aa", ["bb"])

nonempty = ["a", "bb"]
print(
    json.dumps(
        {
            "claim": "call-cons-dispatch",
            "satisfying_original_input": nonempty,
            "submitted_postcondition": "expanded function body ~> #endcall",
            "submitted_final_result_constraint": None,
            "canonical_value": canonical.longest(nonempty),
            "generated_value": generated.longest(nonempty),
        },
        sort_keys=True,
    )
)

print(
    json.dumps(
        {
            "claim": "load-solution",
            "satisfying_state": "empty module scope 0, builtins at -1, empty heap/stack",
            "submitted_postcondition": "exact longestSolution closure installed at scope 0",
        },
        sort_keys=True,
    )
)
