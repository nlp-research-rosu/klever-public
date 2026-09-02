#!/usr/bin/env python3
import json
import re
from pathlib import Path


output = Path("/audit-output/evidence/08-print-axioms.log").read_text()
match = re.search(r"depends on axioms:\s*\[([^\]]*)\]", output)
if match is None:
    raise SystemExit("missing #print axioms output")
used = {item.strip() for item in match.group(1).split(",") if item.strip()}
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
generated_allowlist = {entry["name"] for entry in inventory["allowlist"]}
core_allowed = {"Classical.choice", "propext", "Quot.sound"}
result = {
    "used_axioms": sorted(used),
    "sorryAx_present": "sorryAx" in used,
    "generated_allowlist_count": len(generated_allowlist),
    "used_generated_allowlist_axioms": sorted(used & generated_allowlist),
    "used_core_axioms": sorted(used & core_allowed),
    "unrecorded_or_unapproved_axioms": sorted(
        used - generated_allowlist - core_allowed
    ),
    "passes": (
        "sorryAx" not in used
        and used <= generated_allowlist | core_allowed
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
