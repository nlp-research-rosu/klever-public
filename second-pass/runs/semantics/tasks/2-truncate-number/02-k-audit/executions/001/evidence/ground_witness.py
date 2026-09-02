#!/usr/bin/env python3
"""Concrete satisfying witnesses for the submitted entry claim."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.truncate_number


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
generated = load(Path("/candidate/solution.py"), "generated_witness")

print(
    "PRESTATE=<k>#loadAll(solutionProgram) ~> Call(Name(\"truncate_number\"), "
    "(Float(N), .Exprs))</k>; env=0; default empty module/heap/stack state"
)
for value in (3.5, 1.0, 0.25):
    claimed = value % 1.0
    canonical_value = canonical(value)
    generated_value = generated(value)
    print(
        f"N={value.hex()} claimed_floatMod={claimed.hex()} "
        f"canonical={canonical_value.hex()} generated={generated_value.hex()} "
        f"all_equal={claimed == canonical_value == generated_value}"
    )
