#!/usr/bin/env python3
"""Independent differential test against the trusted HumanEval canonical."""

from __future__ import annotations

import importlib.util
from pathlib import Path


CANONICAL = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/rebuild/solution.py")


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.int_to_mini_roman


def main() -> int:
    canonical = load(CANONICAL, "trusted_canonical")
    generated = load(GENERATED, "generated_solution")

    examples = {19: "xix", 152: "clii", 426: "cdxxvi"}
    boundaries = [1, 2, 3, 4, 5, 8, 9, 10, 11, 39, 40, 41, 49, 50, 51,
                  89, 90, 91, 99, 100, 101, 399, 400, 401, 499, 500,
                  501, 899, 900, 901, 999, 1000]
    # There is no empty value in the integer source domain. Zero is checked
    # separately as the nearest out-of-domain observation; both return "".
    empty_observation = 0

    mismatches: list[tuple[int, str, str]] = []
    for number in range(1, 1001):
        expected = canonical(number)
        actual = generated(number)
        if actual != expected:
            mismatches.append((number, expected, actual))

    example_results = {
        number: (canonical(number), generated(number), expected)
        for number, expected in examples.items()
    }
    boundary_results = {
        number: (canonical(number), generated(number))
        for number in boundaries
    }
    empty_results = (
        canonical(empty_observation),
        generated(empty_observation),
    )

    print(f"trusted_canonical={CANONICAL}")
    print(f"generated_entry={GENERATED}")
    print(f"documented_examples={example_results}")
    print(f"branch_and_domain_boundaries={boundary_results}")
    print(
        "empty_case=not_applicable_to_integer_domain; "
        f"out_of_domain_zero_observation={empty_results}"
    )
    print("generated_input_scope=every integer 1..1000")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(f"first_mismatches={mismatches[:20]}")
        return 1
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
