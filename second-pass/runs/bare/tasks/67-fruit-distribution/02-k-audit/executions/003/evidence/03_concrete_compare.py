#!/usr/bin/env python3
"""Run reviewer concrete inputs and compare generated K to both Python functions."""

from __future__ import annotations

import importlib.util
import subprocess


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_concrete", "/reference/canonical.py")
generated = load(
    "generated_concrete", "/tmp/audit-work/fruit67/candidate/solution.py"
)
work = "/tmp/audit-work/fruit67/candidate"
definition = f"{work}/audit-verification-haskell-kompiled"
cases = [
    ("audit-string-0.mpy", "0 apples and 0 oranges", 0),
    ("audit-string-1.mpy", "5 apples and 6 oranges", 19),
    ("audit-string-2.mpy", "100000 apples and 200000 oranges", 300007),
]

for file_name, source, total in cases:
    expected_canonical = canonical.fruit_distribution(source, total)
    expected_generated = generated.fruit_distribution(source, total)
    assert expected_canonical == expected_generated
    command = [
        "krun",
        f"{work}/{file_name}",
        "--definition",
        definition,
        "--output",
        "pretty",
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    print("COMMAND:", " ".join(command))
    print(result.stdout, end="")
    if result.stderr:
        print("STDERR:", result.stderr, end="")
    print(f"EXIT_STATUS={result.returncode}")
    print(
        f"ORACLES canonical={expected_canonical} generated={expected_generated}"
    )
    assert result.returncode == 0
    assert f"VInt ( {expected_generated} )" in result.stdout

for file_name, expected in [
    ("audit-fruit-0.mpy", 0),
    ("audit-fruit-1.mpy", 8),
]:
    command = [
        "krun",
        f"{work}/{file_name}",
        "--definition",
        definition,
        "--output",
        "pretty",
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    print("COMMAND:", " ".join(command))
    print(result.stdout, end="")
    if result.stderr:
        print("STDERR:", result.stderr, end="")
    print(f"EXIT_STATUS={result.returncode}")
    print(f"ABSTRACT_EXPECTED={expected}")
    assert result.returncode == 0
    assert f"VInt ( {expected} )" in result.stdout

# This is a valid input for both Python implementations but is a boundary
# witness for the generated semantics' failure to model str.split whitespace
# collapsing. A non-final K configuration is expected and recorded.
command = [
    "krun",
    f"{work}/audit-string-extra-spaces.mpy",
    "--definition",
    definition,
    "--output",
    "pretty",
]
result = subprocess.run(command, text=True, capture_output=True)
print("COMMAND:", " ".join(command))
print(result.stdout, end="")
if result.stderr:
    print("STDERR:", result.stderr, end="")
print(f"EXIT_STATUS={result.returncode}")
print(
    "ORACLES canonical="
    f"{canonical.fruit_distribution('5  apples and 6 oranges', 19)} "
    "generated="
    f"{generated.fruit_distribution('5  apples and 6 oranges', 19)}"
)
assert "VInt ( 8 )" not in result.stdout
print("EXPECTED_SEMANTICS_DIVERGENCE=true")
