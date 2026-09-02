#!/usr/bin/env python3
"""Concise witness for the real-Python/generated-semantics control mismatch."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime


def outcome(function, value):
    try:
        return {"kind": "return", "value": function(value)}
    except Exception as err:
        return {"kind": "exception", "type": type(err).__name__}


canonical = load_entry(
    "trusted_canonical_recursion", Path("/tmp/audit-work/trusted/canonical.py")
)
generated = load_entry(
    "submitted_generated_recursion",
    Path("/tmp/audit-work/candidate-src/solution.py"),
)

for n in (1_000_003, 1_022_117):
    print(
        json.dumps(
            {
                "input": n,
                "python_recursion_limit": sys.getrecursionlimit(),
                "canonical": outcome(canonical, n),
                "generated": outcome(generated, n),
            },
            sort_keys=True,
        )
    )
