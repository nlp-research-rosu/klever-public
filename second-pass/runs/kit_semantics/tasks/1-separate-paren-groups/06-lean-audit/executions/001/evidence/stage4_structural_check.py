#!/usr/bin/env python3

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, lemma_discovery_contract, pipeline_contract


stage1 = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")

audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
stored_preflight = json.loads((generation / "preflight.json").read_text())
trust_inventory = json.loads((generation / "trust-inventory.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
source_manifest = json.loads((producer / "source-manifest.json").read_text())
toolchain_lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())

validated = lemma_discovery_contract.validate_trust_boundary(
    stage1, discovery_path
)
discovery_hash = hashlib.sha256(discovery_path.read_bytes()).hexdigest()
expected_source_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
actual_target = klean_export.target_statement(generated)
expected_target = klean_export.expected_target_definition(obligation_map)

producer_files = {
    name: hashlib.sha256((producer / name).read_bytes()).hexdigest()
    for name in ("klean.py", "klean_export.py")
}
audit_generator_image = (
    "sha256:" + Path(audit_input["generation_producer_sources"]).name
)

launcher_hashes_observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(stage1),
    "stage1_export_sha256": klean_export.tree_digest(stage1),
    "discovery_manifest_sha256": pipeline_contract.sha256_file(discovery_path),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

stage1_files = {
    path.relative_to(stage1).as_posix(): hashlib.sha256(
        path.read_bytes()
    ).hexdigest()
    for path in stage1.rglob("*")
    if path.is_file() and not path.is_symlink()
}

target_raw_count = sum(
    path.read_text().count("targetStatement")
    for path in generated.rglob("*.lean")
)

checks = {
    "producer_file_hashes_match_source_manifest": (
        producer_files == source_manifest["files"]
    ),
    "producer_file_hashes_match_generator_manifest": (
        producer_files["klean_export.py"]
        == generator_manifest["exporter_sha256"]
        and producer_files["klean.py"]
        == generator_manifest["klean_py_sha256"]
    ),
    "producer_image_ids_match": (
        audit_generator_image
        == source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
    ),
    "launcher_mode_matches_environment": (
        audit_input["mode"] == os.environ.get("AUDIT_MODE")
    ),
    "launcher_hashes_all_match": (
        launcher_hashes_observed == audit_input["hashes"]
    ),
    "all_772_stage1_file_hashes_match": (
        stage1_files == audit_input["stage1_source_hashes"]
    ),
    "toolchain_lock_exact": generator_manifest["toolchain"] == toolchain_lock,
    "input_workspace_hashes_match": (
        input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == klean_export.tree_digest(stage1)
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
    ),
    "discovery_hashes_match": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == discovery_hash
    ),
    "inventory_hashes_match": (
        input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
        == validated["inventory_sha256"]
    ),
    "verification_hash_matches": (
        input_manifest["verification_sha256"]
        == hashlib.sha256((stage1 / "verification.k").read_bytes()).hexdigest()
    ),
    "input_definitions_exact": (
        input_manifest["definitions"] == validated["definitions"]
    ),
    "domain_source_rules_exact": (
        input_manifest["source_rules"]
        == obligation_map["source_rules"]
        == expected_source_rules
    ),
    "source_rule_obligation_ids_bijective": (
        [rule["source_rule_id"] for rule in expected_source_rules]
        == [
            obligation["source_rule_id"]
            for obligation in obligation_map["obligations"]
        ]
        and len(
            {
                obligation["source_rule_id"]
                for obligation in obligation_map["obligations"]
            }
        )
        == len(obligation_map["obligations"])
    ),
    "obligation_map_hash_matches": (
        generator_manifest["obligation_map_sha256"]
        == hashlib.sha256(
            (generated / "obligation-map.json").read_bytes()
        ).hexdigest()
    ),
    "generated_tree_hash_matches": (
        generator_manifest["generated_tree_sha256"]
        == klean_export.tree_digest(generated)
    ),
    "trust_inventory_hash_matches_export_result": (
        export_result["trust_inventory_sha256"]
        == hashlib.sha256(
            (generation / "trust-inventory.json").read_bytes()
        ).hexdigest()
    ),
    "stored_preflight_hashes_match": (
        stored_preflight["frozen_input_sha256"]
        == klean_export.tree_digest(stage1)
        and stored_preflight["stage3_discovery_manifest_sha256"]
        == discovery_hash
        and stored_preflight["generated_tree_sha256"]
        == klean_export.tree_digest(generated)
    ),
    "genuinely_empty_domain_set": (
        len(validated["domain_lemmas"]) == 0
        and len(expected_source_rules) == 0
        and len(obligation_map["obligations"]) == 0
    ),
    "no_generated_target": (
        expected_target is None
        and actual_target is None
        and generator_manifest["target"] is None
        and audit_input.get("target") is None
        and target_raw_count == 0
    ),
    "no_stage5_candidate": not Path("/candidate").exists(),
}

result = {
    "producer_files": producer_files,
    "producer_image": audit_generator_image,
    "launcher_hashes_observed": launcher_hashes_observed,
    "stage1_file_hash_count": len(stage1_files),
    "classification_counts": {
        "DEFINITION": len(validated["definitions"]),
        "OPERATIONAL_RULE": len(validated["operational_rules"]),
        "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
        "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
    },
    "source_rule_count": len(expected_source_rules),
    "obligation_count": len(obligation_map["obligations"]),
    "trust_parameter_count": len(obligation_map["trust_parameters"]),
    "actual_target": actual_target,
    "expected_target_definition": expected_target,
    "raw_target_statement_occurrences": target_raw_count,
    "export_status": export_result["status"],
    "stored_preflight_status": stored_preflight["status"],
    "trust_declaration_count": len(trust_inventory["allowlist"]),
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}

print(json.dumps(result, indent=2, sort_keys=True))
