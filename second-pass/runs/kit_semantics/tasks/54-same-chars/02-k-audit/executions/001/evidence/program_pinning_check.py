#!/usr/bin/env python3
"""Mechanical constructor comparison between solution.mpy and SPEC's program."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/54-same-chars")
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_#][A-Za-z0-9_#-]*|-?[0-9]+|[(),.]')


def tokens(path: Path) -> list[str]:
    return TOKEN.findall(path.read_text())


def constructor_subtree(stream: list[str], constructor: str) -> list[str]:
    start = stream.index(constructor)
    if stream[start + 1] != "(":
        raise AssertionError(f"{constructor} not followed by '('")
    depth = 0
    for end in range(start + 1, len(stream)):
        if stream[end] == "(":
            depth += 1
        elif stream[end] == ")":
            depth -= 1
            if depth == 0:
                return stream[start : end + 1]
    raise AssertionError(f"unterminated {constructor}")


mpy_tokens = tokens(SCRATCH / "solution.mpy")
spec_tokens = tokens(SCRATCH / "spec.k")
mpy_function = constructor_subtree(mpy_tokens, "FuncDef")
spec_function = constructor_subtree(spec_tokens, "FuncDef")

mpy_serialized = "\0".join(mpy_function).encode()
spec_serialized = "\0".join(spec_function).encode()
equal = mpy_function == spec_function

print(f"solution_mpy_token_count={len(mpy_tokens)}")
print(f"solution_funcdef_token_count={len(mpy_function)}")
print(f"spec_first_funcdef_token_count={len(spec_function)}")
print(f"solution_funcdef_sha256={hashlib.sha256(mpy_serialized).hexdigest()}")
print(f"spec_funcdef_sha256={hashlib.sha256(spec_serialized).hexdigest()}")
print(f"funcdef_constructor_identity={equal}")
print(f"spec_begins_execution_at_load_all={'#loadAll' in spec_tokens}")
print(
    "spec_calls_loaded_same_chars="
    + str(
        'Call' in spec_tokens
        and '"same_chars"' in spec_tokens
        and '"result"' in spec_tokens
    )
)
if not equal:
    for index, pair in enumerate(zip(mpy_function, spec_function)):
        if pair[0] != pair[1]:
            print(f"first_difference_index={index} solution={pair[0]!r} spec={pair[1]!r}")
            break
    raise SystemExit(1)
