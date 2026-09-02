#!/usr/bin/env python3
"""Ground witnesses for the two reviewer-authored false claims."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_positive


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
candidate = load(
    Path("/tmp/audit-work/30-get-positive/solution.py"), "candidate_witness"
)

empty_actual = candidate([])
print(
    "FALSE_POST_WITNESS input=[] precondition=PyList "
    f"canonical={canonical([])!r} candidate={empty_actual!r} "
    "mutated_expected=[1] false="
    f"{empty_actual != [1]}"
)

body_input = [1]
changed_body_result = [x for x in body_input if x > 1]
original_summary = [x for x in body_input if x > 0]
print(
    f"BODY_SENSITIVITY_WITNESS input={body_input!r} precondition=PyList "
    f"changed_threshold_result={changed_body_result!r} "
    f"original_summary={original_summary!r} false="
    f"{changed_body_result != original_summary}"
)
