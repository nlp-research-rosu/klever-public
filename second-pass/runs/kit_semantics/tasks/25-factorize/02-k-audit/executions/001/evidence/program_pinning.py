#!/usr/bin/env python3
"""Mechanical constructor-level comparison of MPY body and claimed closures."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def calls(text: str, constructor: str) -> list[str]:
    matches: list[str] = []
    pattern = re.compile(rf"\b{re.escape(constructor)}\s*\(")
    for match in pattern.finditer(text):
        start = text.find("(", match.start())
        depth = 0
        in_string = False
        escaped = False
        for index in range(start, len(text)):
            character = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
                continue
            if character == '"':
                in_string = True
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    matches.append(text[match.start():index + 1])
                    break
        else:
            raise ValueError(f"unbalanced {constructor} occurrence")
    return matches


def constructor_arguments(term: str) -> list[str]:
    start = term.find("(")
    inside = term[start + 1:-1]
    arguments: list[str] = []
    depth = 0
    in_string = False
    escaped = False
    last = 0
    for index, character in enumerate(inside):
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            arguments.append(inside[last:index])
            last = index + 1
    arguments.append(inside[last:])
    return arguments


def normalize(term: str) -> str:
    compact = re.sub(r"\s+", "", term)
    compact = compact.replace("ListExpr()", "ListExpr(.Exprs)")
    # Explicit `.Stmts` is the unit of K's statement-list production. The
    # translator omits list units in surface syntax; the spec spells them out.
    compact = compact.replace(".Stmts", "")
    return compact


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mpy", required=True)
    parser.add_argument("--spec", required=True)
    args = parser.parse_args()
    mpy = Path(args.mpy).read_text()
    spec = Path(args.spec).read_text()

    function_terms = [
        term
        for term in calls(mpy, "FuncDef")
        if normalize(constructor_arguments(term)[0]) == '"factorize"'
    ]
    closure_terms = [
        term
        for term in calls(spec, "closureVal")
        if normalize(constructor_arguments(term)[0]) == '"n"'
    ]
    if len(function_terms) != 1:
        print(f"factorize_function_count={len(function_terms)}")
        return 1
    function_args = constructor_arguments(function_terms[0])
    function_params = normalize(function_args[1])
    function_body = normalize(function_args[2])
    print(f"factorize_function_count={len(function_terms)}")
    print(f"claim_factorize_closure_count={len(closure_terms)}")
    print(f"function_params={function_params}")
    print(f"function_body_normalized={function_body}")

    all_match = True
    for index, term in enumerate(closure_terms, start=1):
        closure_args = constructor_arguments(term)
        closure_body = normalize(closure_args[1])
        body_match = closure_body == function_body
        anchor_match = normalize(closure_args[2]) == "0"
        print(
            f"closure_{index}: parameter={normalize(closure_args[0])} "
            f"defining_scope={normalize(closure_args[2])} "
            f"body_match={body_match} anchor_match={anchor_match}"
        )
        all_match = all_match and body_match and anchor_match

    import_is_typing = 'ImportFrom("typing","List")' in normalize(mpy)
    entry_call_present = (
        'Call(Name("factorize"),(Int(N:Int),.Exprs))' in normalize(spec)
    )
    print(f"typing_only_import_present={import_is_typing}")
    print(f"symbolic_entry_call_present={entry_call_present}")
    print(f"all_claimed_closures_match={all_match}")
    return 0 if len(closure_terms) == 2 and all_match and entry_call_present else 1


if __name__ == "__main__":
    raise SystemExit(main())
