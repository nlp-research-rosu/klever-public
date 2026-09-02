#!/usr/bin/env python3
"""Mechanical constructor-token comparison between solution.mpy and spec.k."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


TOKEN_RE = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z0-9_]*|-?[0-9]+|[(),:]')


def tokens(text: str) -> list[str]:
    no_line_comments = re.sub(r"//[^\n]*", "", text)
    return TOKEN_RE.findall(no_line_comments)


def balanced_call(source_tokens: list[str], start: int) -> list[str]:
    if start + 1 >= len(source_tokens) or source_tokens[start + 1] != "(":
        raise ValueError("constructor is not followed by '('")
    depth = 0
    for pos in range(start + 1, len(source_tokens)):
        token = source_tokens[pos]
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
            if depth == 0:
                return source_tokens[start : pos + 1]
    raise ValueError("unterminated constructor term")


def count_subsequence(haystack: list[str], needle: list[str]) -> int:
    return sum(
        haystack[pos : pos + len(needle)] == needle
        for pos in range(0, len(haystack) - len(needle) + 1)
    )


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.starts_one_ends


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "usage: 04_constructor_pinning.py "
            "SOLUTION_MPY SPEC_K TRUSTED_CANONICAL SOLUTION_PY"
        )
        return 2

    solution_tokens = tokens(Path(sys.argv[1]).read_text(encoding="utf-8"))
    spec_tokens = tokens(Path(sys.argv[2]).read_text(encoding="utf-8"))

    expected_prefix = [
        "Module",
        "(",
        "FuncDef",
        "(",
        '"starts_one_ends"',
        ",",
        "Params",
        "(",
        '"n"',
        ")",
        ",",
    ]
    prefix_matches = solution_tokens[: len(expected_prefix)] == expected_prefix
    return_start = len(expected_prefix)
    return_body = balanced_call(solution_tokens, return_start)
    expected_suffix = [")", ")"]
    suffix_matches = solution_tokens[return_start + len(return_body) :] == expected_suffix

    closure_term = [
        "closureVal",
        "(",
        '"n"',
        ",",
        *return_body,
        ",",
        "0",
        ")",
    ]
    closure_occurrences = count_subsequence(spec_tokens, closure_term)
    body_occurrences = count_subsequence(spec_tokens, return_body)
    call_term = [
        "Call",
        "(",
        "Name",
        "(",
        '"starts_one_ends"',
        ")",
        ",",
        "N",
        ":",
        "Int",
        ")",
    ]
    call_occurrences = count_subsequence(spec_tokens, call_term)

    canonical = load_entry("trusted_canonical_pinning", Path(sys.argv[3]))
    generated = load_entry("candidate_solution_pinning", Path(sys.argv[4]))
    witness_rows = []
    for n in [1, 2, 7]:
        claimed = 1 if n == 1 else 18 * (10 ** (n - 2))
        witness_rows.append((n, n == 1, n > 1, claimed, canonical(n), generated(n)))

    print(f"solution_prefix_exact = {prefix_matches}")
    print(f"solution_suffix_exact = {suffix_matches}")
    print(f"return_body_token_count = {len(return_body)}")
    print(f"exact_return_body_occurrences_in_spec = {body_occurrences}")
    print(f"exact_closure_binding_occurrences_in_spec = {closure_occurrences}")
    print(f"exact_symbolic_call_occurrences_in_spec = {call_occurrences}")
    for row in witness_rows:
        n, pre_one, pre_multi, claimed, trusted, candidate = row
        print(
            f"witness n={n}: pre_one={pre_one}, pre_multi={pre_multi}, "
            f"claimed={claimed}, trusted={trusted}, candidate={candidate}, "
            f"all_equal={claimed == trusted == candidate}"
        )

    ok = (
        prefix_matches
        and suffix_matches
        and closure_occurrences == 2
        and body_occurrences == 2
        and call_occurrences == 2
        and all(row[3] == row[4] == row[5] for row in witness_rows)
    )
    print(f"constructor_pinning_and_ground_substitution_ok = {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
