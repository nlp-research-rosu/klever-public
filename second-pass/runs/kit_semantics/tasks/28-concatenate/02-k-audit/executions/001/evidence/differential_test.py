#!/usr/bin/env python3
"""Independent differential test for HumanEval/28 concatenate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path
from types import ModuleType


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/candidate/solution.py")
SEED = 280028
GENERATED_CASES = 1000
ALPHABET = [
    "",
    "a",
    "Z",
    "0",
    " ",
    "\n",
    "\x00",
    "é",
    "e\u0301",
    "λ",
    "中",
    "🙂",
]


def import_file(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_cases() -> list[list[str]]:
    fixed = [
        [],  # documented empty example and zero-iteration boundary
        ["a", "b", "c"],  # documented multi-iteration example
        [""],  # one-iteration boundary, empty member
        ["x"],  # one-iteration boundary, nonempty member
        ["", ""],
        ["left", "", "right"],
        [" ", "\n", "\t"],
        ["é", "e\u0301", "λ", "中", "🙂"],
        ["\x00", "a\x00b"],
        ["a" * 4096, "", "b" * 4096],
    ]
    rng = random.Random(SEED)
    generated: list[list[str]] = []
    for _ in range(GENERATED_CASES):
        values: list[str] = []
        for _ in range(rng.randrange(0, 13)):
            values.append("".join(rng.choice(ALPHABET) for _ in range(rng.randrange(0, 21))))
        generated.append(values)
    return fixed + generated


def main() -> int:
    canonical = import_file("trusted_canonical", CANONICAL_PATH)
    candidate = import_file("generated_candidate", CANDIDATE_PATH)
    cases = make_cases()
    serialized = json.dumps(cases, ensure_ascii=True, separators=(",", ":")).encode()
    mismatches: list[dict[str, object]] = []
    for index, values in enumerate(cases):
        expected = canonical.concatenate(values)
        actual = candidate.concatenate(values)
        if actual != expected or type(actual) is not type(expected):
            mismatches.append(
                {
                    "index": index,
                    "input": values,
                    "canonical": expected,
                    "candidate": actual,
                    "canonical_type": type(expected).__name__,
                    "candidate_type": type(actual).__name__,
                }
            )
    report = {
        "canonical": str(CANONICAL_PATH),
        "candidate": str(CANDIDATE_PATH),
        "seed": SEED,
        "generated_cases": GENERATED_CASES,
        "fixed_cases": len(cases) - GENERATED_CASES,
        "total_cases": len(cases),
        "serialized_inputs_sha256": hashlib.sha256(serialized).hexdigest(),
        "inputs": cases,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
    }
    if len(sys.argv) != 2:
        print("usage: differential_test.py REPORT.json", file=sys.stderr)
        return 2
    report_path = Path(sys.argv[1])
    report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n")
    print(
        json.dumps(
            {key: value for key, value in report.items() if key not in {"inputs", "mismatches"}},
            ensure_ascii=True,
            indent=2,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
