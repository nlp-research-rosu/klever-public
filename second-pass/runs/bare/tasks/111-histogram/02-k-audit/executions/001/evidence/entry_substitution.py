#!/usr/bin/env python3
"""Ground witnesses for the two universal entry-claim preconditions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


canonical = load("/reference/canonical.py", "entry_canonical")
generated = load(
    "/tmp/audit-work/111-histogram/solution.py", "entry_generated"
)

for text in ("", "a b b a", "b b b b a"):
    canonical_result = canonical(text)
    generated_result = generated(text)
    print(
        json.dumps(
            {
                "input": text,
                "satisfies_string_precondition": True,
                "token_list_witness": text.split(),
                "canonical": canonical_result,
                "generated": generated_result,
                "equal": canonical_result == generated_result,
            },
            sort_keys=True,
        )
    )
