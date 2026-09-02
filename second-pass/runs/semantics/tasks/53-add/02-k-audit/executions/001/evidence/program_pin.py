#!/usr/bin/env python3
"""Check that verification.k's #loadAll argument is the submitted MPY AST."""

from pathlib import Path


WORK = Path("/tmp/audit-work/53-add")


def normalized(text: str) -> str:
    return "".join(text.split())


def extract_loadall_argument(text: str) -> str:
    marker = "#loadAll("
    marker_at = text.index(marker)
    start = marker_at + len(marker)
    depth = 1
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
                return text[start:index]
    raise ValueError("unbalanced #loadAll argument")


submitted = (WORK / "solution.mpy").read_text(encoding="utf-8")
verification = (WORK / "verification.k").read_text(encoding="utf-8")
embedded = extract_loadall_argument(verification)

print(f"submitted_normalized={normalized(submitted)}")
print(f"embedded_normalized={normalized(embedded)}")
print(f"normalized_byte_sequence_equal={normalized(submitted) == normalized(embedded)}")
raise SystemExit(0 if normalized(submitted) == normalized(embedded) else 1)
