#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for flip_case."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


canonical = load_function(
    Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical"
)
candidate = load_function(
    Path("/tmp/audit-work/candidate/solution.py"), "candidate_solution"
)

# These cover the documented example, empty input, ASCII case-category
# boundaries, whitespace/control/escaping, each UTF-8 width, multi-code-point
# case expansions, combining text, titlecase, the maximum scalar, and lone
# surrogate code points permitted inside a CPython str.
fixed_cases = [
    "",
    "Hello",
    "a",
    "z",
    "A",
    "Z",
    "@[`{",
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789 !?_-",
    "aBc XYZ",
    "\x00\n\t\"\\",
    "\x7f\x80\xff",
    "Straße Δelta",
    "ß",
    "İ",
    "ǰ",
    "ﬃ",
    "µ",
    "ᾀ",
    "ǅǈǋǲ",
    "e\u0301 E\u0301",
    "\u07ff",
    "\u0800",
    "\uffff",
    "\U00010000",
    "\U00010400\U00010428",
    "\U0010ffff",
    "\ud800\udfff",
]

rng = random.Random(27027)
pools = {
    "ascii": list(range(0x80)),
    "two_byte": list(range(0x80, 0x800)),
    "three_byte": list(range(0x800, 0x10000)),
    "four_byte": list(range(0x10000, 0x110000)),
    "case_expansion": [
        codepoint
        for codepoint in range(0x110000)
        if len(chr(codepoint).swapcase()) != 1
    ],
}

generated_cases: list[str] = []
for pool_name, pool in pools.items():
    for length in (0, 1, 2, 3, 7, 16, 64):
        for _ in range(30):
            generated_cases.append(
                "".join(chr(rng.choice(pool)) for _ in range(length))
            )
for _ in range(500):
    length = rng.randrange(0, 81)
    generated_cases.append(
        "".join(chr(rng.randrange(0x110000)) for _ in range(length))
    )

all_cases = fixed_cases + generated_cases
input_digest = hashlib.sha256()
mismatches = []
for index, value in enumerate(all_cases):
    input_digest.update(
        json.dumps(value, ensure_ascii=True).encode("ascii") + b"\n"
    )
    expected = canonical(value)
    actual = candidate(value)
    if actual != expected:
        mismatches.append((index, value, expected, actual))

print("oracle=/tmp/audit-work/trusted/canonical.py:flip_case")
print("candidate=/tmp/audit-work/candidate/solution.py:flip_case")
print("python_fixed_cases")
for value in fixed_cases:
    print(
        json.dumps(value, ensure_ascii=True),
        "=>",
        json.dumps(candidate(value), ensure_ascii=True),
    )
print("generated_pool_sizes", {key: len(value) for key, value in pools.items()})
print("generated_case_count", len(generated_cases))
print("total_case_count", len(all_cases))
print("deterministic_input_sha256", input_digest.hexdigest())
print("mismatch_count", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH", repr(mismatch))
raise SystemExit(1 if mismatches else 0)
