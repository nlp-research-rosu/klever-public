#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for reverse_delete."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.reverse_delete


def words(alphabet: str, maximum_length: int):
    for length in range(maximum_length + 1):
        for chars in itertools.product(alphabet, repeat=length):
            yield "".join(chars)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    candidate = load_entry(args.candidate, "scratch_candidate")

    cases: list[dict[str, str]] = []

    def add(category: str, s: str, c: str):
        cases.append({"category": category, "s": s, "c": c})

    add("example", "abcde", "ae")
    add("example", "abcdef", "b")
    add("example", "abcdedcba", "ab")

    boundary = [
        ("", ""),
        ("", "x"),
        ("a", ""),
        ("a", "a"),
        ("a", "b"),
        ("aa", ""),
        ("ab", ""),
        ("aba", ""),
        ("abba", "x"),
        ("aaaa", "a"),
        ("abab", "a"),
        ("mississippi", "isp"),
        ("🙂a🙂", ""),
        ("🙂a🙂", "🙂"),
        ("e\u0301x\u0301e", "\u0301"),
        ("\u0000a\u0000", "\u0000"),
    ]
    for s, c in boundary:
        add("boundary", s, c)

    for s in words("ab", 6):
        for c in words("ab", 3):
            add("exhaustive-small", s, c)

    rng = random.Random(112)
    alphabet = "abcXYZ09🙂é\u0301"
    for _ in range(500):
        s = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 25)))
        c = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 10)))
        add("generated-seed-112", s, c)

    args.inputs_out.write_text(
        json.dumps(cases, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    mismatches = []
    category_counts: dict[str, int] = {}
    for index, case in enumerate(cases):
        category_counts[case["category"]] = category_counts.get(case["category"], 0) + 1
        expected = canonical(case["s"], case["c"])
        actual = candidate(case["s"], case["c"])
        if actual != expected or type(actual) is not type(expected):
            mismatches.append(
                {
                    "index": index,
                    "case": case,
                    "canonical": repr(expected),
                    "candidate": repr(actual),
                }
            )

    print(f"canonical={args.canonical.resolve()}")
    print(f"candidate={args.candidate.resolve()}")
    print(f"input_manifest={args.inputs_out.resolve()}")
    print(f"category_counts={json.dumps(category_counts, sort_keys=True)}")
    print(f"total_cases={len(cases)}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:20], ensure_ascii=True, indent=2))
        return 1
    print("RESULT: all candidate results exactly matched the trusted canonical")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
