#!/usr/bin/env python3
"""Concrete witnesses for all nine unconditional entry-claim sort pairs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


def observed(function, a: Any, b: Any) -> dict[str, str]:
    try:
        result = function(a, b)
        return {"kind": "return", "type": type(result).__name__, "repr": repr(result)}
    except Exception as error:
        return {"kind": "exception", "type": type(error).__name__, "repr": str(error)}


def intended_contract(a: Any, b: Any) -> Any:
    # Ground interpretation candidate expectedCompare is intended to denote.
    av = float(a.replace(",", ".")) if isinstance(a, str) else a
    bv = float(b.replace(",", ".")) if isinstance(b, str) else b
    if av == bv:
        return None
    return a if av > bv else b


def packed(value: Any) -> dict[str, str]:
    return {"type": type(value).__name__, "repr": repr(value)}


def main() -> int:
    canonical = load_entry(Path("/tmp/audit-work/trusted/canonical.py"), "stage4_canonical")
    generated = load_entry(Path("/tmp/audit-work/candidate-src/solution.py"), "stage4_generated")
    witnesses = [
        ("int-int", 1, 2),
        ("int-float", 1, 2.5),
        ("int-str", 1, "2,3"),
        ("float-int", 2.5, 1),
        ("float-float", 3.0, 3.0),
        ("float-str", 3.0, "3,0"),
        ("str-int", "-2,5", -2),
        ("str-float", "2,5", 2.0),
        ("str-str", "5,1", "6"),
    ]
    mismatches = 0
    for label, a, b in witnesses:
        intended = packed(intended_contract(a, b))
        canonical_result = observed(canonical, a, b)
        generated_result = observed(generated, a, b)
        agrees = canonical_result == generated_result == {"kind": "return", **intended}
        if not agrees:
            mismatches += 1
        print(
            json.dumps(
                {
                    "claim": label,
                    "precondition": "unconditional sort membership",
                    "a": packed(a),
                    "b": packed(b),
                    "intended_ground_expectedCompare": intended,
                    "canonical": canonical_result,
                    "generated": generated_result,
                    "all_agree": agrees,
                },
                sort_keys=True,
            )
        )
    print(f"WITNESS_COUNT={len(witnesses)} MISMATCH_COUNT={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
