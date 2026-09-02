#!/usr/bin/env python3
"""Independent differential test for HumanEval/29.

The oracle and candidate are imported from their separately copied source files.
The generated space is deterministic and described in the final output.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
from typing import Callable


ROOT = Path("/tmp/audit-work/29-filter-by-prefix")
CANONICAL_PATH = ROOT / "trusted" / "canonical.py"
CANDIDATE_PATH = ROOT / "candidate-src" / "solution.py"


def load_entry(path: Path, module_name: str) -> Callable[[list[str], str], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix


oracle = load_entry(CANONICAL_PATH, "trusted_canonical")
candidate = load_entry(CANDIDATE_PATH, "submitted_solution")

documented_and_boundary_cases: list[tuple[list[str], str]] = [
    ([], "a"),
    (["abc", "bcd", "cde", "array"], "a"),
    ([], ""),
    ([""], ""),
    ([""], "a"),
    (["a"], "a"),
    (["a"], "aa"),
    (["aa"], "a"),
    (["ba"], "a"),
    (["a", "aa", "ba"], "aa"),
    (["a", "a", "ba", "a"], "a"),
    (["prefix", "pre", "prefixes", "xprefix"], "prefix"),
    (["éclair", "élan", "eclair", "😊x"], "é"),
    (["😊", "😊x", "x😊"], "😊"),
]

atoms = ["", "a", "b", "aa", "ab", "ba", "bb"]
prefixes = ["", "a", "b", "aa", "ab", "ba", "bb", "aaa"]
generated_lists = [
    list(items)
    for length in range(0, 4)
    for items in itertools.product(atoms, repeat=length)
]
generated_cases = [
    (strings, prefix)
    for strings in generated_lists
    for prefix in prefixes
]

all_cases = documented_and_boundary_cases + generated_cases
mismatches: list[dict[str, object]] = []
for strings, prefix in all_cases:
    expected = oracle(list(strings), prefix)
    actual = candidate(list(strings), prefix)
    if actual != expected:
        mismatches.append(
            {
                "strings": strings,
                "prefix": prefix,
                "canonical": expected,
                "candidate": actual,
            }
        )

print(
    json.dumps(
        {
            "oracle": str(CANONICAL_PATH),
            "candidate": str(CANDIDATE_PATH),
            "documented_and_boundary_cases": documented_and_boundary_cases,
            "generated_domain": {
                "element_atoms": atoms,
                "list_lengths": [0, 1, 2, 3],
                "prefixes": prefixes,
                "generated_list_count": len(generated_lists),
                "generated_case_count": len(generated_cases),
            },
            "total_case_count": len(all_cases),
            "mismatch_count": len(mismatches),
            "mismatches": mismatches[:20],
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
)

raise SystemExit(1 if mismatches else 0)
