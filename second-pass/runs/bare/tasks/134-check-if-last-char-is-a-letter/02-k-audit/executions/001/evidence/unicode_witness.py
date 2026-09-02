#!/usr/bin/env python3
"""Evaluate the ground Unicode witness in both trusted Python artifacts."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_if_last_char_is_a_letter


text = "K"  # U+212A KELVIN SIGN; Python lower() is "k" and isalpha() is true.
canonical = load(Path("/reference/canonical.py"), "unicode_canonical")
candidate = load(Path("/tmp/audit-work/source/solution.py"), "unicode_candidate")
print(f"input={text!r}")
print(f"canonical={canonical(text)!r}")
print(f"candidate={candidate(text)!r}")
