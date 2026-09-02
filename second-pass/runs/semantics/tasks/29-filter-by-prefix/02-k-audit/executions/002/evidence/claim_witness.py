#!/usr/bin/env python3
"""Concrete satisfying witnesses for the formal entry result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_by_prefix


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
candidate = load(Path("/candidate/solution.py"), "candidate_witness")

for strings, prefix in [
    (["a", "b"], "a"),
    (["", "a", "ba"], ""),
]:
    # This is the concrete interpretation of prefixFilter's three equations.
    claimed = [value for value in strings if value.startswith(prefix)]
    trusted = canonical(strings, prefix)
    generated = candidate(strings, prefix)
    print(
        f"strings={strings!r} prefix={prefix!r} "
        f"prefixFilter={claimed!r} canonical={trusted!r} candidate={generated!r}"
    )
    assert claimed == trusted == generated
