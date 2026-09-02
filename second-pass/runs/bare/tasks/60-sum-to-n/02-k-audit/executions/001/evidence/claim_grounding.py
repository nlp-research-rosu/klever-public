#!/usr/bin/env python3
"""Check literal program pinning and ground witnesses for the entry claim."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def balanced_term(text: str, constructor: str) -> str:
    start = text.index(f"{constructor}(")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced {constructor} term")


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) != 5:
        print(
            f"usage: {sys.argv[0]} SPEC.k SOLUTION.mpy SOLUTION.py CANONICAL.py",
            file=sys.stderr,
        )
        return 64

    spec_path, mpy_path, solution_path, canonical_path = map(
        lambda arg: Path(arg).resolve(), sys.argv[1:]
    )
    spec_text = spec_path.read_text(encoding="utf-8")
    mpy_text = mpy_path.read_text(encoding="utf-8")
    claimed_program = balanced_term(spec_text, "Module")
    claimed_normalized = normalized(claimed_program)
    mpy_normalized = normalized(mpy_text)
    pinning_equal = claimed_normalized == mpy_normalized

    print(f"SPEC={spec_path}")
    print(f"SUBMITTED_MPY={mpy_path}")
    print(f"CLAIMED_PROGRAM_NORMALIZED_SHA256={digest(claimed_normalized)}")
    print(f"SUBMITTED_MPY_NORMALIZED_SHA256={digest(mpy_normalized)}")
    print(f"PROGRAM_TERM_BYTE_EQUAL_AFTER_WHITESPACE_NORMALIZATION={pinning_equal}")
    print('CLAIMED_INVOKE=invoke("sum_to_n", N)')
    print("PRECONDITION=N >=Int 0")
    print("POSTCONDITION=result == sumSpec(N)")
    print("SUMSPEC_EQUATION=sumSpec(N) == (N *Int (N +Int 1)) /Int 2")

    candidate = load_module("candidate_solution_grounding", solution_path)
    canonical = load_module("trusted_canonical_grounding", canonical_path)
    failures = 0 if pinning_equal else 1
    for n in [0, 1, 2, 30, 100]:
        precondition = n >= 0
        claimed_result = n * (n + 1) // 2
        candidate_result = candidate.sum_to_n(n)
        canonical_result = canonical.sum_to_n(n)
        all_equal = claimed_result == candidate_result == canonical_result
        print(
            f"WITNESS n={n} precondition={precondition} "
            f"claimed={claimed_result} candidate={candidate_result} "
            f"canonical={canonical_result} all_equal={all_equal}"
        )
        if not precondition or not all_equal:
            failures += 1

    print(f"FAILURES={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
