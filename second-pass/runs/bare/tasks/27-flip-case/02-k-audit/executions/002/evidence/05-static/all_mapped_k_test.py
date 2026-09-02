#!/usr/bin/env python3
"""Exercise every non-identity CPython swapcase mapping in one Haskell krun."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate")
value = "".join(
    chr(codepoint)
    for codepoint in range(0x110000)
    if chr(codepoint).swapcase() != chr(codepoint)
)
expected = value.swapcase()


def k_string(text: str) -> str:
    parts = ['"']
    for byte in text.encode("utf-8"):
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


command = [
    "krun",
    str(WORK / "solution.mpy"),
    "--definition",
    str(WORK / "proof-kompiled"),
    "-cARG=" + k_string(value),
]
result = subprocess.run(
    command, cwd=WORK, text=True, capture_output=True, check=False
)
match = re.search(
    r"<k>\s*strVal\s*\(\s*(\"(?:\\.|[^\"\\])*\")\s*\)\s*~>\s*\.K\s*</k>",
    result.stdout,
)
print("command_argv_prefix", json.dumps(command[:5]))
print("argument_character_count", len(value))
print("argument_utf8_byte_count", len(value.encode("utf-8")))
print("argument_sha256", hashlib.sha256(value.encode("utf-8")).hexdigest())
print("expected_utf8_byte_count", len(expected.encode("utf-8")))
print("expected_sha256", hashlib.sha256(expected.encode("utf-8")).hexdigest())
print("krun_exit_status", result.returncode)
if result.returncode != 0 or match is None:
    print("parse_match", match is not None)
    print("stdout_prefix", result.stdout[:2000])
    print("stderr_prefix", result.stderr[:2000])
    raise SystemExit(2)
byte_chars = ast.literal_eval(match.group(1))
actual = bytes(ord(character) for character in byte_chars).decode("utf-8")
print("actual_utf8_byte_count", len(actual.encode("utf-8")))
print("actual_sha256", hashlib.sha256(actual.encode("utf-8")).hexdigest())
print("matches_python", actual == expected)
raise SystemExit(0 if actual == expected else 1)
