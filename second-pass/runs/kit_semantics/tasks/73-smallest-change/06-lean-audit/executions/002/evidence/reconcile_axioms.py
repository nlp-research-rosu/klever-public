#!/usr/bin/env python3
"""Parse Proof.final dependencies and reconcile them with Stage 4 trust inventory."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import _allowed_axioms, _parse_axioms


output = Path("/audit-output/evidence/11-proof-print-axioms.txt").read_text()
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
used = _parse_axioms(output)
allowed = _allowed_axioms(inventory)
entries = {
    entry["name"]: entry
    for entry in inventory["allowlist"]
    if entry.get("name") in used
}
builtins = {"Classical.choice", "propext", "Quot.sound"}

print(json.dumps({
    "used_axioms": sorted(used),
    "used_count": len(used),
    "sorryAx_present": "sorryAx" in used,
    "unrecorded": sorted(used - allowed),
    "recorded_generated_axioms": [entries[name] for name in sorted(entries)],
    "lean_builtin_trust": sorted(used & builtins),
    "all_reconciled": "sorryAx" not in used and not (used - allowed),
}, indent=2, sort_keys=True))
