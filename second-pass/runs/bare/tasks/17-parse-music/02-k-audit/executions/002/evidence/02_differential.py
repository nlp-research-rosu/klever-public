#!/usr/bin/env python3
"""Compare the trusted HumanEval implementation with the submitted solution."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import sys


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_music


canonical = load_function(
    Path("/tmp/audit-work/reconstruction/trusted-canonical.py"),
    "trusted_canonical",
)
generated = load_function(
    Path("/tmp/audit-work/reconstruction/solution.py"), "submitted_solution"
)

documented_and_boundaries = [
    "o o| .| o| o| .| .| .| .| o o",
    "",
    " ",
    "  ",
    "o",
    "o|",
    ".|",
    "o o|",
    "o| .|",
    "o  o|",
    " o",
    "o ",
    " o| .| ",
]

alphabet = ("o", "o|", ".|")
generated_inputs: set[str] = set(documented_and_boundaries)
for length in range(1, 5):
    for notes in product(alphabet, repeat=length):
        generated_inputs.add(" ".join(notes))
        generated_inputs.add("  ".join(notes))
        generated_inputs.add(" " + " ".join(notes))
        generated_inputs.add(" ".join(notes) + " ")


def outcome(function, input_string: str):
    try:
        return ("return", function(input_string))
    except Exception as error:  # compare exception behavior as an outcome
        return ("raise", type(error).__name__, str(error))


mismatches = []
for input_string in sorted(generated_inputs):
    expected = outcome(canonical, input_string)
    actual = outcome(generated, input_string)
    if actual != expected:
        mismatches.append((input_string, expected, actual))

print(f"cases={len(generated_inputs)}")
print(f"mismatches={len(mismatches)}")
for input_string, expected, actual in mismatches:
    print(f"input={input_string!r} canonical={expected!r} submitted={actual!r}")

if not mismatches:
    print("DIFFERENTIAL=PASS")
    raise SystemExit(0)
print("DIFFERENTIAL=FAIL")
raise SystemExit(1)
