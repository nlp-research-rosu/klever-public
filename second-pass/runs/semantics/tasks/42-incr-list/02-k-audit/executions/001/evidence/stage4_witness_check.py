#!/usr/bin/env python3
"""Concrete substitutions for the two reviewed entry-point witnesses."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.incr_list


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: stage4_witness_check.py CANONICAL GENERATED", file=sys.stderr)
        return 64
    canonical = load_function(Path(sys.argv[1]).resolve(), "stage4_canonical")
    generated = load_function(Path(sys.argv[2]).resolve(), "stage4_generated")

    witnesses = [
        {"name": "entry-empty", "input": [], "formal_result": []},
        {"name": "entry-two-elements", "input": [2, -1], "formal_result": [3, 0]},
        {
            "name": "loop-prefix",
            "input": [2, -1],
            "prefix": [7],
            "formal_heap_result": [7, 3, 0],
        },
    ]
    failures = []
    for witness in witnesses:
        suffix_result = canonical(list(witness["input"]))
        generated_result = generated(list(witness["input"]))
        if witness["name"] == "loop-prefix":
            expected = witness["prefix"] + suffix_result
            actual = witness["prefix"] + generated_result
            formal = witness["formal_heap_result"]
        else:
            expected = suffix_result
            actual = generated_result
            formal = witness["formal_result"]
        record = {
            **witness,
            "canonical": expected,
            "generated": actual,
            "formal": formal,
            "match": expected == actual == formal,
        }
        print(json.dumps(record, sort_keys=True))
        if not record["match"]:
            failures.append(record)
    print(f"WITNESS_FAILURE_COUNT={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
