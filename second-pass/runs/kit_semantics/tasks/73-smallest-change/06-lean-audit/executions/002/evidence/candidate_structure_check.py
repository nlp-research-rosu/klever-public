#!/usr/bin/env python3
"""Check candidate source policy, exact target identity, and immutable Base copy."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.klean_final_gate import _candidate_gate


generation = Path("/reference/klean-generation")
candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/lean-audit-project.rwO5Kz")
manifest = json.loads((generation / "generator-manifest.json").read_text())
target = manifest["target"]

_candidate_gate(candidate, target)
proof = (candidate / "Proof.lean").read_text()
fresh_proof = (fresh / "Proof.lean").read_text()
declaration_pattern = re.compile(
    r"(?m)^\s*(?:noncomputable\s+)?(?:def|theorem|axiom|opaque)\s+"
    r"(?:Klean73SmallestChange\.Lemmas\.)?targetStatement\b"
)
forbidden = re.findall(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", proof)

print(json.dumps({
    "trusted_candidate_gate": "PASS",
    "candidate_proof_sha256": hashlib.sha256(proof.encode()).hexdigest(),
    "fresh_proof_sha256": hashlib.sha256(fresh_proof.encode()).hexdigest(),
    "fresh_proof_exact_copy": proof == fresh_proof,
    "fresh_base_tree_sha256": klean_export.tree_digest(fresh / "Base"),
    "immutable_generated_tree_sha256": klean_export.tree_digest(generation / "generated"),
    "fresh_base_exact_copy_after_build": klean_export.tree_digest(fresh / "Base") == klean_export.tree_digest(generation / "generated"),
    "fresh_target_exact": klean_export.target_statement(fresh / "Base") == target,
    "candidate_target_declarations": declaration_pattern.findall(proof),
    "candidate_shadows_target": bool(declaration_pattern.search(proof)),
    "candidate_forbidden_tokens": forbidden,
    "proof_final_occurrences": len(re.findall(r"(?m)^\s*theorem\s+final\s*:", proof)),
    "parameter_count": len(target["parameters"]),
}, indent=2, sort_keys=True))
