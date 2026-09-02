#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


TRUSTED = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/78-hex-key/candidate-src/solution.py")
RESULTS = Path("/audit-output/evidence/differential-inputs-and-results.jsonl")
HEX = "0123456789ABCDEF"
EXAMPLES = {
    "AB": 1,
    "1077E": 2,
    "ABED1A33": 4,
    "123456789ABCDEF0": 6,
    "2020": 2,
}


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.hex_key


def main() -> int:
    canonical = load_entry("trusted_canonical", TRUSTED)
    generated = load_entry("generated_solution", GENERATED)

    fixed = ["", *EXAMPLES]
    one_char_boundaries = list(HEX)
    exhaustive = [
        "".join(chars)
        for length in range(5)
        for chars in itertools.product(HEX, repeat=length)
    ]
    rng = random.Random(780078)
    random_cases = [
        "".join(rng.choice(HEX) for _ in range(rng.randint(5, 256)))
        for _ in range(300)
    ]

    ordered: list[tuple[str, str]] = []
    seen: set[str] = set()
    for category, values in (
        ("documented-and-empty", fixed),
        ("single-digit-boundaries", one_char_boundaries),
        ("exhaustive-length-0-through-4", exhaustive),
        ("seeded-length-5-through-256", random_cases),
    ):
        for value in values:
            if value not in seen:
                seen.add(value)
                ordered.append((category, value))

    mismatches = 0
    documented_failures = 0
    with RESULTS.open("w", encoding="utf-8") as stream:
        for category, value in ordered:
            expected = canonical(value)
            actual = generated(value)
            match = expected == actual
            if not match:
                mismatches += 1
            if value in EXAMPLES and expected != EXAMPLES[value]:
                documented_failures += 1
            stream.write(
                json.dumps(
                    {
                        "category": category,
                        "input": value,
                        "canonical": expected,
                        "generated": actual,
                        "match": match,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
                + "\n"
            )

    print(f"trusted={TRUSTED}")
    print(f"generated={GENERATED}")
    print(f"results={RESULTS}")
    print("domain=uppercase hexadecimal strings")
    print("exhaustive_lengths=0..4")
    print("random_seed=780078")
    print("random_case_count=300")
    print("random_length_range=5..256")
    print(f"unique_case_count={len(ordered)}")
    print(f"mismatches={mismatches}")
    print(f"documented_example_oracle_failures={documented_failures}")
    return 1 if mismatches or documented_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
