#!/usr/bin/env python3
"""Mechanical constructor pinning plus concrete satisfying witnesses."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import ModuleType


SOLUTION_MPY = Path("/tmp/audit-work/reconstruction/solution.mpy")
SPEC_K = Path("/tmp/audit-work/reconstruction/spec.k")
CANDIDATE_PY = Path("/tmp/audit-work/reconstruction/solution.py")
CANONICAL_PY = Path("/reference/canonical.py")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize(text: str) -> str:
    # These artifacts use full-line K comments. Do not split on "//": it is
    # also the floor-division operator string inside the submitted program.
    no_comments = "\n".join(
        line for line in text.splitlines() if not line.lstrip().startswith("//")
    )
    return re.sub(r"\s+", "", no_comments).replace(".Stmts", "")


def matching_paren(text: str, open_index: int) -> int:
    assert text[open_index] == "("
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
        ch = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return index
    raise AssertionError(f"unmatched parenthesis at {open_index}")


def split_top_level(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, ch in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append(text[start:index])
            start = index + 1
    parts.append(text[start:])
    return parts


def parse_call(term: str, name: str) -> list[str]:
    prefix = name + "("
    assert term.startswith(prefix), f"expected {name}, got {term[:80]}"
    close = matching_paren(term, len(name))
    assert close == len(term) - 1, f"trailing text after {name}: {term[close + 1:]}"
    return split_top_level(term[len(prefix) : close])


def extract_calls(text: str, name: str) -> list[str]:
    needle = name + "("
    found: list[str] = []
    cursor = 0
    while True:
        start = text.find(needle, cursor)
        if start < 0:
            return found
        close = matching_paren(text, start + len(name))
        found.append(text[start : close + 1])
        cursor = close + 1


def odd_digit_recurrence(n: int, accumulator: int) -> int:
    while n > 0:
        digit = n % 10
        if n % 2 == 1:
            accumulator = digit if accumulator == 0 else accumulator * digit
        n = (n - digit) // 10
    return accumulator


def main() -> None:
    translated = normalize(SOLUTION_MPY.read_text())
    spec = normalize(SPEC_K.read_text())

    module_args = parse_call(translated, "Module")
    assert len(module_args) == 1
    function_args = parse_call(module_args[0], "FuncDef")
    assert len(function_args) == 3
    function_name, params, body = function_args
    assert function_name == '"digits"'
    assert params == 'Params("n")'
    print("OK translated module has exactly one FuncDef named digits with parameter n")

    closures = extract_calls(spec, "closureVal")
    assert len(closures) == 3, f"expected 3 closure terms, got {len(closures)}"
    for index, closure in enumerate(closures, 1):
        args = parse_call(closure, "closureVal")
        assert args == ['"n"', body, "0"], (
            f"closure {index} does not contain the translated body"
        )
    print("OK all 3 claim closure bindings contain the exact normalized translated body")

    translated_while = extract_calls(body, "While")
    assert len(translated_while) == 1
    while_args = parse_call(translated_while[0], "While")
    proof_whiles = extract_calls(spec, "#while")
    assert len(proof_whiles) == 1
    proof_while_args = parse_call(proof_whiles[0], "#while")
    assert proof_while_args == while_args
    print("OK auxiliary #while claim matches the submitted While guard and body")

    expected_entry = (
        'Call(Name("digits"),Int(N:Int))=>oddDigitProduct(N,0)'
    )
    assert expected_entry in spec
    print("OK entry claim calls digits and constrains its result to oddDigitProduct(N,0)")

    candidate = load_module("pinning_candidate", CANDIDATE_PY)
    canonical = load_module("pinning_canonical", CANONICAL_PY)
    entry_witnesses = [1, 4, 235, 10203, 13579]
    for n in entry_witnesses:
        summary = odd_digit_recurrence(n, 0)
        assert candidate.digits(n) == canonical.digits(n) == summary
        print(
            f"ENTRY_WITNESS N={n} precondition={n > 0} "
            f"candidate={candidate.digits(n)} canonical={canonical.digits(n)} "
            f"summary={summary}"
        )

    loop_witnesses = [(0, 0), (235, 0), (246, 5), (19, 3)]
    for n, accumulator in loop_witnesses:
        assert n >= 0 and accumulator >= 0
        summary = odd_digit_recurrence(n, accumulator)
        print(
            f"LOOP_WITNESS N={n} A={accumulator} "
            f"precondition={n >= 0 and accumulator >= 0} summary={summary}"
        )

    print("STAGE4_PINNING_OK")


if __name__ == "__main__":
    main()
