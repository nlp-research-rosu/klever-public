#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

from tools.klean_final_gate import _parse_axioms


project = Path("/tmp/audit-work/stage5-clean-project")
result = subprocess.run(
    ["lake", "env", "lean", "AxiomAudit.lean"],
    cwd=project,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
if result.returncode != 0:
    raise SystemExit(result.returncode)

used = _parse_axioms(result.stdout)
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
allowlist = {entry["name"]: entry for entry in inventory["allowlist"]}
standard = {
    "Classical.choice": {
        "kind": "Lean standard",
        "reason": "classical choice",
    },
    "propext": {
        "kind": "Lean standard",
        "reason": "propositional extensionality",
    },
    "Quot.sound": {
        "kind": "Lean standard",
        "reason": "quotient soundness",
    },
}
reconciled = []
unexpected = []
for name in sorted(used):
    if name in allowlist:
        reconciled.append(
            {
                "name": name,
                "recorded": True,
                "inventory_entry": allowlist[name],
            }
        )
    elif name in standard:
        reconciled.append(
            {
                "name": name,
                "recorded": True,
                **standard[name],
            }
        )
    else:
        unexpected.append(name)
        reconciled.append({"name": name, "recorded": False})

summary = {
    "used_axiom_count": len(used),
    "used_axioms": sorted(used),
    "reconciled": reconciled,
    "sorryAx_present": "sorryAx" in used,
    "unexpected_axioms": unexpected,
    "status": (
        "PASS"
        if "sorryAx" not in used and not unexpected
        else "FAIL"
    ),
}
print(json.dumps(summary, indent=2, sort_keys=True))
