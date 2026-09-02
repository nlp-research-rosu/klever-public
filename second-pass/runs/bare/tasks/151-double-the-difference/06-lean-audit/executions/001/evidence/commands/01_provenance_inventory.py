#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


audit_path = Path("/audit-input.json")
stage1 = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")

audit_document = load(audit_path)
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
recorded_hashes = resolution["hashes"]
source_manifest = load(producer / "source-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
input_manifest = load(generation / "input-manifest.json")
export_result = load(generation / "export-result.json")
recorded_preflight = load(generation / "preflight.json")

producer_files = {
    name: sha256_file(producer / name)
    for name in ("klean_export.py", "klean.py")
}
producer_names = sorted(
    path.relative_to(producer).as_posix()
    for path in pipeline_contract._walk_regular_files(
        producer, "mounted producer source bundle"
    )
)
expected_producer_names = [
    "klean.py",
    "klean_export.py",
    "source-manifest.json",
]
image_id = generator_manifest["provenance"]["generator_image_id"]
audit_image_key = Path(resolution["generation_producer_sources"]).name

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(stage1),
    "stage1_export_sha256": klean_export.tree_digest(stage1),
    "discovery_manifest_sha256": sha256_file(discovery_path),
    "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

stage1_source_hashes = {
    path.relative_to(stage1).as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        stage1, "mounted Stage 1 workspace"
    )
}

inventory = k_rule_inventory.inventory_verification(stage1)
validated = lemma_discovery_contract.validate_trust_boundary(
    stage1, discovery_path
)
discovery_document = load(discovery_path)
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [
    rule["source_rule_id"] for rule in discovery_document["rules"]
]
source_lines = (stage1 / "verification.k").read_text().splitlines()

rule_checks = []
for position, (rule, classification) in enumerate(
    zip(inventory["rules"], discovery_document["rules"], strict=True)
):
    normalized = " ".join(rule["text"].split())
    normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
    exact_span = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    rule_checks.append(
        {
            "position": position,
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "attributes": rule["attributes"],
            "normalized_sha256": rule["normalized_sha256"],
            "classification": classification["classification"],
            "span_text_exact": exact_span == rule["text"],
            "normalized_hash_exact": normalized_hash
            == rule["normalized_sha256"],
            "source_rule_id_exact": rule["source_rule_id"]
            == f"rule-{normalized_hash}",
            "text": rule["text"],
        }
    )

canonical_inventory_hash = k_rule_inventory.canonical_json_sha256(
    inventory["rules"]
)

