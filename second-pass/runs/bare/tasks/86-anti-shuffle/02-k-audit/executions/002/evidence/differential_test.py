#!/usr/bin/env python3
"""Independent differential test: trusted canonical.py vs submitted solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
from pathlib import Path
from types import ModuleType


CANONICAL_PATH = Path("/tmp/audit-work/anti-shuffle/trusted/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/anti-shuffle/solution.py")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, value: str) -> tuple[str, str]:
    try:
        return ("return", function(value))
    except BaseException as error:  # The exception is part of the observed outcome.
        return ("raise", f"{type(error).__name__}: {error}")


def describe(value: str) -> str:
    if len(value) <= 120:
        return repr(value)
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"<len={len(value)} utf8_sha256={digest}>"


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL_PATH).anti_shuffle
    generated = load_module("submitted_solution", GENERATED_PATH).anti_shuffle

    named_cases = [
        ("example_hi", "Hi"),
        ("example_hello", "hello"),
        ("example_prompt", "Hello World!!!"),
        ("empty", ""),
        ("one_space", " "),
        ("leading_trailing_repeated_spaces", "  ba  dc "),
        ("one_char", "x"),
        ("equal_insert_branch", "aa"),
        ("less_insert_branch", "ba"),
        ("greater_recursive_insert_branch", "ab"),
        ("punctuation_and_digits", "z9! A0?"),
        ("non_space_whitespace", "b\ta\n"),
        ("nul", "b\x00a"),
        ("unicode_bmp", "éA Ωβ"),
        ("unicode_astral", "😀a🦊"),
        ("combining", "e\u0301 é"),
    ]
    exhaustive = [
        "".join(chars)
        for length in range(6)
        for chars in itertools.product(" ab!", repeat=length)
    ]
    rng = random.Random(860026)
    alphabet = " abcXYZ09!?\t\n\x00éΩβ😀🦊\u0301"
    random_cases = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 101)))
        for _ in range(3000)
    ]

    normal_mismatches: list[tuple[str, str, object, object]] = []
    normal_count = 0
    for label, value in named_cases:
        normal_count += 1
        expected = outcome(canonical, value)
        actual = outcome(generated, value)
        print(
            f"NAMED {label} input={describe(value)} "
            f"canonical={expected!r} generated={actual!r}"
        )
        if expected != actual:
            normal_mismatches.append((label, value, expected, actual))

    for source, cases in (("exhaustive", exhaustive), ("random", random_cases)):
        for index, value in enumerate(cases):
            normal_count += 1
            expected = outcome(canonical, value)
            actual = outcome(generated, value)
            if expected != actual:
                normal_mismatches.append(
                    (f"{source}[{index}]", value, expected, actual)
                )
    print(
        f"NORMAL_SUMMARY cases={normal_count} "
        f"mismatches={len(normal_mismatches)}"
    )
    for label, value, expected, actual in normal_mismatches[:20]:
        print(
            f"NORMAL_MISMATCH {label} input={describe(value)} "
            f"canonical={expected!r} generated={actual!r}"
        )

    stress_cases = [
        ("repeated_900", "a" * 900),
        ("repeated_1100", "a" * 1100),
        ("ascending_unicode_400", "".join(chr(0x1000 + i) for i in range(400))),
        ("ascending_unicode_500", "".join(chr(0x1000 + i) for i in range(500))),
        ("ascending_unicode_700", "".join(chr(0x1000 + i) for i in range(700))),
    ]
    stress_mismatches = []
    for label, value in stress_cases:
        expected = outcome(canonical, value)
        actual = outcome(generated, value)
        print(
            f"STRESS {label} input={describe(value)} "
            f"canonical_kind={expected[0]} generated={actual!r}"
        )
        if expected != actual:
            stress_mismatches.append((label, value, expected, actual))
    print(
        f"STRESS_SUMMARY cases={len(stress_cases)} "
        f"mismatches={len(stress_mismatches)}"
    )

    total_mismatches = len(normal_mismatches) + len(stress_mismatches)
    print(f"TOTAL_MISMATCHES={total_mismatches}")
    return 1 if total_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
