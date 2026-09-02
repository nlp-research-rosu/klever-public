#!/usr/bin/env python3
import json
import re
from pathlib import Path

from tools import klean_export


inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
axiom_output = Path("/audit-output/evidence/12-print-axioms.txt").read_text()
match = re.search(r"depends on axioms: \[(.*?)\]", axiom_output)
if match is None:
    raise SystemExit("cannot parse #print axioms output")
dependencies = [item.strip() for item in match.group(1).split(",") if item.strip()]

generated = Path("/reference/klean-generation/generated")
generated_declarations = {
    declaration["name"]: {
        "kind": declaration["kind"],
        "type": declaration["type"],
    }
    for source in generated.rglob("*.lean")
    for declaration in klean_export.lean_trust_declarations(source)
}
allowlist = {
    entry["name"]: {"kind": entry["kind"], "type": entry["type"]}
    for entry in inventory["allowlist"]
}
candidate_declarations = [
    declaration
    for source in (Path("/candidate/Proof.lean"), Path("/candidate/lakefile.lean"))
    for declaration in klean_export.lean_trust_declarations(source)
]

print("PRINT_AXIOMS_DEPENDENCIES", json.dumps(dependencies))
print("SORRYAX_PRESENT", "sorryAx" in dependencies)
print("GENERATED_DECLARATIONS_EQUAL_ALLOWLIST", generated_declarations == allowlist)
print("GENERATED_ALLOWLIST_COUNT", len(allowlist))
print(
    "FINAL_GENERATED_ALLOWLIST_DEPENDENCIES",
    json.dumps(sorted(set(dependencies) & set(allowlist))),
)
print("CANDIDATE_TRUST_DECLARATIONS", json.dumps(candidate_declarations))
print("INVENTORY_DESIGNATED_SORRIES", inventory["designated_sorries"])
print("INVENTORY_OTHER_SORRIES", inventory["other_sorries"])

core = {
    "propext": "Lean core propositional extensionality",
    "Classical.choice": "Lean core classical choice",
    "Quot.sound": "Lean core quotient soundness",
}
for dependency in dependencies:
    classification = (
        core[dependency]
        if dependency in core
        else (
            "recorded generated declaration"
            if dependency in allowlist
            else "UNRECORDED"
        )
    )
    print(f"{dependency}: {classification}")

unrecorded = [
    dependency
    for dependency in dependencies
    if dependency not in core and dependency not in allowlist
]
print("UNRECORDED_PROOF_TRUST_ESCAPES", json.dumps(unrecorded))
