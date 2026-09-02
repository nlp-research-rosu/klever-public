#!/usr/bin/env python3
"""Mechanical constructor pinning plus concrete witnesses for the entry claim."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def compact_k(text: str) -> str:
    """Remove comments and whitespace outside quoted K String tokens."""
    out: list[str] = []
    quoted = False
    escaped = False
    in_comment = False
    i = 0
    while i < len(text):
        ch = text[i]
        if in_comment:
            if ch == "\n":
                in_comment = False
            i += 1
            continue
        if quoted:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
        elif ch == "/" and i + 1 < len(text) and text[i + 1] == "/":
            in_comment = True
            i += 1
        elif ch == '"':
            quoted = True
            out.append(ch)
        elif not ch.isspace():
            out.append(ch)
        i += 1
    return "".join(out)


def balanced_argument(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    depth = 1
    quoted = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
        elif ch == '"':
            quoted = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start:i]
    raise ValueError(f"unbalanced marker {marker!r}")


submitted = compact_k((ROOT / "solution.mpy").read_text())
verification = compact_k((ROOT / "verification.k").read_text())
executed_module = balanced_argument(verification, "#loadAll(")
pin_ok = submitted == executed_module

print("mechanical_check=compact constructor equality")
print("submitted_term=" + submitted)
print("claim_loaded_term=" + executed_module)
print("constructor_identity=" + ("MATCH" if pin_ok else "MISMATCH"))


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_to_n


canonical = load(Path("/reference/canonical.py"), "canonical_for_witness")
generated = load(ROOT / "solution.py", "generated_for_witness")

print("entry_precondition=N>=0")
print("satisfying_state=N=0 with initial MPY configuration cells from spec.k")
for n in [0, 1, 2, 5, 30, 100]:
    # This is exactly the equation defining triangular in verification.k.
    product = n * (n + 1)
    py_mod = ((product % 2) + 2) % 2
    triangular = (product - py_mod) // 2
    values = (canonical(n), generated(n), triangular)
    print(
        f"N={n} canonical={values[0]} generated={values[1]} "
        f"claimed_triangular={values[2]} all_equal={len(set(values)) == 1}"
    )

sys.exit(0 if pin_ok else 1)
