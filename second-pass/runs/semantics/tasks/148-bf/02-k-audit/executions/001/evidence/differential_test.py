#!/usr/bin/env python3
"""Independent differential and contract-oracle tests for HumanEval 148."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
from pathlib import Path
from typing import Callable


PLANETS = (
    "Mercury",
    "Venus",
    "Earth",
    "Mars",
    "Jupiter",
    "Saturn",
    "Uranus",
    "Neptune",
)


def load_entry(path: Path, module_name: str) -> Callable[[str, str], tuple[str, ...]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.bf


def contract_oracle(planet1: str, planet2: str) -> tuple[str, ...]:
    """Independent index-free formulation of the open orbital interval."""
    if planet1 not in PLANETS or planet2 not in PLANETS:
        return ()
    if planet1 == planet2:
        return ()
    inside = False
    answer: list[str] = []
    for name in PLANETS:
        if name == planet1 or name == planet2:
            if inside:
                break
            inside = True
        elif inside:
            answer.append(name)
    return tuple(answer)


def main() -> None:
    scratch = Path("/tmp/audit-work/148-bf-audit")
    canonical = load_entry(scratch / "canonical.py", "trusted_canonical_148")
    generated = load_entry(scratch / "solution.py", "candidate_solution_148")

    documented = [
        ("Jupiter", "Neptune"),
        ("Earth", "Mercury"),
        ("Mercury", "Uranus"),
    ]
    boundary = [
        ("Mercury", "Mercury"),
        ("Neptune", "Neptune"),
        ("Mercury", "Venus"),
        ("Venus", "Mercury"),
        ("Mercury", "Neptune"),
        ("Neptune", "Mercury"),
        ("", ""),
        ("", "Mercury"),
        ("Mercury", ""),
        ("Pluto", "Earth"),
        ("Earth", "Pluto"),
        ("mercury", "Mercury"),
        ("Mercury", "Neptune "),
        ("☿", "♆"),
        ("Mercury\x00", "Neptune"),
    ]

    cases = list(documented)
    cases.extend(boundary)
    cases.extend(itertools.product(PLANETS, repeat=2))

    invalid = [
        "",
        "M",
        "Mercur",
        "Mercury ",
        " mercury",
        "mercury",
        "Pluto",
        "Sun",
        "Earth\n",
        "☿",
        "\x00",
    ]
    cases.extend(itertools.product(invalid, PLANETS))
    cases.extend(itertools.product(PLANETS, invalid))
    cases.extend(itertools.product(invalid, invalid))

    rng = random.Random(148)
    alphabet = string.ascii_letters + string.digits + " _-\u2600\u263f"
    generated_invalid: list[str] = []
    while len(generated_invalid) < 200:
        length = rng.randrange(0, 20)
        value = "".join(rng.choice(alphabet) for _ in range(length))
        if value not in PLANETS:
            generated_invalid.append(value)
    for value in generated_invalid:
        cases.append((value, rng.choice(PLANETS)))
        cases.append((rng.choice(PLANETS), value))
        cases.append((value, rng.choice(generated_invalid)))

    unique_cases = list(dict.fromkeys(cases))
    mismatches = []
    for planet1, planet2 in unique_cases:
        expected = contract_oracle(planet1, planet2)
        canonical_result = canonical(planet1, planet2)
        generated_result = generated(planet1, planet2)
        if not (canonical_result == generated_result == expected):
            mismatches.append(
                (
                    repr(planet1),
                    repr(planet2),
                    repr(expected),
                    repr(canonical_result),
                    repr(generated_result),
                )
            )

    print(f"documented_examples={len(documented)}")
    print("valid_ordered_pairs=64")
    print(f"fixed_invalid_strings={len(invalid)}")
    print(f"seeded_generated_invalid_strings={len(generated_invalid)} seed=148")
    print(f"unique_cases={len(unique_cases)}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH", mismatch)
    assert not mismatches
    print("DIFFERENTIAL_TEST=PASS")


if __name__ == "__main__":
    main()
