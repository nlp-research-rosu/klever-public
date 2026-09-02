#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval 153."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[str, list[str]], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(Path("/tmp/audit-work/candidate-src/solution.py"), "generated_solution")


def outcome(fn: Callable[..., Any], class_name: str, extensions: list[str]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": fn(class_name, extensions)}
    except Exception as err:  # Differentially compare the documented empty-list boundary.
        return {"kind": "exception", "type": type(err).__name__, "message": str(err)}


named_cases: list[tuple[str, list[str], str]] = [
    ("Slices", ["SErviNGSliCes", "Cheese", "StuFfed"], "prompt worked example"),
    ("my_class", ["AA", "Be", "CC"], "prompt tie example"),
    ("C", [], "empty extension list boundary"),
    ("", [""], "empty class and empty extension name"),
    ("C", ["Zz"], "singleton"),
    ("C", ["abc", "AB", "A-b"], "strict replacement branches"),
    ("C", ["a-1", "--", "A!"], "uncased punctuation and digits"),
    ("C", ["abcd", "a", "xy"], "all-negative scores"),
    ("κλάση", ["é", "É"], "non-ASCII lower/upper boundary"),
    ("类", ["Ω", "ω", "ǅ", "٣", "🙂"], "Unicode categories and uncased characters"),
]

cases: list[tuple[str, list[str], str]] = list(named_cases)

# Exhaust every nonempty list of length 1..3 over a compact branch-covering pool.
small_pool = ["", "A", "a", "-", "Aa", "AA", "aa", "É", "é"]
for length in range(1, 4):
    for exts in itertools.product(small_pool, repeat=length):
        cases.append(("C", list(exts), f"exhaustive pool length {length}"))

# Add a deterministic broader generated sample.
rng = random.Random(153)
alphabet = "ABabZz09-_.ÉéΩωǅ٣🙂"
for index in range(2000):
    class_name = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 8)))
    extensions = [
        "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 10)))
        for _ in range(rng.randrange(1, 7))
    ]
    cases.append((class_name, extensions, f"generated-{index}"))

mismatches: list[dict[str, Any]] = []
for class_name, extensions, label in cases:
    expected = outcome(canonical, class_name, extensions)
    observed = outcome(candidate, class_name, extensions)
    if expected != observed:
        mismatches.append(
            {
                "label": label,
                "class_name": class_name,
                "extensions": extensions,
                "canonical": expected,
                "candidate": observed,
            }
        )

report = {
    "oracle": "/reference/canonical.py:Strongest_Extension",
    "candidate": "/tmp/audit-work/candidate-src/solution.py:Strongest_Extension",
    "named_cases": len(named_cases),
    "exhaustive_pool": small_pool,
    "exhaustive_lengths": [1, 2, 3],
    "generated_seed": 153,
    "generated_cases": 2000,
    "total_cases": len(cases),
    "mismatch_count": len(mismatches),
    "mismatches": mismatches[:20],
}
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(1 if mismatches else 0)
