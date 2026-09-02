#!/usr/bin/env python3
"""Mechanical constructor and concrete-witness checks for the entry claim."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def balanced_call(text: str, marker: str) -> str:
    start = text.index(marker)
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
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    raise ValueError(f"unbalanced term after {marker!r}")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_multiply_prime


def main() -> int:
    if len(sys.argv) != 5:
        raise SystemExit(
            "usage: claim_pinning_check.py SOLUTION_MPY SPEC_K CANONICAL_PY SOLUTION_PY"
        )
    solution_mpy = Path(sys.argv[1]).read_text()
    spec_k = Path(sys.argv[2]).read_text()

    submitted_module = balanced_call(solution_mpy, "Module(")
    claimed_module = balanced_call(spec_k, "Module(")
    constructor_equal = compact(submitted_module) == compact(claimed_module)

    k_cell = spec_k.split("<k>", 1)[1].split("</k>", 1)[0]
    result_text = k_cell.split("=>", 1)[1]
    post_values = [int(x) for x in re.findall(r"A\s*==Int\s*(-?\d+)", result_text)]
    precondition_is_full_bound = bool(re.search(r"requires\s+A\s*<Int\s*100\b", spec_k))

    canonical = load_function("trusted_canonical", Path(sys.argv[3]))
    generated = load_function("candidate_solution", Path(sys.argv[4]))
    witnesses = []
    for value in (30, 16, 99, -1, -(10**30)):
        formal = value in post_values
        expected = canonical(value)
        actual = generated(value)
        witnesses.append({
            "input": value,
            "precondition_holds": value < 100,
            "formal_postcondition": formal,
            "canonical": expected,
            "generated": actual,
            "all_equal": formal is expected is actual,
        })

    result = {
        "constructor_terms_equal_ignoring_whitespace": constructor_equal,
        "submitted_constructor": compact(submitted_module),
        "claimed_constructor": compact(claimed_module),
        "call_is_named_entry": 'Call(Name("is_multiply_prime"),(A:Int,.Exprs))'
        in compact(k_cell),
        "precondition_is_A_lt_100": precondition_is_full_bound,
        "postcondition_values": post_values,
        "postcondition_value_count": len(post_values),
        "witnesses": witnesses,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    ok = (
        constructor_equal
        and result["call_is_named_entry"]
        and precondition_is_full_bound
        and len(post_values) == 22
        and all(w["precondition_holds"] and w["all_equal"] for w in witnesses)
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
