#!/usr/bin/env python3
"""Print concrete witnesses used to instantiate the entry theorem."""

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.anti_shuffle


canonical = load("canonical_ground", Path("/reference/canonical.py"))
generated = load(
    "generated_ground", Path("/tmp/audit-work/86-anti-shuffle/solution.py")
)

expected = {
    "": "",
    "ba": "ab",
    " a": " a",
    "  ba  dc ": "  ab  cd ",
}

for source, wanted in expected.items():
    oracle = canonical(source)
    actual = generated(source)
    print(
        f"input={source!r} canonical={oracle!r} generated={actual!r} "
        f"claimed={wanted!r}"
    )
    if oracle != wanted or actual != wanted:
        raise SystemExit(1)
