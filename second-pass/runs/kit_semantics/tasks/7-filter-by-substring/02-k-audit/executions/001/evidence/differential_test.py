#!/usr/bin/env python3
"""Reviewer-authored differential test for HumanEval/7."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Callable


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_entry(path: Path, module_name: str) -> Callable[[list[str], str], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


def main() -> int:
    canonical = load_entry(SCRATCH / "canonical.py", "trusted_canonical")
    candidate = load_entry(SCRATCH / "solution.py", "generated_solution")

    cases: list[tuple[list[str], str]] = [
        ([], "a"),
        (["abc", "bacd", "cde", "array"], "a"),
        ([], ""),
        ([""], ""),
        (["", "a", "aa", "ba", "ab"], ""),
        (["", "a", "aa", "ba", "ab"], "a"),
        (["abc"], "abc"),
        (["abc"], "abcd"),
        (["abc"], "ab"),
        (["abc"], "bc"),
        (["abc"], "b"),
        (["abc"], "z"),
        (["aaaa", "baaab", "bbb"], "aa"),
        (["é", "café", "e\u0301", "😀x"], "é"),
        (["line\nbreak", "\x00inside", "plain"], "\x00"),
        (["same", "same", "different"], "same"),
    ]

    atoms = ["", "a", "b", "ab", "ba", "aa", "é", "😀", "\x00"]
    needles = ["", "a", "b", "ab", "ba", "aa", "é", "😀", "\x00", "aba"]
    for length in range(4):
        for values in itertools.product(atoms[:6], repeat=length):
            for needle in needles[:6]:
                cases.append((list(values), needle))

    rng = random.Random(0x7F17E2)
    alphabet = ["a", "b", "c", "é", "😀", "\x00"]
    for _ in range(5000):
        values = [
            "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))
            for _ in range(rng.randrange(0, 9))
        ]
        needle = "".join(
            rng.choice(alphabet) for _ in range(rng.randrange(0, 5))
        )
        cases.append((values, needle))

    encoded = json.dumps(cases, ensure_ascii=False, separators=(",", ":")).encode()
    mismatches = []
    for index, (values, needle) in enumerate(cases):
        expected = canonical(values, needle)
        actual = candidate(values, needle)
        if actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "strings": values,
                    "substring": needle,
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    print(f"case_count={len(cases)}")
    print(f"input_sha256={hashlib.sha256(encoded).hexdigest()}")
    print("documented_example_0=" + repr(canonical([], "a")))
    print(
        "documented_example_1="
        + repr(canonical(["abc", "bacd", "cde", "array"], "a"))
    )
    print(
        "coverage=empty lists; empty strings/needle; exact/prefix/suffix/middle/"
        "absent/longer needle; duplicates; combining/unicode/NUL/newline; "
        "small exhaustive products; deterministic random cases"
    )
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH " + json.dumps(mismatch, ensure_ascii=False, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
