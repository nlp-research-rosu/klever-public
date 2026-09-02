#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and claimed bodies."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


MPY = Path("/tmp/audit-work/candidate/solution.mpy")
VERIFICATION = Path("/tmp/audit-work/candidate/verification.k")
SPEC = Path("/tmp/audit-work/candidate/spec.k")


def matching_paren(text: str, open_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
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
    raise ValueError(f"unclosed parenthesis at offset {open_index}")


def split_top_level(text: str) -> list[str]:
    result: list[str] = []
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
            result.append(text[start:index].strip())
            start = index + 1
    result.append(text[start:].strip())
    return result


def tokenize(term: str) -> tuple[str, ...]:
    pattern = re.compile(
        r'"(?:\\.|[^"\\])*"|'
        r'#[A-Za-z_][A-Za-z0-9_-]*|'
        r'[A-Za-z_.][A-Za-z0-9_.-]*|'
        r'-?[0-9]+|'
        r'[(),]'
    )
    tokens = tuple(pattern.findall(term))
    residue = pattern.sub("", term)
    if residue.strip():
        raise ValueError(f"unparsed constructor text: {residue!r} from {term!r}")
    return tokens


def mpy_functions(text: str) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    position = 0
    while True:
        start = text.find("FuncDef(", position)
        if start < 0:
            break
        open_index = start + len("FuncDef")
        close_index = matching_paren(text, open_index)
        args = split_top_level(text[open_index + 1 : close_index])
        if len(args) != 3:
            raise ValueError(f"FuncDef has {len(args)} top-level arguments")
        name_match = re.fullmatch(r'"([^"]+)"', args[0])
        param_match = re.fullmatch(r'Params\("([^"]+)"\)', re.sub(r"\s+", "", args[1]))
        if name_match is None or param_match is None:
            raise ValueError(f"unexpected FuncDef header: {args[:2]}")
        result[name_match.group(1)] = (param_match.group(1), args[2])
        position = close_index + 1
    return result


def rhs_term(text: str, symbol: str) -> str:
    anchor = re.search(rf"(?m)^\s*rule\s+{re.escape(symbol)}\s*$", text)
    if anchor is None:
        raise ValueError(f"missing rule for {symbol}")
    arrow = text.find("=>", anchor.end())
    start = text.find("Return(", arrow)
    if arrow < 0 or start < 0:
        raise ValueError(f"missing Return RHS for {symbol}")
    open_index = start + len("Return")
    close_index = matching_paren(text, open_index)
    return text[start : close_index + 1]


def digest_tokens(tokens: tuple[str, ...]) -> str:
    return hashlib.sha256("\0".join(tokens).encode()).hexdigest()


def main() -> None:
    functions = mpy_functions(MPY.read_text())
    verification = VERIFICATION.read_text()
    spec = SPEC.read_text()
    mapping = {
        "_roman_thousands": ("digit", "romanThousandsBody"),
        "_roman_hundreds": ("digit", "romanHundredsBody"),
        "_roman_tens": ("digit", "romanTensBody"),
        "_roman_ones": ("digit", "romanOnesBody"),
        "int_to_mini_roman": ("number", "romanSolutionBody"),
    }
    failures: list[str] = []

    print(f"translated_functions={sorted(functions)}")
    for name, (expected_param, body_symbol) in mapping.items():
        if name not in functions:
            failures.append(f"translated function missing: {name}")
            continue
        actual_param, translated_body = functions[name]
        claimed_body = rhs_term(verification, body_symbol)
        translated_tokens = tokenize(translated_body)
        claimed_tokens = tokenize(claimed_body)
        body_equal = translated_tokens == claimed_tokens
        binding_pattern = re.compile(
            rf'"{re.escape(name)}"\s*\|->\s*'
            rf'closureVal\("{re.escape(expected_param)}",\s*'
            rf'{re.escape(body_symbol)},\s*0\)'
        )
        binding_count = len(binding_pattern.findall(spec))
        print(
            f"{name}: param={actual_param!r}; body_symbol={body_symbol}; "
            f"constructor_tokens_equal={body_equal}; "
            f"token_sha256={digest_tokens(translated_tokens)}; "
            f"spec_binding_count={binding_count}"
        )
        if actual_param != expected_param:
            failures.append(
                f"{name}: translated param {actual_param!r} != expected {expected_param!r}"
            )
        if not body_equal:
            failures.append(f"{name}: translated and claimed constructor bodies differ")
        if binding_count == 0:
            failures.append(f"{name}: spec does not bind exact parameter/body/parent tuple")

    extra = sorted(set(functions) - set(mapping))
    missing = sorted(set(mapping) - set(functions))
    print(f"extra_translated_functions={extra}")
    print(f"missing_translated_functions={missing}")
    if extra or missing:
        failures.append(f"function-set mismatch extra={extra} missing={missing}")

    entry_call_count = len(
        re.findall(
            r'Call\s*\(\s*Name\s*\(\s*"int_to_mini_roman"\s*\)\s*,\s*Int\s*\(\s*N\s*\)\s*\)',
            spec,
        )
    )
    print(f"symbolic_entry_call_count={entry_call_count}")
    if entry_call_count != 1:
        failures.append(f"expected one symbolic entry call, found {entry_call_count}")

    print(f"failure_count={len(failures)}")
    for failure in failures:
        print(f"FAILURE: {failure}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
