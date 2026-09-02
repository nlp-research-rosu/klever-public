#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with independent Python."""

from __future__ import annotations

import importlib.util
import ast
import re
import subprocess
import sys
from pathlib import Path


sys.dont_write_bytecode = True
WORK = Path("/tmp/audit-work/candidate")
DEFINITION = WORK / "fresh-execution-kompiled"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("canonical_for_k_check", Path("/reference/canonical.py"))
candidate = load_module("candidate_for_k_check", WORK / "solution.py")

RESULT_RE = re.compile(
    r'<result>\s*strVal \( (?P<literal>"[^"]*") \) ~> \.K\s*</result>',
    re.DOTALL,
)


def k_string_literal(value: str) -> str:
    pieces = ['"']
    named_escapes = {
        "\\": "\\\\",
        '"': '\\"',
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
        "\f": "\\f",
    }
    for character in value:
        if character in named_escapes:
            pieces.append(named_escapes[character])
            continue
        code_point = ord(character)
        if 0x20 <= code_point <= 0x7E:
            pieces.append(character)
        elif code_point <= 0xFF:
            pieces.append(f"\\x{code_point:02x}")
        elif code_point <= 0xFFFF:
            pieces.append(f"\\u{code_point:04x}")
        else:
            pieces.append(f"\\U{code_point:08x}")
    pieces.append('"')
    return "".join(pieces)


def run_k(value: str) -> tuple[str, str]:
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        f"-cINPUT={k_string_literal(value)}",
        "--color",
        "off",
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )
    if completed.returncode != 0:
        return ("krun-error", f"exit={completed.returncode}\n{completed.stdout[-2000:]}")
    match = RESULT_RE.search(completed.stdout)
    if match is None:
        return ("parse-error", completed.stdout[-2000:])
    # K's \x, \u, and \U escapes denote code points, matching Python's literal
    # evaluator for the forms emitted by the K pretty-printer.
    return ("return", ast.literal_eval(match.group("literal")))


cases = [
    "",
    "a",
    "aa",
    "ab",
    "cat",
    "cata",
    "aabb",
    "abc",
    "é",
    "λ漢🙂",
    "".join(chr(0x400 + index) for index in range(32)),
]

failures = 0
ascii_failures = 0
non_ascii_failures = 0
for value in cases:
    expected = canonical.make_palindrome(value)
    generated_python = candidate.make_palindrome(value)
    k_outcome = run_k(value)
    expected_outcome = ("return", expected)
    matches = k_outcome == expected_outcome and generated_python == expected
    failures += not matches
    if not matches:
        if value.isascii():
            ascii_failures += 1
        else:
            non_ascii_failures += 1
    rendered_value = (
        repr(value)
        if len(value) <= 20
        else f"<{len(value)} distinct Unicode code points>"
    )
    print(
        f"input={rendered_value} expected={expected!r} "
        f"generated_python={generated_python!r} k={k_outcome!r} "
        f"match={str(matches).lower()}"
    )

print(f"cases={len(cases)}")
print(f"mismatches={failures}")
print(f"ascii_mismatches={ascii_failures}")
print(f"non_ascii_mismatches={non_ascii_failures}")
print(
    "ASCII_CONCRETE_SEMANTICS_CHECK="
    f"{'PASS' if ascii_failures == 0 else 'FAIL'}"
)
print(
    "KRUN_UNICODE_CONFIG_BRIDGE_CHECK="
    f"{'PASS' if non_ascii_failures == 0 else 'FAIL'}"
)
raise SystemExit(0 if failures == 0 else 1)
