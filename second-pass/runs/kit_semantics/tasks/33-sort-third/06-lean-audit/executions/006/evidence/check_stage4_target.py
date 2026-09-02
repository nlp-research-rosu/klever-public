#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, lemma_discovery_contract, stage6_resolution_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


frozen = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
audit_document = json.loads(Path("/audit-input.json").read_text())
resolution, _ = stage6_resolution_contract.verify_audit_input(audit_document)
validated = lemma_discovery_contract.validate_trust_boundary(
    frozen, discovery_path
)

domain_rules = validated["domain_lemmas"]
domain_ids = [rule["source_rule_id"] for rule in domain_rules]
obligations = obligation_map["obligations"]
obligation_ids = [obligation["source_rule_id"] for obligation in obligations]
actual_target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)

conjunct_checks = []
for rule, obligation in zip(domain_rules, obligations, strict=True):
    conjunct = obligation["lean_conjunct"]
    conjunct_checks.append({
        "source_rule_id": rule["source_rule_id"],
        "id_match": rule["source_rule_id"] == obligation["source_rule_id"],
        "span_match": {
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
        } == obligation["source_span"],
        "normalized_hash_match": rule["normalized_sha256"]
        == obligation["normalized_sha256"],
        "conjunct_hash_match": klean_export.sha256_text(conjunct)
        == obligation["lean_conjunct_sha256"],
        "contains_true_literal": "True" in conjunct,
        "contains_false_literal": "False" in conjunct,
        "lean_conjunct": conjunct,
    })

recorded_targets = {
    "generator_manifest": generator_manifest.get("target"),
    "audit_input": resolution.get("target"),
    "audit_input_stage4_preflight": resolution.get("stage4_preflight", {}).get(
        "target"
    ),
}

checks = {
    "domain_ids": domain_ids,
    "obligation_ids": obligation_ids,
    "ordered_bijection": domain_ids == obligation_ids
    and len(obligation_ids) == len(set(obligation_ids)),
    "obligation_count": len(obligations),
    "obligation_count_matches_generator_manifest": len(obligations)
    == generator_manifest.get("obligation_count"),
    "obligation_count_matches_export_result": len(obligations)
    == export_result.get("obligation_count"),
    "obligation_map_hash": file_sha256(generated / "obligation-map.json"),
    "obligation_map_hash_matches": file_sha256(generated / "obligation-map.json")
    == generator_manifest.get("obligation_map_sha256"),
    "generated_tree_hash": klean_export.tree_digest(generated),
    "generated_tree_hash_matches": klean_export.tree_digest(generated)
    == generator_manifest.get("generated_tree_sha256"),
    "verification_hash_matches": file_sha256(frozen / "verification.k")
    == input_manifest.get("verification_sha256"),
    "inventory_hash_matches": validated["inventory_sha256"]
    == input_manifest.get("inventory_sha256"),
    "discovery_hash_matches": file_sha256(discovery_path)
    == input_manifest.get("stage3_discovery_manifest_sha256"),
    "target_matches_all_recorded_copies": all(
        target == actual_target for target in recorded_targets.values()
    ),
    "target": actual_target,
    "recorded_targets": recorded_targets,
    "expected_target_definition": expected_definition,
    "expected_definition_hash": (
        None
        if expected_definition is None
        else klean_export.sha256_text(expected_definition)
    ),
    "definition_hash_matches_expected_conjunction": (
        actual_target is not None
        and expected_definition is not None
        and actual_target["definition_sha256"]
        == klean_export.sha256_text(expected_definition)
    ),
    "conjunct_checks": conjunct_checks,
}

print(json.dumps(checks, indent=2, sort_keys=True))
