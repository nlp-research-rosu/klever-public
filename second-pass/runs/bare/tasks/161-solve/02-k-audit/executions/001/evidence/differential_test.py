#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for solve()."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
from types import ModuleType


RESULTS = Path("/audit-output/evidence/differential-results.jsonl")


def load(name: str, path: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_cases() -> list[tuple[str, str]]:
    cases: list[tuple[str, str]] = [
        ("documented", "1234"),
        ("documented", "ab"),
        ("documented", "#a@C"),
        ("boundary", ""),
        ("boundary", "a"),
        ("boundary", "A"),
        ("boundary", "0"),
        ("boundary", "#"),
        ("boundary", "a1"),
        ("boundary", "1a"),
        ("boundary", "A#z"),
        ("unicode-boundary", "é"),
        ("unicode-boundary", "é1"),
        ("unicode-boundary", "αΒ"),
        ("unicode-boundary", "ß"),
        ("unicode-boundary", "中"),
        ("unicode-boundary", "🙂"),
        ("unicode-boundary", "Ⅰ"),
        ("unicode-boundary", "aⅠ"),
        ("unicode-boundary", "Ⅰa"),
        ("unicode-boundary", "a\u0345"),
    ]

    alphabet = ("a", "Z", "0", "#", "é", "Ⅰ", "\u0345", "🙂")
    for length in range(5):
        for symbols in itertools.product(alphabet, repeat=length):
            cases.append(("generated-length-0-through-4", "".join(symbols)))

    unique: list[tuple[str, str]] = []
    seen: set[str] = set()
    for origin, value in cases:
        if value not in seen:
            unique.append((origin, value))
            seen.add(value)
    return unique


def main() -> int:
    canonical = load("trusted_canonical", "/tmp/audit-work/trusted/canonical.py")
    generated = load("generated_solution", "/tmp/audit-work/candidate-src/solution.py")
    cases = build_cases()
    mismatches: list[dict[str, object]] = []

    with RESULTS.open("w", encoding="utf-8") as output:
        for index, (origin, value) in enumerate(cases):
            expected = canonical.solve(value)
            actual = generated.solve(value)
            record = {
                "index": index,
                "origin": origin,
                "input": value,
                "canonical": expected,
                "generated": actual,
                "match": expected == actual,
            }
            output.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            if expected != actual:
                mismatches.append(record)

    print(f"python_cases={len(cases)} mismatches={len(mismatches)}")
    print(f"full_results={RESULTS}")
    for mismatch in mismatches[:40]:
        print("MISMATCH", json.dumps(mismatch, ensure_ascii=False, sort_keys=True))
    if len(mismatches) > 40:
        print(f"... {len(mismatches) - 40} additional mismatches in full results")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
