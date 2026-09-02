#!/usr/bin/env python3
"""Reconcile the exact #print axioms output with the trusted inventory."""

from __future__ import annotations

import json
from pathlib import Path

from tools.klean_final_gate import _allowed_axioms, _parse_axioms


output = Path("/audit-output/evidence/09-print-axioms.log").read_text()
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
used = _parse_axioms(output)
generated_allowlist = {
    entry["name"] for entry in inventory["allowlist"]
}
lean_core_baseline = {"Classical.choice", "propext", "Quot.sound"}
trusted_gate_allowlist = _allowed_axioms(inventory)
unrecorded_escape = used - generated_allowlist - lean_core_baseline
accounting = {
    name: (
        "generated trust-inventory allowlist"
        if name in generated_allowlist
        else "Lean core logical baseline explicitly accepted by trusted final gate"
    )
    for name in sorted(used)
}
checks = {
    "exact_output_names": used == {"propext", "Quot.sound"},
    "sorryAx_absent": "sorryAx" not in used,
    "no_unrecorded_proof_trust_escape": not unrecorded_escape,
    "all_used_are_accepted_by_trusted_gate": used <= trusted_gate_allowlist,
    "no_generated_axiom_is_used": not (used & generated_allowlist),
    "command_exit_zero": 'COMMAND_EXIT_CODE="0"' in output,
}
checks["all_checks_pass"] = all(checks.values())
result = {
    "checks": checks,
    "used_axioms": sorted(used),
    "accounting": accounting,
    "generated_allowlist_count": len(generated_allowlist),
    "used_generated_axioms": sorted(used & generated_allowlist),
    "lean_core_baseline": sorted(lean_core_baseline),
    "unrecorded_escape": sorted(unrecorded_escape),
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if checks["all_checks_pass"] else 1)
