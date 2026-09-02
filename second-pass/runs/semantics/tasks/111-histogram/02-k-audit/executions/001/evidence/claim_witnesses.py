#!/usr/bin/env python3
"""Concrete satisfying witnesses for each of the 13 K entry claims."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def load_histogram(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    args = parser.parse_args()
    canonical = load_histogram("trusted_canonical_witness", args.canonical)
    generated = load_histogram("candidate_generated_witness", args.generated)

    witnesses = [
        ("c01", "", {}),
        ("c02", "a b c", {"a": 1, "b": 1, "c": 1}),
        ("c03", "a b b a", {"a": 2, "b": 2}),
        ("c04", "a b c a b", {"a": 2, "b": 2}),
        ("c05", "b b b b a", {"b": 4}),
        ("c06", "z", {"z": 1}),
        ("c07", "z z", {"z": 2}),
        ("c08", "z y", {"z": 1, "y": 1}),
        ("c09", "z z z", {"z": 3}),
        ("c10", "z z y", {"z": 2}),
        ("c11", "z y z", {"z": 2}),
        ("c12", "z y y", {"y": 2}),
        ("c13", "z y x", {"z": 1, "y": 1, "x": 1}),
    ]
    failures = []
    for label, value, expected in witnesses:
        oracle = canonical(value)
        observed = generated(value)
        ok = oracle == expected and observed == expected
        record = {
            "claim": label,
            "input": value,
            "expected": expected,
            "canonical": oracle,
            "generated": observed,
            "ok": ok,
        }
        print(json.dumps(record, sort_keys=True))
        if not ok:
            failures.append(record)
    print(f"witness_count={len(witnesses)}")
    print(f"witness_failure_count={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
