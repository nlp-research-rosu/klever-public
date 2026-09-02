#!/usr/bin/env python3
"""Parse exact Lean axiom output with the trusted final-gate parser."""

import json
from pathlib import Path

from tools import klean_final_gate


output = Path("/audit-output/evidence/proof-final-axioms.log").read_text()
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
used = klean_final_gate._parse_axioms(output)
allowed = klean_final_gate._allowed_axioms(inventory)
inventory_names = {entry["name"] for entry in inventory["allowlist"]}
unexpected = used - allowed

print("used_axioms:", sorted(used))
print("inventory_allowlist_count:", len(inventory_names))
print("used_generated_inventory_axioms:", sorted(used & inventory_names))
print(
    "used_lean_core_primitives:",
    sorted(used & {"Classical.choice", "propext", "Quot.sound"}),
)
print("contains_sorryAx:", "sorryAx" in used)
print("unexpected_axioms:", sorted(unexpected))
if "sorryAx" in used or unexpected:
    raise SystemExit(1)
print("axiom_reconciliation: PASS")
