#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools.klean_export import (
    expected_target_definition,
    target_statement,
    tree_digest,
)
from tools.k_rule_inventory import inventory_verification
from tools.pipeline_contract import sha256_tree

root = Path("/reference/klean-generation")
generated = root / "generated"
kroot = Path("/reference/k-proof")
discovery = Path("/reference/lemma-discovery.json")
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
input_manifest = json.loads((root / "input-manifest.json").read_text())
generator = json.loads((root / "generator-manifest.json").read_text())
export = json.loads((root / "export-result.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
inventory = inventory_verification(kroot)
classification = json.loads(discovery.read_text())

# Independently determined by the semantic analysis in
# 03-classification-semantics.txt.
independent_domain_ids = []
manifest_domain_ids = [
    rule["source_rule_id"] for rule in classification["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
source_rule_ids = [rule["source_rule_id"] for rule in input_manifest["source_rules"]]
map_source_ids = [rule["source_rule_id"] for rule in obligation_map["source_rules"]]
obligation_ids = [rule["source_rule_id"] for rule in obligation_map["obligations"]]
actual_target = target_statement(generated)
expected_definition = expected_target_definition(obligation_map)
producer_hashes = {
    name: hashlib.sha256(
        (Path("/reference/generation-tools") / name).read_bytes()
    ).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
lean_text = "\n".join(
    path.read_text() for path in sorted(generated.rglob("*.lean"))
)
checks = {
    "audit_mode": audit["mode"],
    "candidate_absent": not Path("/candidate").exists(),
    "stage1_pipeline_tree_hash_match": (
        sha256_tree(kroot) == audit["hashes"]["k_workspace_sha256"]
    ),
    "stage1_export_tree_hash_match": (
        tree_digest(kroot)
        == audit["hashes"]["stage1_export_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == generator["provenance"]["stage1_workspace_sha256"]
    ),
    "discovery_hash_match": (
        hashlib.sha256(discovery.read_bytes()).hexdigest()
        == audit["hashes"]["discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator["provenance"]["stage3_discovery_manifest_sha256"]
    ),
    "generated_tree_hash_match": (
        tree_digest(generated)
        == audit["hashes"]["generated_tree_sha256"]
        == generator["generated_tree_sha256"]
        == export["generated_tree_sha256"]
    ),
    "generation_pipeline_tree_hash_match": (
        sha256_tree(root) == audit["hashes"]["klean_generation_sha256"]
    ),
    "producer_tree_hash_match": (
        sha256_tree(Path("/reference/generation-tools"))
        == audit["hashes"]["generation_producer_sources_sha256"]
    ),
    "exporter_hash_match": (
        producer_hashes["klean_export.py"]
        == source_manifest["files"]["klean_export.py"]
        == generator["exporter_sha256"]
    ),
    "klean_py_hash_match": (
        producer_hashes["klean.py"]
        == source_manifest["files"]["klean.py"]
        == generator["klean_py_sha256"]
    ),
    "producer_manifest_exact_files": (
        sorted(source_manifest["files"]) == ["klean.py", "klean_export.py"]
    ),
    "generator_image_id_match": (
        source_manifest["generator_image_id"]
        == generator["provenance"]["generator_image_id"]
        == "sha256:" + Path(audit["generation_producer_sources"]).name
    ),
    "inventory_hash_match": (
        inventory["inventory_sha256"]
        == classification["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator["provenance"]["inventory_sha256"]
    ),
    "verification_hash_match": (
        inventory["verification_sha256"] == input_manifest["verification_sha256"]
    ),
    "independent_domain_ids": independent_domain_ids,
    "manifest_domain_ids": manifest_domain_ids,
    "input_source_rule_ids": source_rule_ids,
    "obligation_map_source_rule_ids": map_source_ids,
    "obligation_ids": obligation_ids,
    "exact_empty_bijection": (
        independent_domain_ids == manifest_domain_ids == source_rule_ids
        == map_source_ids == obligation_ids == []
    ),
    "obligation_ids_unique": len(obligation_ids) == len(set(obligation_ids)),
    "obligation_count_consistent": (
        generator["obligation_count"]
        == export["obligation_count"]
        == len(obligation_map["obligations"])
        == 0
    ),
    "obligation_map_hash_match": (
        hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
        == generator["obligation_map_sha256"]
    ),
    "trust_inventory_hash_match": (
        hashlib.sha256((root / "trust-inventory.json").read_bytes()).hexdigest()
        == export["trust_inventory_sha256"]
    ),
    "expected_target_definition": expected_definition,
    "actual_target": actual_target,
    "manifest_target": generator["target"],
    "audit_input_target": audit["target"],
    "preflight_target": audit["stage4_preflight"]["target"],
    "all_targets_absent": (
        expected_definition is None and actual_target is None
        and generator["target"] is None and audit["target"] is None
        and audit["stage4_preflight"]["target"] is None
    ),
    "target_named_declaration_absent": re.search(
        r"(?m)^\s*(?:def|theorem|lemma)\s+(?:KleanTarget|Target|final)\b",
        lean_text,
    ) is None,
    "statuses_consistent": (
        export["status"]
        == audit["selections"]["klean_generation"]["status"]
        == audit["stage4_preflight"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "stage5_result_absent": audit["stage5_result"] is None,
}
print(json.dumps(checks, indent=2, sort_keys=True))
failed = [key for key, value in checks.items() if isinstance(value, bool) and not value]
print("FAILED_BOOLEAN_CHECKS", json.dumps(failed))
