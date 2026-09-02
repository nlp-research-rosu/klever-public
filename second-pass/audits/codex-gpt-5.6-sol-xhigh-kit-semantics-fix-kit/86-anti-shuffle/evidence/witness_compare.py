#!/usr/bin/env python3
"""Compare concrete claim witnesses with trusted and submitted Python."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/86-anti-shuffle")


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    canonical = load("canonical_witness", "canonical.py")
    submitted = load("submitted_witness", "solution.py")
    cases = ["", "ba ab"]
    for value in cases:
        expected = canonical.anti_shuffle(value)
        actual = submitted.anti_shuffle(value)
        print(
            f"input={value!r} codes={list(map(ord, value))} "
            f"canonical={expected!r} submitted={actual!r} result_codes={list(map(ord, actual))}"
        )
        if expected != actual:
            return 1
    helper = submitted.insert_char("b", "a")
    print(f"insert_char('b','a')={helper!r} result_codes={list(map(ord, helper))}")
    return 0 if helper == "ab" else 1


if __name__ == "__main__":
    raise SystemExit(main())
