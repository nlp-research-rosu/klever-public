#!/usr/bin/env python3
"""Ground witness for the universal entry claim's sorted precondition."""

from __future__ import annotations

import importlib.util
import pathlib
import sys


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_threshold


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRUSTED_CANONICAL.py GENERATED.py", file=sys.stderr)
        return 64
    canonical = load(pathlib.Path(sys.argv[1]), "audit_witness_canonical")
    generated = load(pathlib.Path(sys.argv[2]), "audit_witness_generated")

    values = [5]
    threshold = 5
    formal_input = "cons(5, nil)"
    expected = all(value < threshold for value in values)
    canonical_result = canonical(list(values), threshold)
    generated_result = generated(list(values), threshold)

    print("Entry-precondition witness:")
    print("  <k> boot </k>")
    print("  <program> solutionProgram </program>")
    print(f"  <input> {formal_input} </input>")
    print(f"  <threshold> {threshold} </threshold>")
    print("  <l> unbound </l>")
    print("  <t> unbound </t>")
    print("  <x> unbound </x>")
    print("  <result> noResult </result>")
    print(f"Claimed allBelow({formal_input}, {threshold}) = {str(expected).lower()}")
    print(f"trusted canonical result = {canonical_result}")
    print(f"generated Python result = {generated_result}")
    good = type(canonical_result) is bool and type(generated_result) is bool
    good = good and canonical_result == generated_result == expected
    print(f"witness comparison ok = {good}")
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
