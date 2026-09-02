#!/usr/bin/env python3
"""Print concrete satisfying witnesses for each entry-claim shape."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_closest_vowel


root = Path("/tmp/audit-work/reconstruction")
canonical = load(root / "canonical.py", "ground_canonical")
generated = load(root / "solution.py", "ground_generated")

for word in ["", "a", "ab", "bab", "yogurt"]:
    expected_codes = [ord(ch) for ch in canonical(word)]
    actual_codes = [ord(ch) for ch in generated(word)]
    print(
        f"input={word!r} input_codes={[ord(ch) for ch in word]} "
        f"canonical={canonical(word)!r} generated={generated(word)!r} "
        f"result_codes={expected_codes} agree={expected_codes == actual_codes}"
    )
