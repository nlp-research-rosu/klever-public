#!/usr/bin/env python3
"""Independent return-value differential for HumanEval 149.

The test imports the immutable trusted canonical implementation and the exact
candidate solution copied into the clean reconstruction directory.  Inputs are
copied before each call because the canonical implementation sorts its argument
in place as an incidental side effect.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sorted_list_sum


def contract_oracle(words: list[str]) -> list[str]:
    """Filter even-length words, then order by (length, Unicode text)."""
    return sorted((word for word in words if len(word) % 2 == 0), key=lambda word: (len(word), word))


def main() -> int:
    canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_function(
        "candidate_solution", Path("/tmp/audit-work/reconstruction/solution.py")
    )

    named_cases = [
        ("prompt-one", ["aa", "a", "aaa"]),
        ("prompt-two", ["ab", "a", "aaa", "cd"]),
        ("empty-list", []),
        ("empty-string-even", [""]),
        ("all-odd", ["a", "abc", "12345"]),
        ("all-even-length-boundaries", ["", "aa", "bbbb"]),
        ("mixed-length", ["zzzz", "aa", "", "bbb", "c"]),
        ("same-length-lexicographic", ["zy", "ab", "aa", "ba"]),
        ("duplicates", ["ab", "a", "ab", "aa", "aa"]),
        ("unicode-codepoints", ["éé", "e\u0301", "😀😀", "😀", "αβ", "βa"]),
        ("escaping", ['a"', "a\\", "\n\n", "\x00\x00"]),
    ]
    pool = ["", "a", "b", "aa", "ab", "ba", "abc", "zzzz", "é", "😀", "e\u0301"]
    generated_cases = (
        list(items)
        for size in range(5)
        for items in itertools.product(pool, repeat=size)
    )

    mismatches: list[dict[str, object]] = []
    canonical_input_mutations = 0
    candidate_input_mutations = 0
    total = 0
    input_digest = hashlib.sha256()

    def check(label: str, words: list[str]) -> None:
        nonlocal canonical_input_mutations, candidate_input_mutations, total
        total += 1
        input_digest.update(
            json.dumps(words, ensure_ascii=True, separators=(",", ":")).encode()
            + b"\n"
        )
        canonical_arg = list(words)
        candidate_arg = list(words)
        expected = contract_oracle(words)
        canonical_result = canonical(canonical_arg)
        candidate_result = generated(candidate_arg)
        canonical_input_mutations += canonical_arg != words
        candidate_input_mutations += candidate_arg != words
        if canonical_result != expected or candidate_result != expected:
            mismatches.append(
                {
                    "label": label,
                    "input": words,
                    "oracle": expected,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                }
            )

    for label, words in named_cases:
        check(label, words)
        print(
            "NAMED "
            + json.dumps(
                {
                    "label": label,
                    "input": words,
                    "output": generated(list(words)),
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
    for index, words in enumerate(generated_cases):
        check(f"product-{index}", words)

    print(f"pool={json.dumps(pool, ensure_ascii=True)}")
    print("generated_sizes=0..4 inclusive")
    print(f"total_cases={total}")
    print(f"input_stream_sha256={input_digest.hexdigest()}")
    print(f"return_value_mismatches={len(mismatches)}")
    print(f"canonical_argument_mutations={canonical_input_mutations}")
    print(f"candidate_argument_mutations={candidate_input_mutations}")
    if mismatches:
        print("FIRST_MISMATCH " + json.dumps(mismatches[0], ensure_ascii=True))
        return 1
    print("DIFFERENTIAL_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
