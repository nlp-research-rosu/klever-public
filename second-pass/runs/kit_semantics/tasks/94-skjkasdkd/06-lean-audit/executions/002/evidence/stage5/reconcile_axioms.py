#!/usr/bin/env python3
"""Reconcile the exact Lean axiom print with the generated trust inventory."""

import json
import re
from pathlib import Path


output = Path("/audit-output/evidence/stage5/print-axioms-direct.log").read_text()
inventory = json.loads(Path("/reference/klean-generation/trust-inventory.json").read_text())
matches = re.findall(r"'Proof\.final' depends on axioms:\s*\[([^\]]*)\]", output)
if len(matches) != 1:
    raise SystemExit("ambiguous or missing #print axioms result")
used = {item.strip() for item in matches[0].split(",") if item.strip()}
generated_allowlist = {entry["name"] for entry in inventory["allowlist"]}
lean_standard = {"propext", "Classical.choice", "Quot.sound"}
result = {
    "used_axioms": sorted(used),
    "lean_standard_baseline": sorted(lean_standard),
    "generated_trust_inventory_count": len(generated_allowlist),
    "used_generated_trust_declarations": sorted(used & generated_allowlist),
    "unexpected_axioms": sorted(used - lean_standard - generated_allowlist),
    "sorryAx_present": "sorryAx" in used,
    "all_used_axioms_accounted": used <= lean_standard | generated_allowlist,
    "inventory_designated_sorries": inventory["designated_sorries"],
    "inventory_other_sorries": inventory["other_sorries"],
}
print(json.dumps(result, indent=2, sort_keys=True))
if (
    result["sorryAx_present"]
    or result["unexpected_axioms"]
    or not result["all_used_axioms_accounted"]
    or result["inventory_designated_sorries"] != 0
    or result["inventory_other_sorries"] != 0
):
    raise SystemExit(1)