checks = {
    "AUDIT_MODE_environment": os.environ.get("AUDIT_MODE"),
    "audit_mode": resolution["mode"],
    "audit_problem": resolution["problem_id"],
    "audit_condition": resolution["condition"],
    "audit_semantics_mode": resolution["semantics_mode"],
    "resolved_input_sha256": {
        "recorded": audit_document["resolved_input_sha256"],
        "recomputed": resolved_digest,
        "match": audit_document["resolved_input_sha256"] == resolved_digest,
    },
    "producer_exact_file_set": producer_names == expected_producer_names,
    "producer_files": producer_files,
    "producer_matches_source_manifest": producer_files
    == source_manifest["files"],
    "producer_matches_generator_manifest": producer_files
    == {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    },
    "generator_image_id": image_id,
    "source_manifest_image_id": source_manifest["generator_image_id"],
    "audit_producer_path_image_key": audit_image_key,
    "generator_image_matches_source_manifest": image_id
    == source_manifest["generator_image_id"],
    "generator_image_matches_audit_path": image_id.removeprefix("sha256:")
    == audit_image_key,
    "all_recorded_resolution_hashes_match": observed_hashes
    == recorded_hashes,
    "observed_resolution_hashes": observed_hashes,
    "recorded_resolution_hashes": recorded_hashes,
    "stage1_source_hashes_exact": stage1_source_hashes
    == resolution["stage1_source_hashes"],
    "stage1_source_hash_count": len(stage1_source_hashes),
    "generator_generated_tree_hash_exact": generator_manifest[
        "generated_tree_sha256"
    ]
    == observed_hashes["generated_tree_sha256"],
    "generator_stage1_hash_exact": generator_manifest["provenance"][
        "stage1_workspace_sha256"
    ]
    == observed_hashes["stage1_export_sha256"],
    "generator_discovery_hash_exact": generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ]
    == observed_hashes["discovery_manifest_sha256"],
    "input_manifest_stage1_hash_exact": input_manifest[
        "stage1_workspace_sha256"
    ]
    == observed_hashes["stage1_export_sha256"],
    "input_manifest_discovery_hash_exact": input_manifest[
        "stage3_discovery_manifest_sha256"
    ]
    == observed_hashes["discovery_manifest_sha256"],
    "export_result_stage1_hash_exact": export_result[
        "frozen_input_sha256"
    ]
    == observed_hashes["stage1_export_sha256"],
    "export_result_discovery_hash_exact": export_result[
        "stage3_discovery_manifest_sha256"
    ]
    == observed_hashes["discovery_manifest_sha256"],
    "export_result_generated_hash_exact": export_result[
        "generated_tree_sha256"
    ]
    == observed_hashes["generated_tree_sha256"],
    "export_result_trust_inventory_hash_exact": export_result[
        "trust_inventory_sha256"
    ]
    == sha256_file(generation / "trust-inventory.json"),
    "recorded_preflight_stage1_hash_exact": recorded_preflight[
        "stage1_workspace_sha256"
    ]
    == observed_hashes["stage1_export_sha256"],
    "recorded_preflight_discovery_hash_exact": recorded_preflight[
        "stage3_discovery_manifest_sha256"
    ]
    == observed_hashes["discovery_manifest_sha256"],
    "recorded_preflight_generated_hash_exact": recorded_preflight[
        "generated_tree_sha256"
    ]
    == observed_hashes["generated_tree_sha256"],
    "inventory_verification_sha256": inventory["verification_sha256"],
    "inventory_verification_module": inventory["verification_module"],
    "inventory_verification_modules": inventory["verification_modules"],
    "inventory_rule_count": len(inventory["rules"]),
    "inventory_sha256_recomputed": canonical_inventory_hash,
    "inventory_sha256_tool": inventory["inventory_sha256"],
    "inventory_sha256_discovery": discovery_document["inventory_sha256"],
    "inventory_sha256_input_manifest": input_manifest["inventory_sha256"],
    "inventory_sha256_generator_manifest": generator_manifest["provenance"][
        "inventory_sha256"
    ],
    "inventory_hashes_all_exact": len(
        {
            canonical_inventory_hash,
            inventory["inventory_sha256"],
            discovery_document["inventory_sha256"],
            input_manifest["inventory_sha256"],
            generator_manifest["provenance"]["inventory_sha256"],
        }
    )
    == 1,
    "discovery_identity_order_exact": inventory_ids == discovery_ids,
    "discovery_identity_set_bijective": len(inventory_ids)
    == len(discovery_ids)
    == len(set(discovery_ids))
    and set(inventory_ids) == set(discovery_ids),
    "validated_counts": {
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
        "domain_lemmas": len(validated["domain_lemmas"]),
    },
    "all_rule_span_and_identity_checks": all(
        check["span_text_exact"]
        and check["normalized_hash_exact"]
        and check["source_rule_id_exact"]
        for check in rule_checks
    ),
    "rule_checks": rule_checks,
    "no_generated_target": generator_manifest["target"] is None
    and resolution["target"] is None,
    "no_candidate_mount": not Path("/candidate").exists(),
    "selected_stage4_status": resolution["selections"]["klean_generation"][
        "status"
    ],
}

print(json.dumps(checks, indent=2, sort_keys=True))
