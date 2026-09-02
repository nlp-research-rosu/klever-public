#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs submitted solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
from pathlib import Path
import random
import string
import sys


ROOT = Path("/tmp/audit-work/118-get-closest-vowel")
CANONICAL = ROOT / "reference" / "canonical.py"
CANDIDATE = ROOT / "candidate-src" / "solution.py"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def outcome(function, word: str):
    try:
        return ("return", function(word))
    except BaseException as error:  # record semantic divergence, including exceptions
        return ("raise", type(error).__name__, str(error))


def main() -> int:
    canonical = load_entry(CANONICAL, "trusted_canonical_118")
    candidate = load_entry(CANDIDATE, "submitted_solution_118")

    curated = [
        # Prompt examples.
        "yogurt",
        "FULL",
        "quick",
        "ab",
        # Empty and length boundary.
        "",
        "b",
        "bb",
        "bbb",
        "bab",
        "baB",
        "baa",
        "aab",
        "aba",
        "Aba",
        # Recursive-window shapes and rightmost-choice checks.
        "babcc",
        "baccb",
        "bacae",
        "cbaad",
        "zebracadabra",
        "BCDFuGH",
        "aeiou",
        "AEIOU",
    ]

    generated = []
    category_alphabet = "aAbB"
    for length in range(0, 9):
        generated.extend(
            "".join(chars)
            for chars in itertools.product(category_alphabet, repeat=length)
        )

    rng = random.Random(118_20260726)
    random_cases = [
        "".join(rng.choice(string.ascii_letters) for _ in range(rng.randrange(0, 81)))
        for _ in range(20_000)
    ]

    # The source contract has no length bound. Vowel-free words force every
    # recursive call and expose the submitted algorithm's CPython recursion limit.
    long_cases = ["b" * length for length in (900, 950, 975, 990, 1000, 1050, 1200)]

    cases = curated + generated + random_cases + long_cases
    digest = hashlib.sha256()
    for word in cases:
        digest.update(len(word).to_bytes(8, "big"))
        digest.update(word.encode("ascii"))

    mismatches = []
    for index, word in enumerate(cases):
        left = canonical(word)
        right = outcome(candidate, word)
        if right != ("return", left):
            mismatches.append((index, len(word), word[:80], ("return", left), right))

    print(f"canonical={CANONICAL}")
    print(f"candidate={CANDIDATE}")
    print(f"curated_cases={len(curated)}")
    print("exhaustive_alphabet='aAbB'")
    print("exhaustive_lengths=0..8")
    print(f"exhaustive_cases={len(generated)}")
    print("random_seed=11820260726")
    print("random_alphabet=string.ascii_letters")
    print("random_lengths=0..80")
    print(f"random_cases={len(random_cases)}")
    print(f"long_lengths={[len(word) for word in long_cases]}")
    print(f"all_inputs_sha256={digest.hexdigest()}")
    print(f"total_cases={len(cases)}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH={mismatch!r}")
    if len(mismatches) > 20:
        print(f"mismatches_omitted={len(mismatches) - 20}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
