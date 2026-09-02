#!/usr/bin/env python3
"""Ground witnesses for the entry claim's satisfiability and result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.multiply


canonical = load_function(ROOT / "canonical.py", "witness_canonical")
generated = load_function(ROOT / "solution.py", "witness_generated")
spec_text = (ROOT / "spec.k").read_text(encoding="utf-8")
assert "requires " not in "\n".join(
    line for line in spec_text.splitlines() if not line.lstrip().startswith("requires \"")
), "unexpected semantic precondition in claim"

print("ENTRY_PRECONDITION: none beyond A:Int and B:Int sorts")
print(
    "SATISFYING_INITIAL_STATE: A=-1, B=1, <k> multiplyProgram ~> "
    '#invoke("multiply",-1,1), <env> .Map, <functions> .Map, '
    "<result> noResult"
)
for a, b in [(148, 412), (-1, 1), (-1, -1), (0, 0)]:
    claimed = (abs(a) % 10) * (abs(b) % 10)
    print(
        f"A={a} B={b} claimed={claimed} "
        f"generated={generated(a, b)} canonical={canonical(a, b)}"
    )
    assert claimed == generated(a, b)
print("GROUND_CLAIM_SUBSTITUTION: MATCHES_GENERATED_PROGRAM")
