#!/usr/bin/env python3
"""Independent differential tests for HumanEval/12."""

from __future__ import annotations

import importlib.util
import itertools
import json
import pathlib
import random
import sys
from typing import Callable, Optional


def load_longest(path: pathlib.Path, module_name: str) -> Callable[[list[str]], Optional[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.longest


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 64

    canonical = load_longest(pathlib.Path(sys.argv[1]), "trusted_canonical")
    candidate = load_longest(pathlib.Path(sys.argv[2]), "generated_candidate")

    named_cases: list[tuple[str, list[str]]] = [
        ("documented-empty", []),
        ("documented-first-tie", ["a", "b", "c"]),
        ("documented-increasing", ["a", "bb", "ccc"]),
        ("single-element", [""]),
        ("strict-growth-true", ["a", "bb"]),
        ("strict-growth-false-shorter", ["aa", "b"]),
        ("strict-growth-false-equal", ["aa", "bb"]),
        ("late-longest", ["long", "", "x", "longest"]),
        ("late-tie-keeps-first", ["long", "x", "also"]),
        ("empty-string-tie", ["", ""]),
        ("unicode-codepoints", ["é", "e\u0301", "🙂🙂"]),
        ("embedded-controls", ["a\x00", "a\nb", "\t"]),
    ]

    pool = ["", "a", "b", "aa", "ab", "é", "e\u0301", "🙂", "🙂🙂"]
    exhaustive = [
        list(items)
        for length in range(0, 5)
        for items in itertools.product(pool, repeat=length)
    ]

    rng = random.Random(120072026)
    alphabet = ["", "a", "b", "é", "\u0301", "🙂", "\x00", "\n", "漢"]
    generated: list[list[str]] = []
    for _ in range(2500):
        count = rng.randint(0, 24)
        generated.append(
            [
                "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 30)))
                for _ in range(count)
            ]
        )

    cases = [(name, value) for name, value in named_cases]
    cases += [(f"exhaustive-{index}", value) for index, value in enumerate(exhaustive)]
    cases += [(f"generated-{index}", value) for index, value in enumerate(generated)]

    mismatches: list[dict[str, object]] = []
    for name, strings in cases:
        expected = canonical(strings)
        actual = candidate(strings)
        if expected != actual:
            mismatches.append(
                {"name": name, "input": strings, "canonical": expected, "candidate": actual}
            )

    for name, strings in named_cases:
        print(
            "NAMED "
            + json.dumps(
                {
                    "name": name,
                    "input": strings,
                    "canonical": canonical(strings),
                    "candidate": candidate(strings),
                },
                ensure_ascii=True,
                sort_keys=True,
            )
        )
    print(f"named_cases={len(named_cases)}")
    print(f"exhaustive_cases={len(exhaustive)}")
    print(f"generated_cases={len(generated)}")
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH " + json.dumps(mismatch, ensure_ascii=True, sort_keys=True))
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
