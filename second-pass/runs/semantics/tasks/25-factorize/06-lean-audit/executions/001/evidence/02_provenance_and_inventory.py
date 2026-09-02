#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


audit_input_path = Path("/audit-input.json")
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_root = Path("/reference/generation-tools")

audit_input = json.loads(audit_input_path.read_text())
resolution = audit_input["resolution"]
source_manifest = json.loads((producer_root / "source-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
discovery = json.loads(discovery_path.read_text())

exporter_hash = sha256_file(producer_root / "klean_export.py")
klean_hash = sha256_file(producer_root / "klean.py")
audit_recorded_source_path = Path(resolution["generation_producer_sources"])
audit_recorded_image_id = "sha256:" + audit_recorded_source_path.name

producer_checks = {
    "actual_klean_export_sha256": exporter_hash,
    "source_manifest_klean_export_sha256": source_manifest["files"]["klean_export.py"],
    "generator_manifest_klean_export_sha256": generator_manifest["exporter_sha256"],
    "actual_klean_sha256": klean_hash,
    "source_manifest_klean_sha256": source_manifest["files"]["klean.py"],
    "generator_manifest_klean_sha256": generator_manifest["klean_py_sha256"],
    "source_manifest_generator_image_id": source_manifest["generator_image_id"],
    "generator_manifest_generator_image_id": generator_manifest["provenance"][
        "generator_image_id"
    ],
    "audit_input_path_derived_generator_image_id": audit_recorded_image_id,
    "actual_producer_tree_sha256": pipeline_contract.sha256_tree(producer_root),
    "audit_input_producer_tree_sha256": resolution["hashes"][
        "generation_producer_sources_sha256"
    ],
}
producer_checks["all_match"] = (
    len(
        {
            exporter_hash,
            source_manifest["files"]["klean_export.py"],
            generator_manifest["exporter_sha256"],
        }
    )
    == 1
    and len(
        {
            klean_hash,
            source_manifest["files"]["klean.py"],
            generator_manifest["klean_py_sha256"],
        }
    )
    == 1
    and len(
        {
            source_manifest["generator_image_id"],
            generator_manifest["provenance"]["generator_image_id"],
            audit_recorded_image_id,
        }
    )
    == 1
    and producer_checks["actual_producer_tree_sha256"]
    == producer_checks["audit_input_producer_tree_sha256"]
)

tree_checks = {
    "stage1_workspace_tree_actual": pipeline_contract.sha256_tree(workspace),
    "stage1_workspace_tree_audit": resolution["hashes"]["k_workspace_sha256"],
    "stage1_export_tree_actual": klean_export.tree_digest(workspace),
    "stage1_tree_audit_export": resolution["hashes"]["stage1_export_sha256"],
    "stage1_tree_audit_preflight": resolution["stage4_preflight"][
        "stage1_workspace_sha256"
    ],
    "stage1_tree_input_manifest": input_manifest["stage1_workspace_sha256"],
    "stage1_tree_generator_manifest": generator_manifest["provenance"][
        "stage1_workspace_sha256"
    ],
    "stage1_tree_export_result": export_result["frozen_input_sha256"],
    "discovery_file_actual": sha256_file(discovery_path),
    "discovery_file_audit": resolution["hashes"]["discovery_manifest_sha256"],
    "discovery_file_input_manifest": input_manifest[
        "stage3_discovery_manifest_sha256"
    ],
    "discovery_file_generator_manifest": generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ],
    "discovery_file_export_result": export_result[
        "stage3_discovery_manifest_sha256"
    ],
    "generated_tree_actual": klean_export.tree_digest(generated),
    "generated_tree_audit": resolution["hashes"]["generated_tree_sha256"],
    "generated_tree_generator_manifest": generator_manifest[
        "generated_tree_sha256"
    ],
    "generated_tree_export_result": export_result["generated_tree_sha256"],
    "generation_tree_actual": pipeline_contract.sha256_tree(generation),
    "generation_tree_audit": resolution["hashes"]["klean_generation_sha256"],
    "k_audit_tree_actual": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "k_audit_tree_audit": resolution["hashes"]["k_audit_sha256"],
    "obligation_map_actual": sha256_file(generated / "obligation-map.json"),
    "obligation_map_generator_manifest": generator_manifest[
        "obligation_map_sha256"
    ],
    "trust_inventory_actual": sha256_file(generation / "trust-inventory.json"),
    "trust_inventory_export_result": export_result["trust_inventory_sha256"],
}

inventory = k_rule_inventory.inventory_verification(workspace)
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, discovery_path
)

