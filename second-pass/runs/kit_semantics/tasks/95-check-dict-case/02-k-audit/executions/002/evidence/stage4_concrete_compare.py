#!/usr/bin/env python3
"""Concrete satisfying witnesses for the target precondition."""

from pathlib import Path
import importlib.util


def load_function(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_dict_case


candidate = load_function(
    "candidate_stage4",
    Path("/tmp/audit-work/case95/candidate-src/solution.py"),
)
canonical = load_function(
    "canonical_stage4",
    Path("/tmp/audit-work/case95/trusted/canonical.py"),
)

# These plain dictionaries correspond to non-reference ValSeq witnesses and
# to the five K summary claims in stage4_summary_spec.k.
cases = [
    ("empty", {}, False),
    ("lower", {"a": 0}, True),
    ("upper", {"A": 0}, True),
    ("mixed", {"a": 0, "B": 0}, False),
    ("non-string", {8: 0}, False),
]

for name, mapping, claimed in cases:
    candidate_result = candidate(mapping)
    canonical_result = canonical(mapping)
    print(
        f"{name}: input={mapping!r} claimed={claimed!r} "
        f"candidate={candidate_result!r} canonical={canonical_result!r}"
    )
    if candidate_result != claimed or canonical_result != claimed:
        raise SystemExit(1)
