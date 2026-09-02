#!/usr/bin/env python3
"""Ground witnesses for the candidate entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.hex_key


canonical = load_entry("claim_witness_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "claim_witness_generated",
    Path("/tmp/audit-work/rebuild/solution.py"),
)


def prime_hex_count(value: str) -> int:
    return sum(value.count(digit) for digit in ("2", "3", "5", "7", "B", "D"))


for value in ("", "ABED1A33", "123456789ABCDEF0"):
    claimed = prime_hex_count(value)
    canonical_result = canonical(value)
    generated_result = generated(value)
    assert claimed == canonical_result == generated_result
    print(f"S={value!r}")
    print(
        "initial_cells="
        f"<k> exact submitted Module(...) ~> #invoke(\"hex_key\", {value!r}) "
        "</k> <env>.Map</env> <result>noResult</result>"
    )
    print(
        "claimed_final_result="
        f"intVal(primeHexCount(S))=intVal({claimed}) "
        f"canonical={canonical_result} generated={generated_result}"
    )

print("GROUND_WITNESSES_PASS")
