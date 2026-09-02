#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test.

Input scope:
* all documented examples;
* explicit empty/space-only, n=0, below/equal/above-count, case, and repeated
  whitespace boundaries;
* every string of length 0..6 over ``aEbZ `` for every n in 0..7;
* 10,000 deterministic generated strings of length 0..80 over ASCII letters
  and space, with n sampled from 0..len(s)+3.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import string
import sys


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.select_words


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(
    Path("/tmp/audit-work/proof/solution.py"), "generated_solution"
)

documented = [
    ("Mary had a little lamb", 4, ["little"]),
    ("Mary had a little lamb", 3, ["Mary", "lamb"]),
    ("simple white space", 2, []),
    ("Hello world", 4, ["world"]),
    ("Uncle sam", 3, ["Uncle"]),
]

boundaries = [
    ("", 0),
    ("", 1),
    (" ", 0),
    ("     ", 5),
    ("AEIOU", 0),
    ("aeiou", 0),
    ("b", 0),
    ("b", 1),
    ("b", 2),
    ("bcdf", 3),
    ("bcdf", 4),
    ("bcdf", 5),
    ("a b  c   de", 0),
    ("a b  c   de", 1),
    ("a b  c   de", 2),
    ("UPPER lower MiXeD", 3),
    ("UPPER lower MiXeD", 4),
    ("vowels consonants", 20),
]

cases: list[tuple[str, int, list[str] | None, str]] = []
for s, n, expected in documented:
    cases.append((s, n, expected, "documented"))
for s, n in boundaries:
    cases.append((s, n, None, "boundary"))

alphabet = "aEbZ "
for length in range(7):
    for chars in itertools.product(alphabet, repeat=length):
        s = "".join(chars)
        for n in range(8):
            cases.append((s, n, None, "exhaustive"))

rng = random.Random(117_20260726)
random_alphabet = string.ascii_letters + " "
for _ in range(10_000):
    length = rng.randrange(0, 81)
    s = "".join(rng.choice(random_alphabet) for _ in range(length))
    n = rng.randrange(0, length + 4)
    cases.append((s, n, None, "generated"))

digest = hashlib.sha256()
kind_counts: dict[str, int] = {}
mismatches: list[dict[str, object]] = []
for s, n, expected, kind in cases:
    kind_counts[kind] = kind_counts.get(kind, 0) + 1
    digest.update(
        json.dumps([s, n, expected, kind], ensure_ascii=True).encode("utf-8")
        + b"\n"
    )
    trusted_result = canonical(s, n)
    generated_result = generated(s, n)
    if expected is not None and trusted_result != expected:
        mismatches.append(
            {
                "kind": kind,
                "s": s,
                "n": n,
                "oracle": trusted_result,
                "expected": expected,
                "issue": "trusted canonical disagrees with documented result",
            }
        )
    if generated_result != trusted_result:
        mismatches.append(
            {
                "kind": kind,
                "s": s,
                "n": n,
                "oracle": trusted_result,
                "generated": generated_result,
                "issue": "implementation divergence",
            }
        )
    if len(mismatches) >= 20:
        break

print(f"case_counts={json.dumps(kind_counts, sort_keys=True)}")
print(f"case_manifest_sha256={digest.hexdigest()}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(json.dumps(mismatch, sort_keys=True))

if mismatches:
    sys.exit(1)
print("STAGE2_DIFFERENTIAL_OK")
