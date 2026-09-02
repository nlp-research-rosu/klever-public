#!/usr/bin/env python3
"""Concrete satisfying witnesses for every submitted entry claim."""

from __future__ import annotations

import importlib.util
import sys


CLAIMS = [
    (
        "prompt-worked",
        "Slices",
        ["SErviNGSliCes", "Cheese", "StuFfed"],
    ),
    ("prompt-tie", "Witness", ["AA", "Be", "CC"]),
    ("later-stronger", "Witness", ["abc", "AB", "A-b"]),
    ("uncased-characters", "Witness", ["a-1", "--", "A!"]),
    ("empty-first", "Witness", ["", "123", "!"]),
    ("all-negative", "Witness", ["abcd", "a", "xy"]),
    ("singleton", "Witness", ["Zz"]),
]


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


def score(text: str) -> int:
    return sum(
        1 if char.isalpha() and char.isupper()
        else -1 if char.isalpha() and char.islower()
        else 0
        for char in text
    )


def contract(class_name: str, extensions: list[str]) -> str:
    best = extensions[0]
    best_score = score(best)
    for extension in extensions[1:]:
        extension_score = score(extension)
        if extension_score > best_score:
            best = extension
            best_score = extension_score
    return class_name + "." + best


if len(sys.argv) != 3:
    raise SystemExit("usage: claim-witnesses.py CANONICAL SOLUTION")

canonical = load("canonical_witness", sys.argv[1])
submitted = load("solution_witness", sys.argv[2])

for label, class_name, extensions in CLAIMS:
    expected = contract(class_name, extensions)
    trusted = canonical(class_name, extensions)
    candidate = submitted(class_name, extensions)
    status = "MATCH" if expected == trusted == candidate else "MISMATCH"
    print(
        f"{label}: initial env=.Map functions=.Map result=noResult; "
        f"class={class_name!r}; extensions={extensions!r}; "
        f"claimed/concrete={expected!r}; canonical={trusted!r}; "
        f"submitted={candidate!r}; {status}"
    )
