#!/usr/bin/env python3
"""Show that a material submitted-program mutation is false on a satisfying input."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.truncate_number


def main() -> int:
    canonical = load("trusted_canonical_body_probe", Path("/tmp/audit-work/canonical.py"))
    mutated = load(
        "mutated_candidate_body_probe",
        Path("/tmp/audit-work/candidate/auditor-mutated-solution.py"),
    )
    witness = 3.5
    expected = canonical(witness)
    actual = mutated(witness)
    print(f"witness={witness!r} canonical={expected!r} mutated_program={actual!r}")
    print(f"material_divergence={actual != expected}")
    return 0 if actual != expected else 1


if __name__ == "__main__":
    raise SystemExit(main())
