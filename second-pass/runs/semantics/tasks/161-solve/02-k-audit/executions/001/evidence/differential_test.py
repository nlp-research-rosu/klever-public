#!/usr/bin/env python3
"""Independent canonical-vs-submitted differential test for HumanEval 161."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
SUBMITTED_PATH = Path("/tmp/audit-work/161-solve/source/solution.py")


def load_solve(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


canonical_solve = load_solve("trusted_canonical_161", CANONICAL_PATH)
submitted_solve = load_solve("submitted_solution_161", SUBMITTED_PATH)

# Documented examples, empty input, one- and two-character branch boundaries,
# letters in each position, non-letters, cased Unicode, uncased Unicode letters,
# combining marks, and supplementary-plane characters.
named_cases = [
    "",
    "1234",
    "ab",
    "#a@C",
    "0",
    "!",
    "01",
    "!?",
    "a",
    "A",
    "a1",
    "1a",
    "A!",
    "!A",
    "a1B!",
    "ß",
    "ß1",
    "İ",
    "é9",
    "e\u0301",
    "中",
    "中文",
    "中文1",
    "中a",
    "a中",
    "αβ",
    "🙂!",
    "𐀀𐀁",
]

# Exhaust all short strings over symbols that exercise each ASCII branch.
ascii_generated = [
    "".join(chars)
    for length in range(0, 6)
    for chars in itertools.product(("a", "A", "0", "!"), repeat=length)
]

# Exhaust short strings over cased letters, uncased alphabetic code points, and
# non-letters. This is the critical Python-string boundary for this rewrite.
unicode_generated = [
    "".join(chars)
    for length in range(0, 4)
    for chars in itertools.product(("中", "文", "a", "ß", "1", "🙂"), repeat=length)
]

cases = list(dict.fromkeys(named_cases + ascii_generated + unicode_generated))
mismatches = []

for value in cases:
    try:
        expected = canonical_solve(value)
        expected_exc = None
    except Exception as err:  # pragma: no cover - evidence path
        expected = None
        expected_exc = (type(err).__name__, str(err))
    try:
        actual = submitted_solve(value)
        actual_exc = None
    except Exception as err:  # pragma: no cover - evidence path
        actual = None
        actual_exc = (type(err).__name__, str(err))
    if (expected, expected_exc) != (actual, actual_exc):
        mismatches.append(
            {
                "input": value,
                "canonical": expected,
                "canonical_exception": expected_exc,
                "submitted": actual,
                "submitted_exception": actual_exc,
            }
        )

print(f"canonical={CANONICAL_PATH}")
print(f"submitted={SUBMITTED_PATH}")
print(f"named_cases={len(named_cases)}")
print(f"ascii_generated={len(ascii_generated)} alphabet=['a','A','0','!'] lengths=0..5")
print(
    "unicode_generated="
    f"{len(unicode_generated)} alphabet=['中','文','a','ß','1','🙂'] lengths=0..3"
)
print(f"unique_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:80]:
    print(json.dumps(mismatch, ensure_ascii=False, sort_keys=True))
if len(mismatches) > 80:
    print(f"... {len(mismatches) - 80} additional mismatches omitted from bounded log")

raise SystemExit(1 if mismatches else 0)
