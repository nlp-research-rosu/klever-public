#!/usr/bin/env python3
"""Independent differential test: trusted canonical bf vs candidate solution bf."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
from pathlib import Path


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


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.bf


def main() -> None:
    canonical = load_function("trusted_canonical_148", Path("/reference/canonical.py"))
    generated = load_function(
        "candidate_solution_148", Path("/tmp/audit-work/candidate-src/solution.py")
    )

    examples = [
        ("Jupiter", "Neptune", ("Saturn", "Uranus")),
        ("Earth", "Mercury", ("Venus",)),
        (
            "Mercury",
            "Uranus",
            ("Venus", "Earth", "Mars", "Jupiter", "Saturn"),
        ),
    ]
    for first, second, expected in examples:
        assert canonical(first, second) == expected
        assert generated(first, second) == expected
        print(f"example {first!r}, {second!r} -> {expected!r}")

    # Every valid branch partition, including equal and adjacent endpoints.
    cases = list(itertools.product(PLANETS, repeat=2))

    boundary_invalid = (
        "",
        " ",
        "Mercury ",
        " mercury",
        "mercury",
        "NEPTUNE",
        "Pluto",
        "\x00",
        "\n",
        '"',
        "\\",
        "☿",
        "🪐",
        "a" * 1024,
    )
    # Exercise both invalid-argument partitions and both-invalid cases.
    cases.extend(itertools.product(boundary_invalid, PLANETS))
    cases.extend(itertools.product(PLANETS, boundary_invalid))
    cases.extend(itertools.product(boundary_invalid, boundary_invalid))

    rng = random.Random(148)
    alphabet = string.ascii_letters + string.digits + " _-\"\\☿"
    generated_invalid: list[str] = []
    while len(generated_invalid) < 500:
        value = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 25)))
        if value not in PLANETS:
            generated_invalid.append(value)
    cases.extend(zip(generated_invalid[::2], generated_invalid[1::2], strict=True))
    cases.extend((value, rng.choice(PLANETS)) for value in generated_invalid[:100])
    cases.extend((rng.choice(PLANETS), value) for value in generated_invalid[100:200])

    mismatches = []
    for first, second in cases:
        expected = canonical(first, second)
        actual = generated(first, second)
        if actual != expected:
            mismatches.append((first, second, expected, actual))

    print(f"total documented/boundary/generated pairs checked={len(cases) + len(examples)}")
    print(f"all 64 ordered valid-name pairs checked={64}")
    print(f"boundary invalid strings={len(boundary_invalid)}")
    print(f"seeded generated invalid strings={len(generated_invalid)} seed=148")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print(f"MISMATCH {mismatch!r}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
