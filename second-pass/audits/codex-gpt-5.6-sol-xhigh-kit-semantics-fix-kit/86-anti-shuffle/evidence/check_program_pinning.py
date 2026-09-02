#!/usr/bin/env python3
"""Check that the entry claim embeds the submitted Module term exactly."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path("/tmp/audit-work/86-anti-shuffle")


def strip_k_whitespace(text: str) -> str:
    result: list[str] = []
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            result.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            result.append(character)
            in_string = True
        elif not character.isspace():
            result.append(character)
    if in_string:
        raise ValueError("unterminated string")
    return "".join(result)


def balanced_term(text: str, start: int) -> str:
    open_parenthesis = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_parenthesis, len(text)):
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
    raise ValueError("unbalanced term")


def main() -> int:
    submitted = (ROOT / "solution.mpy").read_text()
    spec = (ROOT / "spec.k").read_text()
    entry_module_start = spec.index("Module(", spec.index("module SPEC-ENTRY"))
    embedded = balanced_term(spec, entry_module_start)
    (ROOT / "entry-embedded.mpy").write_text(embedded + "\n")
    (ROOT / "entry-embedded-program-surface.mpy").write_text(
        embedded.replace(".Stmts", "") + "\n"
    )
    normalized_submitted = strip_k_whitespace(submitted)
    normalized_embedded = strip_k_whitespace(embedded)
    print(f"submitted_normalized_sha256={hashlib.sha256(normalized_submitted.encode()).hexdigest()}")
    print(f"embedded_normalized_sha256={hashlib.sha256(normalized_embedded.encode()).hexdigest()}")
    print(f"entry_surface_normalization_equal={normalized_submitted == normalized_embedded}")
    if normalized_submitted != normalized_embedded:
        mismatch = next(
            index
            for index, (left, right) in enumerate(
                zip(normalized_submitted, normalized_embedded, strict=False)
            )
            if left != right
        )
        print(f"first_surface_mismatch_offset={mismatch}")
        print(f"submitted_context={normalized_submitted[max(0, mismatch-40):mismatch+80]!r}")
        print(f"embedded_context={normalized_embedded[max(0, mismatch-40):mismatch+80]!r}")

    required_shapes = {
        "insert_for": "For(Name(\"current\"),Name(\"word\"),If(",
        "outer_for": "For(Name(\"char\"),Name(\"s\"),If(",
        "helper_loop_head": "#loop(str(SUFFIX:IntSeq),Name(\"current\"),If(",
        "outer_loop_head": "#loop(str(REM:IntSeq),Name(\"char\"),If(",
        "target_call": "Call(Name(\"anti_shuffle\"),str(CODES:IntSeq))",
        "target_result": "str(antiFinish(.IntSeq,.IntSeq,CODES))",
    }
    normalized_spec = strip_k_whitespace(spec)
    for name, shape in required_shapes.items():
        present = strip_k_whitespace(shape) in normalized_spec
        print(f"shape_{name}={present}")
        if not present:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
