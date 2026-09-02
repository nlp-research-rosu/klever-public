#!/usr/bin/env python3
"""Compare the trusted HumanEval implementation with the submitted Python one."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import random
import string


def load_function(path: Path):
    spec = importlib.util.spec_from_file_location(f"module_{path.stem}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_palindrome


canonical = load_function(Path("/reference/canonical.py"))
candidate = load_function(Path("/tmp/audit-work/source/solution.py"))

# Prompt examples, empty/small boundaries, equality/mismatch positions,
# whitespace/control characters, combining characters, and non-BMP code points.
fixed_inputs = [
    "",
    "aba",
    "aaaaa",
    "zbcd",
    "a",
    "aa",
    "ab",
    "abc",
    "abba",
    "abca",
    "a b a",
    " a ",
    "\x00",
    "\x00a\x00",
    "\n\t\n",
    "été",
    "éte",
    "e\u0301x\u0301e",
    "🙂",
    "🙂🙃🙂",
    "🙂🙃",
    "𐀀x𐀀",
]

rng = random.Random(480048)
alphabet = list(string.ascii_letters + string.digits + " _-\n\t") + [
    "é",
    "中",
    "🙂",
    "\u0301",
    "\x00",
]
random_inputs: list[str] = []
for length in range(0, 33):
    for _ in range(40):
        random_inputs.append("".join(rng.choice(alphabet) for _ in range(length)))
        half = "".join(rng.choice(alphabet) for _ in range(length))
        random_inputs.append(half + half[::-1])

cases = fixed_inputs + random_inputs
mismatches = []
true_count = 0
false_count = 0
for index, text in enumerate(cases):
    expected = canonical(text)
    actual = candidate(text)
    if expected:
        true_count += 1
    else:
        false_count += 1
    if type(expected) is not bool or type(actual) is not bool or expected != actual:
        mismatches.append(
            {
                "index": index,
                "input": text,
                "canonical": expected,
                "candidate": actual,
                "canonical_type": type(expected).__name__,
                "candidate_type": type(actual).__name__,
            }
        )

summary = {
    "oracle": "/reference/canonical.py:is_palindrome",
    "candidate": "/tmp/audit-work/source/solution.py:is_palindrome",
    "seed": 480048,
    "fixed_cases": len(fixed_inputs),
    "random_cases": len(random_inputs),
    "total_cases": len(cases),
    "true_results": true_count,
    "false_results": false_count,
    "mismatch_count": len(mismatches),
    "fixed_results": [
        {
            "input": text,
            "canonical": canonical(text),
            "candidate": candidate(text),
        }
        for text in fixed_inputs
    ],
    "mismatches": mismatches[:20],
}
print(json.dumps(summary, ensure_ascii=True, indent=2))
raise SystemExit(1 if mismatches else 0)
