#!/usr/bin/env python3
"""Mechanical constructor pinning and concrete claim instantiation checks."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/46-fib4")


def extract_call(text: str, name: str, occurrence: int = 0) -> str:
    marker = name + "("
    cursor = -1
    for _ in range(occurrence + 1):
        cursor = text.find(marker, cursor + 1)
        if cursor < 0:
            raise ValueError(f"missing {name} occurrence {occurrence}")
    start = cursor + len(marker)
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
                return text[start:index]
    raise ValueError(f"unclosed {name}")


def split_top_level(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(text):
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
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def normalize(text: str) -> str:
    result: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            result.append(char)
        elif not char.isspace():
            result.append(char)
    return "".join(result)


def load_fib4(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib4


def recurrence(n: int) -> int:
    values = [0, 0, 2, 0]
    for index in range(4, n + 1):
        values.append(sum(values[index - 4 : index]))
    return values[n]


def main() -> int:
    mpy = (WORK / "regenerated-solution.mpy").read_text()
    spec_text = (WORK / "spec.k").read_text()
    source = (WORK / "solution.py").read_text()

    func_args = split_top_level(extract_call(mpy, "FuncDef"))
    closure_args = split_top_level(extract_call(spec_text, "closureVal"))
    actual_while = split_top_level(extract_call(mpy, "While"))
    claimed_while = split_top_level(extract_call(spec_text, "#while"))

    checks = {
        "one_translated_function": mpy.count("FuncDef(") == 1,
        "translated_name": func_args[0] == '"fib4"',
        "translated_params": normalize(func_args[1]) == 'Params("n")',
        "claim_param": closure_args[0] == '"n"',
        "claim_parent_env": normalize(closure_args[2]) == "0",
        "closure_body_exact": normalize(func_args[2]) == normalize(closure_args[1]),
        "loop_guard_exact": normalize(actual_while[0]) == normalize(claimed_while[0]),
        "loop_body_exact": normalize(actual_while[1]) == normalize(claimed_while[1]),
    }

    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    recursive_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "fib4"
    ]
    while_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.While)]
    checks["source_single_fib4"] = (
        len(functions) == 1
        and functions[0].name == "fib4"
        and [arg.arg for arg in functions[0].args.args] == ["n"]
    )
    checks["source_nonrecursive"] = not recursive_calls
    checks["source_one_loop"] = len(while_nodes) == 1

    print("MECHANICAL PINNING")
    for name, value in checks.items():
        print(f"{name}: {'PASS' if value else 'FAIL'}")
    body_hash = hashlib.sha256(normalize(func_args[2]).encode()).hexdigest()
    claim_hash = hashlib.sha256(normalize(closure_args[1]).encode()).hexdigest()
    print(f"translated_body_normalized_sha256={body_hash}")
    print(f"claimed_body_normalized_sha256={claim_hash}")

    candidate = load_fib4(WORK / "solution.py", "pin_candidate")
    canonical = load_fib4(WORK / "canonical.py", "pin_canonical")
    print("\nSATISFIABLE PRECONDITION WITNESSES")
    print("entry: N=0; exact caller cells are those written in SPEC.fib4-correct")
    print(
        "loop: N=7, I=4, L=1, P=parent(0), E=0, "
        f"locals=(n=7,i=4,a={recurrence(4)},b={recurrence(5)},"
        f"c={recurrence(6)},d={recurrence(7)},e=0)"
    )
    witness_ok = 0 <= 4 <= 7
    print(f"entry_precondition_0_ge_0: PASS")
    print(f"loop_precondition_0_le_4_le_7: {'PASS' if witness_ok else 'FAIL'}")

    print("\nGROUND POSTCONDITION INSTANTIATIONS")
    ground_ok = True
    for n in [0, 1, 2, 3, 4, 5, 7, 10]:
        formal = recurrence(n)
        candidate_value = candidate(n)
        canonical_value = canonical(n)
        ok = formal == candidate_value == canonical_value
        ground_ok &= ok
        print(
            f"N={n} fib4Spec={formal} candidate={candidate_value} "
            f"canonical={canonical_value} {'PASS' if ok else 'FAIL'}"
        )

    return 0 if all(checks.values()) and witness_ok and ground_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
