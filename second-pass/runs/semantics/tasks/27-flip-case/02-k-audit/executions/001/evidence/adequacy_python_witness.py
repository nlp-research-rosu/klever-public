#!/usr/bin/env python3
"""Ground intent and K-code-sequence witness for the entry claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


canonical = load_function(
    "adequacy_canonical",
    Path("/tmp/audit-work/27-flip-case/trusted/canonical.py"),
)
submitted = load_function(
    "adequacy_submitted",
    Path("/tmp/audit-work/27-flip-case/candidate/solution.py"),
)

input_text = "Hello"
expected_text = "hELLO"
result = {
    "input": input_text,
    "input_code_sequence": [ord(char) for char in input_text],
    "claimed_result": expected_text,
    "claimed_result_code_sequence": [ord(char) for char in expected_text],
    "canonical_result": canonical(input_text),
    "submitted_result": submitted(input_text),
}
result["all_equal"] = (
    result["claimed_result"]
    == result["canonical_result"]
    == result["submitted_result"]
)
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["all_equal"] else 1)
