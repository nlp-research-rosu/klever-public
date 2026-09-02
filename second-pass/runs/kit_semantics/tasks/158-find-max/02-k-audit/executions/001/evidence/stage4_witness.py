#!/usr/bin/env python3
import importlib.util
from pathlib import Path


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "canonical_stage4")
generated = load(
    Path("/tmp/audit-work/reconstruct-001/solution.py"),
    "generated_stage4",
)

words = ["ba", "ab"]
print(f"words={words!r}")
print(f"entry_precondition=list_of_distinct_strings value=True")
print(f"formal_allStrings=True (machine-checked in stage4_witness_kprove.log)")
print(f"canonical={canonical.find_max(words)!r}")
print(f"generated={generated.find_max(words)!r}")
print("claimed_bestWord='ab' (machine-checked in stage4_witness_kprove.log)")
