#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, klean_final_gate, pipeline_contract


generation = Path("/reference/klean-generation")
candidate = Path("/candidate")
manifest = json.loads((generation / "generator-manifest.json").read_text())
inventory = json.loads((generation / "trust-inventory.json").read_text())
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
target = manifest["target"]

klean_final_gate._candidate_gate(candidate, target)
proof_text = (candidate / "Proof.lean").read_text()
forbidden = []
for path in sorted(candidate.rglob("*.lean")):
    for match in re.finditer(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", path.read_text()):
        forbidden.append({
            "file": path.relative_to(candidate).as_posix(),
            "token": match.group(),
        })

axiom_output = Path("/audit-output/evidence/42_print_axioms.txt").read_text()
used_axioms = klean_final_gate._parse_axioms(axiom_output)
allowed_axioms = klean_final_gate._allowed_axioms(inventory)

theorem_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    proof_text,
)
normalize = lambda text: " ".join(text.split())
candidate_tree = pipeline_contract.sha256_tree(candidate)

print(json.dumps({
    "candidate_gate": "PASS",
    "forbidden_tokens": forbidden,
    "target_declaration_shadowed": bool(re.search(
        r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b",
        proof_text,
    )),
    "proof_final_count": len(theorem_matches),
    "proof_final_statement": theorem_matches[0] if theorem_matches else None,
    "generator_target_statement": target["statement"],
    "exact_normalized_statement_match": (
        len(theorem_matches) == 1
        and normalize(theorem_matches[0]) == normalize(target["statement"])
    ),
    "candidate_tree_sha256_actual": candidate_tree,
    "candidate_tree_sha256_audit": audit["hashes"]["lean_workspace_sha256"],
    "candidate_tree_sha256_match": (
        candidate_tree == audit["hashes"]["lean_workspace_sha256"]
    ),
    "used_axioms": sorted(used_axioms),
    "allowed_axioms": sorted(allowed_axioms),
    "sorryAx_present": "sorryAx" in used_axioms,
    "unrecorded_axioms": sorted(used_axioms - allowed_axioms),
    "trust_inventory_sha256": hashlib.sha256(
        (generation / "trust-inventory.json").read_bytes()
    ).hexdigest(),
    "fresh_base_tree_sha256": klean_export.tree_digest(
        Path("/tmp/audit-work/lean-audit-DaSChT/Base")
    ),
    "generated_tree_sha256": manifest["generated_tree_sha256"],
}, indent=2, sort_keys=True))
