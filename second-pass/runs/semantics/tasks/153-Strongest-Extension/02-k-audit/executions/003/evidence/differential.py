#!/usr/bin/env python3
"""Independent source-level differential audit for HumanEval 153."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_function(
    "audited_candidate", Path("/tmp/audit-work/candidate/solution.py")
)


def independent_oracle(class_name: str, extensions: list[str]) -> str:
    if not extensions:
        raise IndexError("empty extension list")

    def strength(extension: str) -> int:
        upper = sum(character.isalpha() and character.isupper() for character in extension)
        lower = sum(character.isalpha() and character.islower() for character in extension)
        return upper - lower

    best_index = max(range(len(extensions)), key=lambda index: strength(extensions[index]))
    return class_name + "." + extensions[best_index]


def outcome(function, class_name: str, extensions: list[str]):
    try:
        return ("return", function(class_name, list(extensions)))
    except Exception as error:  # boundary comparison intentionally records failures
        return ("raise", type(error).__name__)


curated = [
    ("Slices", ["SErviNGSliCes", "Cheese", "StuFfed"]),
    ("my_class", ["AA", "Be", "CC"]),
    ("", [""]),
    ("C", [""]),
    ("Single", ["Aa"]),
    ("Tie", ["AA", "CC"]),
    ("GreaterAtSecond", ["a", "A"]),
    ("LowerAtSecond", ["A", "a"]),
    ("LateMaximum", ["a", "Aa", "AAA", "AA"]),
    ("FourWayTie", ["AA", "BB", "CC", "DD"]),
    ("LongList", ["abc", "A", "zz", "ZZ", "", "AaA"]),
    ("Unicode", ["é", "É", "ß", "ΩΩ", "δ"]),
    ("Punctuation", ["!!!", "A-1", "a_2", ""]),
    ("EmptyBoundary", []),
]

alphabet = "aAZz09_-.éÉΩδß"
small_names = [
    "".join(chars)
    for length in range(3)
    for chars in itertools.product(alphabet[:6], repeat=length)
]

rng = random.Random(153)
generated = []
for _ in range(1000):
    class_name = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))
    count = rng.randrange(1, 9)
    extensions = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 13)))
        for _ in range(count)
    ]
    generated.append((class_name, extensions))

# Deterministically cover lengths 1 through 8 with many repeated/equal-strength names.
for length in range(1, 9):
    for offset in range(40):
        names = [
            small_names[(offset * (index + 1) + index) % len(small_names)]
            for index in range(length)
        ]
        generated.append((f"C{length}", names))

cases = curated + generated
mismatches = []
length_counts = {}
for index, (class_name, extensions) in enumerate(cases):
    length_counts[len(extensions)] = length_counts.get(len(extensions), 0) + 1
    expected = outcome(independent_oracle, class_name, extensions)
    trusted = outcome(canonical, class_name, extensions)
    actual = outcome(candidate, class_name, extensions)
    if not (expected == trusted == actual):
        mismatches.append(
            {
                "index": index,
                "class_name": class_name,
                "extensions": extensions,
                "oracle": expected,
                "canonical": trusted,
                "candidate": actual,
            }
        )

print("oracle=independent stable first-maximum using Python character predicates")
print(f"seed=153")
print(f"curated_cases={len(curated)} generated_cases={len(generated)}")
print(f"length_counts={dict(sorted(length_counts.items()))}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"mismatch={mismatch!r}")

if mismatches:
    raise SystemExit(1)
