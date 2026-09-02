#!/usr/bin/env python3
"""Check target preservation, candidate declarations, and trust accounting."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export


generation = Path("/reference/klean-generation")
candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/lean-proof-audit")
manifest = json.loads((generation / "generator-manifest.json").read_text())
trust_inventory = json.loads((generation / "trust-inventory.json").read_text())
target = manifest["target"]

candidate_sources = [
    path
    for path in candidate.rglob("*.lean")
    if "Base" not in path.relative_to(candidate).parts
    and ".lake" not in path.relative_to(candidate).parts
]
candidate_text = "\n".join(path.read_text() for path in candidate_sources)
forbidden = re.findall(
    r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", candidate_text
)

parameter_declaration_counts = {}
for parameter in target["parameters"]:
    name = parameter["name"]
    parameter_declaration_counts[name] = sum(
        len(
            re.findall(
                rf"(?m)^\s*(?:noncomputable\s+)?def\s+{re.escape(name)}"
                rf"\s*(?::|\()",
                path.read_text(),
            )
        )
        for path in candidate_sources
    )

fresh_base_target = klean_export.target_statement(fresh / "Base")
source_copy_hashes = {}
for name in ("Proof.lean", "lake-manifest.json", "lakefile.lean", "lean-toolchain"):
    original = hashlib.sha256((candidate / name).read_bytes()).hexdigest()
    copied = hashlib.sha256((fresh / name).read_bytes()).hexdigest()
    source_copy_hashes[name] = {
        "candidate": original,
        "fresh_copy": copied,
        "match": original == copied,
    }

axiom_output = Path(
    "/audit-output/evidence/06-lean-axiom-and-bridge-audits.log"
).read_text(errors="replace")
used_axioms: list[str] = []
axiom_free = "'Proof.final' does not depend on any axioms" in axiom_output
allowlisted_axioms = {
    entry["name"] for entry in trust_inventory["allowlist"]
}
allowlisted_axioms.update({"Classical.choice", "propext", "Quot.sound"})

theorem_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    (candidate / "Proof.lean").read_text(),
)
normalized_theorem = (
    " ".join(theorem_matches[0].split()) if len(theorem_matches) == 1 else None
)
normalized_target = " ".join(target["statement"].split())

checks = {
    "fresh_base_tree_matches_generated": klean_export.tree_digest(fresh / "Base")
    == klean_export.tree_digest(generation / "generated"),
    "fresh_base_target_matches_manifest": fresh_base_target == target,
    "candidate_does_not_define_targetStatement": not re.search(
        r"(?m)^\s*def\s+targetStatement\b", candidate_text
    ),
    "candidate_parameter_defs_exactly_once": all(
        count == 1 for count in parameter_declaration_counts.values()
    ),
    "candidate_forbidden_tokens_absent": forbidden == [],
    "candidate_source_copy_hashes_match": all(
        row["match"] for row in source_copy_hashes.values()
    ),
    "proof_final_exactly_once": len(theorem_matches) == 1,
    "proof_final_exact_target": normalized_theorem == normalized_target,
    "proof_final_axiom_free": axiom_free and used_axioms == [],
    "sorryAx_absent": "sorryAx" not in used_axioms,
    "unrecorded_axioms_absent": set(used_axioms) <= allowlisted_axioms,
}
failed_checks = sorted(name for name, passed in checks.items() if not passed)
result = {
    "checks": checks,
    "failed_checks": failed_checks,
    "parameter_declaration_counts": parameter_declaration_counts,
    "forbidden_tokens": forbidden,
    "source_copy_hashes": source_copy_hashes,
    "used_axioms": used_axioms,
    "trust_allowlist_count": len(trust_inventory["allowlist"]),
    "target": fresh_base_target,
}
output = Path("/audit-output/evidence/09-candidate-target-checks.json")
output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
if failed_checks:
    raise SystemExit(1)
