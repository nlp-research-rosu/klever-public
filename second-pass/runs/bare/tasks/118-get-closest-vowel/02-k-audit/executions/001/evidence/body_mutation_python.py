#!/usr/bin/env python3
"""Concrete witness for the operational body-sensitivity mutation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


def main() -> int:
    original = load_entry(
        "body_original", Path("/tmp/audit-work/candidate-src/solution.py")
    )
    mutated = load_entry(
        "body_mutated", Path("/tmp/audit-work/body-mutation/solution.py")
    )
    word = "bAb"
    print(f"input={word!r}")
    print(f"original_python={original(word)!r}")
    print(f"mutated_python={mutated(word)!r}")
    print("expected_mutated_result='' because membership in the empty string is false")
    return 0 if original(word) == "A" and mutated(word) == "" else 1


if __name__ == "__main__":
    raise SystemExit(main())
