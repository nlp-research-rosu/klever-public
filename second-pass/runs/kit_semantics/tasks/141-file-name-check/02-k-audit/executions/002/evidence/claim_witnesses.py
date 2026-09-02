#!/usr/bin/env python3
"""Ground witnesses for every SPEC entry precondition and result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/proof")
ASCII_LATIN = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def load_function(module_name: str, path: Path):
    module_spec = importlib.util.spec_from_file_location(module_name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.file_name_check


canonical = load_function("canonical_witness", SCRATCH / "canonical.py")
generated = load_function("generated_witness", SCRATCH / "solution.py")


def dot_count(name: str) -> int:
    return name.count(".")


def first_is_ascii_latin(name: str) -> bool:
    return bool(name) and name[0] in ASCII_LATIN


def extension_is(name: str, extension: str) -> bool:
    return name[-4:] == extension


def allowed_extension(name: str) -> bool:
    return any(extension_is(name, ext) for ext in (".txt", ".exe", ".dll"))


def decimal_digit_count(name: str) -> int:
    return sum(name.count(digit) for digit in "0123456789")


claims = [
    ("empty-name", "", "No", lambda name: name == ""),
    (
        "bad-dot-count",
        "abc",
        "No",
        lambda name: bool(name) and dot_count(name) != 1,
    ),
    (
        "bad-initial",
        "1.txt",
        "No",
        lambda name: (
            bool(name) and dot_count(name) == 1 and not first_is_ascii_latin(name)
        ),
    ),
    (
        "bad-extension",
        "a.pdf",
        "No",
        lambda name: (
            bool(name)
            and dot_count(name) == 1
            and first_is_ascii_latin(name)
            and not allowed_extension(name)
        ),
    ),
    (
        "too-many-digits-txt",
        "a1234.txt",
        "No",
        lambda name: (
            dot_count(name) == 1
            and first_is_ascii_latin(name)
            and extension_is(name, ".txt")
            and decimal_digit_count(name) > 3
        ),
    ),
    (
        "too-many-digits-exe",
        "a1234.exe",
        "No",
        lambda name: (
            dot_count(name) == 1
            and first_is_ascii_latin(name)
            and not extension_is(name, ".txt")
            and extension_is(name, ".exe")
            and decimal_digit_count(name) > 3
        ),
    ),
    (
        "too-many-digits-dll",
        "a1234.dll",
        "No",
        lambda name: (
            dot_count(name) == 1
            and first_is_ascii_latin(name)
            and not extension_is(name, ".txt")
            and not extension_is(name, ".exe")
            and extension_is(name, ".dll")
            and decimal_digit_count(name) > 3
        ),
    ),
    (
        "valid-name-txt",
        "a.txt",
        "Yes",
        lambda name: (
            dot_count(name) == 1
            and first_is_ascii_latin(name)
            and extension_is(name, ".txt")
            and decimal_digit_count(name) <= 3
        ),
    ),
    (
        "valid-name-exe",
        "a.exe",
        "Yes",
        lambda name: (
            dot_count(name) == 1
            and first_is_ascii_latin(name)
            and not extension_is(name, ".txt")
            and extension_is(name, ".exe")
            and decimal_digit_count(name) <= 3
        ),
    ),
    (
        "valid-name-dll",
        "a.dll",
        "Yes",
        lambda name: (
            dot_count(name) == 1
            and first_is_ascii_latin(name)
            and not extension_is(name, ".txt")
            and not extension_is(name, ".exe")
            and extension_is(name, ".dll")
            and decimal_digit_count(name) <= 3
        ),
    ),
]

for label, witness, destination, precondition in claims:
    satisfied = precondition(witness)
    canonical_result = canonical(witness)
    generated_result = generated(witness)
    print(
        f"{label}: witness={witness!r} precondition={satisfied} "
        f"destination={destination} canonical={canonical_result} "
        f"generated={generated_result}"
    )
    assert satisfied
    assert canonical_result == destination
    assert generated_result == destination
