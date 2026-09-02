#!/usr/bin/env python3
"""Independent canonical-versus-submission differential test for compare_one."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


def outcome(fn, a, b):
    try:
        value = fn(a, b)
        return ("return", type(value).__name__, repr(value))
    except Exception as exc:  # Invalid-domain boundary cases are compared too.
        return ("raise", type(exc).__name__)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    generated = load_entry(args.generated, "generated_solution")

    named_cases = [
        ("prompt-1", 1, 2.5),
        ("prompt-2", 1, "2,3"),
        ("prompt-3", "5,1", "6"),
        ("prompt-4", "1", 1),
        ("equal-int", 7, 7),
        ("equal-mixed", "7,0", 7.0),
        ("a-greater", 8, 7),
        ("b-greater", 7, 8),
        ("a-string-path", "8,25", 8),
        ("b-string-path", 8, "8,25"),
        ("negative-order", -3, -4.5),
        ("signed-zero", -0.0, "0"),
        ("empty-a-invalid", "", 0),
        ("empty-b-invalid", 0, ""),
        ("binary-rounding-equality", 2**53 + 1, 2**53),
        ("binary-rounding-order", 2**53 + 2, 2**53 + 1),
        ("large-decimal-string-equality", str(2**53 + 1), 2**53),
    ]

    generated_values = [
        -3,
        -1,
        0,
        1,
        2,
        2**53,
        2**53 + 1,
        2**53 + 2,
        -2.5,
        -0.0,
        0.0,
        0.1,
        1.0,
        1.5,
        2.5,
        float(2**53),
        float(2**53 + 2),
        "-2,5",
        "-0",
        "0",
        "0.0",
        "0,1",
        "1",
        "1.0",
        "1,5",
        "2.5",
        str(2**53),
        str(2**53 + 1),
    ]

    mismatches = []
    records = []
    print("NAMED_CASE_RESULTS")
    for label, a, b in named_cases:
        expected = outcome(canonical, a, b)
        actual = outcome(generated, a, b)
        record = (label, repr(a), repr(b), expected, actual)
        records.append(record)
        print(record)
        if expected != actual:
            mismatches.append(record)

    for a in generated_values:
        for b in generated_values:
            expected = outcome(canonical, a, b)
            actual = outcome(generated, a, b)
            record = ("generated", repr(a), repr(b), expected, actual)
            records.append(record)
            if expected != actual:
                mismatches.append(record)

    digest = hashlib.sha256(repr(records).encode("utf-8")).hexdigest()
    print(f"NAMED_CASE_COUNT={len(named_cases)}")
    print(f"GENERATED_VALUE_COUNT={len(generated_values)}")
    print(f"GENERATED_PAIR_COUNT={len(generated_values) ** 2}")
    print(f"TOTAL_CASE_COUNT={len(records)}")
    print(f"RESULT_SHA256={digest}")
    print(f"MISMATCH_COUNT={len(mismatches)}")
    for mismatch in mismatches:
        print("MISMATCH", mismatch)
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
