#!/usr/bin/env python3
"""Ground witnesses for both claims and the source-contract counterexample."""

from __future__ import annotations

import importlib.util


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


canonical = load_entry("/reference/canonical.py", "canonical_witness")
candidate = load_entry("/candidate/solution.py", "candidate_witness")


def ascii_map_swap(value: str) -> str:
    out = []
    for ch in value:
        code = ord(ch)
        if 65 <= code <= 90:
            out.append(chr(code + 32))
        elif 97 <= code <= 122:
            out.append(chr(code - 32))
        else:
            out.append(ch)
    return "".join(out)


for value in ("a1", "12", "", "1中", "aΣ"):
    mapped = ascii_map_swap(value)
    branch = "swap" if mapped != value else "reverse"
    k_claim_result = mapped if branch == "swap" else value[::-1]
    print(
        f"input={value!r}",
        f"k_precondition_branch={branch}",
        f"k_claim_result={k_claim_result!r}",
        f"canonical={canonical(value)!r}",
        f"candidate_python={candidate(value)!r}",
    )
