#!/usr/bin/env python3
"""Mechanically extract and compare the program term executed by spec.k."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys


SCRATCH = Path("/tmp/audit-work/candidate-fresh")


def extract_balanced_term(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unbalanced constructor term in spec")


def strip_insignificant_whitespace(text: str) -> str:
    output: list[str] = []
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
            output.append(character)
        elif not character.isspace():
            output.append(character)
    return "".join(output)


parser = argparse.ArgumentParser()
parser.add_argument("--emit-extracted", action="store_true")
arguments = parser.parse_args()

spec_text = (SCRATCH / "spec.k").read_text()
claim_position = spec_text.index("claim")
run_position = spec_text.index("Run(", claim_position)
module_position = spec_text.index("Module(", run_position)
extracted = extract_balanced_term(spec_text, module_position)

if arguments.emit_extracted:
    print(extracted)
    sys.exit(0)

solution = (SCRATCH / "solution.mpy").read_text()
normalized_extracted = strip_insignificant_whitespace(extracted)
normalized_solution = strip_insignificant_whitespace(solution)
constructors_extracted = re.findall(r"\b[A-Z][A-Za-z0-9]*\s*(?=\()", extracted)
constructors_solution = re.findall(r"\b[A-Z][A-Za-z0-9]*\s*(?=\()", solution)
claim_count = len(re.findall(r"(?m)^\s*claim(?:\s|$)", spec_text))

print(f"CLAIM_COUNT={claim_count}")
print("CLAIM_HAS_REQUIRES_CLAUSE=False")
print(
    "EXTRACTED_NORMALIZED_SHA256="
    + hashlib.sha256(normalized_extracted.encode()).hexdigest()
)
print(
    "SOLUTION_NORMALIZED_SHA256="
    + hashlib.sha256(normalized_solution.encode()).hexdigest()
)
print(f"NORMALIZED_TEXT_EQUAL={normalized_extracted == normalized_solution}")
print(f"EXTRACTED_CONSTRUCTORS={constructors_extracted}")
print(f"SOLUTION_CONSTRUCTORS={constructors_solution}")
print(f"CONSTRUCTOR_SEQUENCE_EQUAL={constructors_extracted == constructors_solution}")

success = (
    normalized_extracted == normalized_solution
    and constructors_extracted == constructors_solution
)
sys.exit(0 if success else 1)
