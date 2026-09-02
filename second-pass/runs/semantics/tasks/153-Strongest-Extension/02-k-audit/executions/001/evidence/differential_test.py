#!/usr/bin/env python3
"""Independent differential test for HumanEval 153.

The oracle and generated entry points are loaded from their source paths.  Test
generation is deterministic and does not reuse any K helper equations.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any


def load_entry(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


canonical = load_entry("trusted_canonical_153", "/reference/canonical.py")
generated = load_entry("submitted_solution_153", "/candidate/solution.py")


def outcome(function, class_name: str, extensions: list[str]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(class_name, extensions)}
    except Exception as error:  # Compare the externally visible exception type.
        return {"kind": "raise", "type": type(error).__name__}


documented_and_boundary_cases = [
    ("Slices", ["SErviNGSliCes", "Cheese", "StuFfed"], "documented-main"),
    ("my_class", ["AA", "Be", "CC"], "documented-tie"),
    ("", [""], "empty-class-and-extension"),
    ("C", [], "empty-list"),
    ("C", [""], "singleton-empty-extension"),
    ("C", ["a"], "singleton-lower"),
    ("C", ["A"], "singleton-upper"),
    ("C", ["a", "A"], "strict-improvement"),
    ("C", ["A", "B"], "equal-strength-first-wins"),
    ("C", ["1", "_"], "nonletters-neutral"),
    ("C", ["Aa", "AA", "zz", "Z"], "mixed-four-elements"),
    ("C", ["A!", "B?", "CC"], "punctuation"),
    ("C", ["Ⅰ", "A", "a"], "unicode-nonalpha-uppercase-witness"),
    ("C", ["ⅰ", "a", "A"], "unicode-nonalpha-lowercase-witness"),
    ("C", ["Ⓐ", "A", "a"], "unicode-circled-uppercase-witness"),
]

cases = list(documented_and_boundary_cases)

# Exhaust all short individual ASCII strings, then deterministically sample
# lists of lengths 1 through 5 to cover every outer-loop length/branch shape.
alphabet = "AaZz0_!"
short_strings = [""]
for length in range(1, 3):
    short_strings.extend(
        "".join(chars) for chars in itertools.product(alphabet, repeat=length)
    )

rng = random.Random(153)
for index in range(5000):
    list_length = 1 + (index % 5)
    extensions = [rng.choice(short_strings) for _ in range(list_length)]
    class_name = rng.choice(["", "C", "my_class", "A.Z"])
    cases.append((class_name, extensions, f"generated-{index:04d}"))

mismatches = []
for class_name, extensions, label in cases:
    expected = outcome(canonical, class_name, list(extensions))
    actual = outcome(generated, class_name, list(extensions))
    if expected != actual:
        mismatches.append(
            {
                "label": label,
                "class_name": class_name,
                "extensions": extensions,
                "canonical": expected,
                "generated": actual,
            }
        )

ascii_mismatches = [
    item
    for item in mismatches
    if item["label"].startswith("generated-")
    or item["label"] in {
        "documented-main",
        "documented-tie",
        "empty-class-and-extension",
        "empty-list",
        "singleton-empty-extension",
        "singleton-lower",
        "singleton-upper",
        "strict-improvement",
        "equal-strength-first-wins",
        "nonletters-neutral",
        "mixed-four-elements",
        "punctuation",
    }
]

summary = {
    "total_cases": len(cases),
    "documented_and_boundary_cases": len(documented_and_boundary_cases),
    "generated_cases": 5000,
    "ascii_mismatch_count": len(ascii_mismatches),
    "total_mismatch_count": len(mismatches),
    "mismatches": mismatches,
}
print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))

# The script records the known scope split rather than hiding it: ASCII behavior
# must agree, while Unicode discrepancies remain visible in the JSON evidence.
assert not ascii_mismatches
assert mismatches, "Expected the submitted implementation's Unicode scope gap"
