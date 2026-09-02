#!/usr/bin/env python3
"""Independent contract and differential tests for HumanEval 141."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
import sys
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


def contract_oracle(file_name: str) -> str:
    """Direct, independent transcription of the natural-language prompt."""
    if file_name.count(".") != 1:
        return "No"
    base, suffix = file_name.split(".")
    if not base:
        return "No"
    if not ("A" <= base[0] <= "Z" or "a" <= base[0] <= "z"):
        return "No"
    if suffix not in {"txt", "exe", "dll"}:
        return "No"
    if sum("0" <= character <= "9" for character in file_name) > 3:
        return "No"
    return "Yes"


def main() -> int:
    canonical = load_function("trusted_canonical", CANONICAL_PATH)
    candidate = load_function("generated_candidate", CANDIDATE_PATH)

    named_cases = [
        # Documented examples and empty/boundary values.
        "",
        "example.txt",
        "1example.dll",
        ".txt",
        "a.tx",
        "a.txt",
        "a.exe",
        "a.dll",
        # Dot-count branches.
        "atxt",
        "a..txt",
        "a.txt.",
        # First-character ASCII boundaries.
        "@.txt",
        "A.txt",
        "Z.txt",
        "[.txt",
        "`.txt",
        "a.txt",
        "z.txt",
        "{.txt",
        # Suffix branches and case sensitivity.
        "a.bin",
        "a.TXT",
        "a.txtx",
        "aexe.",
        # Digit-count boundary.
        "a123.txt",
        "a1234.txt",
        "a0b1c2.dll",
        "a0b1c2d3.dll",
        # Non-ASCII probes exposing the canonical/Python predicate boundary.
        "é.txt",
        "α.exe",
        "a١٢٣.dll",
        "a١٢٣٤.dll",
    ]

    generated: set[str] = set(named_cases)
    exhaustive_alphabet = "Aaz09._-é١"
    for length in range(0, 6):
        generated.update(
            "".join(chars)
            for chars in itertools.product(exhaustive_alphabet, repeat=length)
        )

    rng = random.Random(141)
    random_alphabet = (
        string.ascii_letters
        + string.digits
        + "._-"
        + "éα١"
    )
    for _ in range(20_000):
        length = rng.randrange(0, 41)
        generated.add("".join(rng.choice(random_alphabet) for _ in range(length)))

    candidate_contract_mismatches: list[tuple[str, str, str]] = []
    candidate_canonical_mismatches: list[tuple[str, str, str]] = []
    canonical_contract_mismatches: list[tuple[str, str, str]] = []
    outcome_counts = {"Yes": 0, "No": 0}

    for value in sorted(generated):
        expected = contract_oracle(value)
        actual_candidate = candidate(value)
        actual_canonical = canonical(value)
        outcome_counts[expected] += 1
        if actual_candidate != expected:
            candidate_contract_mismatches.append((value, actual_candidate, expected))
        if actual_candidate != actual_canonical:
            candidate_canonical_mismatches.append(
                (value, actual_candidate, actual_canonical)
            )
        if actual_canonical != expected:
            canonical_contract_mismatches.append(
                (value, actual_canonical, expected)
            )

    print(f"canonical_path={CANONICAL_PATH}")
    print(f"candidate_path={CANDIDATE_PATH}")
    print("oracle=independent literal transcription of prompt ASCII ranges")
    print(f"named_case_count={len(named_cases)}")
    print(f"total_unique_inputs={len(generated)}")
    print(f"expected_outcomes={outcome_counts}")
    print(f"candidate_vs_contract_mismatches={len(candidate_contract_mismatches)}")
    print(f"candidate_vs_canonical_mismatches={len(candidate_canonical_mismatches)}")
    print(f"canonical_vs_contract_mismatches={len(canonical_contract_mismatches)}")
    print("candidate_vs_canonical_first_20:")
    for value, candidate_result, canonical_result in candidate_canonical_mismatches[:20]:
        print(
            f"  {value!r}: candidate={candidate_result!r} "
            f"canonical={canonical_result!r}"
        )
    print("canonical_vs_contract_first_20:")
    for value, canonical_result, expected in canonical_contract_mismatches[:20]:
        print(
            f"  {value!r}: canonical={canonical_result!r} contract={expected!r}"
        )
    if candidate_contract_mismatches:
        print("candidate_vs_contract_first_20:")
        for value, actual, expected in candidate_contract_mismatches[:20]:
            print(f"  {value!r}: candidate={actual!r} contract={expected!r}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
