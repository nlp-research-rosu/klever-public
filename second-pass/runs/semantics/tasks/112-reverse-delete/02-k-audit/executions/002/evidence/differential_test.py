#!/usr/bin/env python3
"""Independent differential check for HumanEval 112-reverse-delete."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/112-reverse-delete")
INPUT_RECORD = Path("/audit-output/evidence/differential_inputs.json")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def strings(alphabet: tuple[str, ...], maximum: int):
    for length in range(maximum + 1):
        for chars in itertools.product(alphabet, repeat=length):
            yield "".join(chars)


def main() -> int:
    canonical = load_function(SCRATCH / "canonical.py", "trusted_canonical")
    generated = load_function(SCRATCH / "solution.py", "generated_solution")

    labeled_cases: list[tuple[str, str, str]] = [
        ("example-1", "abcde", "ae"),
        ("example-2", "abcdef", "b"),
        ("example-3", "abcdedcba", "ab"),
        ("both-empty", "", ""),
        ("empty-s", "", "anything"),
        ("empty-c", "abba", ""),
        ("one-kept", "a", ""),
        ("one-deleted", "a", "a"),
        ("one-not-member", "a", "b"),
        ("all-deleted", "abc", "abc"),
        ("none-deleted-nonpal", "abc", ""),
        ("front-deleted", "abc", "a"),
        ("middle-deleted", "abc", "b"),
        ("back-deleted", "abc", "c"),
        ("duplicate-c", "bananas", "aaa"),
        ("unicode-emoji", "😀a😀", "a"),
        ("unicode-accent", "éaé", "a"),
        ("combining-codepoint", "e\u0301x\u0301e", "\u0301"),
        ("embedded-nul", "a\u0000a", "\u0000"),
        ("line-break", "a\nb\na", "\n"),
    ]

    cases: list[dict[str, str]] = [
        {"source": label, "s": s, "c": c} for label, s, c in labeled_cases
    ]

    # Exhaust all pairs over small strings, covering both outcomes of membership
    # and palindrome checks at each short length boundary.
    exhaustive_s = tuple(strings(("a", "b"), 6))
    exhaustive_c = tuple(strings(("a", "b"), 3))
    for s in exhaustive_s:
        for c in exhaustive_c:
            cases.append({"source": "exhaustive-ab", "s": s, "c": c})

    rng = random.Random(112)
    alphabet = ("a", "b", "c", "é", "😀", "\u0000")
    for _ in range(2000):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 41)))
        c = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 13)))
        cases.append({"source": "seeded-random-112", "s": s, "c": c})

    INPUT_RECORD.write_text(
        json.dumps(cases, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    mismatches = []
    palindrome_true = 0
    palindrome_false = 0
    for index, case in enumerate(cases):
        args = (case["s"], case["c"])
        expected = canonical(*args)
        actual = generated(*args)
        palindrome_true += int(bool(expected[1]))
        palindrome_false += int(not bool(expected[1]))
        if actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "case": case,
                    "canonical": expected,
                    "generated": actual,
                }
            )

    digest = hashlib.sha256(INPUT_RECORD.read_bytes()).hexdigest()
    print(f"documented_and_boundary_cases={len(labeled_cases)}")
    print(f"exhaustive_cases={len(exhaustive_s) * len(exhaustive_c)}")
    print("random_cases=2000 seed=112 s_length=0..40 c_length=0..12")
    print(f"total_cases={len(cases)}")
    print(f"canonical_palindrome_true={palindrome_true}")
    print(f"canonical_palindrome_false={palindrome_false}")
    print(f"input_record_sha256={digest}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], ensure_ascii=True, indent=2))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
