#!/usr/bin/env python3
"""Mechanical constructor-term pinning and concrete precondition witnesses."""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/50-decode-shift")


def calls(text: str, name: str) -> list[str]:
    """Return the inside text of every balanced name(...) occurrence."""
    result: list[str] = []
    start = 0
    marker = name + "("
    while True:
        found = text.find(marker, start)
        if found < 0:
            return result
        index = found + len(name)
        depth = 0
        in_string = False
        escaped = False
        for cursor in range(index, len(text)):
            char = text[cursor]
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
                    result.append(text[index + 1 : cursor])
                    start = cursor + 1
                    break
        else:
            raise AssertionError(f"unbalanced call: {name} at offset {found}")


def split_args(inner: str) -> list[str]:
    result: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(inner):
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
            result.append(inner[start:index])
            start = index + 1
    result.append(inner[start:])
    return result


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|[A-Za-z_#?.][A-Za-z0-9_#?.-]*|-?[0-9]+|[(),]'
)


def normalized_constructor_tokens(term: str) -> tuple[str, ...]:
    tokens = TOKEN.findall(term)
    # `.Stmts` is the explicit associative-list unit. The translator's syntax
    # macro omits trailing units while the spec spells them out.
    return tuple(token for token in tokens if token != ".Stmts")


def digest_tokens(tokens: tuple[str, ...]) -> str:
    return hashlib.sha256("\0".join(tokens).encode()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decode_code(code: int) -> int:
    return ((code - 102) % 26) + 97


def decode_acc(text: str, accumulator: str = "") -> str:
    result = accumulator
    for character in text:
        result += chr(decode_code(ord(character)))
    return result


def lower_codes(text: str) -> bool:
    return all(97 <= ord(character) <= 122 for character in text)


def main() -> None:
    solution_term = (WORK / "solution.mpy").read_text()
    spec_text = (WORK / "spec.k").read_text()

    function_calls = calls(solution_term, "FuncDef")
    assert len(function_calls) == 1
    function_args = split_args(function_calls[0])
    assert len(function_args) == 3
    assert normalized_constructor_tokens(function_args[0]) == ('"decode_shift"',)
    assert normalized_constructor_tokens(function_args[1]) == (
        "Params",
        "(",
        '"s"',
        ")",
    )
    translated_body = normalized_constructor_tokens(function_args[2])

    closure_calls = calls(spec_text, "closureVal")
    assert len(closure_calls) == 2
    closure_bodies: list[tuple[str, ...]] = []
    for index, closure in enumerate(closure_calls, 1):
        args = split_args(closure)
        assert len(args) == 3
        assert normalized_constructor_tokens(args[0]) == ('"s"',)
        assert normalized_constructor_tokens(args[2]) == ("0",)
        closure_body = normalized_constructor_tokens(args[1])
        closure_bodies.append(closure_body)
        assert closure_body == translated_body, f"closure body {index} differs"
    print(
        "ENTRY_CLOSURES_MATCH_TRANSLATED_BODY "
        f"count={len(closure_bodies)} "
        f"token_count={len(translated_body)} "
        f"sha256={digest_tokens(translated_body)}"
    )

    translated_for_calls = calls(function_args[2], "For")
    assert len(translated_for_calls) == 1
    translated_for_args = split_args(translated_for_calls[0])
    assert len(translated_for_args) == 3
    translated_loop_body = normalized_constructor_tokens(translated_for_args[2])
    loop_calls = calls(spec_text, "#loop")
    assert len(loop_calls) == 1
    loop_args = split_args(loop_calls[0])
    assert len(loop_args) == 3
    assert normalized_constructor_tokens(loop_args[0])[:2] == ("str", "(")
    assert normalized_constructor_tokens(loop_args[1]) == (
        "Name",
        "(",
        '"ch"',
        ")",
    )
    claimed_loop_body = normalized_constructor_tokens(loop_args[2])
    assert claimed_loop_body == translated_loop_body
    print(
        "LOOP_CLAIM_MATCHES_TRANSLATED_FOR_BODY "
        f"token_count={len(translated_loop_body)} "
        f"sha256={digest_tokens(translated_loop_body)}"
    )

    generated = load_module("pin_generated", WORK / "solution.py")
    canonical = load_module("pin_canonical", WORK / "canonical.py")
    concrete_inputs = ("", "a", "e", "f", "z", "fghij", "abcdefghijklmnopqrstuvwxyz")
    for value in concrete_inputs:
        assert lower_codes(value)
        summary = decode_acc(value)
        candidate_value = generated.decode_shift(value)
        canonical_value = canonical.decode_shift(value)
        assert summary == candidate_value == canonical_value
        print(
            f"GROUND_RESULT input={value!r} "
            f"summary={summary!r} candidate={candidate_value!r} "
            f"canonical={canonical_value!r}"
        )

    # Satisfiable witnesses for all three entry preconditions.
    assert 97 <= 97 <= 122
    print("PRECONDITION_WITNESS character-inverse C=97")
    assert lower_codes("")
    print(
        "PRECONDITION_WITNESS loop-invariant "
        "CS=.IntSeq ACC=.IntSeq INPUT=.IntSeq CH=str(.IntSeq)"
    )
    assert lower_codes("f")
    print("PRECONDITION_WITNESS decode-shift CS=iCons(102,.IntSeq)")
    print("PROGRAM_PINNING_CHECK PASS")


if __name__ == "__main__":
    main()
