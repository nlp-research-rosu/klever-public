#!/usr/bin/env python3
"""Ground witnesses for each entry-claim shape and formal result substitution."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/run-118")
VOWELS = set("AEIOUaeiou")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def formal_summary(word: str) -> str:
    """Independent executable reading of closestVowelSpec's equations."""
    if len(word) < 3:
        return ""
    tail = formal_summary(word[1:])
    if tail:
        return tail
    return word[1] if word[0] not in VOWELS and word[1] in VOWELS and word[2] not in VOWELS else ""


canonical = load(SCRATCH / "trusted-canonical.py", "adequacy_canonical")
candidate = load(SCRATCH / "solution.py", "adequacy_candidate")

witnesses = [
    ("empty-claim", ""),
    ("one-code-claim", "b"),
    ("two-code-claim", "ba"),
    ("three-plus-qualifies", "bab"),
    ("three-plus-empty", "bbb"),
    ("rightmost-choice", "babbeb"),
    ("documented-lower", "yogurt"),
    ("documented-upper", "FULL"),
]

records = []
for claim, word in witnesses:
    records.append(
        {
            "claim": claim,
            "word": word,
            "code_sequence": [ord(char) for char in word],
            "formal_closestVowelSpec": formal_summary(word),
            "canonical_python": canonical.get_closest_vowel(word),
            "candidate_python": candidate.get_closest_vowel(word),
        }
    )

print(json.dumps(records, indent=2))
assert all(
    row["formal_closestVowelSpec"]
    == row["canonical_python"]
    == row["candidate_python"]
    for row in records
)
