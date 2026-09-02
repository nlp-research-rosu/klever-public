#!/usr/bin/env python3
"""False intended-behavior witnesses for the unguarded tokenText abstraction."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


canonical = load(Path("/reference/canonical.py"), "bridge_witness_canonical")
candidate = load(
    Path("/tmp/audit-work/111-histogram/solution.py"), "bridge_witness_candidate"
)

# The proof-local equation admits any ValSeq, including token values that no
# no-argument whitespace split can emit as one token.
witnesses = [
    (
        "empty-token",
        "",
        {"": 1},
        "TS = vCons(str(.IntSeq), .ValSeq)",
    ),
    (
        "embedded-space-token",
        "a b",
        {"a b": 1},
        "TS = vCons(str(codes('a b')), .ValSeq)",
    ),
]

for label, concrete_text, bridge_implied, formal_ts in witnesses:
    canonical_result = canonical(concrete_text)
    candidate_result = candidate(concrete_text)
    print(
        f"WITNESS={label} FORMAL_TS={formal_ts} CONCRETE_TEXT={concrete_text!r} "
        f"BRIDGE_IMPLIED={bridge_implied!r} CANONICAL={canonical_result!r} "
        f"CANDIDATE={candidate_result!r}"
    )
    assert canonical_result == candidate_result
    assert candidate_result != bridge_implied

print("These witnesses refute interpreting the unguarded fresh constructor as")
print("a universal bridge from every ValSeq to an actual whitespace-split string.")
