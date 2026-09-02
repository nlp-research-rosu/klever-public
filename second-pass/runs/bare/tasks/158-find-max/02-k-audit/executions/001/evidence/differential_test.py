#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


SOURCE = Path("/tmp/audit-work/source")
OUTPUT = Path("/audit-output/evidence/differential-inputs.jsonl")
SEED = 158_2026_07_23


def load_entry(module_name: str, path: Path) -> Callable[[list[str]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_max


def outcome(function: Callable[[list[str]], str], words: list[str]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(list(words))}
    except Exception as error:  # Boundary behavior is evidence, including errors.
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


def main() -> int:
    canonical = load_entry("trusted_canonical", SOURCE / "canonical.py")
    generated = load_entry("generated_solution", SOURCE / "solution.py")

    explicit: list[tuple[str, list[str], bool]] = [
        ("prompt-1", ["name", "of", "string"], True),
        ("prompt-2", ["name", "enam", "game"], True),
        ("prompt-3", ["aaaaaaa", "bb", "cc"], True),
        ("empty-list-boundary", [], False),
        ("singleton-empty-string", [""], True),
        ("singleton-one-char", ["x"], True),
        ("greater-count-replaces", ["aa", "abc"], True),
        ("smaller-count-retains", ["abc", "aa"], True),
        ("equal-count-lex-smaller-replaces", ["ba", "ab"], True),
        ("equal-count-lex-larger-retains", ["ab", "ba"], True),
        ("all-zero-or-one-counts", ["", "aaaa", "bbbb"], True),
        ("unicode-distinct-count", ["é", "e\u0301", "😀😀a"], True),
        ("unicode-lex-tie", ["éa", "êa", "😀a"], True),
        ("duplicate-word-outside-domain", ["ab", "ab"], False),
    ]

    alphabet_words = [""]
    for length in range(1, 4):
        alphabet_words.extend(
            "".join(chars) for chars in itertools.product("ab", repeat=length)
        )

    cases: list[tuple[str, list[str], bool]] = list(explicit)
    for size in range(1, 4):
        for index, words in enumerate(itertools.permutations(alphabet_words, size)):
            cases.append((f"exhaustive-{size}-{index}", list(words), True))

    rng = random.Random(SEED)
    random_alphabet = ["a", "b", "c", "é", "😀", "\u0301"]
    for index in range(2_000):
        size = rng.randint(1, 8)
        chosen: list[str] = []
        while len(chosen) < size:
            word = "".join(
                rng.choice(random_alphabet) for _ in range(rng.randint(0, 7))
            )
            if word not in chosen:
                chosen.append(word)
        cases.append((f"random-{index}", chosen, True))

    intended_mismatches = 0
    outside_domain_divergences = 0
    records = 0
    with OUTPUT.open("w", encoding="utf-8") as stream:
        for label, words, intended_domain in cases:
            expected = outcome(canonical, words)
            actual = outcome(generated, words)
            matched = expected == actual
            if intended_domain and not matched:
                intended_mismatches += 1
            if not intended_domain and not matched:
                outside_domain_divergences += 1
            record = {
                "label": label,
                "intended_domain": intended_domain,
                "words": words,
                "canonical": expected,
                "generated": actual,
                "matched": matched,
            }
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            records += 1

    print(f"seed={SEED}")
    print("exhaustive_scope=all ordered, pairwise-distinct lists of lengths 1..3")
    print("exhaustive_word_set=all strings over {'a','b'} of lengths 0..3")
    print("random_scope=2000 pairwise-distinct lists, lengths 1..8")
    print("random_alphabet=['a','b','c','é','😀','COMBINING ACUTE']")
    print(f"records={records}")
    print(f"intended_domain_mismatches={intended_mismatches}")
    print(f"outside_domain_divergences={outside_domain_divergences}")
    print(
        "empty_list_boundary="
        f"canonical:{outcome(canonical, [])};generated:{outcome(generated, [])}"
    )
    print(f"inputs_file={OUTPUT}")
    return 0 if intended_mismatches == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