manual_rules = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    manual_hash = hashlib.sha256(normalized.encode()).hexdigest()
    manual_rules.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "normalized_sha256": rule["normalized_sha256"],
            "manual_normalized_sha256": manual_hash,
            "manual_source_rule_id": "rule-" + manual_hash,
            "attributes": rule["attributes"],
            "text": rule["text"],
            "self_consistent": (
                rule["normalized_sha256"] == manual_hash
                and rule["source_rule_id"] == "rule-" + manual_hash
            ),
        }
    )

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
input_manifest_rules = (
    input_manifest["definitions"]
    + input_manifest["operational_rules"]
    + input_manifest["proved_derived_lemmas"]
    + input_manifest["source_rules"]
)
input_manifest_ids = [rule["source_rule_id"] for rule in input_manifest_rules]

inventory_checks = {
    "verification_sha256_actual": sha256_file(workspace / "verification.k"),
    "verification_sha256_inventory": inventory["verification_sha256"],
    "verification_sha256_audit_input": resolution["stage1_source_hashes"][
        "verification.k"
    ],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "inventory_rule_count": len(inventory_ids),
    "inventory_unique_rule_count": len(set(inventory_ids)),
    "discovery_rule_count": len(discovery_ids),
    "discovery_unique_rule_count": len(set(discovery_ids)),
    "inventory_ids": inventory_ids,
    "discovery_ids": discovery_ids,
    "ordered_ids_equal": inventory_ids == discovery_ids,
    "set_ids_equal": set(inventory_ids) == set(discovery_ids),
    "inventory_sha256_actual": inventory["inventory_sha256"],
    "inventory_sha256_manual": canonical_sha256(inventory["rules"]),
    "inventory_sha256_discovery": discovery["inventory_sha256"],
    "inventory_sha256_input_manifest": input_manifest["inventory_sha256"],
    "inventory_sha256_generator_manifest": generator_manifest["provenance"][
        "inventory_sha256"
    ],
    "all_rule_hashes_self_consistent": all(
        rule["self_consistent"] for rule in manual_rules
    ),
    "validated_definition_count": len(validated["definitions"]),
    "validated_operational_rule_count": len(validated["operational_rules"]),
    "validated_proved_derived_lemma_count": len(
        validated["proved_derived_lemmas"]
    ),
    "validated_domain_lemma_count": len(validated["domain_lemmas"]),
    "input_manifest_all_rule_ids": input_manifest_ids,
    "input_manifest_rule_id_set_equal": set(input_manifest_ids)
    == set(inventory_ids),
    "obligation_map_source_rules": obligation_map["source_rules"],
    "obligation_map_obligations": obligation_map["obligations"],
    "obligation_map_trust_parameters": obligation_map["trust_parameters"],
}

result = {
    "audit_mode_environment": os.environ.get("AUDIT_MODE"),
    "audit_mode_json": resolution["mode"],
    "producer_provenance": producer_checks,
    "recorded_hashes": tree_checks,
    "inventory_checks": inventory_checks,
    "reconstructed_inventory": inventory,
    "manual_rule_hash_checks": manual_rules,
    "validated_classification_partition": {
        "definitions": validated["definitions"],
        "operational_rules": validated["operational_rules"],
        "proved_derived_lemmas": validated["proved_derived_lemmas"],
        "domain_lemmas": validated["domain_lemmas"],
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
