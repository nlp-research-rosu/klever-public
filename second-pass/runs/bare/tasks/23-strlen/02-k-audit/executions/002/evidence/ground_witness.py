#!/usr/bin/env python3
"""Concrete satisfying inputs for the entry claim and source contract."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load(name: str, path: Path):
    spec = spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strlen


def main() -> None:
    canonical = load("ground_canonical", Path("/reference/canonical.py"))
    solution = load(
        "ground_solution",
        Path("/tmp/audit-work/23-strlen.30KKVy/work/solution.py"),
    )
    for value in ("", "abc", "😀", "a😀é"):
        print(
            f"input={value!r} canonical={canonical(value)} "
            f"solution={solution(value)}"
        )
    print(
        'entry_precondition_witness=S="abc", functions=.Map, '
        "locals=.Map, result=noResult"
    )


if __name__ == "__main__":
    main()
