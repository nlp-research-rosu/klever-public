#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential for HumanEval 153."""

from __future__ import annotations

import importlib.util
import random
import sys
import unicodedata
from pathlib import Path
from typing import Any, Callable


def load_entry(path: str, module_name: str) -> Callable[[str, list[str]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


def outcome(function: Callable[..., Any], *args: Any) -> tuple[str, str]:
    try:
        return ("return", repr(function(*args)))
    except Exception as error:  # compared as an observable outcome
        return ("raise", f"{type(error).__name__}: {error}")


def main() -> int:
    canonical = load_entry("/reference/canonical.py", "trusted_canonical")
    candidate = load_entry("/candidate/solution.py", "candidate_solution")

    directed: list[tuple[str, list[str]]] = [
        ("Slices", ["SErviNGSliCes", "Cheese", "StuFfed"]),
        ("my_class", ["AA", "Be", "CC"]),
        ("C", ["", "A", "a"]),
        ("C", ["a", "A"]),
        ("C", ["A", "B"]),  # tie retains first
        ("C", ["a", "b"]),  # negative tie retains first
        ("C", ["1!?", "A", "a"]),
        ("", [""]),
        ("ΩClass", ["Ω", "ω", "AA"]),
        ("C", ["A", "\N{ROMAN NUMERAL ONE}\N{ROMAN NUMERAL ONE}"]),
        ("C", ["a", "\N{SMALL ROMAN NUMERAL ONE}\N{SMALL ROMAN NUMERAL ONE}"]),
        ("C", []),  # canonical's own implementation does not define this case
    ]

    nonalpha_cased: list[str] = []
    for codepoint in range(sys.maxunicode + 1):
        character = chr(codepoint)
        if (character.isupper() or character.islower()) and not character.isalpha():
            nonalpha_cased.append(character)
            if len(nonalpha_cased) == 20:
                break
    print(f"nonalpha_cased_sample_count={len(nonalpha_cased)}")
    for character in nonalpha_cased:
        print(
            "nonalpha_cased "
            f"U+{ord(character):04X} "
            f"name={unicodedata.name(character, '<unnamed>')!r} "
            f"category={unicodedata.category(character)} "
            f"isalpha={character.isalpha()} "
            f"isupper={character.isupper()} "
            f"islower={character.islower()}"
        )

    # Generate score boundaries and both sides of each branch. Include Unicode
    # letters as well as CPython-cased, non-alphabetic characters.
    rng = random.Random(153_20260730)
    alphabet = (
        "ABCXYZabcxyz019_-.!?"
        "ΩΔωδЖж"
        "\N{ROMAN NUMERAL ONE}\N{SMALL ROMAN NUMERAL ONE}"
        "\N{CIRCLED LATIN CAPITAL LETTER A}\N{CIRCLED LATIN SMALL LETTER A}"
    )
    generated: list[tuple[str, list[str]]] = []
    for _ in range(2500):
        class_name = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 7)))
        extension_count = rng.randrange(1, 9)
        extensions = [
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 13)))
            for _ in range(extension_count)
        ]
        generated.append((class_name, extensions))

    cases = directed + generated
    mismatches: list[
        tuple[int, str, list[str], tuple[str, str], tuple[str, str]]
    ] = []
    for index, (class_name, extensions) in enumerate(cases):
        expected = outcome(canonical, class_name, extensions)
        actual = outcome(candidate, class_name, extensions)
        if expected != actual:
            mismatches.append((index, class_name, extensions, expected, actual))

    print(
        f"directed_cases={len(directed)} generated_cases={len(generated)} "
        f"total_cases={len(cases)} mismatches={len(mismatches)}"
    )
    for mismatch in mismatches[:30]:
        index, class_name, extensions, expected, actual = mismatch
        print(
            f"MISMATCH index={index} class_name={class_name!r} "
            f"extensions={extensions!r} canonical={expected!r} candidate={actual!r}"
        )
    if len(mismatches) > 30:
        print(f"MISMATCH_OUTPUT_TRUNCATED remaining={len(mismatches) - 30}")

    # A canonical-domain mismatch is expected to make this audit probe fail.
    canonical_domain_mismatches = [
        mismatch for mismatch in mismatches if mismatch[2]  # nonempty extensions
    ]
    print(f"canonical_domain_mismatches={len(canonical_domain_mismatches)}")
    return 1 if canonical_domain_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
