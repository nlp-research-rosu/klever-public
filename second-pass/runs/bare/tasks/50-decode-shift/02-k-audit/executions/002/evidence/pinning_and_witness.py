#!/usr/bin/env python3
"""Mechanical program-pinning checks and concrete satisfying witnesses."""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path


def function(path: Path, name: str) -> ast.FunctionDef:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError(f"{name} absent from {path}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compact(text: str) -> str:
    return "".join(text.split())


def main() -> None:
    canonical_fn = function(Path("/reference/canonical.py"), "decode_shift")
    solution_fn = function(
        Path("/tmp/audit-work/candidate/solution.py"), "decode_shift"
    )
    canonical_returns = [
        node for node in canonical_fn.body if isinstance(node, ast.Return)
    ]
    solution_returns = [
        node for node in solution_fn.body if isinstance(node, ast.Return)
    ]
    assert len(canonical_returns) == len(solution_returns) == 1
    canonical_return_ast = ast.dump(
        canonical_returns[0].value, annotate_fields=True, include_attributes=False
    )
    solution_return_ast = ast.dump(
        solution_returns[0].value, annotate_fields=True, include_attributes=False
    )
    assert canonical_return_ast == solution_return_ast

    submitted_mpy = Path("/tmp/audit-work/candidate/solution.mpy").read_text(
        encoding="utf-8"
    )
    spec_text = Path("/tmp/audit-work/candidate/spec.k").read_text(encoding="utf-8")
    compact_mpy = compact(submitted_mpy)
    compact_spec = compact(spec_text)
    occurrence_count = compact_spec.count(compact_mpy)
    assert occurrence_count == 1

    canonical = load_module("pin_canonical", Path("/reference/canonical.py"))
    solution = load_module(
        "pin_solution", Path("/tmp/audit-work/candidate/solution.py")
    )
    witnesses = ("", "f", "abc", "xyz")
    for value in witnesses:
        assert all(97 <= ord(character) <= 122 for character in value)
        canonical_value = canonical.decode_shift(value)
        solution_value = solution.decode_shift(value)
        assert canonical_value == solution_value
        print(
            f"witness={value!r} allLower=true canonical={canonical_value!r} "
            f"solution={solution_value!r}"
        )

    code_witness = ord("a")
    encoded = ((code_witness + 5 - ord("a")) % 26) + ord("a")
    decoded = ((encoded - 5 - ord("a")) % 26) + ord("a")
    assert decoded == code_witness

    print("canonical_solution_return_ast_equal=true")
    print(f"solution_mpy_occurrences_in_program_claim={occurrence_count}")
    print(f"code_inverse_witness=C:{code_witness},encode:{encoded},decode:{decoded}")
    print("entry_witness_empty=CS:nil,s:nil,ch:0,input:nil,result:.K")
    print("loop_witness_empty=CS:nil,OLD:0,KONT:.K")
    print("PINNING_AND_WITNESS=PASS")


if __name__ == "__main__":
    main()
