#!/usr/bin/env python3
"""Compare the translated Module term with the entry claim's #loadAll argument."""

from __future__ import annotations

import hashlib
from pathlib import Path


MPY = Path("/tmp/audit-work/solution.mpy")
SPEC = Path("/tmp/audit-work/spec.k")
ENTRY_MODULE = Path("/tmp/audit-work/entry-claim-module.mpy")
ENTRY_PROGRAM_MODULE = Path("/tmp/audit-work/entry-claim-module-program.mpy")


def balanced_call(text: str, marker: str, start: int = 0) -> str:
    marker_at = text.index(marker, start)
    open_at = text.index("(", marker_at + len(marker) - 1)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_at, len(text)):
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
                return text[marker_at : index + 1]
    raise ValueError(f"unterminated call at {marker!r}")


def normalize(text: str) -> str:
    result: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            result.append(char)
        elif not char.isspace():
            result.append(char)
    return "".join(result)


def sha(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def main() -> int:
    submitted = MPY.read_text(encoding="utf-8").strip()
    spec = SPEC.read_text(encoding="utf-8")
    loaded = balanced_call(spec, "Module(", spec.index("claim [sum-product]"))
    normalized_submitted = normalize(submitted)
    normalized_loaded = normalize(loaded)
    module_equal = normalized_submitted == normalized_loaded
    ENTRY_MODULE.write_text(loaded + "\n", encoding="utf-8")
    # `.Stmts` and `.Exprs` are explicit associative-list units accepted in K
    # rule syntax.  Program syntax omits these units, yielding the same term.
    program_form = loaded.replace(", .Exprs", "").replace(".Stmts", "")
    ENTRY_PROGRAM_MODULE.write_text(program_form + "\n", encoding="utf-8")

    submitted_for = balanced_call(submitted, "For(")
    loaded_for = balanced_call(loaded, "For(")
    for_equal = normalize(submitted_for) == normalize(loaded_for)
    submitted_return = balanced_call(submitted, "Return(")
    loaded_return = balanced_call(loaded, "Return(")
    return_equal = normalize(submitted_return) == normalize(loaded_return)

    print(f"submitted_module_sha256_normalized={sha(normalized_submitted)}")
    print(f"entry_loaded_module_sha256_normalized={sha(normalized_loaded)}")
    print(f"raw_text_equal_after_whitespace_removal={str(module_equal).lower()}")
    print(f"raw_for_equal_after_whitespace_removal={str(for_equal).lower()}")
    print(f"raw_return_equal_after_whitespace_removal={str(return_equal).lower()}")
    print("raw differences are explicit .Stmts/.Exprs list terminator sugar; K parser identity is checked separately")
    print(f"extracted_entry_module={ENTRY_MODULE}")
    print(f"program_syntax_entry_module={ENTRY_PROGRAM_MODULE}")
    program_form_equal = normalize(submitted) == normalize(program_form)
    print(f"entry_equal_after_eliding_associative_list_units={str(program_form_equal).lower()}")
    return 0 if program_form_equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
