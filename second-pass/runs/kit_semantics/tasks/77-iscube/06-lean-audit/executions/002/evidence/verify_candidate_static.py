#!/usr/bin/env python3
"""Static target-identity and forbidden-trust checks for the fresh proof copy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

from tools import klean_export


fresh = Path("/tmp/audit-work/lean-proof-audit-77-001")
base = fresh / "Base"
manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text(
        encoding="utf-8"
    )
)
audit_input = json.loads(Path("/audit-input.json").read_text(encoding="utf-8"))
target = klean_export.target_statement(base)

candidate_sources = [
    path
    for path in fresh.rglob("*.lean")
    if "Base" not in path.relative_to(fresh).parts
    and path.name != "AuditAxioms.lean"
]
forbidden_pattern = re.compile(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b")
forbidden_hits = [
    {
        "file": path.relative_to(fresh).as_posix(),
        "token": match.group(0),
        "offset": match.start(),
    }
    for path in candidate_sources
    for match in forbidden_pattern.finditer(path.read_text(encoding="utf-8"))
]
proof_path = fresh / "Proof.lean"
proof_text = proof_path.read_text(encoding="utf-8")
definition_counts = {}
for parameter in target["parameters"]:
    name = parameter["name"]
    matches = re.findall(
        rf"(?m)^\s*(?:@\[[^\n]*\]\s*)*"
        rf"(?:noncomputable\s+)?def\s+{re.escape(name)}\s*(?::|\()",
        proof_text,
    )
    definition_counts[name] = len(matches)

theorem_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    proof_text,
)
normalized_final = (
    " ".join(theorem_matches[0].split()) if len(theorem_matches) == 1 else None
)
normalized_target = " ".join(target["statement"].split())

copied_source_hashes = {}
for name in ("Proof.lean", "lakefile.lean", "lake-manifest.json", "lean-toolchain"):
    source = Path("/candidate") / name
    copied = fresh / name
    copied_source_hashes[name] = {
        "candidate": hashlib.sha256(source.read_bytes()).hexdigest(),
        "fresh_copy": hashlib.sha256(copied.read_bytes()).hexdigest(),
        "matches": source.read_bytes() == copied.read_bytes(),
    }

result = {
    "fresh_base_tree_sha256": klean_export.tree_digest(base),
    "reference_generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "target_recomputed": target,
    "target_equals_generator_manifest": target == manifest["target"],
    "target_equals_audit_input": target == audit_input["resolution"]["target"],
    "forbidden_candidate_tokens": forbidden_hits,
    "target_statement_definitions_outside_base": len(
        re.findall(r"(?m)^\s*def\s+targetStatement\b", proof_text)
    ),
    "klean_namespace_declarations_outside_base": len(
        re.findall(r"(?m)^\s*namespace\s+Klean77Iscube(?:\.|\s|$)", proof_text)
    ),
    "parameter_definition_counts": definition_counts,
    "final_theorem_declaration_count": len(theorem_matches),
    "final_statement_normalized": normalized_final,
    "fixed_statement_normalized": normalized_target,
    "final_statement_exact_match": normalized_final == normalized_target,
    "copied_candidate_source_hashes": copied_source_hashes,
}
result["all_static_checks_pass"] = (
    result["fresh_base_tree_sha256"]
    == result["reference_generated_tree_sha256"]
    and result["target_equals_generator_manifest"]
    and result["target_equals_audit_input"]
    and not forbidden_hits
    and result["target_statement_definitions_outside_base"] == 0
    and result["klean_namespace_declarations_outside_base"] == 0
    and all(count == 1 for count in definition_counts.values())
    and result["final_statement_exact_match"]
    and all(item["matches"] for item in copied_source_hashes.values())
)
print(json.dumps(result, indent=2, sort_keys=False))
