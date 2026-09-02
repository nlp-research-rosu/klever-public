#!/usr/bin/env python3
"""Independent differential test for HumanEval 153.

The trusted canonical and submitted solution are imported from paths supplied
on the command line.  The random corpus is reproducible from SEED and includes
ASCII letters, uncased characters, Unicode alphabetic letters, and Unicode
cased non-letters.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


SEED = 153_2026
RANDOM_CASES = 500
ALPHABET = "AaZz09-_.ÉéⅣⅳ"


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, class_name, extensions):
    try:
        return ("return", function(class_name, extensions))
    except Exception as error:  # exception type is observable for boundary cases
        return ("raise", type(error).__name__, str(error))


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential.py TRUSTED_CANONICAL SUBMITTED_SOLUTION")
        return 2

    canonical = load_module("trusted_canonical", sys.argv[1]).Strongest_Extension
    submitted = load_module("submitted_solution", sys.argv[2]).Strongest_Extension

    fixed = [
        ("prompt-worked", "Slices", ["SErviNGSliCes", "Cheese", "StuFfed"]),
        ("prompt-tie", "my_class", ["AA", "Be", "CC"]),
        ("empty-extension-list", "C", []),
        ("single-empty-name", "C", [""]),
        ("single-extension", "C", ["Zz"]),
        ("empty-class", "", ["A", "b"]),
        ("greater-branch", "C", ["abc", "AB", "A-b"]),
        ("equal-branch", "C", ["AA", "BB"]),
        ("less-branch", "C", ["AA", "a"]),
        ("upper-lower-uncased", "C", ["a-1", "--", "A!"]),
        ("all-negative", "C", ["abcd", "a", "xy"]),
        ("unicode-letters", "Κλάση", ["A", "ÉÉ"]),
        ("unicode-cased-nonletter", "C", ["A", "ⅣⅣ"]),
        ("unicode-cased-nonletter-lower", "C", ["a", "ⅳ"]),
    ]

    rng = random.Random(SEED)
    generated = []
    for index in range(RANDOM_CASES):
        class_name = "".join(rng.choice(ALPHABET) for _ in range(rng.randrange(0, 7)))
        count = rng.randrange(1, 6)
        extensions = [
            "".join(rng.choice(ALPHABET) for _ in range(rng.randrange(0, 7)))
            for _ in range(count)
        ]
        generated.append((f"generated-{index:03d}", class_name, extensions))

    cases = fixed + generated
    serialized = json.dumps(cases, ensure_ascii=False, separators=(",", ":")).encode()
    mismatches = []
    for label, class_name, extensions in cases:
        trusted = outcome(canonical, class_name, extensions)
        candidate = outcome(submitted, class_name, extensions)
        if trusted != candidate:
            mismatches.append((label, class_name, extensions, trusted, candidate))

    print(f"seed={SEED}")
    print(f"fixed_cases={len(fixed)} generated_cases={len(generated)} total_cases={len(cases)}")
    print(f"case_corpus_sha256={hashlib.sha256(serialized).hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH " + repr(mismatch))

    roman = next(case for case in mismatches if case[0] == "unicode-cased-nonletter")
    print("required_false-result-witness=" + repr(roman))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
