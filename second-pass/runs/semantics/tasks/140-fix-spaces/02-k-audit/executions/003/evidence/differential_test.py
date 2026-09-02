#!/usr/bin/env python3
"""Independent differential audit for HumanEval 140."""

from __future__ import annotations

import importlib.util
import itertools
import pathlib
import random
import sys


def load_function(path: pathlib.Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fix_spaces


def prompt_oracle(text: str) -> str:
    """Direct reading of the prose: 1/2 spaces -> underscores; >2 -> '-'."""
    output: list[str] = []
    index = 0
    while index < len(text):
        if text[index] != " ":
            output.append(text[index])
            index += 1
            continue
        end = index
        while end < len(text) and text[end] == " ":
            end += 1
        count = end - index
        output.append("-" if count > 2 else "_" * count)
        index = end
    return "".join(output)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 2

    sys.dont_write_bytecode = True
    canonical = load_function(pathlib.Path(sys.argv[1]), "trusted_canonical_140")
    candidate = load_function(pathlib.Path(sys.argv[2]), "candidate_solution_140")

    named = [
        ("documented-1", "Example"),
        ("documented-2", "Example 1"),
        ("documented-3", " Example 2"),
        ("documented-4", " Example   3"),
        ("empty", ""),
        ("only-1-space", " "),
        ("only-2-spaces", "  "),
        ("only-3-spaces", "   "),
        ("only-4-spaces", "    "),
        ("trailing-1", "a "),
        ("trailing-2", "a  "),
        ("trailing-3", "a   "),
        ("leading-2", "  a"),
        ("internal-2", "a  b"),
        ("separated-runs", " a  b   c    d "),
        ("non-ascii", "λ  🙂   z"),
        ("newline-is-not-space", "a\n\tb"),
        ("nul-is-not-space", "a\x00 b"),
    ]

    cases: list[tuple[str, str]] = list(named)
    for length in range(0, 9):
        for chars in itertools.product((" ", "a", "b"), repeat=length):
            cases.append((f"exhaustive-small-{length}", "".join(chars)))

    rng = random.Random(140)
    alphabet = [" ", "a", "Z", "0", "_", "-", "\n", "\t", "λ", "🙂"]
    for index in range(2000):
        length = rng.randrange(0, 65)
        cases.append(
            (
                f"seeded-{index}",
                "".join(rng.choice(alphabet) for _ in range(length)),
            )
        )

    seen: set[str] = set()
    unique_cases: list[tuple[str, str]] = []
    for label, text in cases:
        if text not in seen:
            seen.add(text)
            unique_cases.append((label, text))

    mismatches: list[tuple[str, str, str, str, str]] = []
    candidate_prompt_mismatches = 0
    canonical_prompt_mismatches = 0
    for label, text in unique_cases:
        expected = canonical(text)
        actual = candidate(text)
        prose = prompt_oracle(text)
        candidate_prompt_mismatches += actual != prose
        canonical_prompt_mismatches += expected != prose
        if actual != expected:
            mismatches.append((label, text, expected, actual, prose))

    print(f"named_cases={len(named)}")
    print("exhaustive_alphabet=[' ', 'a', 'b']")
    print("exhaustive_lengths=0..8")
    print("random_seed=140")
    print("seeded_generated_attempts=2000")
    print(f"unique_total_cases={len(unique_cases)}")
    print(f"candidate_vs_canonical_mismatches={len(mismatches)}")
    print(f"candidate_vs_prompt_oracle_mismatches={candidate_prompt_mismatches}")
    print(f"canonical_vs_prompt_oracle_mismatches={canonical_prompt_mismatches}")
    for index, (label, text, expected, actual, prose) in enumerate(mismatches[:40], 1):
        print(
            f"mismatch[{index}] label={label} input={text!r} "
            f"canonical={expected!r} candidate={actual!r} prompt_oracle={prose!r}"
        )
    print(f"mismatches_omitted={max(0, len(mismatches) - 40)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
