#!/usr/bin/env python3
"""Closed substitutions for the entry postcondition's scan equations."""

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
    return module


def paren_input(value: str) -> bool:
    return all(char in "() " for char in value)


def formal_parsed_parens(value: str) -> list[int]:
    depth = 0
    maximum = 0
    completed: list[int] = []
    for char in value:
        if char == "(":
            depth += 1
            maximum = max(depth, maximum)
        elif char == ")":
            depth -= 1
        elif char == " ":
            completed.append(maximum)
            depth = 0
            maximum = 0
        else:
            raise ValueError("outside parenInput")
    completed.append(maximum)
    return completed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--submission", type=Path, required=True)
    args = parser.parse_args()
    canonical = load(args.canonical, "canonical_witness")
    submission = load(args.submission, "submission_witness")

    cases = [
        "(()()) ((())) () ((())()())",
        "",
        " ()",
        "()  ()",
        "(()",
    ]
    for value in cases:
        formal = formal_parsed_parens(value)
        submitted = submission.parse_nested_parens(value)
        trusted = canonical.parse_nested_parens(value)
        record = {
            "input": value,
            "entry_precondition_parenInput": paren_input(value),
            "formal_parsedParens": formal,
            "submission_python": submitted,
            "canonical_python": trusted,
            "formal_equals_submission": formal == submitted,
            "formal_equals_canonical": formal == trusted,
        }
        print(json.dumps(record, sort_keys=True))
        assert record["entry_precondition_parenInput"]
        assert record["formal_equals_submission"]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
