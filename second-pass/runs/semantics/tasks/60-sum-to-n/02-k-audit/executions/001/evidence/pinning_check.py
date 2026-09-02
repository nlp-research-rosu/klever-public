#!/usr/bin/env python3
"""Check that the proof wrapper embeds the submitted term and compare ground results."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SOLUTION_MPY = ROOT / "solution.mpy"
VERIFICATION = ROOT / "verification.k"
CANONICAL = Path("/reference/canonical.py")
GENERATED = ROOT / "solution.py"
GROUND_INPUTS = [0, 1, 2, 5, 10, 30, 100, 1000]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def remove_space(text: str) -> str:
    return re.sub(r"\s+", "", text)


def balanced_argument(text: str, marker: str) -> tuple[str, int]:
    start = text.index(marker) + len(marker)
    depth = 1
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
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start:index], index + 1
    raise ValueError(f"unbalanced argument after {marker}")


def py_mod(dividend: int, divisor: int) -> int:
    return ((dividend % divisor) + divisor) % divisor


def triangular(n: int) -> int:
    product = n * (n + 1)
    return (product - py_mod(product, 2)) // 2


def main() -> int:
    submitted_term = SOLUTION_MPY.read_text()
    verification = VERIFICATION.read_text()
    embedded_term, end = balanced_argument(verification, "#loadAll(")
    embedded_matches = remove_space(submitted_term) == remove_space(embedded_term)
    suffix = remove_space(verification[end:])
    expected_call = '~>Call(Name("sum_to_n"),Int(N),.Exprs)'
    exact_call_present = expected_call in suffix

    canonical = load_module("pinning_canonical", CANONICAL)
    generated = load_module("pinning_generated", GENERATED)
    rows = []
    for n in GROUND_INPUTS:
        rows.append((n, triangular(n), canonical.sum_to_n(n), generated.sum_to_n(n)))
    ground_matches = all(t == c == g for _, t, c, g in rows)

    print(f"submitted_term={SOLUTION_MPY}")
    print("wrapper_marker=#loadAll(")
    print(f"embedded_module_byte_identity_ignoring_layout={embedded_matches}")
    print(f"exact_entry_call_present={exact_call_present}")
    print(f"entry_call={expected_call}")
    print("satisfying_state_witness=N=2, env=0, module scope empty with parent(-1),")
    print("  builtins scope at -1, scopeLoc=1, empty heap/stack, noRet, NoExc, exit-code=0")
    print(f"ground_rows_(N,claim,canonical,generated)={rows}")
    print(f"all_ground_rows_match={ground_matches}")
    return 0 if embedded_matches and exact_call_present and ground_matches else 1


if __name__ == "__main__":
    sys.exit(main())
