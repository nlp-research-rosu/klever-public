#!/usr/bin/env python3
"""Final independent target, shadowing, and candidate-source checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.klean_final_gate import _candidate_gate


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


generation = Path("/reference/klean-generation")
generated = generation / "generated"
candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/68-pluck-proof-audit-001")
fresh_base = fresh / "Base"
manifest = json.loads((generation / "generator-manifest.json").read_text())
audit_input = json.loads(Path("/audit-input.json").read_text())
target = manifest["target"]

# Re-run the trusted structural candidate check.  It requires one exact def
# for every target parameter, the exact theorem final type, and rejects the
# forbidden token set in every non-Base Lean source.
_candidate_gate(candidate, target)

candidate_lean = [
    path
    for path in candidate.rglob("*.lean")
    if "Base" not in path.relative_to(candidate).parts
]
fresh_candidate_lean = [
    path
    for path in fresh.rglob("*.lean")
    if "Base" not in path.relative_to(fresh).parts
]
forbidden = re.compile(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b")
shadow = re.compile(
    r"(?m)^\s*(?:def|theorem|lemma|axiom|opaque)\s+targetStatement\b"
)

candidate_texts = {
    path.relative_to(candidate).as_posix(): path.read_text()
    for path in candidate_lean
}
fresh_texts = {
    path.relative_to(fresh).as_posix(): path.read_text()
    for path in fresh_candidate_lean
}
candidate_forbidden = {
    name: sorted(set(forbidden.findall(text)))
    for name, text in candidate_texts.items()
    if forbidden.search(text)
}
candidate_target_shadows = [
    name for name, text in candidate_texts.items() if shadow.search(text)
]

generated_target = klean_export.target_statement(generated)
fresh_target = klean_export.target_statement(fresh_base)
result = {
    "trusted_candidate_structure_check": "PASS",
    "candidate_non_base_lean_files": sorted(candidate_texts),
    "candidate_forbidden_tokens": candidate_forbidden,
    "candidate_target_statement_shadows": candidate_target_shadows,
    "candidate_proof_sha256": sha256_file(candidate / "Proof.lean"),
    "fresh_copy_proof_sha256": sha256_file(fresh / "Proof.lean"),
    "proof_copy_exact": (
        sha256_file(candidate / "Proof.lean")
        == sha256_file(fresh / "Proof.lean")
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "fresh_base_tree_sha256_after_clean_build": (
        klean_export.tree_digest(fresh_base)
    ),
    "fresh_base_exactly_generated_after_clean_build": (
        klean_export.tree_digest(generated)
        == klean_export.tree_digest(fresh_base)
    ),
    "generated_target": generated_target,
    "fresh_base_target": fresh_target,
    "fresh_base_target_exact": fresh_target == generated_target,
    "target_exactly_manifest_and_audit_input": (
        generated_target
        == target
        == audit_input["resolution"]["target"]
        == audit_input["resolution"]["stage4_preflight"]["target"]
    ),
    "operational_bridge_audit_sha256": sha256_file(
        fresh / "OperationalBridgeAudit.lean"
    ),
}
result["all_checks_pass"] = all(
    (
        result["trusted_candidate_structure_check"] == "PASS",
        not result["candidate_forbidden_tokens"],
        not result["candidate_target_statement_shadows"],
        result["proof_copy_exact"],
        result["fresh_base_exactly_generated_after_clean_build"],
        result["fresh_base_target_exact"],
        result["target_exactly_manifest_and_audit_input"],
    )
)
print(json.dumps(result, indent=2, sort_keys=True))
