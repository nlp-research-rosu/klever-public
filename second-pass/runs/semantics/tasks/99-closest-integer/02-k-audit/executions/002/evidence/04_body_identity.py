#!/usr/bin/env python3
"""Mechanical token-level constructor comparison of .mpy and executed K body."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


mpy = Path("/tmp/audit-work/candidate-src/solution.regenerated.mpy").read_text()
verification = Path("/tmp/audit-work/candidate-src/verification.k").read_text()

prefix = 'Module(\n  FuncDef("closest_integer", Params("value"),\n'
assert mpy.startswith(prefix)
assert mpy.endswith("))\n")
translated_body = mpy[len(prefix) : -3]

match = re.search(
    r"rule\s+closestBody\(\)\s*=>\s*(.*?)"
    r"\n\s*// Execute the body",
    verification,
    flags=re.DOTALL,
)
assert match is not None
executed_body = match.group(1).strip()

token_pattern = re.compile(
    r'"(?:\\.|[^"\\])*"|'
    r"\.Stmts|"
    r"[A-Za-z_#][A-Za-z0-9_#-]*|"
    r"-?[0-9]+(?:\.[0-9]+)?|"
    r"[(),]"
)


def normalized_tokens(text: str) -> list[str]:
    # `.Stmts` is the explicit spelling of the same empty List{Stmt,""}
    # that the translator renders as a blank list argument.
    tokens = token_pattern.findall(text)
    return [token for token in tokens if token != ".Stmts"]


translated_tokens = normalized_tokens(translated_body)
executed_tokens = normalized_tokens(executed_body)
translated_hash = hashlib.sha256(
    "\0".join(translated_tokens).encode()
).hexdigest()
executed_hash = hashlib.sha256("\0".join(executed_tokens).encode()).hexdigest()

print(f"translated_token_count={len(translated_tokens)}")
print(f"executed_token_count={len(executed_tokens)}")
print(f"translated_constructor_sha256={translated_hash}")
print(f"executed_constructor_sha256={executed_hash}")
print(f"constructor_identity={translated_tokens == executed_tokens}")
if translated_tokens != executed_tokens:
    for index, (left, right) in enumerate(zip(translated_tokens, executed_tokens)):
        if left != right:
            print(f"first_difference={index}: translated={left!r} executed={right!r}")
            break
    raise SystemExit(1)
