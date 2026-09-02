import json
import re
from pathlib import Path

from tools.klean_final_gate import _allowed_axioms


manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
gate = json.loads(
    Path("/audit-output/evidence/12_mechanical_final_gate.json").read_text()
)
proof_text = Path("/candidate/Proof.lean").read_text()

expected_definitions = {
    "«_-Int_»": "def «_-Int_» (x y : SortInt) : SortInt := x - y",
    "_andBool_": (
        "def _andBool_ (x y : SortBool) : SortBool := x && y"
    ),
    "«_>=Int_»": (
        "def «_>=Int_» (x y : SortInt) : SortBool := decide (x >= y)"
    ),
    "«_<Int_»": (
        "def «_<Int_» (x y : SortInt) : SortBool := decide (x < y)"
    ),
    "«_<=Int_»": (
        "def «_<=Int_» (x y : SortInt) : SortBool := decide (x <= y)"
    ),
    "«_==Int_»": (
        "def «_==Int_» (x y : SortInt) : SortBool := decide (x = y)"
    ),
    "«_+Int_»": "def «_+Int_» (x y : SortInt) : SortInt := x + y",
    "«_*Int_»": "def «_*Int_» (x y : SortInt) : SortInt := x * y",
}
hook_meanings = {
    "Lbl'Unds'-Int'Unds'": "INT.sub / unbounded integer subtraction",
    "Lbl'Unds'andBool'Unds'": "BOOL.and / Boolean conjunction",
    "Lbl'Unds-GT-Eqls'Int'Unds'": "INT.ge / integer greater-or-equal",
    "Lbl'Unds-LT-'Int'Unds'": "INT.lt / integer strict less-than",
    "Lbl'Unds-LT-Eqls'Int'Unds'": "INT.le / integer less-or-equal",
    "Lbl'UndsEqlsEqls'Int'Unds'": "INT.eq / integer equality",
    "Lbl'UndsPlus'Int'Unds'": "INT.add / unbounded integer addition",
    "Lbl'UndsStar'Int'Unds'": "INT.mul / unbounded integer multiplication",
}

candidate_lines = {
    match.group(1): match.group(0).strip()
    for match in re.finditer(
        r"(?m)^def\s+(\S+)\s+\([^\n]+\)\s*:[^\n]+$",
        proof_text,
    )
}
bridge_records = []
for parameter in manifest["target"]["parameters"]:
    name = parameter["name"]
    bridge_records.append(
        {
            **parameter,
            "k_hook_meaning": hook_meanings[parameter["kore_symbol"]],
            "candidate_definition": candidate_lines.get(name),
            "expected_candidate_definition": expected_definitions[name],
            "definition_exact": (
                candidate_lines.get(name) == expected_definitions[name]
            ),
        }
    )

used = set(gate["used_axioms"])
inventory_names = {
    entry["name"] for entry in inventory["allowlist"]
}
foundational = {"Classical.choice", "propext", "Quot.sound"}
allowed = _allowed_axioms(inventory)

report = {
    "axiom_reconciliation": {
        "used_axioms": sorted(used),
        "used_generated_inventory_axioms": sorted(used & inventory_names),
        "used_standard_lean_foundational_axioms": sorted(
            used & foundational
        ),
        "unexpected_axioms": sorted(used - allowed),
        "depends_on_sorryAx": "sorryAx" in used,
        "generated_inventory_count": len(inventory_names),
        "unused_generated_inventory_count": len(inventory_names - used),
    },
    "operational_bridge": {
        "parameter_count": len(manifest["target"]["parameters"]),
        "candidate_definition_count": len(candidate_lines),
        "all_eight_exact": (
            len(bridge_records) == 8
            and all(record["definition_exact"] for record in bridge_records)
        ),
        "records": bridge_records,
    },
}

print(json.dumps(report, indent=2, sort_keys=True))
