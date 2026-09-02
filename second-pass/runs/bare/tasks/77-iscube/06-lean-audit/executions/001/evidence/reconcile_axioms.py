#!/usr/bin/env python3
"""Reconcile the exact #print axioms result with the trusted policy."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import _allowed_axioms, _parse_axioms


inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
output = Path(
    "/audit-output/evidence/proof-print-axioms-success.log"
).read_text()
used = _parse_axioms(output)
allowed = _allowed_axioms(inventory)
generated_allowlist = {
    entry["name"] for entry in inventory["allowlist"]
}

result = {
    "used_axioms": sorted(used),
    "sorryAx_present": "sorryAx" in used,
    "unexpected_axioms": sorted(used - allowed),
    "used_generated_trust_declarations": sorted(
        used & generated_allowlist
    ),
    "used_core_allowed_axioms": sorted(
        used & {"Classical.choice", "propext", "Quot.sound"}
    ),
    "generated_trust_declaration_count": len(generated_allowlist),
}
print(json.dumps(result, indent=2, sort_keys=True))
