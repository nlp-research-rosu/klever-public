#!/usr/bin/env python3
"""Compare fresh generated-semantics execution with both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


def find_result(term):
    if isinstance(term, dict):
        label = term.get("label", {})
        if label.get("name") == "<result>":
            token = term["args"][0]
            assert token["node"] == "KToken"
            assert token["sort"]["name"] == "String"
            return json.loads(token["token"])
        for value in term.values():
            found = find_result(value)
            if found is not None:
                return found
    elif isinstance(term, list):
        for value in term:
            found = find_result(value)
            if found is not None:
                return found
    return None


candidate = load_function(
    "generated_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)
canonical = load_function(
    "trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)

cases = ["", "a", "z", "hi", "A", "!", "aA", "é", "🙂"]
k_matches_candidate = True
k_errors = 0
for value in cases:
    command = [
        "krun",
        "/tmp/audit-work/candidate-src/solution.mpy",
        f"-cINPUT={json.dumps(value, ensure_ascii=False)}",
        "--definition",
        "/tmp/audit-work/concrete-kompiled",
        "--output",
        "json",
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        k_errors += 1
        k_matches_candidate = False
        print(
            f"CASE input={value!r} krun_error_exit={completed.returncode} "
            f"stderr={completed.stderr.strip()!r}"
        )
        continue
    result = find_result(json.loads(completed.stdout)["term"])
    python_result = candidate(value)
    canonical_result = canonical(value)
    agrees = result == python_result
    k_matches_candidate &= agrees
    print(
        f"CASE input={value!r} k={result!r} submitted_python={python_result!r} "
        f"canonical={canonical_result!r} "
        f"k_eq_submitted={agrees} k_eq_canonical={result == canonical_result}"
    )

print(
    f"SUMMARY cases={len(cases)} k_errors={k_errors} "
    f"k_matches_submitted_python={k_matches_candidate}"
)
