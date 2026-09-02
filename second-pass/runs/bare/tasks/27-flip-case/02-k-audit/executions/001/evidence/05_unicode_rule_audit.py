#!/usr/bin/env python3
"""Exhaustively compare unicode-case.k equations with this CPython runtime."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
import sys
import unicodedata


RULE = re.compile(r'^\s*rule pySwapChar\(("(?:[^"\\]|\\.)*")\) => ("(?:[^"\\]|\\.)*")\s*$')
OWISE = "rule pySwapChar(C) => C [owise]"


def decode_k_bytes(token: str) -> bytes:
    if not (token.startswith('"') and token.endswith('"')):
        raise ValueError(token)
    text = token[1:-1]
    output = bytearray()
    index = 0
    while index < len(text):
        char = text[index]
        if char != "\\":
            codepoint = ord(char)
            if codepoint > 0x7F:
                raise ValueError(f"unexpected raw non-ASCII in {token}")
            output.append(codepoint)
            index += 1
            continue
        index += 1
        escape = text[index]
        if escape == "x":
            output.append(int(text[index + 1:index + 3], 16))
            index += 3
        elif escape == '"':
            output.append(ord('"'))
            index += 1
        elif escape == "\\":
            output.append(ord("\\"))
            index += 1
        elif escape == "n":
            output.append(0x0A)
            index += 1
        elif escape == "r":
            output.append(0x0D)
            index += 1
        elif escape == "t":
            output.append(0x09)
            index += 1
        else:
            raise ValueError(f"unsupported escape \\{escape} in {token}")
    return bytes(output)


path = Path("/tmp/audit-work/candidate-src/unicode-case.k")
actual: dict[bytes, tuple[bytes, int]] = {}
duplicates: list[tuple[bytes, int, int]] = []
unparsed_rule_lines: list[tuple[int, str]] = []
owise_lines: list[int] = []

for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
    match = RULE.match(line)
    if match:
        lhs = decode_k_bytes(match.group(1))
        rhs = decode_k_bytes(match.group(2))
        if lhs in actual:
            duplicates.append((lhs, actual[lhs][1], line_number))
        actual[lhs] = (rhs, line_number)
    elif line.strip() == OWISE:
        owise_lines.append(line_number)
    elif line.lstrip().startswith("rule "):
        unparsed_rule_lines.append((line_number, line))

expected: dict[bytes, bytes] = {}
for codepoint in range(sys.maxunicode + 1):
    char = chr(codepoint)
    swapped = char.swapcase()
    if swapped != char:
        expected[char.encode("utf-8")] = swapped.encode("utf-8")

actual_simple = {lhs: value[0] for lhs, value in actual.items()}
missing = sorted(set(expected) - set(actual_simple))
extra = sorted(set(actual_simple) - set(expected))
wrong = sorted(
    lhs for lhs in set(expected) & set(actual_simple)
    if expected[lhs] != actual_simple[lhs]
)

lhs_widths = Counter(len(lhs) for lhs in actual_simple)
rhs_expansions = sum(
    1 for lhs, rhs in actual_simple.items()
    if len(rhs.decode("utf-8")) != 1
)

print(f"python={sys.version.split()[0]}")
print(f"unicode_database={unicodedata.unidata_version}")
print(f"explicit_rule_count={len(actual_simple)}")
print(f"expected_changed_codepoints={len(expected)}")
print(f"lhs_utf8_widths={dict(sorted(lhs_widths.items()))}")
print(f"multi_codepoint_rhs_count={rhs_expansions}")
print(f"owise_lines={owise_lines}")
print(f"duplicate_count={len(duplicates)}")
print(f"unparsed_rule_count={len(unparsed_rule_lines)}")
print(f"missing_count={len(missing)}")
print(f"extra_count={len(extra)}")
print(f"wrong_mapping_count={len(wrong)}")
if duplicates:
    print(f"first_duplicates={duplicates[:10]}")
if unparsed_rule_lines:
    print(f"first_unparsed={unparsed_rule_lines[:10]}")
if missing:
    print(f"first_missing={[x.hex() for x in missing[:10]]}")
if extra:
    print(f"first_extra={[x.hex() for x in extra[:10]]}")
if wrong:
    print(
        "first_wrong="
        + repr([
            (lhs.hex(), actual_simple[lhs].hex(), expected[lhs].hex())
            for lhs in wrong[:10]
        ])
    )

if (
    duplicates
    or unparsed_rule_lines
    or len(owise_lines) != 1
    or missing
    or extra
    or wrong
):
    raise SystemExit(1)
