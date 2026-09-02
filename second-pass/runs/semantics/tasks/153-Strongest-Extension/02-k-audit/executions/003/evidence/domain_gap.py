#!/usr/bin/env python3
"""Concrete witnesses for the formal theorem's source-contract gaps."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(module_name: str, path: Path):
    module_spec = importlib.util.spec_from_file_location(module_name, path)
    assert module_spec and module_spec.loader
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.Strongest_Extension


canonical = load_function("canonical_gap", Path("/reference/canonical.py"))
candidate = load_function(
    "candidate_gap", Path("/tmp/audit-work/candidate/solution.py")
)


def ascii_proof_summary(class_name: str, extensions: list[str]) -> str:
    def strength(extension: str) -> int:
        return sum(
            (1 if "A" <= character <= "Z" else 0)
            - (1 if "a" <= character <= "z" else 0)
            for character in extension
        )

    best = extensions[0]
    best_strength = strength(best)
    for extension in extensions:
        candidate_strength = strength(extension)
        if candidate_strength > best_strength:
            best = extension
            best_strength = candidate_strength
    return class_name + "." + best


unicode_input = ("C", ["A", "ΩΩ", "BB"])
unicode_canonical = canonical(*unicode_input)
unicode_candidate = candidate(*unicode_input)
unicode_k_summary = ascii_proof_summary(*unicode_input)
print(f"unicode_input={unicode_input!r}")
print(f"canonical={unicode_canonical!r}")
print(f"candidate={unicode_candidate!r}")
print(f"k_ascii_summary={unicode_k_summary!r}")
print(f"unicode_summary_diverges={unicode_k_summary != unicode_candidate}")

four_input = ("C", ["a", "A", "zz", "ZZZ"])
four_canonical = canonical(*four_input)
four_candidate = candidate(*four_input)
print(f"four_element_input={four_input!r}")
print(f"canonical={four_canonical!r}")
print(f"candidate={four_candidate!r}")
print("entry_precondition_exists=False (spec.k requires exactly three vCons nodes)")

if not (
    unicode_canonical == unicode_candidate == "C.ΩΩ"
    and unicode_k_summary == "C.BB"
    and four_canonical == four_candidate == "C.ZZZ"
):
    raise SystemExit(1)
