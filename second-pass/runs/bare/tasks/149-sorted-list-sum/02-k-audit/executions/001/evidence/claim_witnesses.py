#!/usr/bin/env python3
"""Concrete satisfying witnesses for every entry claim in spec.k."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


def expected(words: list[str]) -> list[str]:
    return sorted(
        (word for word in words if len(word) % 2 == 0),
        key=lambda word: (len(word), word),
    )


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: claim_witnesses.py CANONICAL GENERATED")
        return 2
    canonical = load(Path(sys.argv[1]), "witness_canonical")
    generated = load(Path(sys.argv[2]), "witness_generated")
    witnesses = [
        ("universal-correctness", [], "INPUT=.Words"),
        ("base", [], "fixed empty list"),
        (
            "symbolic-two",
            ["aa", "bb"],
            "length(A)=length(B)=2 and A < B",
        ),
        (
            "symbolic-two-reverse",
            ["bb", "aa"],
            "length(A)=length(B)=2 and not(A < B)",
        ),
        (
            "symbolic-three",
            ["zzzz", "aa", "odd"],
            "length(A)=4, length(B)=2, length(C)=3",
        ),
        ("prompt-example-one", ["aa", "a", "aaa"], "fixed example"),
        (
            "prompt-example-two",
            ["ab", "a", "aaa", "cd"],
            "fixed example",
        ),
    ]
    bad = 0
    for claim, words, precondition in witnesses:
        want = expected(words)
        c_result = canonical(list(words))
        g_result = generated(list(words))
        matches = c_result == want and g_result == want
        bad += not matches
        print(
            json.dumps(
                {
                    "claim": claim,
                    "precondition_witness": precondition,
                    "input": words,
                    "claimed_ascii_result": want,
                    "canonical_result": c_result,
                    "generated_result": g_result,
                    "matches": matches,
                },
                separators=(",", ":"),
            )
        )

    unicode_words = ["😀"]
    print(
        json.dumps(
            {
                "claim": "universal-correctness",
                "additional_satisfying_input": unicode_words,
                "python_contract_result": expected(unicode_words),
                "note": "fresh K execution is preserved separately in unicode_witness.log",
            },
            ensure_ascii=False,
            separators=(",", ":"),
        )
    )
    return int(bool(bad))


if __name__ == "__main__":
    raise SystemExit(main())
