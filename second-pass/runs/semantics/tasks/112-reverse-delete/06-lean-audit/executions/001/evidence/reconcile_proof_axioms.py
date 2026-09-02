#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import _parse_axioms


output = Path("/audit-output/evidence/proof-final-axioms-exact.log").read_text()
used = _parse_axioms(output)
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
recorded = {entry["name"]: entry for entry in inventory["allowlist"]}
builtins = {
    "Classical.choice": "Lean logical foundation",
    "propext": "Lean logical foundation",
    "Quot.sound": "Lean logical foundation",
}

assert "sorryAx" not in used
assert len(used) == 32
for name in sorted(used):
    if name in builtins:
        print(f"{name}\tBUILTIN\t{builtins[name]}")
        continue
    entry = recorded.get(name)
    assert entry is not None, f"unrecorded axiom: {name}"
    print(
        "\t".join(
            (
                name,
                entry["kind"],
                entry["source"],
                entry["line"],
                entry["type"],
            )
        )
    )

unexpected = used - set(recorded) - set(builtins)
print(f"used_axiom_count\t{len(used)}")
print(f"sorryAx_present\t{'yes' if 'sorryAx' in used else 'no'}")
print(f"unrecorded_axiom_count\t{len(unexpected)}")
print("AXIOM_RECONCILIATION: PASS")
