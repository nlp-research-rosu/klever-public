#!/usr/bin/env python3
"""Stage-4 claim witnesses and literal-program pinning checks."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


scratch = Path("/tmp/audit-work/71-triangle-area")
canonical = load(Path("/reference/canonical.py"), "adequacy_canonical")
submitted = load(scratch / "solution.py", "adequacy_submitted")

translated = re.sub(r"\s+", "", (scratch / "solution.mpy").read_text())
verification = (scratch / "verification.k").read_text()
literal = verification.split("rule solutionProgram =>", 1)[1].rsplit(
    "endmodule", 1
)[0]
literal = re.sub(r"\s+", "", literal)
print(f"solution_program_literal_byte_tokens_match={literal == translated}")
if literal != translated:
    raise SystemExit("verification.k solutionProgram does not pin solution.mpy")

# Each row is (claim, satisfying args, formal result interpreted as Python-scale).
rows = [
    ("concrete-example-3-4-5", (3, 4, 5), 6.00),
    ("concrete-example-5-12-13", (5, 12, 13), 30.00),
    ("concrete-example-2-2-2", (2, 2, 2), 1.73),
    ("universal-valid witness", (3, 4, 5), 6.00),
    ("invalid-first witness", (1, 2, 3), -1),
    ("invalid-second witness", (1, 3, 2), -1),
    ("invalid-third witness", (3, 2, 1), -1),
]

for label, args, claimed in rows:
    can = canonical(*args)
    sub = submitted(*args)
    print(
        f"{label}: args={args!r} claimed={claimed!r} "
        f"canonical={can!r} submitted={sub!r} "
        f"all_equal={claimed == can == sub}"
    )

# This input also satisfies the universal valid precondition but refutes the
# bridge from the K claim's exact-rational result to real CPython execution.
precision_args = (10**16, 10**16, 1)
a, b, c = precision_args
precondition = a + b > c and a + c > b and b + c > a
print(
    "precision-loss witness: "
    f"args={precision_args!r} precondition={precondition} "
    "K_claim_interpretation=5000000000000000.00 "
    f"canonical={canonical(*precision_args)!r} "
    f"submitted={submitted(*precision_args)!r}"
)
