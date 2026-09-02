#!/usr/bin/env python3
"""Exhibit satisfying inputs and compare concrete claim interpretations."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path("/tmp/audit-work/audit19")
WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def numwords_term(words: list[str]) -> str:
    term = ".NumWords"
    for word in reversed(words):
        term = f"nw({word}W, {term})"
    return term


def main() -> int:
    canonical = load("trusted_canonical_subst", ROOT / "canonical.py")
    submitted = load("submitted_solution_subst", ROOT / "solution.py")

    helper_failures = 0
    print("ENTRY_STATE=<initial MPY configuration from core.k lines 49-60>")
    print("ENTRY_REQUIRES=true (all eleven claims)")
    for expected, word in enumerate(WORDS):
        actual = submitted.number_value(word)
        ok = actual == expected
        helper_failures += not ok
        print(
            f"helper word={word!r} satisfying_input=yes "
            f"claimed={expected} submitted={actual} match={str(ok).lower()}"
        )

    samples = [
        [],
        ["zero"],
        ["nine"],
        ["three", "one", "five"],
        ["nine", "zero", "nine", "two", "one"],
        list(reversed(WORDS)),
    ]
    mismatches = 0
    for words in samples:
        concrete_input = " ".join(words)
        trusted = canonical.sort_numbers(concrete_input)
        actual = submitted.sort_numbers(concrete_input)
        # numericOutput is interpreted only through the supplied sortKeyVS
        # contract: stable ascending sort under the supplied key closure.
        interpreted_claim = " ".join(sorted(words, key=WORDS.index))
        ok = trusted == actual == interpreted_claim
        mismatches += not ok
        print(
            json.dumps(
                {
                    "WORDS": numwords_term(words),
                    "encoded_input": concrete_input,
                    "numericOutput_under_sortKeyVS_contract": interpreted_claim,
                    "trusted_python": trusted,
                    "submitted_python": actual,
                    "match": ok,
                },
                sort_keys=True,
            )
        )
    print(f"helper_failure_count={helper_failures}")
    print(f"main_substitution_mismatch_count={mismatches}")
    return 1 if helper_failures or mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
