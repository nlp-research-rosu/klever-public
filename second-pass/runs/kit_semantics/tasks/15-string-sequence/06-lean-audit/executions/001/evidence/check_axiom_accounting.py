#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.klean_final_gate import _allowed_axioms, _parse_axioms

output = Path("/audit-output/evidence/26_print_axioms.txt").read_text()
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
used = _parse_axioms(output)
allowed = _allowed_axioms(inventory)
unrecorded = sorted(used - allowed)

print(
    json.dumps(
        {
            "used_axioms": sorted(used),
            "core_allowed_axioms": [
                "Classical.choice",
                "Quot.sound",
                "propext",
            ],
            "generated_allowlist_count": len(inventory["allowlist"]),
            "used_generated_allowlist_axioms": sorted(
                used
                & {
                    entry["name"]
                    for entry in inventory["allowlist"]
                }
            ),
            "sorryAx_present": "sorryAx" in used,
            "unrecorded_axioms": unrecorded,
            "accounting_pass": "sorryAx" not in used and not unrecorded,
        },
        indent=2,
        sort_keys=True,
    )
)
