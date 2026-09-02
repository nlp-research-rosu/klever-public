#!/usr/bin/env python3
"""Concrete satisfying source-domain witnesses for the entry claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("canonical_witness", Path("/reference/canonical.py"))
candidate = load_module("candidate_witness", Path("/candidate/solution.py"))

for label, value, codes, formal_model_result in [
    ("empty", "", [], 0),
    ("documented", "xyzXYZ", [120, 121, 122, 88, 89, 90], 3),
    ("unicode_accent", "éÉ", [233, 201], 2),
    ("unicode_dotted_i", "İ", [304], 1),
]:
    print(
        json.dumps(
            {
                "label": label,
                "input": value,
                "code_points": codes,
                "canonical_python": canonical.count_distinct_characters(value),
                "candidate_python": candidate.count_distinct_characters(value),
                "formal_ascii_lower_model": formal_model_result,
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )
