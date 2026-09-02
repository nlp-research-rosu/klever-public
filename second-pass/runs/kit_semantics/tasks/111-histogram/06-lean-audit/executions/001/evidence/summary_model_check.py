#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json


def source_histogram(test: str) -> dict[str, int]:
    result: dict[str, int] = {}
    max_count = 0
    for letter in test:
        if letter != " ":
            count = 0
            for candidate in test:
                if candidate == letter:
                    count += 1
            if count > max_count:
                max_count = count
    for letter in test:
        if letter != " ":
            count = 0
            for candidate in test:
                if candidate == letter:
                    count += 1
            if count == max_count:
                result[letter] = count
    return result


def count_histogram_code(sequence: str, target: str, accumulator: int) -> int:
    if not sequence:
        return accumulator
    head, tail = sequence[0], sequence[1:]
    return count_histogram_code(
        tail,
        target,
        accumulator + 1 if head == target else accumulator,
    )


def max_histogram_count(remaining: str, original: str, maximum: int) -> int:
    if not remaining:
        return maximum
    head, tail = remaining[0], remaining[1:]
    if head == " ":
        return max_histogram_count(tail, original, maximum)
    count = count_histogram_code(original, head, 0)
    return max_histogram_count(tail, original, count if count > maximum else maximum)


def build_histogram(
    remaining: str,
    original: str,
    maximum: int,
    accumulated: dict[str, int],
) -> dict[str, int]:
    if not remaining:
        return accumulated
    head, tail = remaining[0], remaining[1:]
    updated = dict(accumulated)
    if head != " " and count_histogram_code(original, head, 0) == maximum:
        updated[head] = count_histogram_code(original, head, 0)
    return build_histogram(tail, original, maximum, updated)


def histogram_result(test: str) -> dict[str, int]:
    maximum = max_histogram_count(test, test, 0)
    return build_histogram(test, test, maximum, {})


def mutant_counts_spaces(test: str) -> dict[str, int]:
    maximum = max((test.count(character) for character in test), default=0)
    return {
        character: test.count(character)
        for character in test
        if character != " " and test.count(character) == maximum
    }


def mutant_build_strict(test: str) -> dict[str, int]:
    maximum = max_histogram_count(test, test, 0)
    return {
        character: test.count(character)
        for character in test
        if character != " " and test.count(character) > maximum
    }


alphabet = " ab"
inputs = [
    "".join(chars)
    for length in range(7)
    for chars in itertools.product(alphabet, repeat=length)
]
mismatches = [
    {
        "input": value,
        "source": source_histogram(value),
        "summary": histogram_result(value),
    }
    for value in inputs
    if source_histogram(value) != histogram_result(value)
]
adversarial = {
    value: {
        "source": source_histogram(value),
        "summary": histogram_result(value),
    }
    for value in ["", " ", "   ", "a", "aaa", "a b a", "abbbcc", "abba", "zz z"]
}
counterfactuals = {
    "count_spaces_in_max": {
        "witness": "  a",
        "source": source_histogram("  a"),
        "mutant": mutant_counts_spaces("  a"),
        "distinguished": source_histogram("  a") != mutant_counts_spaces("  a"),
    },
    "strict_build_condition": {
        "witness": "a",
        "source": source_histogram("a"),
        "mutant": mutant_build_strict("a"),
        "distinguished": source_histogram("a") != mutant_build_strict("a"),
    },
    "constant_empty_result": {
        "witness": "abbbcc",
        "source": source_histogram("abbbcc"),
        "mutant": {},
        "distinguished": source_histogram("abbbcc") != {},
    },
}
result = {
    "alphabet": alphabet,
    "max_length": 6,
    "input_count": len(inputs),
    "mismatch_count": len(mismatches),
    "mismatches": mismatches,
    "adversarial_examples": adversarial,
    "counterfactuals": counterfactuals,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(
    0
    if not mismatches and all(item["distinguished"] for item in counterfactuals.values())
    else 1
)
