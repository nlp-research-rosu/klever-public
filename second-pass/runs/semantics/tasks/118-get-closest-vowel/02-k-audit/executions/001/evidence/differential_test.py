#!/usr/bin/env python3
"""Independent differential audit for HumanEval 118.

Input scope:
* the four documented examples;
* curated empty/length/branch/tie/case boundaries;
* exhaustive strings of lengths 0..5 over ``aAEbBy``;
* 10,000 deterministic random ASCII-letter strings, lengths 0..40, seed 118;
* long strings around and beyond CPython's recursion limit.

The oracle is the trusted /reference/canonical.py implementation.  The tested
implementation is the scratch-copied /candidate/solution.py.
"""

from __future__ import annotations

import importlib.util
import hashlib
import itertools
import json
import random
import string
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/run-118")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(SCRATCH / "trusted-canonical.py", "trusted_canonical")
candidate = load(SCRATCH / "solution.py", "candidate_solution")

documented = ["yogurt", "FULL", "quick", "ab"]
curated = [
    "",
    "a",
    "b",
    "aa",
    "ba",
    "bab",
    "bAb",
    "bbb",
    "aba",
    "bbbabb",
    "babbeb",
    "BAZZE",
    "xAy",
    "aei",
    "bubab",
    "babab",
    "zOz",
    "zIz",
    "UUU",
    "bcUdf",
]
branch_alphabet = "aAEbBy"
random_seed = 118
random_count = 10_000
random_max_length = 40
long_lengths = [900, 950, 975, 990, 995, 1000, 1001, 1100, 2000]


def outcome(fn, word: str):
    try:
        return {"kind": "return", "value": fn(word)}
    except BaseException as err:  # Record divergence, including RecursionError.
        return {"kind": "exception", "type": type(err).__name__, "message": str(err)}


def generated_inputs():
    yield from documented
    yield from curated
    for length in range(0, 6):
        for chars in itertools.product(branch_alphabet, repeat=length):
            yield "".join(chars)
    rng = random.Random(random_seed)
    for _ in range(random_count):
        length = rng.randrange(random_max_length + 1)
        yield "".join(rng.choice(string.ascii_letters) for _ in range(length))
    for length in long_lengths:
        yield "b" * length
        # A qualifying vowel is present, but tail recursion still traverses the
        # whole suffix before returning it during unwinding.
        yield "b" * (length - 3) + "bab"


seen = set()
ordered_inputs = []
tested = 0
mismatches = []
for word in generated_inputs():
    if word in seen:
        continue
    seen.add(word)
    ordered_inputs.append(word)
    tested += 1
    expected = outcome(canonical.get_closest_vowel, word)
    actual = outcome(candidate.get_closest_vowel, word)
    if actual != expected:
        mismatches.append(
            {
                "length": len(word),
                "word_preview": word if len(word) <= 80 else word[:40] + "..." + word[-40:],
                "canonical": expected,
                "candidate": actual,
            }
        )

input_corpus_path = Path("/audit-output/evidence/differential_inputs.jsonl")
input_corpus_bytes = "".join(
    json.dumps({"index": index, "word": word}) + "\n"
    for index, word in enumerate(ordered_inputs)
).encode()
input_corpus_path.write_bytes(input_corpus_bytes)

summary = {
    "python": sys.version,
    "recursion_limit": sys.getrecursionlimit(),
    "documented_examples": documented,
    "curated_inputs": curated,
    "exhaustive": {"alphabet": branch_alphabet, "lengths": [0, 1, 2, 3, 4, 5]},
    "random": {
        "seed": random_seed,
        "count_before_deduplication": random_count,
        "alphabet": "string.ascii_letters",
        "length_range": [0, random_max_length],
    },
    "long_lengths_each_with_two_patterns": long_lengths,
    "unique_inputs_tested": tested,
    "preserved_input_corpus": {
        "path": str(input_corpus_path),
        "sha256": hashlib.sha256(input_corpus_bytes).hexdigest(),
        "bytes": len(input_corpus_bytes),
    },
    "mismatch_count": len(mismatches),
    "mismatches": mismatches[:50],
}
print(json.dumps(summary, indent=2))
raise SystemExit(1 if mismatches else 0)
