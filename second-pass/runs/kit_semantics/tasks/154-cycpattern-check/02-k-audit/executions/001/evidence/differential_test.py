#!/usr/bin/env python3
"""Independent differential test for HumanEval 154.

The oracle is implemented here from the natural-language contract. It does not
reuse the candidate's algorithm or K summary functions.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from types import ModuleType


CANONICAL_PATH = Path("/tmp/audit-work/cycpattern-audit/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/cycpattern-audit/candidate-src/solution.py")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract_oracle(a: str, b: str) -> bool:
    if b == "":
        return True
    return any((b[offset:] + b[:offset]) in a for offset in range(len(b)))


DIRECTED_CASES = [
    # Six documented examples.
    ("abcd", "abd", "example false"),
    ("hello", "ell", "example direct substring"),
    ("whassup", "psus", "example false"),
    ("abab", "baa", "example rotation true"),
    ("efef", "eeff", "example false"),
    ("himenss", "simen", "example late rotation true"),
    # Empty and length boundaries.
    ("", "", "both empty"),
    ("abc", "", "empty second word"),
    ("", "a", "empty first word"),
    ("a", "a", "single-character direct"),
    ("a", "b", "single-character false"),
    ("ba", "ab", "length-two rotation true"),
    ("ab", "ba", "length-two rotation true reverse direction"),
    ("a", "aa", "second word longer"),
    # Branch-sensitive and representative cases.
    ("zzabcdzz", "abcd", "initial result true"),
    ("zzbcda", "abcd", "first nonidentity rotation true"),
    ("zzdabc", "abcd", "last nonidentity rotation true"),
    ("zzcabd", "abcd", "all rotations false"),
    ("aaaaa", "aaa", "repeated characters"),
    ("abab", "abab", "periodic direct"),
    ("baba", "abab", "periodic rotation"),
    ("éΩ🙂x", "Ω🙂é", "unicode rotation true"),
    ("🙂", "🙂🙂", "unicode longer false"),
]


def all_strings(alphabet: str, maximum_length: int):
    for length in range(maximum_length + 1):
        for characters in itertools.product(alphabet, repeat=length):
            yield "".join(characters)


def main() -> int:
    canonical = load_module("trusted_canonical", CANONICAL_PATH).cycpattern_check
    candidate = load_module("generated_candidate", CANDIDATE_PATH).cycpattern_check
    cases: list[tuple[str, str, str]] = list(DIRECTED_CASES)

    exhaustive = list(all_strings("ab", 5))
    for a in exhaustive:
        for b in exhaustive:
            cases.append((a, b, "exhaustive alphabet=ab lengths=0..5"))

    rng = random.Random(154)
    random_alphabet = ["a", "b", "c", "é", "Ω", "🙂"]
    for _ in range(5000):
        a = "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 13)))
        b = "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 10)))
        cases.append((a, b, "deterministic generated unicode sample"))

    mismatches = []
    for index, (a, b, label) in enumerate(cases):
        expected = contract_oracle(a, b)
        canonical_result = canonical(a, b)
        candidate_result = candidate(a, b)
        if (
            type(canonical_result) is not bool
            or type(candidate_result) is not bool
            or canonical_result != expected
            or candidate_result != expected
        ):
            mismatches.append(
                {
                    "index": index,
                    "label": label,
                    "a": a,
                    "b": b,
                    "oracle": expected,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                    "canonical_type": type(canonical_result).__name__,
                    "candidate_type": type(candidate_result).__name__,
                }
            )

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print(f"directed_cases={len(DIRECTED_CASES)}")
    for a, b, label in DIRECTED_CASES:
        print(
            f"DIRECTED {label}: a={a!r} b={b!r} "
            f"result={contract_oracle(a, b)}"
        )
    print(f"exhaustive_strings={len(exhaustive)}")
    print(f"exhaustive_pairs={len(exhaustive) ** 2}")
    print("generated_cases=5000 seed=154 alphabet='abcéΩ🙂'")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
