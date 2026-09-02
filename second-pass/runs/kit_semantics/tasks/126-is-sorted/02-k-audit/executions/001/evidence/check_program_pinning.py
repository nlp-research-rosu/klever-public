#!/usr/bin/env python3
"""Mechanical constructor-level comparison of translated body and K claims."""

from __future__ import annotations

import re
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/126-is-sorted/solution.mpy")
SPEC = Path("/tmp/audit-work/126-is-sorted/spec.k")


def find_matching_paren(text: str, opening: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
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
                return index
    raise ValueError(f"unmatched parenthesis at {opening}")


def applications(text: str, name: str) -> list[str]:
    result: list[str] = []
    for match in re.finditer(rf"(?<![A-Za-z0-9_#]){re.escape(name)}\s*\(", text):
        opening = text.find("(", match.start())
        closing = find_matching_paren(text, opening)
        result.append(text[opening + 1 : closing])
    return result


def split_top_arguments(contents: str) -> list[str]:
    result: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(contents):
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
            result.append(contents[start:index])
            start = index + 1
    result.append(contents[start:])
    return result


def normalize_constructor_term(text: str) -> str:
    without_units = re.sub(r"(?<![A-Za-z0-9_])\.Stmts(?![A-Za-z0-9_])", "", text)
    return re.sub(r"\s+", "", without_units)


def main() -> int:
    solution = SOLUTION.read_text()
    spec = SPEC.read_text()
    failures: list[str] = []

    function_nodes = applications(solution, "FuncDef")
    if len(function_nodes) != 1:
        failures.append(f"expected one FuncDef, found {len(function_nodes)}")
        function_args: list[str] = []
    else:
        function_args = split_top_arguments(function_nodes[0])
        if len(function_args) != 3:
            failures.append(
                f"expected three FuncDef arguments, found {len(function_args)}"
            )

    closure_nodes = applications(spec, "closureVal")
    closure_args = [split_top_arguments(node) for node in closure_nodes]
    valid_closures = [
        args
        for args in closure_args
        if len(args) == 3
        and normalize_constructor_term(args[0]) == '"lst"'
        and normalize_constructor_term(args[2]) == "0"
    ]
    print(f"solution_FuncDef_count={len(function_nodes)}")
    print(f"spec_closureVal_count={len(closure_nodes)}")
    print(f"spec_matching_is_sorted_closure_count={len(valid_closures)}")
    if len(valid_closures) != 2:
        failures.append(
            "entry claim should contain the same closure in source and target "
            f"scopes twice, found {len(valid_closures)}"
        )

    if len(function_args) == 3:
        print(
            "function_name="
            f"{normalize_constructor_term(function_args[0])}"
        )
        print(
            "function_params="
            f"{normalize_constructor_term(function_args[1])}"
        )
        expected_body = normalize_constructor_term(function_args[2])
        for index, args in enumerate(valid_closures):
            actual_body = normalize_constructor_term(args[1])
            equal = actual_body == expected_body
            print(f"closure_body_{index}_equals_solution_body={equal}")
            print(
                f"closure_body_{index}_normalized_length={len(actual_body)}"
            )
            if not equal:
                failures.append(f"closure body {index} differs from solution")

        for_nodes = applications(function_args[2], "For")
        loop_nodes = applications(spec, "#loop")
        print(f"solution_For_count={len(for_nodes)}")
        print(f"spec_#loop_count={len(loop_nodes)}")
        if len(for_nodes) != 1 or len(loop_nodes) != 1:
            failures.append("expected exactly one source For and one #loop claim")
        else:
            for_args = split_top_arguments(for_nodes[0])
            loop_args = split_top_arguments(loop_nodes[0])
            print(f"solution_For_argument_count={len(for_args)}")
            print(f"spec_#loop_argument_count={len(loop_args)}")
            if len(for_args) != 3 or len(loop_args) != 3:
                failures.append("For/#loop arguments are malformed")
            else:
                target_equal = (
                    normalize_constructor_term(for_args[0])
                    == normalize_constructor_term(loop_args[1])
                )
                body_equal = (
                    normalize_constructor_term(for_args[2])
                    == normalize_constructor_term(loop_args[2])
                )
                iterable_name = normalize_constructor_term(for_args[1])
                loop_iterable = normalize_constructor_term(loop_args[0])
                print(f"loop_target_equals_source_target={target_equal}")
                print(f"loop_body_equals_source_body={body_equal}")
                print(f"source_iterable={iterable_name}")
                print(f"loop_runtime_iterable={loop_iterable}")
                if not target_equal or not body_equal:
                    failures.append("helper loop target/body differs from source")
                if iterable_name != 'Name("lst")':
                    failures.append("source For does not iterate lst")
                if loop_iterable != "list(REMAINING:ValSeq)":
                    failures.append("helper claim is not at evaluated list suffix")

    print(f"FAILURE_COUNT={len(failures)}")
    for failure in failures:
        print(f"FAILURE {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
