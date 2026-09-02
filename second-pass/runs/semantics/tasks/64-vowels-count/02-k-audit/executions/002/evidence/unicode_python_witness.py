#!/usr/bin/env python3
"""Explain the concrete CPython side of the U+0130 false-conclusion witness."""

import importlib.util
import pathlib


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, pathlib.Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


text = "\u0130"
lowered = text.lower()
canonical = load(
    "/tmp/audit-work/proof/trusted/canonical.py", "unicode_canonical"
)
generated = load("/tmp/audit-work/proof/solution.py", "unicode_generated")

print(f"input={text!r} codepoints={[ord(char) for char in text]}")
print(f"cpython_lower={lowered!r} codepoints={[ord(char) for char in lowered]}")
print(f"canonical_result={canonical(text)}")
print(f"generated_result={generated(text)}")
assert canonical(text) == 0
assert generated(text) == 1
