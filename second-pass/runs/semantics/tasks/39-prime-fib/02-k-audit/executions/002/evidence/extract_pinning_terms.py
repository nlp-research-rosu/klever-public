#!/usr/bin/env python3
"""Extract source-derived and verification-provided closure terms for K parsing."""

from __future__ import annotations

from pathlib import Path

WORK = Path("/tmp/audit-work/prime-fib-audit")


def balanced_call(text: str, start: int) -> str:
    opening = text.find("(", start)
    if opening < 0:
        raise ValueError("missing opening parenthesis")
    depth = 0
    quote = False
    escape = False
    for index in range(start, len(text)):
        char = text[index]
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and index >= opening:
                return text[start : index + 1]
    raise ValueError("unterminated constructor")


def split_top_level(call: str) -> tuple[str, list[str]]:
    opening = call.find("(")
    name = call[:opening].strip()
    content = call[opening + 1 : -1]
    parts = []
    start = 0
    depth = 0
    quote = False
    escape = False
    for index, char in enumerate(content):
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(content[start:index].strip())
            start = index + 1
    parts.append(content[start:].strip())
    return name, parts


mpy = (WORK / "regenerated-solution.mpy").read_text()
verification = (WORK / "verification.k").read_text()

pairs = [
    ("_is_prime", "isPrimeClosure", "isprime"),
    ("prime_fib", "primeFibClosure", "primefib"),
]
for function_name, alias_name, stem in pairs:
    function_start = mpy.index(f'FuncDef("{function_name}"')
    function_term = balanced_call(mpy, function_start)
    ctor, function_args = split_top_level(function_term)
    if ctor != "FuncDef" or len(function_args) != 3:
        raise SystemExit(f"unexpected {function_name} constructor: {function_args}")
    params_ctor, params_args = split_top_level(function_args[1])
    if params_ctor != "Params":
        raise SystemExit(f"unexpected params for {function_name}")
    param_names = ", ".join(params_args)
    expected = f"closureVal({param_names}, {function_args[2]}, 0)\n"

    rule_start = verification.index(f"rule {alias_name}")
    closure_start = verification.index("closureVal(", rule_start)
    actual = balanced_call(verification, closure_start) + "\n"

    expected_path = WORK / f"pinning-{stem}-source.k"
    raw_actual_path = WORK / f"pinning-{stem}-verification-raw.k"
    actual_path = WORK / f"pinning-{stem}-verification.k"
    expected_path.write_text(expected)
    raw_actual_path.write_text(actual)
    # `.Stmts` is accepted in rule syntax but the standalone program parser
    # spells the same empty List{Stmt,""} by omitting the list element.
    actual_path.write_text(actual.replace(".Stmts", ""))
    print(
        f"{function_name}: source_term={expected_path.name} "
        f"verification_raw={raw_actual_path.name} "
        f"verification_parse_term={actual_path.name}"
    )
