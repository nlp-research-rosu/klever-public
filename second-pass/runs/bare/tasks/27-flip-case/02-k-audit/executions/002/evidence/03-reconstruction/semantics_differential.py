#!/usr/bin/env python3
"""Compare fresh concrete K execution with independent CPython execution."""

from __future__ import annotations

import ast
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")
DEFINITION = WORK / (sys.argv[1] if len(sys.argv) > 1 else "concrete-kompiled")
PROGRAM = WORK / "solution.mpy"


def load_solution(path: Path):
    spec = importlib.util.spec_from_file_location("candidate_solution_kdiff", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


def k_string(value: str) -> str:
    parts = ['"']
    for byte in value.encode("utf-8", "surrogatepass"):
        if 0x20 <= byte <= 0x7E and byte not in (0x22, 0x5C):
            parts.append(chr(byte))
        elif byte == 0x22:
            parts.append(r"\"")
        elif byte == 0x5C:
            parts.append(r"\\")
        else:
            parts.append(rf"\x{byte:02x}")
    parts.append('"')
    return "".join(parts)


def parse_k_string(literal: str) -> str:
    byte_characters = ast.literal_eval(literal)
    return bytes(ord(character) for character in byte_characters).decode(
        "utf-8", "surrogatepass"
    )


cases = [
    "",
    "Hello",
    "aAzZ@[`{",
    "\x00\n\t\"\\",
    "\x7f\x80\xff",
    "Straße Δelta",
    "ß",
    "İ",
    "ﬃ",
    "\u07ff\u0800\uffff",
    "\U00010400\U00010428",
    "\U0010ffff",
    "\ud800\udfff",
]
solution = load_solution(WORK / "solution.py")
mismatches = []

for value in cases:
    argument = k_string(value)
    command = [
        "krun",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        "-cARG=" + argument,
    ]
    result = subprocess.run(
        command, cwd=WORK, text=True, capture_output=True, check=False
    )
    match = re.search(
        r"<k>\s*strVal\s*\(\s*(\"(?:\\.|[^\"\\])*\")\s*\)\s*~>\s*\.K\s*</k>",
        result.stdout,
    )
    if result.returncode != 0 or match is None:
        print("EXECUTION_ERROR", json.dumps(value, ensure_ascii=True))
        print("command", json.dumps(command))
        print("exit", result.returncode)
        print("stdout", result.stdout)
        print("stderr", result.stderr)
        raise SystemExit(2)
    actual = parse_k_string(match.group(1))
    expected = solution(value)
    print(
        "case",
        json.dumps(value, ensure_ascii=True),
        "k_result",
        json.dumps(actual, ensure_ascii=True),
        "python_result",
        json.dumps(expected, ensure_ascii=True),
        "match",
        actual == expected,
    )
    if actual != expected:
        mismatches.append((value, expected, actual))

print("definition", DEFINITION)
print("program", PROGRAM)
print("case_count", len(cases))
print("mismatch_count", len(mismatches))
raise SystemExit(1 if mismatches else 0)
