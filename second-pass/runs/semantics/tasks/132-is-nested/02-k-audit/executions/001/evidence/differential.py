#!/usr/bin/env python3
"""Independent differential test for HumanEval 132 on its stated domain."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_nested


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function(
    "generated_solution", Path("/tmp/audit-work/132-is-nested/source/solution.py")
)

documented = [
    "[[]]",
    "[]]]]]]][[[[[]",
    "[][]",
    "[]",
    "[[][]]",
    "[[]][[",
]

boundaries = [
    "",
    "[",
    "]",
    "[[",
    "]]",
    "[]]",
    "[[]",
    "[[]]",
    "[[[]]]",       # drives every automaton branch, including saturated state
    "]]][[[",
    "[" * 5000 + "]" * 5000,
    "[]" * 5000,
]


def all_small_strings(max_length: int):
    for length in range(max_length + 1):
        for chars in itertools.product("[]", repeat=length):
            yield "".join(chars)


def random_strings(seed: int, count: int):
    rng = random.Random(seed)
    for _ in range(count):
        length = rng.randint(13, 80)
        yield "".join(rng.choice("[]") for _ in range(length))


def branch_labels(value: str) -> set[str]:
    state = 0
    labels: set[str] = set()
    for char in value:
        if char == "[":
            if state < 2:
                labels.add("open/state<2:true")
                state += 1
            else:
                labels.add("open/state<2:false")
        else:
            if state > 1:
                labels.add("close/state>1:true")
                if state < 4:
                    labels.add("close/state<4:true")
                    state += 1
                else:
                    labels.add("close/state<4:false")
            else:
                labels.add("close/state>1:false")
    return labels


def main() -> int:
    mismatches: list[tuple[str, bool, bool]] = []
    seen: set[str] = set()
    covered: set[str] = set()
    categories = [
        ("documented", documented),
        ("boundaries", boundaries),
        ("exhaustive-length-0-through-12", list(all_small_strings(12))),
        ("random-seed-132-count-1000-length-13-through-80", list(random_strings(132, 1000))),
    ]
    category_counts: dict[str, int] = {}
    for category, inputs in categories:
        category_counts[category] = len(inputs)
        for value in inputs:
            covered.update(branch_labels(value))
            if value in seen:
                continue
            seen.add(value)
            expected = canonical(value)
            actual = generated(value)
            if type(expected) is not bool or type(actual) is not bool:
                raise AssertionError(
                    f"non-bool result for {value!r}: canonical={expected!r}, generated={actual!r}"
                )
            if expected != actual:
                mismatches.append((value, expected, actual))

    print("DOCUMENTED RESULTS")
    for value in documented:
        print(f"{value!r}: canonical={canonical(value)!r} generated={generated(value)!r}")
    print(f"CATEGORY COUNTS: {category_counts}")
    print(f"UNIQUE INPUTS: {len(seen)}")
    print(f"BRANCH COVERAGE: {sorted(covered)}")
    print(f"MISMATCHES: {len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    required_labels = {
        "open/state<2:true",
        "open/state<2:false",
        "close/state>1:true",
        "close/state>1:false",
        "close/state<4:true",
        "close/state<4:false",
    }
    if covered != required_labels:
        print(f"BRANCH COVERAGE FAILURE: missing={sorted(required_labels - covered)}")
        return 2
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
