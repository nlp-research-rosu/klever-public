#!/usr/bin/env python3
"""Ground substitutions for the entry claim's CS and decodeCodes(CS)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path("/tmp/audit-work/38-decode-cyclic")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def decode_codes(codes: tuple[int, ...]) -> tuple[int, ...]:
    if len(codes) < 3:
        return codes
    return (codes[2], codes[0], codes[1]) + decode_codes(codes[3:])


canonical = load("canonical_witness", ROOT / "trusted/canonical.py")
candidate = load("candidate_witness", ROOT / "candidate/solution.py")

witnesses = ["", "a", "ab", "bca", "bcaefdg", "elho lorwld"]
failures = 0
for text in witnesses:
    codes = tuple(ord(char) for char in text)
    formal_codes = decode_codes(codes)
    formal_text = "".join(chr(code) for code in formal_codes)
    canonical_text = canonical.decode_cyclic(text)
    candidate_text = candidate.decode_cyclic(text)
    agreed = formal_text == canonical_text == candidate_text
    failures += not agreed
    print(
        json.dumps(
            {
                "input": text,
                "CS": codes,
                "decodeCodes(CS)": formal_codes,
                "formal_string": formal_text,
                "canonical": canonical_text,
                "candidate": candidate_text,
                "all_equal": agreed,
            },
            ensure_ascii=False,
        )
    )

print(f"witnesses={len(witnesses)} failures={failures}")
raise SystemExit(1 if failures else 0)
