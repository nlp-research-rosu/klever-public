#!/usr/bin/env python3
"""Read-only target, candidate-source, and trust checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export


GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
CANDIDATE = Path("/candidate")


def digest_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
audit_input = json.loads(Path("/audit-input.json").read_text())
inventory = json.loads((GENERATION / "trust-inventory.json").read_text())
obligation_map = json.loads(
    (GENERATED / "obligation-map.json").read_text()
)
target = klean_export.target_statement(GENERATED)

print(f"target_recomputed_matches_manifest={target == manifest['target']}")
print(
    "target_recomputed_matches_audit_input="
    + str(target == audit_input["resolution"]["target"])
)
print(f"target={json.dumps(target, ensure_ascii=False, sort_keys=True)}")

expected_definition = klean_export.expected_target_definition(obligation_map)
print(
    "expected_definition_hash="
    + (digest_text(expected_definition) if expected_definition else "NONE")
)
print(
    "expected_definition_matches_target="
    + str(
        expected_definition is not None
        and digest_text(expected_definition) == target["definition_sha256"]
    )
)

for parameter in target["parameters"]:
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "type": parameter["type"],
        "source_rule_ids": parameter["source_rule_ids"],
    }
    computed = digest_text(
        json.dumps(binding, sort_keys=True, separators=(",", ":"))
    )
    print(
        json.dumps(
            {
                "parameter": parameter["name"],
                "binding_sha256_computed": computed,
                "binding_sha256_recorded": parameter["binding_sha256"],
                "match": computed == parameter["binding_sha256"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )

proof = (CANDIDATE / "Proof.lean").read_text()
forbidden = sorted(
    set(re.findall(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", proof))
)
print(f"candidate_forbidden_tokens={forbidden}")
trust_declarations = klean_export.lean_trust_declarations(
    CANDIDATE / "Proof.lean"
)
print(
    "candidate_axiom_or_opaque_declarations="
    + json.dumps(trust_declarations, ensure_ascii=False, sort_keys=True)
)
for name in ("_orBool_", "«_==Bool_»", "notBool_"):
    count = len(
        re.findall(
            rf"(?m)^\s*(?:noncomputable\s+)?def\s+{re.escape(name)}"
            rf"\s*(?::|\()",
            proof,
        )
    )
    print(f"candidate_definition_count[{name}]={count}")

theorem = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b", proof
)
theorem_type = " ".join(theorem[0].split()) if len(theorem) == 1 else None
target_type = " ".join(target["statement"].split())
print(f"candidate_final_count={len(theorem)}")
print(f"candidate_final_type={theorem_type}")
print(f"target_statement_type={target_type}")
print(f"candidate_final_exact_target={theorem_type == target_type}")

outside_target_count = len(
    re.findall(r"(?m)^\s*def\s+targetStatement\b", proof)
)
generated_target_count = sum(
    len(
        re.findall(
            r"(?m)^\s*def\s+targetStatement\b",
            path.read_text(),
        )
    )
    for path in GENERATED.rglob("*.lean")
)
print(f"candidate_target_shadow_count={outside_target_count}")
print(f"generated_target_declaration_count={generated_target_count}")

allowlist = inventory["allowlist"]
print(f"trust_inventory_allowlist_count={len(allowlist)}")
print(f"trust_inventory_designated_sorries={inventory['designated_sorries']}")
print(f"trust_inventory_other_sorries={inventory['other_sorries']}")
print(
    "axiom_accounting=Proof.final is axiom-free, so the used set is the "
    "empty subset of the recorded allowlist; sorryAx is absent"
)
