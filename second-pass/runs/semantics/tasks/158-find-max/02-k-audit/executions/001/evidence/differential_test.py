#!/usr/bin/env python3
"""Independent differential test for HumanEval 158 find_max."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable


EVIDENCE = Path("/audit-output/evidence")
CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[list[str]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_max


def outcome(function: Callable[[list[str]], str], words: list[str]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(list(words))}
    except Exception as exc:  # evidence includes boundary-domain exceptions
        return {"kind": "raise", "type": type(exc).__name__, "message": str(exc)}


canonical = load_entry(CANONICAL_PATH, "trusted_canonical_158")
candidate = load_entry(CANDIDATE_PATH, "audited_candidate_158")

explicit_cases: list[tuple[str, list[str], str]] = [
    ("example-1", ["name", "of", "string"], "documented"),
    ("example-2", ["name", "enam", "game"], "documented"),
    ("example-3", ["aaaaaaa", "bb", "cc"], "documented"),
    ("empty-list", [], "empty boundary outside canonical entry domain"),
    ("single-empty-word", [""], "single-element boundary"),
    ("single-word", ["abc"], "single-element boundary"),
    ("greater-score", ["a", "ab"], "unique > max_unique branch"),
    ("lower-score", ["abc", "aaaa"], "unique < max_unique branch"),
    ("equal-score-lex-smaller", ["ba", "ab"], "tie and word < best branch"),
    ("equal-score-not-smaller", ["ab", "ba"], "tie and not word < best branch"),
    ("repeated-characters", ["zzzz", "abab", "xyz"], "set/dedup boundaries"),
    ("empty-and-nonempty", ["", "a"], "zero-score then positive-score boundary"),
    ("unicode-codepoints", ["éé", "😀a", "e\u0301"], "Unicode representative"),
    ("duplicate-words", ["ab", "ab"], "outside distinct-words precondition"),
]

generated_cases: list[tuple[str, list[str], str]] = []
pool = ["", "a", "b", "aa", "ab", "ba", "bb", "abc", "cab"]
case_number = 0
for length in range(1, 5):
    for words_tuple in itertools.permutations(pool, length):
        case_number += 1
        generated_cases.append(
            (f"exhaustive-{case_number:04d}", list(words_tuple), "distinct small permutation")
        )

rng = random.Random(158)
alphabet = ["a", "b", "c", "z", "é", "😀"]
for random_number in range(500):
    target_size = rng.randint(1, 8)
    words_set: set[str] = set()
    while len(words_set) < target_size:
        word_length = rng.randint(0, 8)
        words_set.add("".join(rng.choice(alphabet) for _ in range(word_length)))
    words = list(words_set)
    rng.shuffle(words)
    generated_cases.append(
        (f"random-{random_number:04d}", words, "seeded distinct generated input")
    )

records: list[dict[str, Any]] = []
intended_mismatches: list[dict[str, Any]] = []
out_of_domain_differences: list[dict[str, Any]] = []

for case_id, words, category in explicit_cases + generated_cases:
    canonical_outcome = outcome(canonical, words)
    candidate_outcome = outcome(candidate, words)
    # The canonical implementation indexes element zero of sorted(words), so its
    # executable entry domain is nonempty; the prose separately requires distinct words.
    in_intended_domain = bool(words) and len(words) == len(set(words))
    same = canonical_outcome == candidate_outcome
    record = {
        "id": case_id,
        "category": category,
        "words": words,
        "in_intended_domain": in_intended_domain,
        "canonical": canonical_outcome,
        "candidate": candidate_outcome,
        "same": same,
    }
    records.append(record)
    if not same and in_intended_domain:
        intended_mismatches.append(record)
    elif not same:
        out_of_domain_differences.append(record)

inputs = [
    {
        "id": record["id"],
        "category": record["category"],
        "words": record["words"],
        "in_intended_domain": record["in_intended_domain"],
    }
    for record in records
]
EVIDENCE.joinpath("differential-inputs.json").write_text(
    json.dumps(inputs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
EVIDENCE.joinpath("differential-results.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

summary = {
    "total_cases": len(records),
    "intended_domain_cases": sum(record["in_intended_domain"] for record in records),
    "intended_domain_mismatches": len(intended_mismatches),
    "out_of_domain_differences": len(out_of_domain_differences),
    "explicit_results": records[: len(explicit_cases)],
}
print(json.dumps(summary, ensure_ascii=False, indent=2))

if intended_mismatches:
    raise SystemExit(1)
