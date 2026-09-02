#!/usr/bin/env python3
"""Independent structural pinning and satisfying-witness checks."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path("/tmp/audit-work/142-sum-squares")


def compact(text: str) -> str:
    return "".join(text.split())


def ast_surface_normalize(text: str) -> str:
    # The submitted translator omits explicit K list terminators where the K
    # parser inserts them. The spec spells those `.Stmts` units out. They are
    # the same parsed Stmts term, so normalize only this surface-syntax unit.
    return compact(text).replace(".Stmts", "")


def balanced_term(text: str, marker: str, start: int = 0) -> str:
    begin = text.index(marker, start)
    open_paren = begin + len(marker) - 1
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
                return text[begin : index + 1]
    raise ValueError(f"unbalanced term for {marker}")


def split_arguments(term: str) -> list[str]:
    inner = term[term.index("(") + 1 : -1]
    arguments = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(inner):
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
        elif char == "," and depth == 0:
            arguments.append(inner[start:index])
            start = index + 1
    arguments.append(inner[start:])
    return arguments


def import_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


def formal_fold(values: list[int], start_index: int = 0, accumulator: int = 0) -> int:
    total = accumulator
    index = start_index
    for value in values:
        if index % 3 == 0:
            total += value * value
        elif index % 4 == 0:
            total += value * value * value
        else:
            total += value
        index += 1
    return total


def int_seq(values: list[int]) -> str:
    result = ".IntSeq"
    for value in reversed(values):
        result = f"iCons({value},{result})"
    return result


def main() -> int:
    mpy = compact((ROOT / "solution.mpy").read_text())
    spec = compact((ROOT / "spec.k").read_text())
    verification = compact((ROOT / "verification.k").read_text())

    load_identity = (
        f"#loadAll({ast_surface_normalize(mpy)})" in ast_surface_normalize(spec)
    )

    solution_for = balanced_term(mpy, "For(")
    solution_for_args = split_arguments(solution_for)
    loop_term = balanced_term(spec, "#loop(")
    loop_args = split_arguments(loop_term)
    target_identity = solution_for_args[0] == loop_args[1]
    body_identity = ast_surface_normalize(solution_for_args[2]) == ast_surface_normalize(
        loop_args[2]
    )

    spec_context = spec[spec.index("<k>") : spec.index("</exit-code>") + len("</exit-code>")]
    verification_module = verification.rindex("moduleVERIFICATION")
    verification_context = verification[
        verification.index("<k>", verification_module) : verification.index(
            "</exit-code>", verification_module
        )
        + len("</exit-code>")
    ]
    bridge_context_identity = spec_context == verification_context

    print(f"ENTRY_LOADS_EXACT_SOLUTION_MPY={load_identity}")
    print(f"LOOP_TARGET_MATCHES_REAL_FOR={target_identity}")
    print(f"LOOP_BODY_MATCHES_REAL_FOR={body_identity}")
    print(f"LOOP_BRIDGE_CONTEXT_IDENTICAL_TO_LOOP_CLAIM={bridge_context_identity}")

    canonical = import_entry("trusted_canonical_witness", Path("/reference/canonical.py"))
    generated = import_entry("generated_witness", ROOT / "solution.py")
    for values in ([], [1, 2, 3], [-1, -5, 2, -1, -5], [2, -3, 5, -7, 11]):
        formal = formal_fold(values)
        observed = {
            "input": values,
            "int_seq": int_seq(values),
            "formal_sumSquaresFrom": formal,
            "trusted_canonical": canonical(list(values)),
            "generated_python": generated(list(values)),
        }
        print("ENTRY_WITNESS=" + json.dumps(observed, sort_keys=True))
        if len({formal, observed["trusted_canonical"], observed["generated_python"]}) != 1:
            return 1

    # Reachable loop-head state after processing indices 0..3 of this input.
    full_input = [2, -3, 5, -7, 11]
    prefix = full_input[:4]
    suffix = full_input[4:]
    accumulator = formal_fold(prefix)
    loop_result = formal_fold(suffix, start_index=4, accumulator=accumulator)
    loop_witness = {
        "IS": int_seq(suffix),
        "I": 4,
        "A": accumulator,
        "OLD": -7,
        "INPUT": int_seq(full_input),
        "MODULE": ".Map",
        "BUILTINS": "builtinsScope",
        "env": 1,
        "scopeLoc": 2,
        "heap": ".Map",
        "heapLoc": 0,
        "stack": "ListItem(frame(.K,0,1))",
        "ret": "noRet",
        "exc": "NoExc",
        "exit-code": 0,
        "sumSquaresFrom(IS,I,A)": loop_result,
        "whole_program_result": generated(full_input),
    }
    print("LOOP_PRECONDITION_WITNESS=" + json.dumps(loop_witness, sort_keys=True))
    if loop_result != generated(full_input):
        return 1

    all_structural = (
        load_identity and target_identity and body_identity and bridge_context_identity
    )
    print(f"ALL_STRUCTURAL_PINNING_CHECKS={all_structural}")
    return 0 if all_structural else 1


if __name__ == "__main__":
    raise SystemExit(main())
