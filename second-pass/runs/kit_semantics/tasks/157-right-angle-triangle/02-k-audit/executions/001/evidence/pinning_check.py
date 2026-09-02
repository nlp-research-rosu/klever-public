#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and the claim closure."""

from __future__ import annotations

import ast
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def extract_call(text: str, name: str, start: int = 0) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*\(", text[start:])
    if match is None:
        raise AssertionError(f"missing constructor call: {name}")
    begin = start + match.start()
    open_paren = text.index("(", begin)
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
    raise AssertionError(f"unbalanced constructor call: {name}")


def call_parts(call: str) -> tuple[str, list[str]]:
    open_paren = call.index("(")
    name = call[:open_paren].strip()
    body = call[open_paren + 1 : -1]
    parts: list[str] = []
    depth = 0
    in_string = False
    escaped = False
    part_start = 0
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
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(body[part_start:index].strip())
            part_start = index + 1
    parts.append(body[part_start:].strip())
    return name, parts


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> None:
    generated = (SCRATCH / "regenerated-solution.mpy").read_text()
    submitted = (SCRATCH / "solution.mpy").read_text()
    verification = (SCRATCH / "verification.k").read_text()
    assert generated.encode() == submitted.encode()

    canonical_module = ast.parse((SCRATCH / "canonical.py").read_text())
    candidate_module = ast.parse((SCRATCH / "solution.py").read_text())
    canonical_function = next(
        node for node in canonical_module.body if isinstance(node, ast.FunctionDef)
    )
    candidate_function = next(
        node for node in candidate_module.body if isinstance(node, ast.FunctionDef)
    )
    canonical_body = list(canonical_function.body)
    if (
        canonical_body
        and isinstance(canonical_body[0], ast.Expr)
        and isinstance(canonical_body[0].value, ast.Constant)
        and isinstance(canonical_body[0].value.value, str)
    ):
        canonical_body.pop(0)
    source_ast_equal = (
        ast.dump(canonical_function.args, include_attributes=False)
        == ast.dump(candidate_function.args, include_attributes=False)
        and ast.dump(ast.Module(body=canonical_body, type_ignores=[]), include_attributes=False)
        == ast.dump(
            ast.Module(body=candidate_function.body, type_ignores=[]),
            include_attributes=False,
        )
    )
    print(f"SOURCE canonical_vs_candidate_function_ast_equal={source_ast_equal}")
    assert source_ast_equal

    _, func_parts = call_parts(extract_call(generated, "FuncDef"))
    assert len(func_parts) == 3
    function_name, params_call, generated_body = func_parts
    assert function_name == '"right_angle_triangle"'
    _, params_parts = call_parts(params_call)

    closure_start = verification.index("rule rightAngleTriangleClosure()")
    _, closure_parts = call_parts(
        extract_call(verification, "closureVal", start=closure_start)
    )
    assert len(closure_parts) == 3
    closure_params, closure_body, defining_scope = closure_parts

    normalized_params = normalize(closure_params)
    expected_params = normalize("(" + ",".join(params_parts) + ")")
    body_equal = normalize(generated_body) == normalize(closure_body)
    params_equal = normalized_params == expected_params
    scope_equal = defining_scope.strip() == "0"

    print("TRANSLATION submitted_vs_trusted_regeneration=BYTE_IDENTICAL")
    print(
        "PINNING "
        f"function_name={function_name} "
        f"params_equal={params_equal} "
        f"body_constructor_equal={body_equal} "
        f"defining_scope_zero={scope_equal}"
    )
    assert params_equal and body_equal and scope_equal


if __name__ == "__main__":
    main()
