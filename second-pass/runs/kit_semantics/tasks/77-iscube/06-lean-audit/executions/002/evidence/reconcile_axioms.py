#!/usr/bin/env python3
"""Reconcile the exact #print axioms output with the generated trust ledger."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import _allowed_axioms, _parse_axioms


output = Path("/audit-output/evidence/18-print-axioms-proof-final.log").read_text(
    encoding="utf-8"
)
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text(
        encoding="utf-8"
    )
)
used = _parse_axioms(output)
generated = {entry["name"] for entry in inventory["allowlist"]}
core = {"Classical.choice", "propext", "Quot.sound"}
allowed = _allowed_axioms(inventory)
result = {
    "used_axioms": sorted(used),
    "standard_lean_core_allowance": sorted(core),
    "generated_trust_inventory_count": len(generated),
    "used_generated_trust_declarations": sorted(used & generated),
    "used_standard_core_axioms": sorted(used & core),
    "sorryAx_present": "sorryAx" in used,
    "unrecorded_or_noncore_axioms": sorted(used - allowed),
    "all_dependencies_reconciled": (
        "sorryAx" not in used and not (used - allowed)
    ),
}
print(json.dumps(result, indent=2, sort_keys=False))
