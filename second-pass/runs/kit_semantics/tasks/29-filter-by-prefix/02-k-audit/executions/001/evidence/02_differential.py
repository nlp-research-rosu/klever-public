#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval/29."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_function(Path("/tmp/audit-work/work/solution.py"), "generated_solution")

named_cases = [
    ("documented-empty", [], "a"),
    ("documented-mixed", ["abc", "bcd", "cde", "array"], "a"),
    ("empty-prefix", ["", "x", "xy"], ""),
    ("empty-string-nonempty-prefix", [""], "a"),
    ("equal-prefix", ["abc"], "abc"),
    ("longer-prefix", ["abc"], "abcd"),
    ("one-shorter-prefix", ["abc"], "ab"),
    ("true-false-boundary", ["a", "b", "aa", ""], "a"),
    ("duplicates-and-order", ["ab", "x", "ab", "abc"], "ab"),
    ("unicode", ["α", "αβ", "β", "😀alpha", "😀"], "😀"),
    ("nul-and-newline", ["a\x00b", "a\n", "\n", "\x00"], "a"),
]

corpus = ["", "a", "b", "aa", "ab", "ba", "abc", "α", "αβ", "😀", "😀a", "a\x00"]
prefixes = ["", "a", "b", "aa", "ab", "abc", "α", "αβ", "β", "😀", "😀a", "\x00"]

cases: list[tuple[list[str], str]] = [(items, prefix) for _, items, prefix in named_cases]
for length in range(4):
    for items in itertools.product(corpus[:7], repeat=length):
        for prefix in prefixes[:7]:
            cases.append((list(items), prefix))

rng = random.Random(290729)
alphabet = ["", "a", "b", "é", "α", "😀", "\x00", "\n"]
for _ in range(2500):
    items = []
    for _ in range(rng.randrange(0, 9)):
        size = rng.randrange(0, 10)
        items.append("".join(rng.choice(alphabet) for _ in range(size)))
    prefix_size = rng.randrange(0, 7)
    prefix = "".join(rng.choice(alphabet) for _ in range(prefix_size))
    cases.append((items, prefix))

digest = hashlib.sha256()
mismatches = []
for index, (items, prefix) in enumerate(cases):
    expected = canonical(items, prefix)
    actual = candidate(items, prefix)
    digest.update(
        json.dumps(
            [items, prefix, expected, actual],
            ensure_ascii=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    digest.update(b"\n")
    if actual != expected:
        mismatches.append((index, items, prefix, expected, actual))

print("COMMAND: python3 /audit-output/evidence/02_differential.py")
print("oracle=/reference/canonical.py:filter_by_prefix")
print("candidate=/tmp/audit-work/work/solution.py:filter_by_prefix")
print("formal_input_domain=list[str], prefix=str")
print("generated_scope=exhaustive corpus[0:7] lists of lengths 0..3 x 7 prefixes; plus 2500 seed-290729 cases")
for name, items, prefix in named_cases:
    print(
        "NAMED",
        name,
        "input=" + repr((items, prefix)),
        "expected=" + repr(canonical(items, prefix)),
        "actual=" + repr(candidate(items, prefix)),
    )
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
print(f"result_digest_sha256={digest.hexdigest()}")
for mismatch in mismatches[:20]:
    print("MISMATCH", repr(mismatch))
raise SystemExit(1 if mismatches else 0)
