#!/usr/bin/env python3
"""Generate concrete K runs from the freshly translated solution Module."""

from __future__ import annotations

import json
import sys
from pathlib import Path


CASES = {
    "empty": [],
    "prompt_one": ["aa", "a", "aaa"],
    "all_odd": ["a", "bbb", "ccccc"],
    "ordering_duplicates": ["zy", "ab", "x", "aa", "abcd", "ba", "ab"],
    "empty_string_lengths": ["aaaa", "aa", "", "bbb", "b", "zz"],
    "emoji_single": ["😀"],
    "latin1_single": ["é"],
    "combining_pair": ["e\u0301"],
    "unicode_length_order": ["😀😀", "aaaa"],
    "unicode": ["😀", "é", "e\u0301", "😀😀", "éé", ""],
    "reverse_equal": ["ba", "ab", "ab"],
}


def quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def oracle(words: list[str]) -> list[str]:
    return sorted(
        (word for word in words if len(word) % 2 == 0),
        key=lambda word: (len(word), word),
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: generate_concrete_cases.py SCRATCH_DIR")
        return 2
    scratch = Path(sys.argv[1])
    module = (scratch / "solution.mpy").read_text(encoding="utf-8").strip()

    for name, words in CASES.items():
        list_expr = "ListExpr(" + ", ".join(f"Str({quote(word)})" for word in words) + ")"
        run = (
            f'Run({module}, Call(Name("sorted_list_sum"), {list_expr}))\n'
        )
        expected = oracle(words)
        expected_words = " , ".join(quote(word) for word in expected)
        if expected_words:
            expected_words += " , .Words"
        else:
            expected_words = ".Words"
        fragment = f"Result ( VList ( {expected_words} ) )"

        (scratch / f"audit-{name}.run").write_text(run, encoding="utf-8")
        (scratch / f"audit-{name}.expected").write_text(
            fragment + "\n", encoding="utf-8"
        )
        print(
            json.dumps(
                {"case": name, "input": words, "expected": expected},
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
