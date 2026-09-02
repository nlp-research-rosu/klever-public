#!/usr/bin/env python3
"""Record CPython recursion-limit behavior outside the finite normal corpus."""

from __future__ import annotations

import importlib.util
import json
import sys


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def record(function, value):
    try:
        return {"kind": "value", "value": function(value)}
    except BaseException as error:
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL.py CANDIDATE.py", file=sys.stderr)
        return 64
    canonical = load_module("resource_canonical", sys.argv[1])
    candidate = load_module("resource_candidate", sys.argv[2])
    cases = [
        ("long-list-1500", [1] * 1500),
        ("single-1050-digit-int", [int("1" * 1050)]),
    ]
    differences = 0
    print(f"PYTHON_RECURSION_LIMIT: {sys.getrecursionlimit()}")
    for label, values in cases:
        canonical_result = record(canonical.count_nums, values)
        candidate_result = record(candidate.count_nums, values)
        if canonical_result != candidate_result:
            differences += 1
        print(
            json.dumps(
                {
                    "label": label,
                    "length": len(values),
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                },
                sort_keys=True,
            )
        )
    print(f"RESOURCE_BOUNDARY_DIFFERENCES: {differences}")
    return 1 if differences else 0


if __name__ == "__main__":
    raise SystemExit(main())
