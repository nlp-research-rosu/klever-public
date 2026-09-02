#!/usr/bin/env python3
"""Concrete satisfying-input substitution for the entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/64-vowels-count")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


canonical = load(WORK / "trusted-canonical.py", "pinning_canonical")
generated = load(WORK / "solution.py", "pinning_generated")
witness = "abcde"
expected_claim_result = 2
canonical_result = canonical(witness)
generated_result = generated(witness)
print(f"witness={witness!r}")
print("loader_precondition=<k> solutionProgram ~> #entry(\"abcde\") </k>, "
      "<env>.Map</env>, <functions>.Map</functions>, <stack>.List</stack>")
print("correctness_precondition=<k> Call(Name(\"vowels_count\"), "
      "strVal(\"abcde\")) </k>, exact singleton vowels_count binding, "
      "<env>.Map</env>, <stack>.List</stack>")
print(f"claimed_result={expected_claim_result}")
print(f"trusted_canonical_result={canonical_result}")
print(f"generated_python_result={generated_result}")
assert canonical_result == expected_claim_result
assert generated_result == expected_claim_result
print("CONCRETE_PRECONDITIONS_SATISFIABLE_AND_RESULTS_AGREE")
