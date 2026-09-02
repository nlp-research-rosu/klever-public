#!/usr/bin/env python3
"""Concrete satisfying states and Python results for every candidate claim."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


CLAIMS = (
    ("case-01-empty", "DictVal()", {}),
    (
        "case-02-lower",
        'DictVal(StrVal("a") StrVal("b"))',
        {"a": 0, "b": 0},
    ),
    (
        "case-03-mixed",
        'DictVal(StrVal("a") StrVal("A") StrVal("B"))',
        {"a": 0, "A": 0, "B": 0},
    ),
    (
        "case-04-int",
        'DictVal(StrVal("a") IntVal(8))',
        {"a": 0, 8: 0},
    ),
    (
        "case-05-title",
        'DictVal(StrVal("Name") StrVal("Age") StrVal("City"))',
        {"Name": 0, "Age": 0, "City": 0},
    ),
    (
        "case-06-upper",
        'DictVal(StrVal("STATE") StrVal("ZIP"))',
        {"STATE": 0, "ZIP": 0},
    ),
    (
        "case-07-lower-uncased",
        'DictVal(StrVal("abc-123") StrVal("z9"))',
        {"abc-123": 0, "z9": 0},
    ),
    (
        "case-08-upper-uncased",
        'DictVal(StrVal("ABC-123") StrVal("Z9"))',
        {"ABC-123": 0, "Z9": 0},
    ),
    ("case-09-uncased", 'DictVal(StrVal("123"))', {"123": 0}),
    ("case-10-single-mixed", 'DictVal(StrVal("aA"))', {"aA": 0}),
    ("case-11-bool", "DictVal(BoolVal(true))", {True: 0}),
)


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


def contract(value: dict) -> bool:
    if not value:
        return False
    keys = tuple(value)
    return all(isinstance(k, str) for k in keys) and (
        all(k.islower() for k in keys) or all(k.isupper() for k in keys)
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: claim_witnesses.py SCRATCH", file=sys.stderr)
        return 2
    scratch = Path(sys.argv[1])
    canonical = load_entry(scratch / "canonical.py", "claim_canonical")
    generated = load_entry(scratch / "solution.py", "claim_generated")
    mismatch_count = 0
    for label, k_input, value in CLAIMS:
        expected = contract(value)
        canonical_result = canonical(value)
        generated_result = generated(value)
        if canonical_result != expected or generated_result != expected:
            mismatch_count += 1
        print(
            json.dumps(
                {
                    "claim": label,
                    "formal_precondition": "none beyond the exact ground initial cells",
                    "satisfying_k_input": k_input,
                    "python_keys": [repr(key) for key in value],
                    "contract_result": expected,
                    "canonical_result": canonical_result,
                    "generated_result": generated_result,
                },
                sort_keys=True,
            )
        )
    print(json.dumps({"claims": len(CLAIMS), "mismatch_count": mismatch_count}))
    return 0 if mismatch_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
