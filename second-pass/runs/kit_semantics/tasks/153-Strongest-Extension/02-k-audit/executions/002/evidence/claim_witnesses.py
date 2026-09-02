#!/usr/bin/env python3
"""Concrete satisfying witnesses for the two entry-claim preconditions."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


def main() -> int:
    generated = load_entry(Path(sys.argv[1]), "witness_solution")
    canonical = load_entry(Path(sys.argv[2]), "witness_canonical")

    empty = ("", [])
    empty_generated = generated(*empty)
    try:
        empty_canonical = repr(canonical(*empty))
    except Exception as err:
        empty_canonical = f"{type(err).__name__}: {err}"
    print(
        "ENTRY_EMPTY_WITNESS",
        "CLASS=.IntSeq",
        "extensions=.ValSeq",
        "expected_fixed_model='.'",
        f"generated={empty_generated!r}",
        f"canonical={empty_canonical}",
    )
    assert empty_generated == "."

    nonempty = ("C", ["a", "B"])
    expected = "C.B"
    nonempty_generated = generated(*nonempty)
    nonempty_canonical = canonical(*nonempty)
    print(
        "ENTRY_NONEMPTY_WITNESS",
        "CLASS=[67]",
        "FIRST=[97]",
        "RESTEXTS=[str([66])]",
        "allStrings(RESTEXTS)=true",
        f"expected={expected!r}",
        f"generated={nonempty_generated!r}",
        f"canonical={nonempty_canonical!r}",
    )
    assert nonempty_generated == expected
    assert nonempty_canonical == expected
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
