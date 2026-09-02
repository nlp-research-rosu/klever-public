#!/usr/bin/env python3
"""Token-level pinning check between solution.mpy and solutionProgram."""

from pathlib import Path


def strip_k_whitespace(text: str) -> str:
    out = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            out.append(char)
        elif not char.isspace():
            out.append(char)
    if in_string:
        raise ValueError("unterminated string")
    return "".join(out)


def balanced_module_term(text: str) -> str:
    marker = "rule solutionProgram =>"
    start = text.index("Module(", text.index(marker))
    depth = 0
    in_string = False
    escaped = False
    for pos in range(start, len(text)):
        char = text[pos]
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
                return text[start : pos + 1]
    raise ValueError("unbalanced Module term")


root = Path("/tmp/audit-work/review-57")
submitted = (root / "src/solution.mpy").read_text()
regenerated = (root / "build/solution.trusted-regenerated.mpy").read_text()
verification = (root / "src/verification.k").read_text()
embedded = balanced_module_term(verification)

submitted_tokens = strip_k_whitespace(submitted)
regenerated_tokens = strip_k_whitespace(regenerated)
embedded_tokens = strip_k_whitespace(embedded)

print(f"SUBMITTED_TOKEN_CHARS: {len(submitted_tokens)}")
print(f"REGENERATED_TOKEN_CHARS: {len(regenerated_tokens)}")
print(f"EMBEDDED_TOKEN_CHARS: {len(embedded_tokens)}")
print(f"SUBMITTED_EQUALS_REGENERATED: {submitted_tokens == regenerated_tokens}")
print(f"SUBMITTED_EQUALS_EMBEDDED: {submitted_tokens == embedded_tokens}")

if submitted_tokens != regenerated_tokens:
    raise AssertionError("submitted solution.mpy differs from trusted regeneration")
if submitted_tokens != embedded_tokens:
    raise AssertionError("solutionProgram differs from submitted solution.mpy")
