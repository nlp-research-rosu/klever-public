#!/usr/bin/env python3
"""Focused normal-return/RecursionError boundary witness."""

import importlib.util
import sys
from pathlib import Path


def load_entry(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


def outcome(function, value):
    try:
        result = function(value)
        return f"value(length={len(result)})"
    except Exception as error:
        return f"exception({type(error).__name__}: {error})"


canonical = load_entry("canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "generated", Path("/tmp/audit-work/reconstruction/solution.py")
)

print(f"python={sys.version.split()[0]} recursionlimit={sys.getrecursionlimit()}")
for length in (995, 996):
    value = "a" * length
    print(
        f"length={length} canonical={outcome(canonical, value)} "
        f"generated={outcome(generated, value)}"
    )
