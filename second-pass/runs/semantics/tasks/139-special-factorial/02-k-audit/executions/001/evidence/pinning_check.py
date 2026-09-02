#!/usr/bin/env python3
"""Check that the function constructor in spec.k is the submitted MPY function."""

from __future__ import annotations

import hashlib
from pathlib import Path


def balanced_call(text: str, constructor: str) -> str:
    start = text.index(constructor + "(")
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
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
                return text[start : index + 1]
    raise ValueError(f"unterminated {constructor} call")


def normalize(text: str) -> str:
    return "".join(text.split())


def main() -> int:
    task = Path("/tmp/audit-work/139-special-factorial")
    submitted_text = (task / "solution.mpy").read_text()
    spec_text = (task / "spec.k").read_text()
    submitted_function = normalize(balanced_call(submitted_text, "FuncDef"))
    claimed_function = normalize(balanced_call(spec_text, "FuncDef"))
    submitted_digest = hashlib.sha256(submitted_function.encode()).hexdigest()
    claimed_digest = hashlib.sha256(claimed_function.encode()).hexdigest()
    submitted_count = normalize(submitted_text).count("FuncDef(")
    spec_count = normalize(spec_text).count("FuncDef(")
    print(f"submitted_funcdef_count={submitted_count}")
    print(f"spec_funcdef_count={spec_count}")
    print(f"submitted_function_sha256={submitted_digest}")
    print(f"claimed_function_sha256={claimed_digest}")
    print(f"function_constructor_byte_equal_after_whitespace={submitted_function == claimed_function}")
    return 0 if submitted_count == 1 and spec_count == 1 and submitted_function == claimed_function else 1


if __name__ == "__main__":
    raise SystemExit(main())
