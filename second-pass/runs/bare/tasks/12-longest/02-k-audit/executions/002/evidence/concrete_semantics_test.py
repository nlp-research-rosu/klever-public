#!/usr/bin/env python3
"""Concrete generated-semantics checks against both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import shlex
import subprocess
import sys
from typing import Callable, Optional


def load_longest(path: pathlib.Path, module_name: str) -> Callable[[list[str]], Optional[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.longest


def main() -> int:
    if len(sys.argv) != 5:
        print(
            f"usage: {sys.argv[0]} SOLUTION.mpy DEFINITION CANONICAL.py SOLUTION.py",
            file=sys.stderr,
        )
        return 64

    program = pathlib.Path(sys.argv[1]).resolve()
    definition = pathlib.Path(sys.argv[2]).resolve()
    canonical = load_longest(pathlib.Path(sys.argv[3]), "trusted_canonical_concrete")
    candidate = load_longest(pathlib.Path(sys.argv[4]), "candidate_concrete")
    cases = [
        ("empty-loop-zero", [], "listVal()", "noneVal"),
        ("single-empty-string", [""], 'listVal(strVal(""))', 'strVal("")'),
        (
            "strict-growth",
            ["a", "bb", "ccc"],
            'listVal(strVal("a"),strVal("bb"),strVal("ccc"))',
            'strVal("ccc")',
        ),
        (
            "strict-no-growth-shorter",
            ["aa", "b"],
            'listVal(strVal("aa"),strVal("b"))',
            'strVal("aa")',
        ),
        (
            "strict-no-growth-tie",
            ["aa", "b", "cc"],
            'listVal(strVal("aa"),strVal("b"),strVal("cc"))',
            'strVal("aa")',
        ),
    ]

    failures = 0
    for name, python_input, k_args, expected_k in cases:
        expected_python = canonical(python_input)
        actual_python = candidate(python_input)
        command = [
            "krun",
            str(program),
            "--definition",
            str(definition),
            f"-cARGS={k_args}",
            "--pattern",
            f"<out> {expected_k} </out>",
            "--output",
            "pretty",
        ]
        result = subprocess.run(command, text=True, capture_output=True)
        print(f"CASE {name}")
        print("INPUT " + json.dumps(python_input, ensure_ascii=True))
        print(
            "PYTHON "
            + json.dumps(
                {"canonical": expected_python, "candidate": actual_python},
                ensure_ascii=True,
                sort_keys=True,
            )
        )
        print("COMMAND " + shlex.join(command))
        print(f"EXIT_STATUS {result.returncode}")
        print("STDOUT " + result.stdout.rstrip())
        if result.stderr:
            print("STDERR " + result.stderr.rstrip())
        if (
            result.returncode != 0
            or result.stdout.strip() != "#Top"
            or actual_python != expected_python
        ):
            failures += 1
    print(f"cases={len(cases)}")
    print(f"failures={failures}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
