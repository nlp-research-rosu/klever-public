#!/usr/bin/env python3
"""Mechanical body comparison and satisfiable-claim witnesses."""

from __future__ import annotations

import hashlib
import importlib.util
import re
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/122-add-elements-audit")


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add_elements


def extract_constructor(text: str, constructor: str, occurrence: int = 1) -> str:
    matches = list(re.finditer(rf"\b{re.escape(constructor)}\s*\(", text))
    if len(matches) < occurrence:
        raise ValueError(f"{constructor} occurrence {occurrence} not found")
    start = matches[occurrence - 1].start()
    open_paren = text.find("(", matches[occurrence - 1].start())
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
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
                return text[start : index + 1]
    raise ValueError(f"unclosed constructor {constructor}")


def split_constructor_args(call: str) -> list[str]:
    open_paren = call.find("(")
    body = call[open_paren + 1 : -1]
    args = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(body):
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
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(body[start:index].strip())
            start = index + 1
    args.append(body[start:].strip())
    return args


def normalized_constructor_sequence(text: str) -> str:
    text = re.sub(r"//[^\n]*", "", text)
    text = text.replace(".Stmts", "")
    return re.sub(r"\s+", "", text)


def formal_summary(arr: list[int], k: int) -> int:
    return sum(value for value in arr[:k] if abs(value) < 100)


def main() -> int:
    failures = []
    solution_text = (WORK / "solution.mpy").read_text(encoding="utf-8")
    spec_text = (WORK / "spec.k").read_text(encoding="utf-8")

    func_def = extract_constructor(solution_text, "FuncDef")
    closure = extract_constructor(spec_text, "closureVal")
    func_args = split_constructor_args(func_def)
    closure_args = split_constructor_args(closure)

    solution_name = func_args[0].strip()
    solution_params = re.findall(r'"([^"]*)"', func_args[1])
    spec_params = re.findall(r'"([^"]*)"', closure_args[0])
    solution_body = normalized_constructor_sequence(func_args[2])
    spec_body = normalized_constructor_sequence(closure_args[1])
    closure_parent = closure_args[2].strip()

    print(f"solution_function_name={solution_name}")
    print(f"solution_params={solution_params}")
    print(f"spec_closure_params={spec_params}")
    print(f"spec_closure_parent={closure_parent}")
    print(
        "solution_body_normalized_sha256="
        f"{hashlib.sha256(solution_body.encode()).hexdigest()}"
    )
    print(
        "spec_body_normalized_sha256="
        f"{hashlib.sha256(spec_body.encode()).hexdigest()}"
    )
    print(f"constructor_body_equal={solution_body == spec_body}")
    print(f"params_equal={solution_params == spec_params}")

    if solution_name != '"add_elements"':
        failures.append("wrong generated function name")
    if solution_params != ["arr", "k"] or spec_params != solution_params:
        failures.append("parameter constructor mismatch")
    if solution_body != spec_body:
        failures.append("entry claim closure body differs from solution.mpy")
    if closure_parent != "0":
        failures.append("entry claim closure parent is not module scope 0")

    canonical = load_entry("trusted_canonical_stage4", WORK / "canonical.py")
    candidate = load_entry("candidate_stage4", WORK / "solution.py")
    witness_cases = [
        {
            "label": "documented-positive-witness",
            "prefix": [111, 21, 3],
            "suffix": [4000, 5],
        },
        {
            "label": "negative-domain-disagreement-witness",
            "prefix": [-99],
            "suffix": [],
        },
    ]
    for case in witness_cases:
        prefix = case["prefix"]
        suffix = case["suffix"]
        arr = prefix + suffix
        k = len(prefix)
        preconditions = {
            "prefix_nonempty": bool(prefix),
            "all_prefix_ints": all(type(value) is int for value in prefix),
            "all_suffix_ints": all(type(value) is int for value in suffix),
            "total_length_at_most_100": len(arr) <= 100,
            "k_valid": 1 <= k <= len(arr),
        }
        formal = formal_summary(arr, k)
        canonical_result = canonical(arr, k)
        candidate_result = candidate(arr, k)
        print(
            f"WITNESS label={case['label']} arr={arr} k={k} "
            f"preconditions={preconditions} formal={formal} "
            f"candidate={candidate_result} canonical={canonical_result}"
        )
        if not all(preconditions.values()):
            failures.append(f"unsatisfied entry precondition: {case['label']}")
        if formal != candidate_result:
            failures.append(f"formal summary differs from candidate: {case['label']}")

    loop_state = {
        "globals": {},
        "arr": [21, 3, 4000],
        "k": 3,
        "acc": 5,
        "old_element": 111,
        "v": 21,
        "vs": [3, 4000],
    }
    loop_preconditions = {
        "abs_not_shadowed": "abs" not in loop_state["globals"],
        "v_is_int": type(loop_state["v"]) is int,
        "vs_all_ints": all(type(value) is int for value in loop_state["vs"]),
    }
    loop_result = loop_state["acc"] + formal_summary(
        [loop_state["v"]] + loop_state["vs"], 1 + len(loop_state["vs"])
    )
    print(
        f"LOOP_WITNESS state={loop_state} preconditions={loop_preconditions} "
        f"claimed_final_total={loop_result}"
    )
    if not all(loop_preconditions.values()):
        failures.append("loop witness does not satisfy precondition")

    print(f"failure_count={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
