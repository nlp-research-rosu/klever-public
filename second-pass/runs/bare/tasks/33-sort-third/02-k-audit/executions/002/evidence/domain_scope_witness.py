#!/usr/bin/env python3
"""Witness source-contract inputs that the integer-only K claim cannot express."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    canonical = load_entry(args.canonical, "trusted_canonical_scope")
    candidate = load_entry(args.candidate, "candidate_solution_scope")

    cases = [
        ["z", "kept-1", "kept-2", "a"],
        [3.5, 20.25, 10.75, -1.5, 8.0, 9.0, 2.25],
    ]
    for values in cases:
        expected = canonical(values)
        actual = candidate(values)
        print(f"input={values!r}")
        print(f"canonical={expected!r}")
        print(f"candidate={actual!r}")
        assert actual == expected

    print("source_level_mismatches=0")
    print("formal_VList_Ints_representable=0")


if __name__ == "__main__":
    main()
