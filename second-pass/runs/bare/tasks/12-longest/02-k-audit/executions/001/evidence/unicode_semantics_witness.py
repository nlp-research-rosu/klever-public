#!/usr/bin/env python3
"""Concrete false-conclusion witnesses for semantic.k:134."""

from __future__ import annotations

import importlib.util
import json
import shlex
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/12-longest-audit")
DEFINITIONS = [
    WORK / "semantic-concrete-search-kompiled",
    WORK / "verification-fresh-kompiled",
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.longest


def q(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def kval(strings: list[str]) -> str:
    return "listVal(" + ",".join(f"strVal({q(s)})" for s in strings) + ")"


def k_utf8_bytes(s: str) -> str:
    """K's displayed byte-string spelling for a Python Unicode value."""
    pieces = []
    for byte in s.encode("utf-8"):
        if 0x20 <= byte <= 0x7E and byte not in (0x22, 0x5C):
            pieces.append(chr(byte))
        elif byte == 0x22:
            pieces.append('\\"')
        elif byte == 0x5C:
            pieces.append("\\\\")
        else:
            pieces.append(f"\\x{byte:02x}")
    return '"' + "".join(pieces) + '"'


def run_pattern(
    definition: Path,
    strings: list[str],
    expected: str,
    *,
    byte_spelling: bool = False,
) -> tuple[int, str]:
    literal = k_utf8_bytes(expected) if byte_spelling else q(expected)
    command = [
        "krun",
        "solution.mpy",
        "--definition",
        str(definition),
        "-cARGS=" + kval(strings),
        "--pattern",
        f"<out> strVal({literal}) </out>",
        "--output",
        "pretty",
    ]
    print("$ " + shlex.join(command))
    result = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    print(result.stdout, end="")
    print(f"KRUN_EXIT_STATUS={result.returncode}")
    return result.returncode, result.stdout.strip()


canonical = load(WORK / "canonical.py", "trusted_unicode_oracle")
candidate = load(WORK / "solution.py", "unicode_subject")

witnesses = [
    (["😀", "aa"], "aa", "😀"),
    (["😀😀", "abc"], "abc", "😀😀"),
]

for strings, python_expected, k_wrong in witnesses:
    c = canonical(strings)
    s = candidate(strings)
    print(f"INPUT={strings!r}")
    print(f"PYTHON_LENGTHS={[len(x) for x in strings]!r}")
    print(f"CANONICAL={c!r} CANDIDATE={s!r}")
    assert c == s == python_expected

    for definition in DEFINITIONS:
        print(f"DEFINITION={definition}")
        expected_status, expected_output = run_pattern(
            definition, strings, python_expected
        )
        wrong_status, wrong_output = run_pattern(
            definition, strings, k_wrong, byte_spelling=True
        )
        assert expected_status == 0 and expected_output == "#Bottom"
        assert wrong_status == 0 and wrong_output == "#Top"
        print("FALSE_CONCLUSION_WITNESS=CONFIRMED")

print("WITNESS_SCRIPT_RESULT=PASS")
