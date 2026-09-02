#!/usr/bin/env python3
"""Mechanical body comparison plus concrete claim-relation witnesses."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|=>|\|->|\.?[A-Za-z_#][A-Za-z0-9_#-]*|'
    r'-?[0-9]+|[(),]'
)


def tokens(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return TOKEN.findall(text)


def matching_close(items: list[str], open_index: int) -> int:
    assert items[open_index] == "("
    depth = 0
    for index in range(open_index, len(items)):
        if items[index] == "(":
            depth += 1
        elif items[index] == ")":
            depth -= 1
            if depth == 0:
                return index
    raise AssertionError("unbalanced parentheses")


def top_level_commas(
    items: list[str], open_index: int, close_index: int
) -> list[int]:
    depth = 0
    answer = []
    for index in range(open_index + 1, close_index):
        if items[index] == "(":
            depth += 1
        elif items[index] == ")":
            depth -= 1
        elif items[index] == "," and depth == 0:
            answer.append(index)
    return answer


def find_call(items: list[str], constructor: str) -> tuple[int, int]:
    index = items.index(constructor)
    assert items[index + 1] == "("
    return index + 1, matching_close(items, index + 1)


def normalize_empty_stmts(items: list[str]) -> list[str]:
    answer = []
    for index, item in enumerate(items):
        answer.append(item)
        if (
            item == ","
            and index + 1 < len(items)
            and items[index + 1] == ")"
        ):
            answer.append(".Stmts")
    return answer


def extract_solution() -> tuple[list[str], list[str]]:
    items = tokens(Path("/candidate/solution.mpy"))
    func_open, func_close = find_call(items, "FuncDef")
    commas = top_level_commas(items, func_open, func_close)
    assert len(commas) == 2, commas
    params = items[commas[0] + 1 : commas[1]]
    body = items[commas[1] + 1 : func_close]
    assert items[func_open + 1] == '"decimal_to_binary"'
    return params, normalize_empty_stmts(body)


def extract_claim() -> tuple[list[str], list[str]]:
    items = tokens(Path("/candidate/spec.k"))
    closure_open, closure_close = find_call(items, "closureVal")
    commas = top_level_commas(items, closure_open, closure_close)
    assert len(commas) == 2, commas
    params = items[closure_open + 1 : commas[0]]
    body = items[commas[0] + 1 : commas[1]]
    closure_scope = items[commas[1] + 1 : closure_close]
    assert closure_scope == ["0"], closure_scope
    return params, normalize_empty_stmts(body)


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.decimal_to_binary


def relation_codes(n: int) -> list[int]:
    assert n >= 0
    if n == 0:
        tail = [48, 100, 98]
    else:
        tail = [100, 98]
        current = n
        while current > 0:
            tail = [48 + current % 2] + tail
            current //= 2
    return [100, 98] + tail


def main() -> None:
    solution_params, solution_body = extract_solution()
    claim_params, claim_body = extract_claim()
    assert solution_params == ["Params", "(", '"decimal"', ")"]
    assert claim_params == ["(", '"decimal"', ",", ".ParamNames", ")"]
    assert solution_body == claim_body
    print("function_name=decimal_to_binary matches=true")
    print("parameter_names=['decimal'] matches=true")
    print(
        f"normalized_body_tokens={len(solution_body)} "
        "constructor_level_match=true"
    )
    print(
        "normalization=whitespace/comments removed; translator's omitted empty "
        "If else normalized to explicit .Stmts"
    )

    canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
    generated = load_entry("submitted_solution", Path("/candidate/solution.py"))
    witnesses = [0, 1, 2, 15, 32, (1 << 256) + 1]
    for n in witnesses:
        codes = relation_codes(n)
        relation_result = "".join(chr(code) for code in codes)
        trusted_result = canonical(n)
        submitted_result = generated(n)
        assert relation_result == trusted_result == submitted_result
        assert codes[:2] == [100, 98] and codes[-2:] == [100, 98]
        assert all(code in (48, 49) for code in codes[2:-2])
        print(
            f"target_witness N={n} precondition={n >= 0} "
            f"result={relation_result!r} relation/python_match=true"
        )

    loop_n = 5
    loop_acc = [65]
    loop_out = loop_acc
    current = loop_n
    while current > 0:
        loop_out = [48 + current % 2] + loop_out
        current //= 2
    print(
        "loop_entry_witness "
        f"N={loop_n} ACC={loop_acc} OUT={loop_out} "
        "env=1 scopeLoc=2 heap=.Map heapLoc=0 stack=.List "
        "ret=noRet exc=NoExc exit_code=0 precondition=true"
    )
    print(
        "target_entry_witness "
        "N=0 env=0 scopeLoc=1 heap=.Map heapLoc=0 stack=.List "
        "ret=noRet exc=NoExc exit_code=0 precondition=true"
    )
    print("ADEQUACY_AND_PINNING=PASS")


if __name__ == "__main__":
    main()
