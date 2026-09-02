#!/usr/bin/env python3
"""Extract the translated FuncDef body and emit a proof-local identity claim."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


SOURCE = Path("/tmp/audit-work/repro/regenerated-solution.mpy")
OUTPUT = Path("/tmp/audit-work/repro/spec-body-identity.k")


def matching_paren(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("unbalanced parentheses")


def top_level_commas(text: str) -> list[int]:
    depth = 0
    quoted = False
    escaped = False
    result: list[int] = []
    for index, char in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            result.append(index)
    return result


def main() -> None:
    translated = SOURCE.read_text()
    func_start = translated.index("FuncDef(")
    opening = translated.index("(", func_start)
    closing = matching_paren(translated, opening)
    arguments = translated[opening + 1 : closing]
    commas = top_level_commas(arguments)
    if len(commas) != 2:
        raise ValueError(f"expected three FuncDef arguments, got commas={commas}")
    body = arguments[commas[1] + 1 :].strip()
    # The external MPY parser accepts an omitted Stmts list in constructor
    # argument position; K source claims spell that same identity explicitly.
    body, explicit_empty_count = re.subn(r",\s*\)", ", .Stmts)", body)
    body_hash = hashlib.sha256("".join(body.split()).encode()).hexdigest()
    spec = (
        'requires "verification.k"\n\n'
        "module BODY-IDENTITY\n"
        "  imports VERIFICATION\n\n"
        "  claim [translated-body-identity]:\n"
        f"    <k> findMaxFunctionBody => {body} </k>\n"
        "endmodule\n"
    )
    OUTPUT.write_text(spec)
    print("COMMAND: python3 /audit-output/evidence/make_body_identity_spec.py")
    print(f"source={SOURCE}")
    print(f"output={OUTPUT}")
    print(f"extracted_body_normalized_sha256={body_hash}")
    print(f"extracted_body_chars={len(body)}")
    print(f"omitted_empty_stmts_normalized={explicit_empty_count}")
    print("--- generated spec ---")
    print(spec, end="")


if __name__ == "__main__":
    main()
