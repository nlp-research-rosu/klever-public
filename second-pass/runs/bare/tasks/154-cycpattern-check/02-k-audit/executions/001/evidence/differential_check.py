#!/usr/bin/env python3
"""Independent differential check of the trusted canonical and submitted entry points."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Callable


CANONICAL_PATH = Path("/tmp/audit-work/154-cycpattern-check/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/154-cycpattern-check/candidate-src/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[str, str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cycpattern_check


def all_words(alphabet: str, max_length: int) -> list[str]:
    return [
        "".join(chars)
        for length in range(max_length + 1)
        for chars in itertools.product(alphabet, repeat=length)
    ]


def make_cases() -> tuple[list[tuple[str, str]], dict[str, int]]:
    documented = [
        ("abcd", "abd"),
        ("hello", "ell"),
        ("whassup", "psus"),
        ("abab", "baa"),
        ("efef", "eeff"),
        ("himenss", "simen"),
    ]
    explicit_boundaries = [
        ("", ""),
        ("a", ""),
        ("anything", ""),
        ("", "a"),
        ("a", "a"),
        ("ba", "ab"),       # matching rotation at i = 1 (last iteration)
        ("cab", "abc"),     # matching rotation at i = 2 (last iteration)
        ("bc", "abc"),      # b longer than a
        ("aaaa", "aa"),
        ("abab", "abab"),
        ("xxbcaYY", "abc"), # matching rotation strictly after i = 0
        ("ab", "abc"),      # all rotation branches false
        ("héllo", "llohé"),
        ("🙂ab", "ab🙂"),
    ]
    words = all_words("ab", 5)
    exhaustive = list(itertools.product(words, repeat=2))

    rng = random.Random(154)
    alphabet = "abcxyz"
    generated = [
        (
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 13))),
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9))),
        )
        for _ in range(600)
    ]

    ordered = documented + explicit_boundaries + exhaustive + generated
    cases = list(dict.fromkeys(ordered))
    counts = {
        "documented": len(documented),
        "explicit_boundaries": len(explicit_boundaries),
        "exhaustive_ab_words_through_length_5_before_dedup": len(exhaustive),
        "seeded_generated_before_dedup": len(generated),
        "unique_total": len(cases),
    }
    return cases, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exclude-empty-b", action="store_true")
    parser.add_argument("--record-inputs", type=Path)
    args = parser.parse_args()

    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    generated = load_entry(GENERATED_PATH, "submitted_solution")
    cases, counts = make_cases()
    if args.exclude_empty_b:
        cases = [(a, b) for a, b in cases if b != ""]

    encoded = json.dumps(cases, ensure_ascii=False, separators=(",", ":")).encode()
    if args.record_inputs:
        args.record_inputs.write_bytes(encoded + b"\n")

    mismatches = []
    outcome_counts: dict[str, int] = {}
    for a, b in cases:
        expected = canonical(a, b)
        actual = generated(a, b)
        key = f"canonical={expected},generated={actual}"
        outcome_counts[key] = outcome_counts.get(key, 0) + 1
        if type(expected) is not bool or type(actual) is not bool or expected != actual:
            mismatches.append(
                {"a": a, "b": b, "canonical": expected, "generated": actual}
            )

    print("oracle=trusted /reference/canonical.py::cycpattern_check")
    print("subject=/candidate/solution.py scratch copy::cycpattern_check")
    print("generation_counts=" + json.dumps(counts, sort_keys=True))
    print(f"exclude_empty_b={args.exclude_empty_b}")
    print(f"executed_unique_cases={len(cases)}")
    print(f"input_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("outcome_counts=" + json.dumps(outcome_counts, sort_keys=True))
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:30]:
        print("MISMATCH " + json.dumps(mismatch, ensure_ascii=False, sort_keys=True))
    if len(mismatches) > 30:
        print(f"MISMATCH_OUTPUT_TRUNCATED={len(mismatches) - 30}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
