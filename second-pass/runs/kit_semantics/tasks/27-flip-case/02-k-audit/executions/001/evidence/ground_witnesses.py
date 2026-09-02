#!/usr/bin/env python3
"""Compare concrete claim substitutions with both trusted Python programs."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/27-flip-case")


def load(module_name: str, filename: str):
    spec = importlib.util.spec_from_file_location(module_name, SCRATCH / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


canonical = load("ground_canonical", "canonical.py")
candidate = load("ground_candidate", "solution.py")

for label, value, k_codes in [
    ("ASCII A", "A", [97]),
    ("Unicode e-acute", "é", [233]),
    ("Unicode sharp-s", "ß", [223]),
]:
    canonical_result = canonical(value)
    candidate_result = candidate(value)
    python_codes = [ord(character) for character in candidate_result]
    print(
        f"{label}: input_codes={[ord(character) for character in value]} "
        f"canonical={canonical_result!r}/{[ord(character) for character in canonical_result]} "
        f"candidate={candidate_result!r}/{python_codes} "
        f"supplied_K_mapSwap_codes={k_codes} "
        f"K_matches_real={k_codes == python_codes}"
    )
    assert canonical_result == candidate_result

assert [ord(character) for character in candidate("A")] == [97]
assert [ord(character) for character in candidate("é")] == [201]
assert [ord(character) for character in candidate("ß")] == [83, 83]
print("GROUND_PYTHON_COMPARISON=PASS")
