#!/usr/bin/env python3
"""Mechanical constructor-token comparison of solution.mpy and the entry closure."""

from __future__ import annotations

import hashlib
import pathlib
import re
import sys


WORK = pathlib.Path("/tmp/audit-work/reconstruction")
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|-?\d+|[A-Za-z_#.?][A-Za-z0-9_#.?\-]*|[(),]')


def tokens(path: pathlib.Path) -> list[str]:
    return TOKEN.findall(path.read_text(encoding="utf-8"))


def constructor_args(stream: list[str], name: str, occurrence: int = 1) -> list[list[str]]:
    seen = 0
    for index, token in enumerate(stream):
        if token != name or index + 1 >= len(stream) or stream[index + 1] != "(":
            continue
        seen += 1
        if seen != occurrence:
            continue
        depth = 1
        args: list[list[str]] = [[]]
        cursor = index + 2
        while cursor < len(stream):
            token = stream[cursor]
            if token == "(":
                depth += 1
                args[-1].append(token)
            elif token == ")":
                depth -= 1
                if depth == 0:
                    return args
                args[-1].append(token)
            elif token == "," and depth == 1:
                args.append([])
            else:
                args[-1].append(token)
            cursor += 1
        raise ValueError(f"unclosed constructor {name}")
    raise ValueError(f"constructor {name} occurrence {occurrence} not found")


def normalize_body(body: list[str], from_translator: bool) -> list[str]:
    result: list[str] = []
    index = 0
    while index < len(body):
        # The translator elides the empty Stmts terminator; the spec spells it out.
        if (
            from_translator
            and body[index] == ","
            and index + 1 < len(body)
            and body[index + 1] == ")"
        ):
            result.extend([",", ".Stmts"])
            index += 1
            continue
        result.append(body[index])
        index += 1
    if from_translator:
        result.append(".Stmts")
    return result


def digest(stream: list[str]) -> str:
    return hashlib.sha256("\0".join(stream).encode()).hexdigest()


def main() -> int:
    mpy = tokens(WORK / "solution-regenerated.mpy")
    spec = tokens(WORK / "spec.k")
    function = constructor_args(mpy, "FuncDef")
    closure = constructor_args(spec, "closureVal")
    if len(function) != 3:
        print(f"unexpected FuncDef arity: {len(function)}")
        return 1
    if len(closure) != 3:
        print(f"unexpected closureVal arity: {len(closure)}")
        return 1

    name_ok = function[0] == ['"reverse_delete"']
    translated_params = [
        token
        for token in function[1]
        if token.startswith('"') and token.endswith('"')
    ]
    closure_param_tokens = [
        token
        for token in closure[0]
        if token not in {"(", ")", ",", ".ParamNames"}
    ]
    params_ok = translated_params == closure_param_tokens == ['"s"', '"c"']

    translated_body = normalize_body(function[2], from_translator=True)
    closure_body = normalize_body(closure[1], from_translator=False)
    body_ok = translated_body == closure_body
    defining_env_ok = closure[2] == ["0"]

    print(f"name_match={name_ok}")
    print(f"parameter_match={params_ok}; params={translated_params}")
    print(f"translated_body_tokens={len(translated_body)}")
    print(f"closure_body_tokens={len(closure_body)}")
    print(f"translated_body_sha256={digest(translated_body)}")
    print(f"closure_body_sha256={digest(closure_body)}")
    print(f"body_constructor_identity={body_ok}")
    print(f"defining_environment_is_module_zero={defining_env_ok}")
    if not body_ok:
        for index, (left, right) in enumerate(zip(translated_body, closure_body)):
            if left != right:
                print(f"first_body_difference={index}: translated={left!r}, closure={right!r}")
                break
        if len(translated_body) != len(closure_body):
            print("body lengths differ")
    return 0 if name_ok and params_ok and body_ok and defining_env_ok else 1


if __name__ == "__main__":
    sys.exit(main())
