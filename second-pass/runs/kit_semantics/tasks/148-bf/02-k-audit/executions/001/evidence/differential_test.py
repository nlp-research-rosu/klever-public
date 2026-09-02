#!/usr/bin/env python3
"""Independent differential test for HumanEval 148.

The oracle uses an index map plus enumeration and does not reuse either
implementation's tuple slicing.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/fresh")
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
DOCUMENTED = (
    ("Jupiter", "Neptune", ("Saturn", "Uranus")),
    ("Earth", "Mercury", ("Venus",)),
    (
        "Mercury",
        "Uranus",
        ("Venus", "Earth", "Mars", "Jupiter", "Saturn"),
    ),
)


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.bf


def oracle(planet1: str, planet2: str) -> tuple[str, ...]:
    positions = {name: index for index, name in enumerate(PLANETS)}
    if planet1 not in positions or planet2 not in positions:
        return ()
    low = min(positions[planet1], positions[planet2])
    high = max(positions[planet1], positions[planet2])
    return tuple(
        name
        for index, name in enumerate(PLANETS)
        if low < index < high
    )


def main() -> int:
    canonical = load_function(SCRATCH / "canonical.py", "trusted_canonical_148")
    generated = load_function(SCRATCH / "solution.py", "generated_solution_148")

    fixed_invalid = (
        "",
        "Pluto",
        "mercury",
        "MERCURY",
        " Mercury",
        "Neptune ",
        "Sun",
        "Earth\0",
        "🪐",
        "\N{MERCURY}",
        "é",
    )
    mutations = tuple(
        variant
        for name in PLANETS
        for variant in (
            name.lower(),
            name.upper(),
            name[:-1],
            name + "x",
            "x" + name,
        )
    )
    exhaustive_short = tuple(
        "".join(chars)
        for length in range(5)
        for chars in itertools.product("Me r", repeat=length)
    )
    corpus = tuple(dict.fromkeys(PLANETS + fixed_invalid + mutations + exhaustive_short))

    cases: list[tuple[str, str, str]] = []
    for planet1, planet2, _ in DOCUMENTED:
        cases.append(("documented", planet1, planet2))
    for planet1, planet2 in itertools.product(PLANETS, repeat=2):
        cases.append(("all-valid-pairs", planet1, planet2))
    for invalid in corpus:
        for planet in PLANETS:
            cases.append(("invalid-first", invalid, planet))
            cases.append(("invalid-second", planet, invalid))
        cases.append(("same-generated-string", invalid, invalid))

    rng = random.Random(148)
    alphabet = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz"
        "0123456789 _-\0é🪐"
    )
    generated_strings = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 25)))
        for _ in range(1000)
    ]
    mixed_pool = corpus + tuple(generated_strings)
    for _ in range(5000):
        cases.append(
            (
                "seeded-generated-pair",
                rng.choice(mixed_pool),
                rng.choice(mixed_pool),
            )
        )

    mismatches: list[tuple[str, str, str, object, object, object]] = []
    category_counts: dict[str, int] = {}
    seen: set[tuple[str, str, str]] = set()
    input_pairs: set[tuple[str, str]] = set()
    for category, planet1, planet2 in cases:
        key = (category, planet1, planet2)
        if key in seen:
            continue
        seen.add(key)
        input_pairs.add((planet1, planet2))
        category_counts[category] = category_counts.get(category, 0) + 1
        expected = oracle(planet1, planet2)
        trusted_result = canonical(planet1, planet2)
        generated_result = generated(planet1, planet2)
        if (
            trusted_result != expected
            or generated_result != expected
            or type(trusted_result) is not tuple
            or type(generated_result) is not tuple
        ):
            mismatches.append(
                (
                    category,
                    repr(planet1),
                    repr(planet2),
                    trusted_result,
                    generated_result,
                    expected,
                )
            )

    for planet1, planet2, expected in DOCUMENTED:
        assert canonical(planet1, planet2) == expected
        assert generated(planet1, planet2) == expected

    print(f"corpus_strings={len(corpus)}")
    for category, count in sorted(category_counts.items()):
        print(f"category[{category}]={count}")
    print(f"distinct_labeled_records={len(seen)}")
    print(f"unique_input_pairs={len(input_pairs)}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
