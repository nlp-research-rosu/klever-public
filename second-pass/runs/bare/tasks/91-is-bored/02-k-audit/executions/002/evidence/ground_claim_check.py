#!/usr/bin/env python3
"""Compare every submitted ground claim with both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


canonical = load_function(
    "trusted_canonical_claims", Path("/tmp/audit-work/trusted/canonical.py")
)
candidate = load_function(
    "submitted_solution_claims",
    Path("/tmp/audit-work/reconstruction/solution.py"),
)

claims = [
    ("Hello world", 0),
    ("The sky is blue. The sun is shining. I love this weather", 1),
    ("I am bored. I am still bored! Are you? I think so.", 3),
    (" I am here?You are there!  I agree", 2),
    ("It is cold. Island life! In time? I agree", 1),
    ("... ! ?  . I count!", 1),
    ("\tI tabbed.\nI newline?\rNot me!", 2),
    ("I first! No. I second?", 2),
]

canonical_mismatches = 0
candidate_mismatches = 0
for index, (text, claimed) in enumerate(claims, 1):
    trusted_value = canonical(text)
    submitted_value = candidate(text)
    canonical_ok = trusted_value == claimed
    candidate_ok = submitted_value == claimed
    canonical_mismatches += not canonical_ok
    candidate_mismatches += not candidate_ok
    print(
        f"claim={index} input={text!r} claimed={claimed} "
        f"canonical={trusted_value} canonical_matches={canonical_ok} "
        f"candidate={submitted_value} candidate_matches={candidate_ok}"
    )

print(f"canonical_mismatches={canonical_mismatches}")
print(f"candidate_mismatches={candidate_mismatches}")
raise SystemExit(1 if canonical_mismatches or candidate_mismatches else 0)
