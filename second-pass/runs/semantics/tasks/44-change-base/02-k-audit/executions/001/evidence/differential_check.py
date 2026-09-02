#!/usr/bin/env python3
"""Compare the trusted canonical and submitted generated Python entry points."""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[int, int], str]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


def outcome(function: Callable[[int, int], str], x: int, base: int) -> dict[str, Any]:
    try:
        value = function(x, base)
        return {
            "kind": "return",
            "type": type(value).__name__,
            "value": value,
        }
    except BaseException as error:  # compare observable failures as well as returns
        return {
            "kind": "raise",
            "type": type(error).__name__,
            "message": str(error),
        }


def compact(result: dict[str, Any]) -> dict[str, Any]:
    result = dict(result)
    value = result.get("value")
    if isinstance(value, str) and len(value) > 80:
        result["value"] = f"{value[:32]}...{value[-32:]}"
        result["value_length"] = len(value)
    return result


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/reconstruction/solution.py"), "generated_solution"
    )

    named: list[tuple[str, int, int]] = [
        ("documented-8-base-3", 8, 3),
        ("documented-8-base-2", 8, 2),
        ("documented-7-base-2", 7, 2),
        ("empty-result-x-zero", 0, 2),
    ]
    for base in range(2, 10):
        named.extend(
            [
                (f"base-{base}-x-one", 1, base),
                (f"base-{base}-one-digit-max", base - 1, base),
                (f"base-{base}-first-two-digit", base, base),
                (f"base-{base}-after-boundary", base + 1, base),
                (f"base-{base}-two-digit-max", base * base - 1, base),
                (f"base-{base}-first-three-digit", base * base, base),
            ]
        )

    exhaustive = [
        ("small-exhaustive", x, base)
        for base in range(2, 10)
        for x in range(0, 513)
    ]

    rng = random.Random(440044)
    generated_cases = []
    for index in range(256):
        bits = rng.randint(0, 512)
        x = rng.getrandbits(bits)
        base = rng.randint(2, 9)
        generated_cases.append((f"generated-{index}", x, base))

    stress = [
        ("recursion-boundary-base-2", 1 << (sys.getrecursionlimit() + 50), 2),
        ("large-base-9", 1 << (sys.getrecursionlimit() + 50), 9),
    ]

    ambiguous_contract = [
        ("prompt-does-not-exclude-negative-x-minus-1-base-2", -1, 2),
        ("prompt-does-not-exclude-negative-x-minus-2-base-3", -2, 3),
        ("prompt-does-not-exclude-negative-x-minus-7-base-9", -7, 9),
    ]

    cases = named + exhaustive + generated_cases + stress + ambiguous_contract
    mismatches: list[dict[str, Any]] = []
    for name, x, base in cases:
        expected = outcome(canonical, x, base)
        actual = outcome(generated, x, base)
        if expected != actual:
            mismatches.append(
                {
                    "name": name,
                    "x": str(x),
                    "base": base,
                    "canonical": compact(expected),
                    "generated": compact(actual),
                }
            )

    print("ORACLE=/reference/canonical.py:change_base")
    print("GENERATED=/tmp/audit-work/reconstruction/solution.py:change_base")
    print(f"PYTHON_RECURSION_LIMIT={sys.getrecursionlimit()}")
    print(
        "SCOPE="
        f"{len(named)} named/example/boundary; "
        f"{len(exhaustive)} exhaustive x=0..512/base=2..9; "
        f"{len(generated_cases)} deterministic generated up to 512 bits; "
        f"{len(stress)} recursion stress; "
        f"{len(ambiguous_contract)} literal-prompt domain probes outside the formal precondition"
    )
    print(f"TOTAL_CASES={len(cases)}")
    print(f"MISMATCHES={len(mismatches)}")
    for mismatch in mismatches:
        print("MISMATCH=" + json.dumps(mismatch, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
