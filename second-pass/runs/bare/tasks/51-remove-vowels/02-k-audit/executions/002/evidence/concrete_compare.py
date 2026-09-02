#!/usr/bin/env python3
"""Compare fresh Haskell-backend K execution with both Python functions."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import subprocess


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_vowels


oracle = load_function(Path("/reference/canonical.py"), "concrete_oracle")
candidate = load_function(
    Path("/tmp/audit-work/candidate/solution.py"), "concrete_candidate"
)
work = Path("/tmp/audit-work/candidate")
definition = work / "semantic-haskell-kompiled"

cases = [
    "",
    "a",
    "A",
    "b",
    "U",
    "AEIOUaeiou",
    "bAEIOUaeiouz",
    "abcdef\nghijklm",
    "abcdef",
    "aaaaa",
    "aaBAA",
    "zbcd",
    "\n\t\r\0",
    "café naïve résumé",
    "İıſK",
    "a\u0301e\u0301i\u0301o\u0301u\u0301",
    "😀A🚀e終",
    ("AEIOUaeiouxyz" * 64),
]

result_pattern = re.compile(
    r'<result>\s*result\s*\(\s*("(?:\\.|[^"\\])*")\s*\)\s*</result>',
    re.DOTALL,
)


def k_string_literal(value: str) -> str:
    rendered: list[str] = ['"']
    named = {
        0x09: r"\t",
        0x0A: r"\n",
        0x0D: r"\r",
        0x22: r"\"",
        0x5C: r"\\",
    }
    for byte in value.encode("utf-8"):
        if byte in named:
            rendered.append(named[byte])
        elif 0x20 <= byte <= 0x7E:
            rendered.append(chr(byte))
        else:
            rendered.append(f"\\x{byte:02x}")
    rendered.append('"')
    return "".join(rendered)


def decode_k_string(token: str) -> str:
    body = token[1:-1]
    result = bytearray()
    index = 0
    named = {
        "t": 0x09,
        "n": 0x0A,
        "r": 0x0D,
        '"': 0x22,
        "\\": 0x5C,
    }
    while index < len(body):
        if body[index] != "\\":
            result.extend(body[index].encode("ascii"))
            index += 1
        elif body[index + 1] == "x":
            result.append(int(body[index + 2:index + 4], 16))
            index += 4
        else:
            result.append(named[body[index + 1]])
            index += 2
    return result.decode("utf-8")


mismatches = 0
for index, value in enumerate(cases):
    literal = k_string_literal(value)
    command = [
        "krun",
        "solution.mpy",
        f"-cINPUT={literal}",
        "--definition",
        str(definition),
    ]
    completed = subprocess.run(
        command,
        cwd=work,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        print(
            f"case={index} input={value!r} krun_exit={completed.returncode} "
            f"stderr={completed.stderr!r}"
        )
        mismatches += 1
        continue
    match = result_pattern.search(completed.stdout)
    if match is None:
        print(f"case={index} input={value!r} UNPARSED output={completed.stdout!r}")
        mismatches += 1
        continue
    k_value = decode_k_string(match.group(1))
    oracle_value = oracle(value)
    candidate_value = candidate(value)
    equal = k_value == oracle_value == candidate_value
    print(
        f"case={index} input={value!r} k={k_value!r} "
        f"oracle={oracle_value!r} candidate={candidate_value!r} equal={equal}"
    )
    if not equal:
        mismatches += 1

print(f"cases={len(cases)} mismatches={mismatches}")
raise SystemExit(1 if mismatches else 0)
