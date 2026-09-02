#!/usr/bin/env python3
"""Independent candidate/canonical differential for HumanEval 162."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import random
import string
import sys
from typing import Any, Callable


ROOT = Path("/tmp/audit-work/reconstruction")


def load_entry(module_name: str, path: Path) -> Callable[[str], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_to_md5


def outcome(function: Callable[[str], Any], value: str) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(value)}
    except BaseException as error:
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def main() -> int:
    canonical = load_entry("trusted_canonical", ROOT / "canonical.py")
    candidate = load_entry("generated_candidate", ROOT / "solution.py")

    cases: list[tuple[str, str]] = [
        ("documented-empty", ""),
        ("documented-example", "Hello world"),
        ("first-nonempty", "a"),
        ("single-nul", "\0"),
        ("single-space", " "),
        ("padding-55", "a" * 55),
        ("padding-56", "a" * 56),
        ("padding-57", "a" * 57),
        ("block-63", "b" * 63),
        ("block-64", "b" * 64),
        ("block-65", "b" * 65),
        ("two-block-padding-119", "c" * 119),
        ("two-block-padding-120", "c" * 120),
        ("two-block-padding-121", "c" * 121),
        ("length-127", "d" * 127),
        ("length-128", "d" * 128),
        ("length-129", "d" * 129),
        ("ascii-control-boundaries", "\0\t\n\r\x1f\x7f"),
        ("unicode-latin1", "é"),
        ("unicode-bmp", "π"),
        ("unicode-astral", "😀"),
        ("unicode-mixed", "Aπ😀z"),
        ("unicode-surrogate", "\ud800"),
    ]

    rng = random.Random(162)
    alphabet = string.ascii_letters + string.digits + string.punctuation + " \t\n"
    for index in range(100):
        length = rng.choice(
            [0, 1, 2, 7, 15, 31, 54, 55, 56, 57, 63, 64, 65, 79, 80, 119, 120, 127, 128, 129, 191]
        )
        value = "".join(rng.choice(alphabet) for _ in range(length))
        cases.append((f"generated-ascii-{index:03d}-len-{length}", value))

    mismatches: list[dict[str, Any]] = []
    for label, value in cases:
        expected = outcome(canonical, value)
        actual = outcome(candidate, value)
        record = {
            "label": label,
            "input": value,
            "canonical": expected,
            "candidate": actual,
            "match": expected == actual,
        }
        print(json.dumps(record, ensure_ascii=True, sort_keys=True))
        if expected != actual:
            mismatches.append(record)

    print(
        json.dumps(
            {
                "summary": {
                    "total": len(cases),
                    "matches": len(cases) - len(mismatches),
                    "mismatches": len(mismatches),
                    "mismatch_labels": [record["label"] for record in mismatches],
                    "oracle": str(ROOT / "canonical.py"),
                    "candidate": str(ROOT / "solution.py"),
                    "seed": 162,
                }
            },
            sort_keys=True,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
