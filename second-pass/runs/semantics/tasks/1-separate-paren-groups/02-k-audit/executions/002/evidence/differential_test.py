#!/usr/bin/env python3
"""Independent differential test for HumanEval/1 on its balanced-input domain."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.separate_paren_groups


def balanced_words(max_pairs: int) -> list[str]:
    words: list[str] = []
    for pairs in range(max_pairs + 1):
        for chars in itertools.product("()", repeat=2 * pairs):
            word = "".join(chars)
            depth = 0
            valid = True
            for char in word:
                depth += 1 if char == "(" else -1
                if depth < 0:
                    valid = False
                    break
            if valid and depth == 0:
                words.append(word)
    return words


def add_spaces(word: str, mask: int) -> str:
    # There are len(word)+1 legal gaps, including leading/trailing gaps.
    pieces: list[str] = []
    for index in range(len(word) + 1):
        if mask & (1 << index):
            pieces.append(" ")
        if index < len(word):
            pieces.append(word[index])
    return "".join(pieces)


def random_balanced(rng: random.Random, pairs: int) -> str:
    opens = closes = 0
    out: list[str] = []
    for _ in range(2 * pairs):
        if opens == pairs:
            char = ")"
        elif closes == opens:
            char = "("
        else:
            char = rng.choice("()")
        if char == "(":
            opens += 1
        else:
            closes += 1
        out.append(char)
        if rng.randrange(4) == 0:
            out.append(" ")
    if rng.randrange(2):
        out.insert(0, " ")
    if rng.randrange(2):
        out.append(" ")
    return "".join(out)


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/reconstruction/solution.py"), "candidate_solution"
    )
    documented = [
        "( ) (( )) (( )( ))",
        "",
        " ",
        "()",
        "(())",
        "()()",
        "(()())()",
        "  (()())() ",
        "(((())))",
    ]
    exhaustive: list[str] = []
    for word in balanced_words(5):
        gaps = len(word) + 1
        # Exhaust all placements for up to 3 pairs; deterministic boundary
        # placements for larger words keep this run bounded.
        masks = range(1 << gaps) if len(word) <= 6 else (0, 1, 1 << (gaps - 1), (1 << gaps) - 1)
        exhaustive.extend(add_spaces(word, mask) for mask in masks)
    rng = random.Random(0xA11D17)
    generated_cases = [random_balanced(rng, rng.randrange(0, 31)) for _ in range(2_000)]
    cases = documented + exhaustive + generated_cases
    mismatches = []
    for index, value in enumerate(cases):
        expected = canonical(value)
        actual = generated(value)
        if actual != expected:
            mismatches.append((index, value, expected, actual))
            if len(mismatches) >= 20:
                break
    print(f"documented_and_boundaries={len(documented)}")
    print(f"exhaustive_balanced_with_spaces={len(exhaustive)}")
    print(f"seeded_generated={len(generated_cases)}")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches:
        print(repr(mismatch))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
