#!/usr/bin/env python3
"""Concrete satisfying states and substitutions for all three positive claims."""

from __future__ import annotations

import importlib.util
import re
import shlex
import subprocess
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def chars_term(value: str) -> str:
    term = "nil"
    for char in reversed(value):
        term = f"cons({ord(char)}, {term})"
    return term


def decode_code(code: int) -> int:
    return ((code - 5 - 97) % 26) + 97


def encode_code(code: int) -> int:
    return ((code + 5 - 97) % 26) + 97


def run_k(program: Path, definition: Path, encoded: str) -> tuple[int, list[int], str]:
    command = [
        "krun",
        str(program),
        "--definition",
        str(definition),
        f"-cINPUT={chars_term(encoded)}",
    ]
    print(f"K_COMMAND {shlex.join(command)}")
    completed = subprocess.run(command, text=True, capture_output=True)
    print(f"K_EXIT_STATUS {completed.returncode}")
    match = re.search(
        r"<result>\s*VChars\s*\((.*?)\)\s*~>\s*\.K\s*</result>",
        completed.stdout,
        re.S,
    )
    codes = [] if match is None else [int(x) for x in re.findall(r"-?\d+", match.group(1))]
    return completed.returncode, codes, completed.stdout


def main() -> int:
    if len(sys.argv) != 5:
        print("usage: adequacy_witness.py CANONICAL SOLUTION PROGRAM DEFINITION")
        return 64

    canonical = load_module("adequacy_canonical", Path(sys.argv[1]))
    generated = load_module("adequacy_generated", Path(sys.argv[2]))
    program = Path(sys.argv[3]).resolve()
    definition = Path(sys.argv[4]).resolve()
    failures = 0

    code = 97
    encoded_code = encode_code(code)
    decoded_code = decode_code(encoded_code)
    print("CLAIM code-inverse")
    print("SATISFYING_STATE <k> decodeCode(encodeCode(97)) ~> KONT </k>")
    print("PRECONDITION isLowerCode(97)=true")
    print(f"SUBSTITUTED_RESULT decodeCode(encodeCode(97))={decoded_code}")
    py_encoded = canonical.encode_shift(chr(code))
    print(f"CANONICAL_ENCODE {py_encoded!r}")
    print(f"CANONICAL_DECODE {canonical.decode_shift(py_encoded)!r}")
    print(f"GENERATED_DECODE {generated.decode_shift(py_encoded)!r}")
    failures += decoded_code != code

    for claim, encoded, old in [
        ("loop-correct", "afz", 42),
        ("program-correct", "fgh", 0),
    ]:
        expected = canonical.decode_shift(encoded)
        generated_result = generated.decode_shift(encoded)
        print(f"CLAIM {claim}")
        if claim == "loop-correct":
            print(
                "SATISFYING_STATE "
                f"<k> comp(\"ch\", DECODE_EXPR, {chars_term(encoded)}) ~> .K </k> "
                f"<ch> {old} </ch>"
            )
        else:
            print(
                "SATISFYING_STATE "
                f"<k> SUBMITTED_MODULE </k> <s> nil </s> <ch> 0 </ch> "
                f"<input> {chars_term(encoded)} </input> <result> .K </result>"
            )
        print(f"PRECONDITION allLower({chars_term(encoded)})=true")
        print(f"SUBSTITUTED_RESULT_CODES {[ord(char) for char in expected]}")
        print(f"CANONICAL_RESULT {expected!r}")
        print(f"GENERATED_RESULT {generated_result!r}")
        status, k_codes, k_output = run_k(program, definition, encoded)
        print(f"K_RESULT_CODES {k_codes}")
        expected_codes = [ord(char) for char in expected]
        match = status == 0 and expected == generated_result and k_codes == expected_codes
        print(f"THREE_WAY_MATCH {str(match).lower()}")
        if not match:
            failures += 1
            print("K_STDOUT")
            print(k_output)

    print(f"FAILURE_COUNT {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
