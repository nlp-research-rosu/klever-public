#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential for HumanEval/50."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import string
from pathlib import Path

EVIDENCE_DIR = Path("/audit-output/evidence")
TRUSTED_CANONICAL = Path(
    "/tmp/audit-work/50-decode-shift/trusted-src/canonical.py"
)
CANDIDATE_SOLUTION = Path(
    "/tmp/audit-work/50-decode-shift/candidate-src/solution.py"
)


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", TRUSTED_CANONICAL)
candidate = load_module("audited_candidate", CANDIDATE_SOLUTION)

# The documented contract restricts decode inputs to outputs of encode_shift.
# Character-wise Caesar encoding is onto [a-z], so the intended decode domain
# is exactly strings over the 26 lowercase ASCII letters, including empty.
documented_and_boundaries = [
    "",
    "a",
    "e",  # last encoded character whose decode wraps
    "f",  # first encoded character whose decode does not wrap
    "z",
    "c",
    "mjqqt",
    "fghijklmnopqrstuvwxyzabcde",
    string.ascii_lowercase,
    string.ascii_lowercase[::-1],
]

exhaustive_small = [
    "".join(chars)
    for length in range(4)
    for chars in itertools.product(string.ascii_lowercase, repeat=length)
]

rng = random.Random(50050)
generated = [
    "".join(rng.choice(string.ascii_lowercase) for _ in range(rng.randrange(0, 65)))
    for _ in range(2000)
]

cases = list(dict.fromkeys(documented_and_boundaries + exhaustive_small + generated))
(EVIDENCE_DIR / "differential_inputs.json").write_text(
    json.dumps(cases, indent=2) + "\n", encoding="utf-8"
)

mismatches = []
roundtrip_failures = []
for encoded in cases:
    expected = canonical.decode_shift(encoded)
    actual = candidate.decode_shift(encoded)
    if actual != expected:
        mismatches.append(
            {"input": encoded, "canonical": expected, "candidate": actual}
        )

    # This checks the natural-language inverse bridge separately. Each encoded
    # input has a canonical decoded preimage in the lowercase alphabet.
    decoded = expected
    encoded_again = canonical.encode_shift(decoded)
    if encoded_again != encoded or actual != decoded:
        roundtrip_failures.append(
            {
                "encoded": encoded,
                "decoded": decoded,
                "encoded_again": encoded_again,
                "candidate_decoded": actual,
            }
        )

summary = {
    "domain": "strings over lowercase ASCII [a-z], including empty",
    "documented_and_boundary_count_before_dedup": len(documented_and_boundaries),
    "exhaustive_scope": "all lowercase strings of lengths 0, 1, 2, and 3",
    "exhaustive_small_count": len(exhaustive_small),
    "generated_scope": (
        "2000 deterministic PRNG cases; seed 50050; lengths 0..64 inclusive"
    ),
    "generated_count_before_dedup": len(generated),
    "unique_case_count": len(cases),
    "mismatch_count": len(mismatches),
    "roundtrip_failure_count": len(roundtrip_failures),
    "boundary_results": {
        value: {
            "canonical": canonical.decode_shift(value),
            "candidate": candidate.decode_shift(value),
        }
        for value in documented_and_boundaries
    },
    "first_mismatches": mismatches[:20],
    "first_roundtrip_failures": roundtrip_failures[:20],
}
print(json.dumps(summary, indent=2, sort_keys=True))

if mismatches or roundtrip_failures:
    raise SystemExit(1)
