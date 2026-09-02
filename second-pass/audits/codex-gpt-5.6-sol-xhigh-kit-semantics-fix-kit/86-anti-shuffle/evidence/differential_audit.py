#!/usr/bin/env python3
"""Independent differential audit for HumanEval 86 anti_shuffle."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType


ROOT = Path("/tmp/audit-work/86-anti-shuffle")
SEED = 860726


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load_module("trusted_canonical", ROOT / "canonical.py")
    generated = load_module("submitted_solution", ROOT / "solution.py")

    named_cases = [
        ("documented_Hi", "Hi"),
        ("documented_hello", "hello"),
        ("documented_multiword", "Hello World!!!"),
        ("empty", ""),
        ("single_space", " "),
        ("adjacent_spaces", "  "),
        ("leading_space", " ba"),
        ("trailing_space", "ba "),
        ("space_between", "ba ab"),
        ("already_sorted", "ab"),
        ("reverse_sorted", "ba"),
        ("equal_chars", "aa"),
        ("insert_before_first", "ba"),
        ("insert_after_all", "ab"),
        ("ascii_low_high", "\x7f\x00 ~!"),
        ("tab_is_character", "b\ta"),
        ("newline_is_character", "b\na"),
        ("unicode_latin", "éa é"),
        ("unicode_mixed", "🙂Ωa 🙂"),
        ("unicode_extremes", "\U0010ffff\x80a"),
    ]

    cases: list[tuple[str, str]] = list(named_cases)

    exhaustive_alphabet = " aA!~\x00\x7f"
    for length in range(6):
        for values in itertools.product(exhaustive_alphabet, repeat=length):
            cases.append((f"ascii_exhaustive_len_{length}", "".join(values)))

    unicode_alphabet = " aéΩ🙂"
    for length in range(5):
        for values in itertools.product(unicode_alphabet, repeat=length):
            cases.append((f"unicode_exhaustive_len_{length}", "".join(values)))

    rng = random.Random(SEED)
    random_alphabet = [
        chr(code)
        for code in list(range(128))
        + [0x80, 0xFF, 0x100, 0x3A9, 0x20AC, 0x1F642, 0x10FFFF]
    ]
    for index in range(5000):
        length = rng.randrange(0, 65)
        value = "".join(rng.choice(random_alphabet) for _ in range(length))
        cases.append((f"deterministic_random_{index}", value))

    mismatches: list[dict[str, str]] = []
    input_digest = hashlib.sha256()
    for label, value in cases:
        encoded = json.dumps([label, value], ensure_ascii=True, separators=(",", ":"))
        input_digest.update(encoded.encode("ascii"))
        expected = canonical.anti_shuffle(value)
        actual = generated.anti_shuffle(value)
        if expected != actual:
            mismatches.append(
                {
                    "label": label,
                    "input": repr(value),
                    "canonical": repr(expected),
                    "generated": repr(actual),
                }
            )

    helper_cases = [
        ("", "a"),
        ("b", "a"),
        ("a", "b"),
        ("a", "a"),
        ("abz", "m"),
        ("\x00\x7f", " "),
        ("aΩ", "é"),
    ]
    helper_mismatches: list[dict[str, str]] = []
    for word, char in helper_cases:
        expected = "".join(sorted(word + char))
        actual = generated.insert_char(word, char)
        if expected != actual:
            helper_mismatches.append(
                {
                    "word": repr(word),
                    "char": repr(char),
                    "expected": repr(expected),
                    "actual": repr(actual),
                }
            )

    for label, value in named_cases:
        print(
            json.dumps(
                {
                    "label": label,
                    "input": value,
                    "canonical": canonical.anti_shuffle(value),
                    "generated": generated.anti_shuffle(value),
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
    print(f"seed={SEED}")
    print(f"entry_cases={len(cases)}")
    print(f"entry_input_sha256={input_digest.hexdigest()}")
    print(f"entry_mismatches={len(mismatches)}")
    print(f"helper_cases={len(helper_cases)}")
    print(f"helper_mismatches={len(helper_mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], ensure_ascii=True, sort_keys=True))
    if helper_mismatches:
        print(json.dumps(helper_mismatches, ensure_ascii=True, sort_keys=True))
    return 1 if mismatches or helper_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
