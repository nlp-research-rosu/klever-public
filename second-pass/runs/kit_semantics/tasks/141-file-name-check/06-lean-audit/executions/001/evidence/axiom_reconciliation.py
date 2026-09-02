#!/usr/bin/env python3
import json
from pathlib import Path

from tools.klean_final_gate import _allowed_axioms, _parse_axioms


output = Path(
    "/audit-output/evidence/11-print-axioms-and-final.log"
).read_text()
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
used = _parse_axioms(output)
allowed = _allowed_axioms(inventory)
generated_names = {
    entry["name"] for entry in inventory["allowlist"]
}
standard_core_allowance = {
    "Classical.choice",
    "propext",
    "Quot.sound",
}
unexpected = sorted(used - allowed)
checks = {
    "sorryAx_absent": "sorryAx" not in used,
    "all_used_axioms_allowed_by_trusted_gate": not unexpected,
    "standard_core_allowance_matches_gate_delta": (
        allowed - generated_names == standard_core_allowance
    ),
    "no_generated_trust_dependency_used": not (used & generated_names),
}
result = {
    "used_axioms": sorted(used),
    "generated_trust_inventory_count": len(generated_names),
    "used_generated_trust_declarations": sorted(used & generated_names),
    "standard_core_allowance": sorted(standard_core_allowance),
    "unexpected": unexpected,
    "checks": checks,
    "overall": "PASS" if all(checks.values()) else "FAIL",
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if all(checks.values()) else 1)
