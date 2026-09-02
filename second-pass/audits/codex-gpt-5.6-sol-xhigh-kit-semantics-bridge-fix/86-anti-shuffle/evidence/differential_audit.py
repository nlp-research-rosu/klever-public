#!/usr/bin/env python3
"""Independent differential test for HumanEval 86 anti_shuffle."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    solution = load_entry(args.solution, "candidate_solution")

    documented = ["Hi", "hello", "Hello World!!!"]
    boundaries = [
        "", " ", "  ", "   ", "a", "a ", " a", " a ", "a  b",
        "ba", "ab", "b a", "B a", "!a0 Zz~", "\tba\n", "éa Ωß",
    ]
    alphabet = " aAzZ09!~"
    exhaustive = [
        "".join(chars)
        for length in range(6)
        for chars in itertools.product(alphabet, repeat=length)
    ]
    rng = random.Random(860086)
    random_alphabet = " abcXYZ019!?~\t\néΩß🙂"
    generated = [
        "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(65)))
        for _ in range(2048)
    ]

    groups = [
        ("documented", documented),
        ("boundaries", boundaries),
        ("exhaustive_len_0_to_5", exhaustive),
        ("seeded_random", generated),
    ]
    seen: set[str] = set()
    checked = 0
    mismatches: list[dict[str, str]] = []
    digest = hashlib.sha256()
    group_counts: dict[str, int] = {}
    samples: dict[str, list[dict[str, str]]] = {}

    for group_name, cases in groups:
        group_count = 0
        samples[group_name] = []
        for value in cases:
            if value in seen:
                continue
            seen.add(value)
            expected = canonical(value)
            actual = solution(value)
            checked += 1
            group_count += 1
            digest.update(json.dumps([value, expected, actual], ensure_ascii=False).encode())
            if len(samples[group_name]) < 5:
                samples[group_name].append(
                    {"input": value, "canonical": expected, "solution": actual}
                )
            if expected != actual:
                mismatches.append(
                    {"input": value, "canonical": expected, "solution": actual}
                )
                if len(mismatches) >= 20:
                    break
        group_counts[group_name] = group_count
        if mismatches:
            break

    print(json.dumps({
        "canonical": str(args.canonical.resolve()),
        "solution": str(args.solution.resolve()),
        "input_groups": group_counts,
        "checked_unique": checked,
        "mismatch_count": len(mismatches),
        "samples": samples,
        "result_digest_sha256": digest.hexdigest(),
        "first_mismatches": mismatches,
    }, indent=2, ensure_ascii=False, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
