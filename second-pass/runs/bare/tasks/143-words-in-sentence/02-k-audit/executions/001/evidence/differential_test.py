#!/usr/bin/env python3
"""Independent differential test for HumanEval 143.

Oracle: /reference/canonical.py loaded by absolute path.
Candidate: /tmp/audit-work/rebuild/solution.py loaded by absolute path.
The script records every tested input and both results as JSONL.
"""

from __future__ import annotations

import importlib.util
import json
import random
import string
from pathlib import Path


ORACLE_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/rebuild/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/differential-inputs.jsonl")
SEED = 143_2026_07_23
GENERATED_CASES = 5000


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.words_in_sentence


def word(length: int, letter: str = "a") -> str:
    return letter * length


def add(cases: list[tuple[str, str]], label: str, sentence: str) -> None:
    cases.append((label, sentence))


def build_cases() -> list[tuple[str, str]]:
    cases: list[tuple[str, str]] = []

    # Documented examples, empty diagnostic, and explicit branch shapes.
    add(cases, "example-1", "This is a test")
    add(cases, "example-2", "lets go for swimming")
    add(cases, "empty-outside-contract", "")
    add(cases, "minimum-one", "a")
    add(cases, "skip-then-first-select", "a bb")
    add(cases, "first-select-then-skip", "bb cccc")
    add(cases, "two-selected-inner-else", "bb ccc")
    add(cases, "all-skipped", "a cccc xxxxxx")
    add(cases, "leading-and-repeated-space-diagnostic", "  aa   bbb  ")

    # Every membership branch boundary for a single word length 0..100.
    # n=0 is the empty diagnostic; 1..100 covers the entire formal length bound.
    for n in range(0, 101):
        add(cases, f"single-word-length-{n}", word(n))

    # Adjacent length pairs around every transition and mixed accumulator paths.
    for n in range(1, 100):
        add(cases, f"adjacent-lengths-{n}-{n + 1}", f"{word(n, 'a')} {word(n + 1, 'b')}")

    # Whole-sentence boundaries and the candidate's explicit maximum prime.
    add(cases, "length-100-composite", word(100))
    add(cases, "length-100-2-plus-97", f"{word(2)} {word(97, 'b')}")
    add(cases, "prime-97", word(97))
    add(cases, "composite-98", word(98))
    add(cases, "composite-99", word(99))
    add(cases, "composite-100", word(100))

    rng = random.Random(SEED)
    alphabet = string.ascii_letters
    for index in range(GENERATED_CASES):
        # Construct 1..12 nonempty words, then shrink until total length <= 100.
        count = rng.randint(1, 12)
        lengths = [rng.randint(1, 40) for _ in range(count)]
        while sum(lengths) + len(lengths) - 1 > 100:
            slot = rng.randrange(len(lengths))
            if lengths[slot] > 1:
                lengths[slot] -= 1
            elif len(lengths) > 1:
                lengths.pop(slot)
        words = [
            "".join(rng.choice(alphabet) for _ in range(length))
            for length in lengths
        ]
        add(cases, f"generated-{index:04d}", " ".join(words))

    return cases


def main() -> int:
    oracle = load_entry(ORACLE_PATH, "trusted_canonical_143")
    candidate = load_entry(CANDIDATE_PATH, "audited_solution_143")
    cases = build_cases()
    mismatches = []

    with INPUT_RECORD.open("w", encoding="utf-8") as output:
        for label, sentence in cases:
            expected = oracle(sentence)
            actual = candidate(sentence)
            record = {
                "label": label,
                "sentence": sentence,
                "length": len(sentence),
                "canonical": expected,
                "candidate": actual,
                "match": expected == actual,
            }
            output.write(json.dumps(record, ensure_ascii=True, sort_keys=True) + "\n")
            if expected != actual:
                mismatches.append(record)

    summary = {
        "oracle": str(ORACLE_PATH),
        "candidate": str(CANDIDATE_PATH),
        "seed": SEED,
        "generated_cases": GENERATED_CASES,
        "total_cases": len(cases),
        "mismatches": len(mismatches),
        "input_record": str(INPUT_RECORD),
    }
    print(json.dumps(summary, sort_keys=True))
    for mismatch in mismatches[:20]:
        print(json.dumps(mismatch, ensure_ascii=True, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
