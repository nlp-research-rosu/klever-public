#!/usr/bin/env python3
"""Mechanical comparison of translated function bodies with spec closures."""

from __future__ import annotations

import json
import re
from pathlib import Path


MPY = Path("/tmp/audit-work/19-sort-numbers/solution.mpy")
VERIFICATION = Path("/tmp/audit-work/19-sort-numbers/verification.k")
RESULT = Path("/audit-output/evidence/04-pinning-results.json")


def remove_space(text: str) -> str:
    output = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    return "".join(output)


def strip_line_comments(text: str) -> str:
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def balanced_term(text: str, start: int) -> str:
    opening = text.find("(", start)
    if opening < 0:
        raise ValueError("opening parenthesis not found")
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
                return text[start : index + 1]
    raise ValueError("unterminated term")


def function_parts(compact_mpy: str, name: str) -> tuple[str, str]:
    function = balanced_term(compact_mpy, compact_mpy.index(f'FuncDef("{name}"'))
    params_start = function.index("Params(")
    params = balanced_term(function, params_start)
    param_payload = params[len("Params(") : -1]
    body_start = params_start + len(params)
    if function[body_start] != ",":
        raise ValueError(f"unexpected function separator for {name}")
    body = function[body_start + 1 : -1]
    # The translator emits an empty Exprs sequence as a trailing comma.
    body = body.replace(",)", ",.Exprs)")
    return param_payload, body


def closure_rhs(compact_verification: str, macro: str) -> str:
    marker = f"rule{macro}=>closureVal("
    start = compact_verification.index(marker) + len(f"rule{macro}=>")
    return balanced_term(compact_verification, start)


def main() -> int:
    compact_mpy = remove_space(MPY.read_text())
    compact_verification = remove_space(
        strip_line_comments(VERIFICATION.read_text())
    )
    comparisons = {}
    functions = {
        "_number_key": "numberKeyClosure",
        "sort_numbers": "sortNumbersClosure",
    }
    for function, macro in functions.items():
        parameters, body = function_parts(compact_mpy, function)
        expected = f"closureVal(({parameters},.ParamNames),({body}.Stmts),0)"
        actual = closure_rhs(compact_verification, macro)
        comparisons[function] = {
            "macro": macro,
            "expected_closure_term": expected,
            "actual_closure_term": actual,
            "constructor_match": expected == actual,
        }

    translated_bindings = re.findall(r'FuncDef\("([^"]+)"', compact_mpy)
    result = {
        "translated_bindings": translated_bindings,
        "claimed_bindings": list(functions),
        "binding_set_match": set(translated_bindings) == set(functions),
        "comparisons": comparisons,
    }
    RESULT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    ok = result["binding_set_match"] and all(
        item["constructor_match"] for item in comparisons.values()
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
