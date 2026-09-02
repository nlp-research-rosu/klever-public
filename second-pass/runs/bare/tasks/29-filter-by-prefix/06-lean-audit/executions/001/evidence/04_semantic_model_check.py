#!/usr/bin/env python3
"""Finite adversarial check of the frozen K recurrence against its loop rules."""

from __future__ import annotations

import itertools
import json


def k_starts_with(string: str, prefix: str) -> bool:
    if len(prefix) > len(string):
        return False
    return string[: len(prefix)] == prefix


def append_one(items: list[str], value: str) -> list[str]:
    if not items:
        return [value]
    return [items[0], *append_one(items[1:], value)]


def filter_acc(
    remaining: list[str], prefix: str, accumulator: list[str]
) -> list[str]:
    if not remaining:
        return accumulator
    head, *tail = remaining
    if k_starts_with(head, prefix):
        return filter_acc(tail, prefix, append_one(accumulator, head))
    return filter_acc(tail, prefix, accumulator)


def operational_loop(
    remaining: list[str], prefix: str, accumulator: list[str]
) -> list[str]:
    state = list(accumulator)
    for string in remaining:
        condition = k_starts_with(string, prefix)
        if condition:
            state = append_one(state, string)
    return state


strings = ["", "a", "aa", "ab", "b", "\x00a", "é", "😀a"]
prefixes = ["", "a", "aa", "b", "\x00", "é", "😀", "longer"]
accumulators = [[], ["seed"], ["x", "x"]]
mismatches = []
case_count = 0
for length in range(5):
    for values in itertools.product(strings, repeat=length):
        for prefix in prefixes:
            for accumulator in accumulators:
                case_count += 1
                summary = filter_acc(
                    list(values), prefix, list(accumulator)
                )
                operational = operational_loop(
                    list(values), prefix, list(accumulator)
                )
                if summary != operational:
                    mismatches.append(
                        {
                            "input": values,
                            "prefix": prefix,
                            "accumulator": accumulator,
                            "summary": summary,
                            "operational": operational,
                        }
                    )

assert not mismatches
adversarial = [
    {
        "input": [],
        "prefix": "a",
        "result": operational_loop([], "a", []),
        "purpose": "empty input",
    },
    {
        "input": ["", "a", "aa", "b"],
        "prefix": "",
        "result": operational_loop(["", "a", "aa", "b"], "", []),
        "purpose": "empty prefix preserves every item",
    },
    {
        "input": ["a"],
        "prefix": "aa",
        "result": operational_loop(["a"], "aa", []),
        "purpose": "prefix longer than string",
    },
    {
        "input": ["aa", "x", "aa"],
        "prefix": "a",
        "result": operational_loop(["aa", "x", "aa"], "a", []),
        "purpose": "duplicates and stable order",
    },
    {
        "input": ["\x00a", "\x00", "a"],
        "prefix": "\x00",
        "result": operational_loop(["\x00a", "\x00", "a"], "\x00", []),
        "purpose": "embedded NUL",
    },
    {
        "input": ["😀a", "😀", "a😀"],
        "prefix": "😀",
        "result": operational_loop(["😀a", "😀", "a😀"], "😀", []),
        "purpose": "non-ASCII prefix",
    },
]
counterfactuals = {
    "constant_empty_rejected_by": {
        "input": ["abc"],
        "prefix": "a",
        "correct": operational_loop(["abc"], "a", []),
        "mutated": [],
    },
    "identity_rejected_by": {
        "input": ["abc", "b"],
        "prefix": "a",
        "correct": operational_loop(["abc", "b"], "a", []),
        "mutated": ["abc", "b"],
    },
    "prepend_rejected_by": {
        "input": ["a", "aa"],
        "prefix": "a",
        "correct": operational_loop(["a", "aa"], "a", []),
        "mutated": ["aa", "a"],
    },
}
for witness in counterfactuals.values():
    assert witness["correct"] != witness["mutated"]

print(
    json.dumps(
        {
            "status": "PASS",
            "finite_case_count": case_count,
            "mismatch_count": len(mismatches),
            "adversarial_cases": adversarial,
            "counterfactual_mutations": counterfactuals,
        },
        indent=2,
        sort_keys=True,
        ensure_ascii=True,
    )
)
