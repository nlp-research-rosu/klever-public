#!/usr/bin/env python3
import json
import re
from pathlib import Path


output = Path("/audit-output/evidence/08-axiom-audit.log").read_text()
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
match = re.search(r"depends on axioms:\s*\[([^]]*)\]", output)
if match is None:
    raise SystemExit("axiom output was not parseable")
used = sorted(item.strip() for item in match.group(1).split(",") if item.strip())
baseline = {"Classical.choice", "propext", "Quot.sound"}
recorded = {
    entry["name"] for entry in inventory.get("allowlist", [])
    if isinstance(entry, dict) and isinstance(entry.get("name"), str)
}
allowed = baseline | recorded
print(json.dumps({
    "used_axioms": used,
    "baseline_allowed": sorted(baseline),
    "trust_inventory_allowlist_count": len(recorded),
    "unrecorded_axioms": sorted(set(used) - allowed),
    "uses_sorryAx": "sorryAx" in used,
    "used_generated_trust_declarations": sorted(set(used) & recorded),
    "reconciled": not (set(used) - allowed) and "sorryAx" not in used,
}, indent=2, sort_keys=True))
