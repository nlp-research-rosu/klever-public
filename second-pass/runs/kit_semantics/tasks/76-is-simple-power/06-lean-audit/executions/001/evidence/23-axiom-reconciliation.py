#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.klean_export import lean_trust_declarations


axiom_output = Path(
    "/audit-output/evidence/14-print-axioms-proof-final.txt"
).read_text()
match = re.search(
    r"'Proof\.final' depends on axioms: \[([^\]]*)\]",
    axiom_output,
)
if match is None:
    raise AssertionError("could not parse exact #print axioms output")
dependencies = {
    name.strip()
    for name in match.group(1).split(",")
    if name.strip()
}

inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
recorded_project_trust = {
    entry["name"] for entry in inventory["allowlist"]
}
candidate_declarations = lean_trust_declarations(
    Path("/tmp/audit-work/lean-proof-audit/Proof.lean")
)

foundational = {"propext", "Classical.choice", "Quot.sound"}
print(f"Proof.final dependencies={sorted(dependencies)}")
print(f"Lean foundational dependencies={sorted(dependencies & foundational)}")
print(
    "recorded generated trust dependencies="
    f"{sorted(dependencies & recorded_project_trust)}"
)
print(f"recorded generated trust declarations={len(recorded_project_trust)}")
print(f"candidate trust declarations={candidate_declarations}")
print(f"sorryAx present={'sorryAx' in dependencies}")

if dependencies != foundational:
    raise AssertionError("unexpected axiom dependency")
if dependencies & recorded_project_trust:
    raise AssertionError("Proof.final depends on generated project trust")
if candidate_declarations:
    raise AssertionError("candidate introduced axiom or opaque declaration")
if "sorryAx" in dependencies:
    raise AssertionError("Proof.final depends on sorryAx")
