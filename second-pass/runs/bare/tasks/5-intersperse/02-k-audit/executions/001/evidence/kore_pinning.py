#!/usr/bin/env python3
"""Compare the parsed submitted Pgm with the parsed Pgm embedded in SPEC KORE."""

from pathlib import Path


def extract_application(text: str, label_prefix: str) -> str:
    start = text.index(label_prefix)
    opening = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
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
                return text[start : index + 1]
    raise ValueError(f"unbalanced KORE application for {label_prefix}")


submitted = Path("/audit-output/evidence/submitted-program.kore").read_text(
    encoding="utf-8"
).strip()
spec_kore = Path("/audit-output/evidence/spec-dry-run.kore").read_text(
    encoding="utf-8"
)
embedded = extract_application(spec_kore, "LblModule'LParUndsRParUnds'")

print(f"submitted_parsed_program_chars={len(submitted)}")
print(f"spec_embedded_parsed_program_chars={len(embedded)}")
print(f"parsed_program_terms_byte_identical={submitted == embedded}")
if submitted != embedded:
    raise SystemExit(1)
