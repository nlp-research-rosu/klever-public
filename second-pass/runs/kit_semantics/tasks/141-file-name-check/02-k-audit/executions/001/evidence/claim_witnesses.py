#!/usr/bin/env python3
"""Ground witnesses for every SPEC entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.file_name_check


canonical = load_entry(
    "trusted_canonical_witness", Path("/tmp/audit-work/trusted/canonical.py")
)
generated = load_entry(
    "generated_solution_witness",
    Path("/tmp/audit-work/reconstruction/solution.py"),
)

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
extensions = (".txt", ".exe", ".dll")


def dot_count(value: str) -> int:
    return value.count(".")


def initial_ok(value: str) -> bool:
    return bool(value) and value[0] in alphabet


def extension_is(value: str, extension: str) -> bool:
    return value[-4:] == extension


def allowed_extension(value: str) -> bool:
    return any(extension_is(value, extension) for extension in extensions)


def digit_count(value: str) -> int:
    return sum(value.count(str(digit)) for digit in range(10))


witnesses = [
    ("empty-name", "", "No", lambda s: s == ""),
    (
        "bad-dot-count",
        "abc",
        "No",
        lambda s: bool(s) and dot_count(s) != 1,
    ),
    (
        "bad-initial",
        "1.txt",
        "No",
        lambda s: dot_count(s) == 1 and not initial_ok(s),
    ),
    (
        "bad-extension",
        "a.pdf",
        "No",
        lambda s: dot_count(s) == 1
        and initial_ok(s)
        and not allowed_extension(s),
    ),
    (
        "too-many-digits-txt",
        "a1234.txt",
        "No",
        lambda s: dot_count(s) == 1
        and initial_ok(s)
        and extension_is(s, ".txt")
        and digit_count(s) > 3,
    ),
    (
        "too-many-digits-exe",
        "a1234.exe",
        "No",
        lambda s: dot_count(s) == 1
        and initial_ok(s)
        and not extension_is(s, ".txt")
        and extension_is(s, ".exe")
        and digit_count(s) > 3,
    ),
    (
        "too-many-digits-dll",
        "a1234.dll",
        "No",
        lambda s: dot_count(s) == 1
        and initial_ok(s)
        and not extension_is(s, ".txt")
        and not extension_is(s, ".exe")
        and extension_is(s, ".dll")
        and digit_count(s) > 3,
    ),
    (
        "valid-name-txt",
        "a123.txt",
        "Yes",
        lambda s: dot_count(s) == 1
        and initial_ok(s)
        and extension_is(s, ".txt")
        and digit_count(s) <= 3,
    ),
    (
        "valid-name-exe",
        "a123.exe",
        "Yes",
        lambda s: dot_count(s) == 1
        and initial_ok(s)
        and not extension_is(s, ".txt")
        and extension_is(s, ".exe")
        and digit_count(s) <= 3,
    ),
    (
        "valid-name-dll",
        "a123.dll",
        "Yes",
        lambda s: dot_count(s) == 1
        and initial_ok(s)
        and not extension_is(s, ".txt")
        and not extension_is(s, ".exe")
        and extension_is(s, ".dll")
        and digit_count(s) <= 3,
    ),
]

for label, value, expected, precondition in witnesses:
    assert precondition(value), (label, value)
    generated_result = generated(value)
    canonical_result = canonical(value)
    assert generated_result == expected
    assert canonical_result == expected
    print(
        f"{label}: witness={value!r} precondition=true "
        f"generated={generated_result} canonical={canonical_result}"
    )

print(f"CLAIM_WITNESSES=PASS count={len(witnesses)}")
