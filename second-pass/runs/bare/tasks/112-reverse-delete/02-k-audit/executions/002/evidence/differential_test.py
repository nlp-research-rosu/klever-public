#!/usr/bin/env python3
"""Independent differential test: trusted canonical vs candidate solution."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/112-reverse-delete")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def words(alphabet: str, max_length: int):
    for length in range(max_length + 1):
        for chars in itertools.product(alphabet, repeat=length):
            yield "".join(chars)


def main() -> int:
    canonical = load_function("trusted_canonical", SCRATCH / "trusted-canonical.py")
    candidate = load_function("candidate_solution", SCRATCH / "solution.py")

    named_cases = [
        ("prompt-1", "abcde", "ae"),
        ("prompt-2", "abcdef", "b"),
        ("prompt-3", "abcdedcba", "ab"),
        ("both-empty", "", ""),
        ("empty-source", "", "xyz"),
        ("empty-delete-set", "abba", ""),
        ("single-kept", "x", ""),
        ("single-deleted", "x", "x"),
        ("all-deleted", "aaaa", "a"),
        ("none-deleted", "abc", "xyz"),
        ("mixed-branches", "abac", "a"),
        ("duplicate-delete-chars", "abcabc", "aaac"),
        ("palindrome-created", "abXba", "X"),
        ("non-palindrome-created", "abXca", "X"),
        ("whitespace-and-nul", " a\x00a ", "\x00"),
        ("non-bmp", "😀a😀", "a"),
        ("non-bmp-vs-latin1-byte", "😀", "ð"),
        ("combining-codepoint", "e\u0301x\u0301e", "x"),
        ("newline-and-tab", "a\nb\ta", "\n\t"),
    ]

    cases: list[tuple[str, str, str]] = list(named_cases)
    for s in words("ab", 6):
        for c in words("ab", 3):
            cases.append(("exhaustive-ab", s, c))

    rng = random.Random(112)
    alphabet = "abcXYZ01 \n\t\x00é\u0301😀"
    for _ in range(1000):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 33)))
        c = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))
        cases.append(("seeded-generated", s, c))

    mismatches = []
    result_digest = hashlib.sha256()
    for index, (label, s, c) in enumerate(cases):
        expected = canonical(s, c)
        actual = candidate(s, c)
        result_digest.update(
            json.dumps(
                [label, s, c, expected, actual],
                ensure_ascii=True,
                separators=(",", ":"),
            ).encode()
        )
        if actual != expected:
            mismatches.append((index, label, s, c, expected, actual))

    print("named_cases:")
    for label, s, c in named_cases:
        print(
            json.dumps(
                {
                    "label": label,
                    "s": s,
                    "c": c,
                    "canonical": canonical(s, c),
                    "candidate": candidate(s, c),
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
    print(f"total_cases={len(cases)}")
    print(f"exhaustive_ab_cases={sum(1 for x in cases if x[0] == 'exhaustive-ab')}")
    print(f"seeded_generated_cases={sum(1 for x in cases if x[0] == 'seeded-generated')}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"result_digest_sha256={result_digest.hexdigest()}")
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    return int(bool(mismatches))


if __name__ == "__main__":
    raise SystemExit(main())
