#!/usr/bin/env python3
"""Concrete falsifying witness for the fresh hyphen-separator mutation."""

import importlib.util
import pathlib


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, pathlib.Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


text = "three one five"
canonical = load("/reference/canonical.py", "canonical")
candidate = load("/candidate/solution.py", "candidate")
canonical_result = canonical(text)
candidate_result = candidate(text)
mutated_obligation = "one-three-five"

print(f"input={text!r}")
print("precondition_satisfied=True  # all tokens are allowed numeral words")
print(f"canonical={canonical_result!r}")
print(f"candidate={candidate_result!r}")
print(f"mutated_obligation={mutated_obligation!r}")
print(f"obligation_holds={candidate_result == mutated_obligation}")
raise SystemExit(0 if candidate_result != mutated_obligation else 1)
