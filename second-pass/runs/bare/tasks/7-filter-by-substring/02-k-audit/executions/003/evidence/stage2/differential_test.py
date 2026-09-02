#!/usr/bin/env python3
"""Independent differential test for HumanEval/7.

Oracle and candidate are imported from explicit mounted/scratch paths.  The
test vectors are deterministic and include every predicate branch boundary,
the prompt examples, Unicode, duplicates, and generated small cases.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_substring


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(Path("/tmp/audit-work/source/solution.py"), "candidate_solution")

curated = [
    ([], "a"),
    (["abc", "bacd", "cde", "array"], "a"),
    ([], ""),
    ([""], ""),
    ([""], "a"),
    (["a"], "a"),
    (["a"], ""),
    (["a"], "aa"),
    (["ab", "ba", "cab", "xyz"], "ab"),
    (["prefix", "xprefix", "prefixx", "pre"], "prefix"),
    (["x", "x", ""], ""),
    (["aaaa", "baaab", "bbb"], "aaa"),
    (["é", "café", "e\u0301"], "é"),
    (["🙂", "a🙂b", "🙃"], "🙂"),
    (["line\nbreak", "tab\tchar", "plain"], "\n"),
    (["a\x00b", "\x00", "ab"], "\x00"),
]

rng = random.Random(7007)
alphabet = ["", "a", "b", "ab", "ba", "aa", "🙂", "a🙂"]
substrings = ["", "a", "b", "ab", "bb", "🙂", "a🙂", "🙂a"]
generated = []

# Exhaust all lists of length 0..2 over the small value alphabet.
for length in range(3):
    for values in itertools.product(alphabet, repeat=length):
        for needle in substrings:
            generated.append((list(values), needle))

# Add deterministic larger representative lists.
for _ in range(400):
    length = rng.randrange(0, 9)
    values = [rng.choice(alphabet) for _ in range(length)]
    generated.append((values, rng.choice(substrings)))

cases = curated + generated
mismatches = []
print(f"curated_cases={len(curated)}")
for index, (strings, substring) in enumerate(curated):
    expected = canonical(strings, substring)
    actual = candidate(strings, substring)
    print(
        f"CURATED {index:02d}: strings={strings!r} substring={substring!r} "
        f"canonical={expected!r} candidate={actual!r}"
    )

for index, (strings, substring) in enumerate(cases):
    expected = canonical(strings, substring)
    actual = candidate(strings, substring)
    if actual != expected:
        mismatches.append((index, strings, substring, expected, actual))

print("generated_scope=all lists length 0..2 over 8 strings x 8 substrings")
print("random_scope=400 lists length 0..8, seed=7007")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
