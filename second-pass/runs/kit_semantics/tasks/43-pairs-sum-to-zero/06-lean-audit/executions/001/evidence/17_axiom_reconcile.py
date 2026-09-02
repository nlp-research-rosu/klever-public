#!/usr/bin/env python3
"""Reconcile the exact #print axioms output with the trusted inventory."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import _allowed_axioms, _parse_axioms


output = Path("/audit-output/evidence/09_print_axioms.log").read_text()
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
used = _parse_axioms(output)
allowed = _allowed_axioms(inventory)
generated_allowlist = {
    entry["name"] for entry in inventory["allowlist"]
}
facts = {
    "used_axioms": sorted(used),
    "sorryAx_present": "sorryAx" in used,
    "unrecorded_or_nonfoundational": sorted(used - allowed),
    "generated_allowlist_count": len(generated_allowlist),
    "generated_allowlist_dependencies_used": sorted(
        used & generated_allowlist
    ),
    "foundational_dependencies_used": sorted(
        used & {"Classical.choice", "propext", "Quot.sound"}
    ),
    "inventory_designated_sorries": inventory["designated_sorries"],
    "inventory_other_sorries": inventory["other_sorries"],
}
print(json.dumps(facts, indent=2, sort_keys=True))
if (
    facts["sorryAx_present"]
    or facts["unrecorded_or_nonfoundational"]
    or facts["inventory_designated_sorries"] != 0
    or facts["inventory_other_sorries"] != 0
):
    raise SystemExit("AXIOM_RECONCILIATION: FAIL")
print("AXIOM_RECONCILIATION: PASS")
