#!/usr/bin/env python3
"""Independent differential test for HumanEval/28 concatenate.

Oracle: the trusted /reference/canonical.py entry point.
Subject: the scratch copy of the candidate's /candidate/solution.py.
The deterministic generator spans both loop branch boundaries (zero versus
one-or-more iterations), varying list lengths, empty elements, Unicode,
embedded NUL/newline characters, and longer strings.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/28-concatenate-audit")
SEED = 280028
RANDOM_CASES = 5000


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.concatenate


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_function(SCRATCH / "solution.py", "candidate_solution")

fixed_cases: list[list[str]] = [
    [],                                    # documented empty example / zero iterations
    ["a", "b", "c"],                       # documented non-empty example
    [""],                                  # one iteration, empty element
    ["a"],                                 # one iteration, non-empty element
    ["", ""],                              # two iterations, empty identity
    ["hello", "", " world"],               # empty internal element
    ["prefix", "suffix"],
    ["🙂", "λ", "漢字"],                    # non-ASCII code points
    ["a\n", "\tb", "\0", "c"],             # control and embedded NUL characters
    ["x" * 4096],
    ["a" * 1024, "", "b" * 2048, "c" * 4096],
    [""] * 128,
    [str(i) for i in range(256)],
]

alphabet = ["", "a", "b", "XYZ", " ", "\n", "\0", "🙂", "λ", "漢", "é"]
rng = random.Random(SEED)
generated_cases: list[list[str]] = []
length_choices = [0, 1, 2, 3, 4, 7, 16, 31, 64]
for _ in range(RANDOM_CASES):
    length = rng.choice(length_choices)
    case: list[str] = []
    for _ in range(length):
        if rng.randrange(5) == 0:
            width = rng.randrange(0, 65)
            case.append("".join(rng.choice(alphabet) for _ in range(width)))
        else:
            case.append(rng.choice(alphabet))
    generated_cases.append(case)

all_cases = fixed_cases + generated_cases
case_encoding = json.dumps(all_cases, ensure_ascii=False, separators=(",", ":")).encode()
case_digest = hashlib.sha256(case_encoding).hexdigest()

mismatches = []
for index, strings in enumerate(all_cases):
    expected = canonical(strings)
    actual = candidate(strings)
    if type(actual) is not str or actual != expected:
        mismatches.append(
            {
                "index": index,
                "input": strings,
                "expected": expected,
                "actual": actual,
                "actual_type": type(actual).__name__,
            }
        )
        if len(mismatches) >= 20:
            break

print(f"oracle=/reference/canonical.py:concatenate")
print(f"subject={SCRATCH / 'solution.py'}:concatenate")
print(f"seed={SEED}")
print(f"fixed_cases={len(fixed_cases)}")
print(f"generated_cases={len(generated_cases)}")
print(f"total_cases={len(all_cases)}")
print(f"case_set_sha256={case_digest}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches, ensure_ascii=False, indent=2))
    raise SystemExit(1)
print("DIFFERENTIAL_PASS")
