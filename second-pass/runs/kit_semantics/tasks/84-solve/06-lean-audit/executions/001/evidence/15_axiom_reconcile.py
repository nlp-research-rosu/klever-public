#!/usr/bin/env python3
import json
import re
from pathlib import Path

inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
output = Path("/audit-output/evidence/06_print_axioms.log").read_text()
match = re.search(r"depends on axioms:\s*\[([^\]]*)\]", output)
if match is None:
    raise SystemExit("missing #print axioms result")
used = {
    item.strip()
    for item in match.group(1).split(",")
    if item.strip()
}
lean_core = {"Classical.choice", "propext", "Quot.sound"}
generated_allowlist = {entry["name"] for entry in inventory["allowlist"]}
allowed = lean_core | generated_allowlist

print(f"used_axioms={sorted(used)}")
print(f"lean_core_axioms={sorted(lean_core)}")
print(f"generated_allowlist_count={len(generated_allowlist)}")
print(f"used_generated_axioms={sorted(used & generated_allowlist)}")
print(f"unexpected_axioms={sorted(used - allowed)}")
print(f"sorryAx_present={'sorryAx' in used}")
print(f"used_axioms_fully_accounted={used <= allowed}")
