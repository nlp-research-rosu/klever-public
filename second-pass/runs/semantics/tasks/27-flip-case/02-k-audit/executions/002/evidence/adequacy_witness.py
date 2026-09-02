#!/usr/bin/env python3
"""Ground substitutions for the claim's mapSwap postcondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(path: Path):
    spec = importlib.util.spec_from_file_location(f"adequacy_{path.stem}_{id(path)}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


def k_swap_code(code: int) -> int:
    # Exactly methods.k:149-152.
    if 65 <= code <= 90:
        return code + 32
    if 97 <= code <= 122:
        return code - 32
    return code


def k_map_swap(value: str) -> str:
    # This interpretation is only used on scalar code points in these witnesses.
    return "".join(chr(k_swap_code(ord(char))) for char in value)


canonical = load_function(Path("/reference/canonical.py"))
candidate = load_function(Path("/tmp/audit-work/27-flip-case/solution.py"))

inputs = ["", "Hello", "é", "ß", "Σ"]
mismatches = 0
for value in inputs:
    formal = k_map_swap(value)
    trusted = canonical(value)
    generated = candidate(value)
    agrees = formal == trusted == generated
    mismatches += not agrees
    print(
        f"input={value!r} codes={[ord(c) for c in value]} "
        f"K_mapSwap={formal!r}/{[ord(c) for c in formal]} "
        f"canonical={trusted!r}/{[ord(c) for c in trusted]} "
        f"candidate={generated!r}/{[ord(c) for c in generated]} "
        f"all_agree={agrees}"
    )

print(f"formal_vs_python_mismatches={mismatches}")
