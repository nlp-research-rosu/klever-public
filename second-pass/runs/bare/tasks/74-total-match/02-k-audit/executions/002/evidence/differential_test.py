#!/usr/bin/env python3
"""Independent differential and contract tests for HumanEval/74."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_entry(module_name: str, source: str):
    spec = importlib.util.spec_from_file_location(module_name, source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.total_match


canonical = load_entry("trusted_canonical_74", "/reference/canonical.py")
generated = load_entry(
    "candidate_solution_74", "/tmp/audit-work/candidate/solution.py"
)


def oracle(first: list[str], second: list[str]) -> list[str]:
    first_total = sum(len(item) for item in first)
    second_total = sum(len(item) for item in second)
    return first if first_total <= second_total else second


documented = [
    ([], []),
    (["hi", "admin"], ["hI", "Hi"]),
    (["hi", "admin"], ["hi", "hi", "admin", "project"]),
    (["hi", "admin"], ["hI", "hi", "hi"]),
    (["4"], ["1", "2", "3", "4", "5"]),
]
boundary = [
    ([""], []),                       # tie at zero; first list
    ([], [""]),                       # tie at zero; first list
    (["a"], [""]),                    # second strictly smaller
    ([""], ["a"]),                    # first strictly smaller
    (["a"], ["b"]),                   # positive tie; first list
    (["", "ab"], ["c", "d"]),         # equal totals, distinct shapes
    (["abc"], ["", "x"]),             # second total smaller
    (["x"], ["abc", ""]),             # first total smaller
    (["é"], ["e\u0301"]),             # Python code-point lengths differ
    (["😀"], ["ab"]),                  # astral code point versus two chars
    (["\x00"], ["x"]),                # embedded NUL, equal code-point totals
    (["\n\t"], ["xy"]),                # control characters, equal totals
    (["a" * 4096], ["b" * 4095]),     # long-string second branch boundary
    (["a" * 4095], ["b" * 4096]),     # long-string first branch boundary
]

seed = 740074
rng = random.Random(seed)
alphabet = ["", "a", "Z", "0", " ", "\n", "é", "λ", "😀", "\x00"]
generated_cases: list[tuple[list[str], list[str]]] = []
for _ in range(4000):
    lists: list[list[str]] = []
    for _side in range(2):
        values = []
        for _item in range(rng.randrange(0, 9)):
            length = rng.randrange(0, 13)
            values.append("".join(rng.choice(alphabet) for _ in range(length)))
        lists.append(values)
    generated_cases.append((lists[0], lists[1]))

cases = documented + boundary + generated_cases
corpus_json = json.dumps(cases, ensure_ascii=False, separators=(",", ":"))
corpus_sha256 = hashlib.sha256(corpus_json.encode()).hexdigest()
branch_counts = {"first_lt": 0, "first_eq": 0, "second_lt": 0}
mismatches = []
for index, (first, second) in enumerate(cases):
    first_total = sum(map(len, first))
    second_total = sum(map(len, second))
    branch = (
        "first_lt"
        if first_total < second_total
        else "first_eq"
        if first_total == second_total
        else "second_lt"
    )
    branch_counts[branch] += 1
    expected = oracle(first, second)
    canonical_result = canonical(first, second)
    generated_result = generated(first, second)
    ok = (
        canonical_result == expected
        and generated_result == expected
        and canonical_result == generated_result
        and canonical_result is expected
        and generated_result is expected
    )
    if not ok:
        mismatches.append(
            {
                "index": index,
                "first": first,
                "second": second,
                "first_total": first_total,
                "second_total": second_total,
                "expected": expected,
                "canonical": canonical_result,
                "generated": generated_result,
            }
        )

print(f"seed={seed}")
print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundary)}")
print(f"generated_cases={len(generated_cases)}")
print(f"total_cases={len(cases)}")
print(f"corpus_sha256={corpus_sha256}")
print(f"branch_counts={branch_counts}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:10], ensure_ascii=False, indent=2))
    raise SystemExit(1)
print("DIFFERENTIAL_PASS")
