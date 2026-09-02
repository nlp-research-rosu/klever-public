#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import pipeline_contract
from tools.klean_export import target_statement, tree_digest


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/stage5-audit.VpzibW")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
manifest = json.loads((generation / "generator-manifest.json").read_text())
target = manifest["target"]
proof = (candidate / "Proof.lean").read_text()

candidate_sources = {
    str(path.relative_to(candidate)): path.read_text()
    for path in candidate.rglob("*.lean")
    if "Base" not in path.relative_to(candidate).parts
}

parameter_counts = {}
for parameter in target["parameters"]:
    name = parameter["name"]
    parameter_counts[name] = sum(
        len(
            re.findall(
                rf"(?m)^\s*(?:noncomputable\s+)?def\s+{re.escape(name)}"
                rf"\s*(?::|\()",
                text,
            )
        )
        for text in candidate_sources.values()
    )

theorem_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    proof,
)
proof_statement = theorem_matches[0] if len(theorem_matches) == 1 else ""
normalize = lambda text: " ".join(text.split())

forbidden_occurrences = []
for relative, text in candidate_sources.items():
    for match in re.finditer(
        r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text
    ):
        forbidden_occurrences.append(
            {"file": relative, "token": match.group(0), "offset": match.start()}
        )

shadow_occurrences = []
for relative, text in candidate_sources.items():
    for match in re.finditer(
        r"(?m)^\s*(?:def|theorem|axiom|opaque|abbrev|inductive|structure|class)"
        r"\s+(?:Klean106F\.Lemmas\.)?targetStatement\b",
        text,
    ):
        shadow_occurrences.append(
            {"file": relative, "offset": match.start()}
        )

target_source = (
    fresh / "Base" / target["file"]
).read_text()
target_definition_count = len(
    re.findall(r"(?m)^\s*def\s+targetStatement\b", target_source)
)
fresh_target = target_statement(fresh / "Base")

checks = {
    "audit_mode_is_proof": audit["mode"] == "CLASSIFICATION_AND_PROOF",
    "candidate_pipeline_tree_matches_audit_input": (
        pipeline_contract.sha256_tree(candidate)
        == audit["hashes"]["lean_workspace_sha256"]
    ),
    "candidate_proof_copied_exactly_to_fresh_project": (
        sha(candidate / "Proof.lean") == sha(fresh / "Proof.lean")
    ),
    "candidate_lakefile_copied_exactly_to_fresh_project": (
        sha(candidate / "lakefile.lean") == sha(fresh / "lakefile.lean")
    ),
    "candidate_toolchain_copied_exactly_to_fresh_project": (
        sha(candidate / "lean-toolchain") == sha(fresh / "lean-toolchain")
    ),
    "fresh_base_tree_is_exact_generated_tree": (
        tree_digest(fresh / "Base")
        == tree_digest(generated)
        == manifest["generated_tree_sha256"]
        == audit["hashes"]["generated_tree_sha256"]
    ),
    "fresh_base_has_one_target_declaration": target_definition_count == 1,
    "fresh_target_matches_generator_manifest": fresh_target == target,
    "fresh_target_matches_audit_input": fresh_target == audit["target"],
    "target_definition_hash_matches": (
        fresh_target["definition_sha256"] == target["definition_sha256"]
    ),
    "target_statement_hash_matches": (
        hashlib.sha256(target["statement"].encode()).hexdigest()
        == target["statement_sha256"]
    ),
    "candidate_defines_every_parameter_exactly_once": (
        all(count == 1 for count in parameter_counts.values())
        and len(parameter_counts) == len(target["parameters"])
    ),
    "candidate_has_exactly_one_final": len(theorem_matches) == 1,
    "final_statement_is_exact_fixed_target": (
        normalize(proof_statement) == normalize(target["statement"])
    ),
    "candidate_does_not_shadow_target": not shadow_occurrences,
    "candidate_has_no_forbidden_tokens": not forbidden_occurrences,
}

print("$ PYTHONPATH=/reference python3 /audit-output/evidence/check_candidate_target_identity.py")
print("CANDIDATE_HASHES")
print(
    json.dumps(
        {
            "pipeline_tree_actual": pipeline_contract.sha256_tree(candidate),
            "pipeline_tree_expected": audit["hashes"]["lean_workspace_sha256"],
            "klean_tree_actual": tree_digest(candidate),
            "Proof.lean_sha256": sha(candidate / "Proof.lean"),
        },
        indent=2,
        sort_keys=True,
    )
)
print("PARAMETER_DEFINITION_COUNTS")
print(json.dumps(parameter_counts, indent=2, sort_keys=True))
print("FORBIDDEN_OCCURRENCES")
print(json.dumps(forbidden_occurrences, indent=2, sort_keys=True))
print("TARGET_SHADOW_OCCURRENCES")
print(json.dumps(shadow_occurrences, indent=2, sort_keys=True))
print("FINAL_STATEMENT")
print(proof_statement.strip())
print("FIXED_TARGET_STATEMENT")
print(target["statement"])
print("CHECKS")
print(json.dumps(checks, indent=2, sort_keys=True))
passed = all(checks.values())
print("RESULT=" + ("PASS" if passed else "FAIL"))
raise SystemExit(0 if passed else 1)
