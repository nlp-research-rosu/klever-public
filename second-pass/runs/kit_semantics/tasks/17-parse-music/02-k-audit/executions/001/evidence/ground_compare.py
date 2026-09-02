#!/usr/bin/env python3
"""Show concrete substitutions used in AUDIT-GROUND-SPEC in both Python bodies."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_music


canonical = load("ground_canonical", Path("/reference/canonical.py"))
generated = load(
    "ground_generated", Path("/tmp/audit-work/candidate-src/solution.py")
)

for text, expected in (("", []), ("o o| .|", [4, 2, 1])):
    canonical_result = canonical(text)
    generated_result = generated(text)
    assert canonical_result == generated_result == expected
    print(
        "input="
        + repr(text)
        + " codes="
        + repr([ord(character) for character in text])
        + " canonical="
        + repr(canonical_result)
        + " generated="
        + repr(generated_result)
    )
