"""Independent candidate/canonical/source-contract differential for HumanEval 123."""

from __future__ import annotations

import importlib.util
import hashlib
import random
from pathlib import Path
from typing import Callable


def load_entry(path: str, module_name: str) -> Callable[[int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_odd_collatz


def exact_contract_oracle(n: int) -> list[int]:
    """Direct unbounded-integer interpretation of the prompt's Collatz contract."""
    odd_values: list[int] = []
    current = n
    while True:
        if current % 2 == 1:
            odd_values.append(current)
        if current == 1:
            return sorted(odd_values)
        current = current // 2 if current % 2 == 0 else 3 * current + 1


def outcome(function: Callable[[int], list[int]], n: int) -> tuple[str, object]:
    try:
        return ("value", function(n))
    except Exception as error:  # Deliberately compare observable exception outcomes.
        return ("exception", (type(error).__name__, str(error)))


def compact(result: tuple[str, object]) -> tuple[str, object]:
    if result[0] == "exception":
        return result
    values = result[1]
    assert isinstance(values, list)
    digest = hashlib.sha256(repr(values).encode()).hexdigest()[:16]
    return (
        "value",
        {
            "length": len(values),
            "first": values[:5],
            "last": values[-5:],
            "sha256_prefix": digest,
        },
    )


def main() -> None:
    canonical = load_entry("/reference/canonical.py", "trusted_canonical_123")
    generated = load_entry("/candidate/solution.py", "generated_solution_123")

    documented = [5]
    boundaries = [1, 2, 3, 4, 5, 6, 7, 8]
    exhaustive_small = list(range(1, 301))
    pseudo_random = random.Random(123_20260729).sample(range(1, 1_000_001), 200)
    precision_boundaries = [
        2**53 - 1,
        2**53,
        2**53 + 1,
        2 * (2**53 + 1),
        2**63 - 1,
        2**63,
        2**1024,
        2**1025,
        2**2048,
    ]

    intended_inputs = list(
        dict.fromkeys(
            documented
            + boundaries
            + exhaustive_small
            + pseudo_random
            + precision_boundaries
        )
    )
    Path("/audit-output/evidence/03_inputs.txt").write_text(
        "\n".join(str(value) for value in intended_inputs) + "\n",
        encoding="utf-8",
    )

    canonical_mismatches = []
    generated_contract_mismatches = []
    canonical_contract_mismatches = []
    for n in intended_inputs:
        expected = ("value", exact_contract_oracle(n))
        trusted = outcome(canonical, n)
        actual = outcome(generated, n)
        if trusted != actual:
            canonical_mismatches.append((n, trusted, actual))
        if actual != expected:
            generated_contract_mismatches.append((n, expected, actual))
        if trusted != expected:
            canonical_contract_mismatches.append((n, expected, trusted))

    print(f"documented={documented}")
    print(f"boundaries={boundaries}")
    print(f"intended_inputs={len(intended_inputs)}")
    print(f"candidate_vs_canonical_mismatches={len(canonical_mismatches)}")
    print(f"candidate_vs_contract_mismatches={len(generated_contract_mismatches)}")
    print(f"canonical_vs_contract_mismatches={len(canonical_contract_mismatches)}")
    print(
        "candidate_vs_canonical_examples=",
        [
            (n, compact(trusted), compact(actual))
            for n, trusted, actual in canonical_mismatches[:10]
        ],
    )
    print(
        "canonical_vs_contract_examples=",
        [
            (n, compact(expected), compact(trusted))
            for n, expected, trusted in canonical_contract_mismatches[:10]
        ],
    )

    # There is no "empty integer" in the positive-integer domain. These probes
    # explicitly document the nearest excluded boundary and a negative value.
    excluded = [0, -1]
    print(
        "excluded_domain_probes=",
        [
            (n, outcome(canonical, n), outcome(generated, n))
            for n in excluded
        ],
    )

    if generated_contract_mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
