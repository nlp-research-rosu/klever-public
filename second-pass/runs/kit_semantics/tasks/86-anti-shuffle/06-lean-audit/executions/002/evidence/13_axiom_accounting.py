#!/usr/bin/env python3
"""Reconcile #print axioms with the generated ledger and trusted baseline."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import _allowed_axioms, _parse_axioms


inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
output = Path("/audit-output/evidence/08-print-axioms.log").read_text()
used = _parse_axioms(output)
generated_names = {entry["name"] for entry in inventory["allowlist"]}
allowed = _allowed_axioms(inventory)
result = {
    "used_axioms": sorted(used),
    "generated_allowlist_count": len(generated_names),
    "used_generated_allowlist_axioms": sorted(used & generated_names),
    "trusted_core_baseline_used": sorted(
        used & {"Classical.choice", "propext", "Quot.sound"}
    ),
    "unexpected_axioms": sorted(used - allowed),
    "sorryAx_present": "sorryAx" in used,
}
result["accounting_pass"] = (
    not result["unexpected_axioms"] and not result["sorryAx_present"]
)
print(json.dumps(result, indent=2, sort_keys=True))
if not result["accounting_pass"]:
    raise SystemExit(1)
