#!/usr/bin/env python3
"""Trusted/submitted Python result for the lowercase Unicode semantics witness."""

from __future__ import annotations

import importlib.util
import sys


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Strongest_Extension


if len(sys.argv) != 3:
    raise SystemExit("usage: unicode-lower-oracle.py CANONICAL SOLUTION")

canonical = load("canonical_lower", sys.argv[1])
submitted = load("solution_lower", sys.argv[2])
arguments = ("C", ["a", "éé"])
print(f"arguments={arguments!r}")
print(f"'é'.isalpha()={'é'.isalpha()} 'é'.islower()={'é'.islower()}")
print(f"canonical={canonical(*arguments)!r}")
print(f"submitted={submitted(*arguments)!r}")
