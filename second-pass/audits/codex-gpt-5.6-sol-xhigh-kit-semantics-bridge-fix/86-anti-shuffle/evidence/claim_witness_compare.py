#!/usr/bin/env python3
"""Concrete substitutions for the K entry postcondition."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


def anti_shuffle_codes_model(value: str) -> str:
    emitted: list[str] = []
    word: list[str] = []
    for char in value:
        if ord(char) == 32:
            emitted.extend(sorted(word))
            emitted.append(" ")
            word.clear()
        else:
            word.append(char)
    emitted.extend(sorted(word))
    return "".join(emitted)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    args = parser.parse_args()
    canonical = load(args.canonical, "witness_canonical")
    solution = load(args.solution, "witness_solution")
    cases = ["", "ba", "a  b", "Hello World!!!"]
    records = []
    for value in cases:
        model = anti_shuffle_codes_model(value)
        expected = canonical(value)
        actual = solution(value)
        records.append({
            "input": value,
            "input_codes": [ord(char) for char in value],
            "k_summary_model": model,
            "result_codes": [ord(char) for char in model],
            "canonical": expected,
            "solution": actual,
            "all_equal": model == expected == actual,
        })
    print(json.dumps(records, indent=2, ensure_ascii=False))
    return 0 if all(record["all_equal"] for record in records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
