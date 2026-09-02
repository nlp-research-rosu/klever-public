#!/usr/bin/env python3
"""Reconcile Proof.final dependencies with generated and Lean-core trust."""

from __future__ import annotations

import json
import re
from pathlib import Path


log = Path("/audit-output/evidence/06_print_axioms.log").read_text()
match = re.search(r"depends on axioms: \[([^\]]*)\]", log)
if match is None:
    raise SystemExit("could not parse #print axioms output")
dependencies = [
    name.strip() for name in match.group(1).split(",") if name.strip()
]
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
generated = set(inventory["axioms"])
lean_core = {"propext", "Classical.choice", "Quot.sound"}

result = {
    "exact_print_axioms_dependencies": dependencies,
    "lean_core_dependencies": sorted(set(dependencies) & lean_core),
    "generated_inventory_dependencies": sorted(
        set(dependencies) & generated
    ),
    "unreconciled_dependencies": sorted(
        set(dependencies) - lean_core - generated
    ),
    "sorryAx_present": "sorryAx" in dependencies,
    "generated_axiom_inventory_count": len(generated),
    "generated_designated_sorries": inventory["designated_sorries"],
    "generated_other_sorries": inventory["other_sorries"],
    "automatic_axiomatization": inventory["automatic_axiomatization"],
}
print(json.dumps(result, indent=2, sort_keys=True))
