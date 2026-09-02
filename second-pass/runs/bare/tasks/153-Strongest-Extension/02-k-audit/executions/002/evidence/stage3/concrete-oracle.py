#!/usr/bin/env python3
"""Print trusted and submitted Python outcomes for the K concrete cases."""

from __future__ import annotations

import importlib.util
import sys


CASES = [
    ("prompt-worked", "Slices", ["SErviNGSliCes", "Cheese", "StuFfed"]),
    ("singleton", "C", ["Zz"]),
    ("empty-name", "C", [""]),
    ("greater", "C", ["abc", "AB", "A-b"]),
    ("equal", "C", ["AA", "BB"]),
    ("unicode-letter", "C", ["A", "ÉÉ"]),
    ("unicode-cased-nonletter", "C", ["A", "ⅣⅣ"]),
    ("empty-list", "C", []),
]


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


def result(function, class_name, extensions):
    try:
        return ("return", function(class_name, extensions))
    except Exception as error:
        return ("raise", type(error).__name__, str(error))


if len(sys.argv) != 3:
    raise SystemExit("usage: concrete-oracle.py CANONICAL SOLUTION")

canonical = load("canonical_concrete", sys.argv[1])
submitted = load("solution_concrete", sys.argv[2])
for label, class_name, extensions in CASES:
    print(
        f"{label}: canonical={result(canonical, class_name, extensions)!r} "
        f"submitted={result(submitted, class_name, extensions)!r}"
    )
