#!/usr/bin/env python3
"""Independent differential test for HumanEval 118.

The trusted oracle is imported from /reference/canonical.py.  The candidate
entry point is imported from the source-only scratch copy.  The deterministic
input corpus is also serialized so the exact run can be reproduced.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
import string
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs-out", required=True, type=Path)
    args = parser.parse_args()

    canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
    candidate = load_entry(
        "scratch_candidate", Path("/tmp/audit-work/candidate-src/solution.py")
    )

    examples = {
        "yogurt": "u",
        "FULL": "U",
        "quick": "",
        "ab": "",
    }
    directed = [
        "",
        "a",
        "Z",
        "ab",
        "AA",
        "aba",   # immediate consonant-vowel-consonant success
        "bAb",   # uppercase vowel success
        "abb",   # middle consonant, then base case
        "aab",   # middle vowel, left vowel
        "baa",   # middle vowel, right vowel
        "bbb",   # no vowel
        "cabd",  # recurse once, then find "a"
        "zaBcd", # recurse twice, then find "a"
        "baeb",  # overlapping vowels, no eligible vowel
        "xUyz",  # recurse once, then find uppercase "U"
        "AEIOU",
        "BCDFG",
    ]

    # a/A and b/B span lower/uppercase vowel/consonant categories.  Exhaustive
    # category-shape coverage through length 7 exercises every recursion branch.
    category_exhaustive = [
        "".join(chars)
        for length in range(8)
        for chars in itertools.product("aAbB", repeat=length)
    ]

    rng = random.Random(118)
    generated = [
        "".join(rng.choice(string.ascii_letters) for _ in range(rng.randrange(33)))
        for _ in range(2000)
    ]

    all_inputs = list(dict.fromkeys([*examples, *directed, *category_exhaustive, *generated]))
    args.inputs_out.write_text(
        json.dumps(
            {
                "documented_examples": examples,
                "directed_inputs": directed,
                "category_alphabet": "aAbB",
                "category_lengths": [0, 7],
                "random_seed": 118,
                "random_count": 2000,
                "random_length_range": [0, 32],
                "random_alphabet": string.ascii_letters,
                "all_inputs": all_inputs,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    for word in all_inputs:
        want = canonical(word)
        got = candidate(word)
        if want != got:
            mismatches.append({"word": word, "canonical": want, "candidate": got})

    bad_examples = []
    for word, expected in examples.items():
        canonical_value = canonical(word)
        candidate_value = candidate(word)
        if canonical_value != expected or candidate_value != expected:
            bad_examples.append(
                {
                    "word": word,
                    "expected": expected,
                    "canonical": canonical_value,
                    "candidate": candidate_value,
                }
            )

    corpus_digest = hashlib.sha256(
        json.dumps(all_inputs, ensure_ascii=True, separators=(",", ":")).encode()
    ).hexdigest()
    print(f"documented_examples={len(examples)} bad_examples={len(bad_examples)}")
    for word, expected in examples.items():
        print(
            f"example {word!r}: expected={expected!r} "
            f"canonical={canonical(word)!r} candidate={candidate(word)!r}"
        )
    print(f"directed_inputs={len(directed)}")
    print(f"category_exhaustive_inputs={len(category_exhaustive)}")
    print(f"generated_inputs={len(generated)} seed=118")
    print(f"unique_total_inputs={len(all_inputs)}")
    print(f"corpus_sha256={corpus_digest}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], indent=2, sort_keys=True))
    return 1 if mismatches or bad_examples else 0


if __name__ == "__main__":
    raise SystemExit(main())
