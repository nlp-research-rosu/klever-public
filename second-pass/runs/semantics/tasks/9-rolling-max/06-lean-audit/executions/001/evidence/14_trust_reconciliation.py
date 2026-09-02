#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import _allowed_axioms, _parse_axioms
from tools.klean_preflight import _lean_sources, _trust_declarations


generation = Path("/reference/klean-generation")
generated = generation / "generated"
inventory = json.loads((generation / "trust-inventory.json").read_text())
axiom_output = Path("/audit-output/evidence/10_print_axioms.log").read_text()

declared = _trust_declarations(_lean_sources(generated))
recorded = {
    entry["name"]: (entry["kind"], entry["type"])
    for entry in inventory["allowlist"]
}
used = _parse_axioms(axiom_output)
allowed = _allowed_axioms(inventory)

result = {
    "generated_trust_declaration_count": len(declared),
    "recorded_allowlist_count": len(recorded),
    "generated_declarations_equal_recorded_allowlist": declared == recorded,
    "used_axioms": sorted(used),
    "used_axioms_recorded_or_lean_core": sorted(used & allowed),
    "unexpected_axioms": sorted(used - allowed),
    "sorryAx_used": "sorryAx" in used,
    "proof_is_axiom_free": not used,
    "candidate_adds_no_trust_declarations": True,
    "candidate_static_evidence": "07_candidate_static.log",
}
result["trust_reconciliation_pass"] = (
    declared == recorded
    and not (used - allowed)
    and "sorryAx" not in used
    and not used
)
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["trust_reconciliation_pass"] else 1)
