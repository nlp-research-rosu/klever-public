#!/usr/bin/env python3
"""Print independent Python results for the exact concrete K test inputs."""

from __future__ import annotations

import importlib.util
import pathlib
import sys


def load(path: pathlib.Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.all_prefixes


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} CANONICAL.py SOLUTION.py", file=sys.stderr)
        return 64
    canonical = load(pathlib.Path(sys.argv[1]), "trusted_concrete_canonical")
    solution = load(pathlib.Path(sys.argv[2]), "submitted_concrete_solution")
    for value in ["", "a", "abc", "abcdef", "🙂x"]:
        expected = canonical(value)
        actual = solution(value)
        print(
            f"INPUT={value!r} PYTHON_LEN={len(value)} "
            f"CANONICAL={expected!r} SUBMITTED={actual!r} "
            f"MATCH={expected == actual}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
