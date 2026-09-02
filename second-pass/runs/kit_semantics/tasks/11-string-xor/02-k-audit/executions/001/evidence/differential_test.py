#!/usr/bin/env python3
"""Independent differential test of trusted canonical versus candidate Python."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_xor


def bit_strings_through(max_length: int) -> list[str]:
    values: list[str] = []
    for length in range(max_length + 1):
        values.extend("".join(bits) for bits in itertools.product("01", repeat=length))
    return values


def main() -> int:
    canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
    candidate = load_function("candidate_solution", Path("/candidate/solution.py"))

    named_cases = [
        ("documented_example", "010", "110", "100"),
        ("both_empty", "", "", ""),
        ("left_empty", "", "101", ""),
        ("right_empty", "101", "", ""),
        ("equal_zero", "0", "0", "0"),
        ("zero_one", "0", "1", "1"),
        ("one_zero", "1", "0", "1"),
        ("equal_one", "1", "1", "0"),
        ("left_shorter", "01", "10110", "11"),
        ("right_shorter", "10110", "01", "11"),
        ("alternating", "01010101", "10101010", "11111111"),
    ]
    mismatches: list[str] = []
    checked = 0
    for label, a, b, expected in named_cases:
        trusted = canonical(a, b)
        generated = candidate(a, b)
        checked += 1
        print(
            f"NAMED {label} a={a!r} b={b!r}"
            f" expected={expected!r} canonical={trusted!r} candidate={generated!r}"
        )
        if trusted != expected or generated != expected:
            mismatches.append(
                f"{label}: expected={expected!r}, canonical={trusted!r},"
                f" candidate={generated!r}"
            )

    values = bit_strings_through(7)
    exhaustive_pairs = 0
    for a in values:
        for b in values:
            trusted = canonical(a, b)
            generated = candidate(a, b)
            exhaustive_pairs += 1
            checked += 1
            if trusted != generated:
                mismatches.append(
                    f"exhaustive a={a!r} b={b!r}:"
                    f" canonical={trusted!r}, candidate={generated!r}"
                )
                if len(mismatches) >= 20:
                    break
        if len(mismatches) >= 20:
            break

    rng = random.Random(0x11A0D17)
    random_pairs = 1000
    max_random_length = 256
    for index in range(random_pairs):
        a = "".join(rng.choice("01") for _ in range(rng.randrange(max_random_length + 1)))
        b = "".join(rng.choice("01") for _ in range(rng.randrange(max_random_length + 1)))
        trusted = canonical(a, b)
        generated = candidate(a, b)
        checked += 1
        if trusted != generated:
            mismatches.append(
                f"random index={index} len(a)={len(a)} len(b)={len(b)}:"
                f" canonical={trusted!r}, candidate={generated!r}"
            )
            if len(mismatches) >= 20:
                break

    print(
        "SUMMARY"
        f" named_cases={len(named_cases)}"
        f" exhaustive_values={len(values)}"
        f" exhaustive_pairs={exhaustive_pairs}"
        f" random_pairs={random_pairs}"
        f" random_max_length={max_random_length}"
        f" total_checks={checked}"
        f" mismatches={len(mismatches)}"
    )
    for mismatch in mismatches:
        print(f"MISMATCH {mismatch}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
