#!/usr/bin/env python3
"""Independent Python differential test for HumanEval 79."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_function(path: Path, module_name: str) -> Callable[[Any], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.decimal_to_binary


def generated_inputs() -> list[int]:
    # Examples, numeric "empty" value, sign boundary, binary-recursion boundary,
    # a dense small range, powers-of-two neighborhoods, and seeded broad samples.
    values = [15, 32, -2, -1, 0, 1, 2, 3]
    values.extend(range(-128, 129))
    for exponent in range(0, 130):
        power = 1 << exponent
        values.extend((power - 1, power, power + 1))
        values.extend((-(power + 1), -power, -(power - 1)))
    rng = random.Random(790079)
    for _ in range(160):
        magnitude = rng.getrandbits(rng.randrange(0, 513))
        values.append(-magnitude if rng.randrange(2) else magnitude)
    # Preserve order while removing duplicates.
    return list(dict.fromkeys(values))


def normalized_function(path: Path) -> tuple[ast.arguments, list[ast.stmt]]:
    module = ast.parse(path.read_text(), filename=str(path))
    function = next(
        node for node in module.body
        if isinstance(node, ast.FunctionDef) and node.name == "decimal_to_binary"
    )
    body = list(function.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body.pop(0)
    return function.args, body


def outcome(function: Callable[[Any], Any], value: Any) -> tuple[str, str, str]:
    try:
        result = function(value)
        return ("return", type(result).__name__, repr(result))
    except Exception as error:  # Intentional parity check outside the integer domain.
        return ("raise", type(error).__name__, str(error))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--emit-inputs", action="store_true")
    parser.add_argument("--inputs", type=Path)
    args = parser.parse_args()

    if args.emit_inputs:
        print(json.dumps(generated_inputs(), separators=(",", ":")))
        return 0
    if args.inputs is None:
        parser.error("--inputs is required unless --emit-inputs is used")

    test_inputs = json.loads(args.inputs.read_text())
    canonical = load_function(args.canonical, "trusted_canonical_79")
    generated = load_function(args.generated, "generated_solution_79")

    canonical_ast = normalized_function(args.canonical)
    generated_ast = normalized_function(args.generated)
    ast_equal = ast.dump(canonical_ast[0], include_attributes=False) == ast.dump(
        generated_ast[0], include_attributes=False
    ) and ast.dump(ast.Module(body=canonical_ast[1], type_ignores=[]),
                   include_attributes=False) == ast.dump(
        ast.Module(body=generated_ast[1], type_ignores=[]),
        include_attributes=False,
    )
    print(f"AST_FUNCTION_EQUAL_AFTER_DOCSTRING_REMOVAL={ast_equal}")

    mismatches: list[tuple[int, tuple[str, str, str], tuple[str, str, str]]] = []
    for value in test_inputs:
        expected = outcome(canonical, value)
        actual = outcome(generated, value)
        if actual != expected:
            mismatches.append((value, expected, actual))

    raw_inputs = args.inputs.read_bytes()
    print(f"INTEGER_INPUT_COUNT={len(test_inputs)}")
    print(f"INTEGER_INPUTS_SHA256={hashlib.sha256(raw_inputs).hexdigest()}")
    print(f"DOCUMENTED_15={generated(15)!r}")
    print(f"DOCUMENTED_32={generated(32)!r}")
    for value in (-2, -1, 0, 1, 2, 3):
        print(f"BOUNDARY_{value}={generated(value)!r}")
    print(f"INTEGER_MISMATCH_COUNT={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH", mismatch)

    # Empty/non-integer inputs are outside the K theorem's Int domain. Check that
    # the exact Python rewrite nevertheless retains canonical exception behavior.
    out_of_domain = ["", None, 0.0, [], {}]
    parity = []
    for value in out_of_domain:
        expected = outcome(canonical, value)
        actual = outcome(generated, value)
        parity.append(actual == expected)
        print(f"OUT_OF_DOMAIN {value!r} canonical={expected!r} generated={actual!r}")

    passed = ast_equal and not mismatches and all(parity)
    print(f"PASS={passed}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
