#!/usr/bin/env python3
"""Static target, trust, and candidate-source checks for the fresh Lean audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, klean_preflight


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/proof-audit")
reference_generated = Path("/reference/klean-generation/generated")
fresh_base = fresh / "Base"
generation = Path("/reference/klean-generation")

candidate_sources = sorted(
    path
    for path in candidate.rglob("*.lean")
    if "Base" not in path.relative_to(candidate).parts
)
candidate_text = {
    path.relative_to(candidate).as_posix(): path.read_text(encoding="utf-8")
    for path in candidate_sources
}

forbidden = {}
for name, text in candidate_text.items():
    findings = {
        token: [match.start() for match in re.finditer(rf"\b{token}\b", text)]
        for token in ("sorry", "admit", "unsafe")
    }
    findings["target_declaration"] = [
        match.start()
        for match in re.finditer(
            r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b",
            text,
        )
    ]
    forbidden[name] = findings

candidate_trust = [
    {**entry, "source": path.relative_to(candidate).as_posix()}
    for path in candidate_sources
    for entry in klean_export.lean_trust_declarations(path)
]

generated_sources = klean_preflight._lean_sources(fresh_base)
generated_trust = klean_preflight._trust_declarations(generated_sources)
trust_inventory = load(generation / "trust-inventory.json")
allowlist = {
    entry["name"]: (entry["kind"], entry["type"])
    for entry in trust_inventory["allowlist"]
}

generator_manifest = load(generation / "generator-manifest.json")
obligation_map_path = fresh_base / "obligation-map.json"
obligation_map = load(obligation_map_path)
expected_definition = klean_export.expected_target_definition(obligation_map)
target = klean_export.target_statement(fresh_base)

proof_text = (candidate / "Proof.lean").read_text(encoding="utf-8")
parameter = generator_manifest["target"]["parameters"][0]
parameter_def_pattern = re.compile(
    rf"(?m)^[ \t]*def[ \t]+{re.escape(parameter['name'])}[ \t]*:"
)
parameter_def_matches = list(parameter_def_pattern.finditer(proof_text))

result = {
    "candidate_sources": sorted(candidate_text),
    "candidate_forbidden_findings": forbidden,
    "candidate_has_no_forbidden_tokens": all(
        not positions
        for findings in forbidden.values()
        for positions in findings.values()
    ),
    "candidate_new_axiom_or_opaque_declarations": candidate_trust,
    "candidate_has_no_new_axiom_or_opaque": not candidate_trust,
    "generated_trust_declaration_count": len(generated_trust),
    "trust_inventory_allowlist_count": len(allowlist),
    "generated_trust_exactly_matches_inventory": generated_trust == allowlist,
    "fresh_base_tree_sha256": klean_export.tree_digest(fresh_base),
    "reference_generated_tree_sha256": klean_export.tree_digest(
        reference_generated
    ),
    "fresh_base_unchanged": (
        klean_export.tree_digest(fresh_base)
        == klean_export.tree_digest(reference_generated)
    ),
    "target_reconstructed": target,
    "target_manifest": generator_manifest["target"],
    "target_exactly_matches_manifest": target == generator_manifest["target"],
    "expected_target_definition_sha256": (
        hashlib.sha256(expected_definition.encode()).hexdigest()
        if expected_definition is not None
        else None
    ),
    "obligation_map_sha256": hashlib.sha256(
        obligation_map_path.read_bytes()
    ).hexdigest(),
    "obligation_map_hash_matches_manifest": (
        hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
        == generator_manifest["obligation_map_sha256"]
    ),
    "parameter_binding": parameter,
    "parameter_exact_def_match_count": len(parameter_def_matches),
    "parameter_exact_def_line": (
        proof_text.count("\n", 0, parameter_def_matches[0].start()) + 1
        if len(parameter_def_matches) == 1
        else None
    ),
    "proof_source_sha256": hashlib.sha256(proof_text.encode()).hexdigest(),
}

print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
