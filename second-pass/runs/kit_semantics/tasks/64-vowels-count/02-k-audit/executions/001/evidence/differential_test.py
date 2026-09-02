#!/usr/bin/env python3
"""Independent differential test for HumanEval/64.

The trusted and generated modules are loaded from explicit paths.  The
documented nonempty-word domain is checked separately from the empty-string
boundary because the trusted canonical implementation indexes s[-1].
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


def outcome(fn, text: str):
    try:
        return ("return", fn(text))
    except Exception as exc:  # boundary behavior is part of the comparison
        return ("raise", type(exc).__name__, str(exc))


def main() -> int:
    root = Path("/tmp/audit-work/reconstruction")
    canonical = load_entry(root / "canonical.py", "trusted_canonical")
    generated = load_entry(root / "solution.py", "generated_solution")

    directed = [
        "abcde",
        "ACEDY",
        "a",
        "A",
        "b",
        "y",
        "Y",
        "ay",
        "ya",
        "YY",
        "Yy",
        "xyz",
        "rhythm",
        "aeiou",
        "AEIOU",
        "bcdfg",
        "aYe",
        "hello!",
        "123y",
        "éY",
        "🙂y",
    ]
    alphabet = "aeiouAEIOUyYbcdfgxyzXYZ012!-é🙂"
    exhaustive = [
        "".join(chars)
        for length in range(1, 4)
        for chars in itertools.product(alphabet[:14], repeat=length)
    ]
    rng = random.Random(640064)
    random_cases = [
        "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 64)))
        for _ in range(10_000)
    ]
    intended_cases = directed + exhaustive + random_cases

    mismatches = []
    for text in intended_cases:
        left = outcome(canonical, text)
        right = outcome(generated, text)
        if left != right:
            mismatches.append((text, left, right))
            if len(mismatches) >= 20:
                break

    empty_left = outcome(canonical, "")
    empty_right = outcome(generated, "")

    print("directed_cases=", len(directed), sep="")
    print("exhaustive_alphabet=", repr(alphabet[:14]), sep="")
    print("exhaustive_lengths=1..3")
    print("exhaustive_cases=", len(exhaustive), sep="")
    print("random_seed=640064")
    print("random_alphabet=", repr(alphabet), sep="")
    print("random_lengths=1..64")
    print("random_cases=", len(random_cases), sep="")
    print("intended_nonempty_total=", len(intended_cases), sep="")
    print("intended_nonempty_mismatches=", len(mismatches), sep="")
    for mismatch in mismatches:
        print("MISMATCH", repr(mismatch))
    print("empty_canonical=", repr(empty_left), sep="")
    print("empty_generated=", repr(empty_right), sep="")
    print("empty_outcomes_equal=", empty_left == empty_right, sep="")

    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
