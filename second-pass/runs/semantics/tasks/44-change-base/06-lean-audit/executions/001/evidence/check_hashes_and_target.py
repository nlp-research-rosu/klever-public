#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_tree


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
hashes = audit["hashes"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
validated = validate_trust_boundary(
    Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
)

pipeline_trees = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(generation),
    "lean_workspace_sha256": sha256_tree(Path("/candidate")),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
}
klean_trees = {
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
}
file_hashes = {
    "discovery_manifest_sha256": sha256_file(
        Path("/reference/lemma-discovery.json")
    ),
    "verification_sha256": sha256_file(
        Path("/reference/k-proof/verification.k")
    ),
    "obligation_map_sha256": sha256_file(obligation_map_path),
    "generator_manifest_sha256": sha256_file(
        generation / "generator-manifest.json"
    ),
    "input_manifest_sha256": sha256_file(generation / "input-manifest.json"),
    "trust_inventory_sha256": sha256_file(
        generation / "trust-inventory.json"
    ),
    "export_result_sha256": sha256_file(generation / "export-result.json"),
}

target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
expected_definition_sha256 = klean_export.sha256_text(expected_definition)
source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
validated_domain = validated["domain_lemmas"]

source_ids = [entry["source_rule_id"] for entry in source_rules]
obligation_ids = [entry["source_rule_id"] for entry in obligations]
domain_ids = [entry["source_rule_id"] for entry in validated_domain]

candidate_text = Path("/candidate/Proof.lean").read_text()
candidate_forbidden = {
    token: [
        match.start()
        for match in re.finditer(
            rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])",
            candidate_text,
        )
    ]
    for token in ("sorry", "admit", "unsafe", "axiom", "opaque")
}
candidate_target_declarations = [
    line
    for line in candidate_text.splitlines()
    if re.search(r"^\s*(?:def|theorem|axiom|opaque)\s+.*targetStatement", line)
]

source_hash_checks = {
    relative: sha256_file(Path("/reference/k-proof") / relative) == expected
    for relative, expected in audit["stage1_source_hashes"].items()
}

checks = {
    "all_pipeline_tree_hashes_match_audit_input": all(
        observed == hashes[name] for name, observed in pipeline_trees.items()
    ),
    "all_klean_tree_hashes_match_audit_input": all(
        observed == hashes[name] for name, observed in klean_trees.items()
    ),
    "discovery_hash_matches_audit_input": (
        file_hashes["discovery_manifest_sha256"]
        == hashes["discovery_manifest_sha256"]
    ),
    "all_stage1_source_hashes_match": all(source_hash_checks.values()),
    "generated_tree_matches_generator_manifest": (
        klean_trees["generated_tree_sha256"]
        == generator["generated_tree_sha256"]
    ),
    "generated_tree_matches_export_result": (
        klean_trees["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
    ),
    "obligation_map_hash_matches_generator": (
        file_hashes["obligation_map_sha256"]
        == generator["obligation_map_sha256"]
    ),
    "input_source_rules_equal_obligation_source_rules": (
        input_manifest["source_rules"] == source_rules
    ),
    "domain_source_rule_order_bijective": (
        source_ids == obligation_ids == domain_ids
        and len(source_ids) == len(set(source_ids))
    ),
    "obligation_count_matches": (
        len(obligations) == generator["obligation_count"] == 3
    ),
    "all_conjunct_hashes_match": all(
        entry["lean_conjunct_sha256"]
        == klean_export.sha256_text(entry["lean_conjunct"])
        for entry in obligations
    ),
    "target_equals_generator_manifest": target == generator["target"],
    "target_equals_audit_input": target == audit["target"],
    "target_definition_is_exact_conjunction": (
        expected_definition_sha256 == target["definition_sha256"]
    ),
    "candidate_has_no_forbidden_tokens": not any(candidate_forbidden.values()),
    "candidate_does_not_declare_target": not candidate_target_declarations,
}

print(
    json.dumps(
        {
            "pipeline_tree_hashes": pipeline_trees,
            "klean_tree_hashes": klean_trees,
            "file_hashes": file_hashes,
            "source_hash_checks": source_hash_checks,
            "domain_ids": domain_ids,
            "source_ids": source_ids,
            "obligation_ids": obligation_ids,
            "obligations": obligations,
            "target": target,
            "expected_target_definition": expected_definition,
            "expected_target_definition_sha256": expected_definition_sha256,
            "candidate_forbidden_token_offsets": candidate_forbidden,
            "candidate_target_declarations": candidate_target_declarations,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
