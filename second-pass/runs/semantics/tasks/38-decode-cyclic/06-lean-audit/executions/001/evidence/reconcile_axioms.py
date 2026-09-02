#!/usr/bin/env python3
import json
import re
from pathlib import Path

axiom_output = Path(
    "/audit-output/evidence/19-print-axioms-proof-final-exact.log"
).read_text()
match = re.search(r"depends on axioms: \[(.*)\]", axiom_output)
reported = (
    [item.strip() for item in match.group(1).split(",")]
    if match is not None
    else []
)
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
allowlist = {entry["name"] for entry in inventory["allowlist"]}
lean_core = {"propext", "Classical.choice", "Quot.sound"}

print(
    json.dumps(
        {
            "reported_by_lean": reported,
            "lean_core_logical_axioms": sorted(lean_core),
            "reported_exactly_core_logical_axioms": set(reported)
            == lean_core,
            "generated_trust_allowlist_count": len(allowlist),
            "reported_generated_allowlist_dependencies": sorted(
                set(reported) & allowlist
            ),
            "unrecognized_dependencies": sorted(
                set(reported) - lean_core - allowlist
            ),
            "contains_sorryAx": "sorryAx" in reported,
        },
        indent=2,
        sort_keys=True,
    )
)
