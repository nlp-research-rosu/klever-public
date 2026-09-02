#!/usr/bin/env python3
"""Independent exhaustive comparison of trusted canonical and generated Python."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys


ROOT = pathlib.Path("/tmp/audit-work")
INPUT_DESCRIPTION = pathlib.Path("/audit-output/evidence/differential_inputs.json")


def load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    inputs = json.loads(INPUT_DESCRIPTION.read_text(encoding="utf-8"))
    canonical = load_module("trusted_canonical", pathlib.Path("/reference/canonical.py"))
    generated = load_module("scratch_generated", ROOT / "src" / "solution.py")

    examples = inputs["documented_examples"]
    boundaries = inputs["named_boundary_cases"]
    print(f"oracle=/reference/canonical.py:solve")
    print(f"generated={ROOT / 'src' / 'solution.py'}:solve")
    print(f"documented_examples={examples}")
    print(f"named_boundary_cases={boundaries}")
    print("exhaustive_inputs=range(0, 10001)")

    mismatches: list[tuple[int, object, object]] = []
    observed_outputs: set[str] = set()
    for n in range(0, 10001):
        expected = canonical.solve(n)
        actual = generated.solve(n)
        if not isinstance(actual, str):
            mismatches.append((n, expected, f"non-string {actual!r}"))
        elif actual != expected:
            mismatches.append((n, expected, actual))
        observed_outputs.add(actual)

    for n in examples + boundaries:
        print(
            f"case n={n}: canonical={canonical.solve(n)!r} "
            f"generated={generated.solve(n)!r}"
        )

    print(f"tested=10001")
    print(f"distinct_outputs={len(observed_outputs)}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(f"first_mismatches={mismatches[:20]}")
        return 1
    print("PASS: generated and canonical results are identical over 0..10000")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
