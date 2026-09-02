#!/usr/bin/env python3
"""Run the freshly compiled generated semantics and compare Python oracles."""

from __future__ import annotations

import importlib.util
import ast
import json
import re
import subprocess
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fix_spaces


generated = load_entry(
    "generated_solution_for_krun", Path("/tmp/audit-work/candidate/solution.py")
)
canonical = load_entry(
    "trusted_canonical_for_krun", Path("/tmp/audit-work/reference/canonical.py")
)

cases = [
    "",
    "Example",
    "Example 1",
    " Example 2",
    " Example   3",
    " ",
    "  ",
    "   ",
    "    ",
    "a  ",
    "a   b  ",
    "é  😀",
]
definition = "/tmp/audit-work/build/semantic-kompiled"
program = "/tmp/audit-work/candidate/solution.mpy"
failures = 0


def decode_k_string(token: str) -> str:
    """Decode K's mixed code-point/UTF-8 \\xNN pretty-printing."""
    data = ast.literal_eval(token).encode("latin-1")
    decoded: list[str] = []
    index = 0
    while index < len(data):
        first = data[index]
        width = (
            2 if 0xC2 <= first <= 0xDF
            else 3 if 0xE0 <= first <= 0xEF
            else 4 if 0xF0 <= first <= 0xF4
            else 1
        )
        chunk = data[index:index + width]
        if width > 1 and len(chunk) == width and all(
            0x80 <= byte <= 0xBF for byte in chunk[1:]
        ):
            try:
                decoded.append(chunk.decode("utf-8"))
                index += width
                continue
            except UnicodeDecodeError:
                pass
        decoded.append(chr(first))
        index += 1
    return "".join(decoded)

for text in cases:
    input_term = json.dumps(text, ensure_ascii=False)
    command = [
        "krun",
        program,
        "--definition",
        definition,
        f"-cINPUT={input_term}",
    ]
    print(f"COMMAND_JSON={json.dumps(command, ensure_ascii=False)}")
    run = subprocess.run(command, text=True, capture_output=True)
    print(f"EXIT_STATUS={run.returncode}")
    print("STDOUT_BEGIN")
    print(run.stdout, end="")
    print("STDOUT_END")
    if run.stderr:
        print("STDERR_BEGIN")
        print(run.stderr, end="")
        print("STDERR_END")

    matches = re.findall(r'^\s*("(?:[^"\\]|\\.)*") ~> \.K\s*$', run.stdout, re.M)
    k_result = decode_k_string(matches[-1]) if matches else None
    generated_result = generated(text)
    canonical_result = canonical(text)
    print(
        "COMPARISON "
        f"input={text!r} k={k_result!r} generated={generated_result!r} "
        f"canonical={canonical_result!r} "
        f"k_matches_generated={k_result == generated_result} "
        f"k_matches_canonical={k_result == canonical_result}"
    )
    if run.returncode != 0 or k_result != generated_result:
        failures += 1

print(f"case_count={len(cases)}")
print(f"k_vs_generated_failure_count={failures}")
raise SystemExit(1 if failures else 0)
