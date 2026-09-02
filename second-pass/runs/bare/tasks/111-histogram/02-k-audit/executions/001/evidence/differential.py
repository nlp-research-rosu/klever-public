#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 111."""

from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path
from typing import Callable


def load_histogram(path: Path, module_name: str) -> Callable[[str], dict]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


canonical = load_histogram(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_histogram(
    Path("/tmp/audit-work/111-histogram/solution.py"), "audited_generated"
)

documented_and_boundaries = [
    "",
    "a",
    "a b c",
    "a b b a",
    "a b c a b",
    "b b b b a",
    "a a",
    "a b",
    "a a b",
    "a a b b",
    "a a a b b c c",
    "c a c b a b",
]

# The natural-language domain is a sequence of lowercase letters separated by
# one ASCII space. Exhaust all a/b/c token lists through length eight.
generated_valid = [
    " ".join(tokens)
    for length in range(0, 9)
    for tokens in itertools.product(("a", "b", "c"), repeat=length)
]

# Record ambiguous separator cases separately. These are useful for auditing
# the bridge to canonical.py, but are not silently folded into the strict
# single-space domain above.
separator_edge_cases = [
    " ",
    "  ",
    " a",
    "a ",
    "a  b",
    "a   a",
    " a b ",
    "a\tb",
    "a\nb",
]


def compare(cases: list[str]) -> list[dict]:
    mismatches: list[dict] = []
    for text in cases:
        expected = canonical(text)
        actual = generated(text)
        if expected != actual:
            mismatches.append(
                {"input": text, "canonical": expected, "generated": actual}
            )
    return mismatches


valid_cases = list(dict.fromkeys(documented_and_boundaries + generated_valid))
valid_mismatches = compare(valid_cases)
edge_mismatches = compare(separator_edge_cases)

report = {
    "oracle": "/reference/canonical.py:histogram",
    "generated": "/tmp/audit-work/111-histogram/solution.py:histogram",
    "valid_domain": "lowercase a/b/c token lists joined by one ASCII space",
    "documented_and_boundary_inputs": documented_and_boundaries,
    "generated_valid_case_count": len(generated_valid),
    "unique_valid_case_count": len(valid_cases),
    "valid_mismatch_count": len(valid_mismatches),
    "valid_mismatches": valid_mismatches,
    "separator_edge_inputs": separator_edge_cases,
    "separator_edge_mismatch_count": len(edge_mismatches),
    "separator_edge_mismatches": edge_mismatches,
}
print(json.dumps(report, indent=2, sort_keys=True))

if valid_mismatches:
    raise SystemExit(1)
