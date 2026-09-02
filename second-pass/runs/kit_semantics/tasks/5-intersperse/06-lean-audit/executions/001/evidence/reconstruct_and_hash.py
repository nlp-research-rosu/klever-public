#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
producer_sources = Path("/reference/generation-tools")
audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
discovery = json.loads(discovery_path.read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
source_manifest = json.loads(
    (producer_sources / "source-manifest.json").read_text()
)

inventory = inventory_verification(workspace)
validated = validate_trust_boundary(workspace, discovery_path)
source_lines = (workspace / "verification.k").read_text().splitlines()

rule_checks = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    exact_span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    rule_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "attributes": rule["attributes"],
            "text": rule["text"],
            "normalized_text": normalized,
            "independent_normalized_sha256": normalized_sha256,
            "normalized_sha256_matches": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id_matches": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
            "exact_source_span_matches": exact_span_text == rule["text"],
        }
    )

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
producer_file_hashes = {
    name: file_sha256(producer_sources / name)
    for name in ("klean_export.py", "klean.py")
}
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
generator_image_key = generator_image_id.removeprefix("sha256:")

result = {
    "audit_mode": {
        "environment": os.environ.get("AUDIT_MODE"),
        "audit_input": resolution["mode"],
        "match": os.environ.get("AUDIT_MODE") == resolution["mode"],
    },
    "canonical_inventory": inventory,
    "independent_rule_checks": rule_checks,
    "inventory_hash_recomputed": canonical_json_sha256(inventory["rules"]),
    "inventory_hash_matches_self": (
        canonical_json_sha256(inventory["rules"])
        == inventory["inventory_sha256"]
    ),
    "inventory_hash_matches_discovery": (
        inventory["inventory_sha256"] == discovery["inventory_sha256"]
    ),
    "manifest_bijection_and_order": {
        "canonical_ids": canonical_ids,
        "manifest_ids": manifest_ids,
        "same_order": canonical_ids == manifest_ids,
        "canonical_unique": len(canonical_ids) == len(set(canonical_ids)),
        "manifest_unique": len(manifest_ids) == len(set(manifest_ids)),
        "missing": [value for value in canonical_ids if value not in manifest_ids],
        "extra": [value for value in manifest_ids if value not in canonical_ids],
    },
    "validated_classification_counts": {
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
        "domain_lemmas": len(validated["domain_lemmas"]),
    },
    "source_and_tree_hashes": {
        "verification_file": file_sha256(workspace / "verification.k"),
        "verification_audit_input": resolution["stage1_source_hashes"][
            "verification.k"
        ],
        "stage1_export_actual": klean_export.tree_digest(workspace),
        "stage1_export_audit_input": resolution["hashes"][
            "stage1_export_sha256"
        ],
        "stage1_full_tree_actual": pipeline_contract.sha256_tree(workspace),
        "stage1_full_tree_audit_input": resolution["hashes"][
            "k_workspace_sha256"
        ],
        "stage2_full_tree_actual": pipeline_contract.sha256_tree(
            Path("/reference/k-audit")
        ),
        "stage2_full_tree_audit_input": resolution["hashes"]["k_audit_sha256"],
        "discovery_actual": file_sha256(discovery_path),
        "discovery_audit_input": resolution["hashes"][
            "discovery_manifest_sha256"
        ],
        "generation_full_tree_actual": pipeline_contract.sha256_tree(generation),
        "generation_full_tree_audit_input": resolution["hashes"][
            "klean_generation_sha256"
        ],
        "generated_tree_actual": klean_export.tree_digest(
            generation / "generated"
        ),
        "generated_tree_audit_input": resolution["hashes"][
            "generated_tree_sha256"
        ],
        "producer_tree_actual": pipeline_contract.sha256_tree(producer_sources),
        "producer_tree_audit_input": resolution["hashes"][
            "generation_producer_sources_sha256"
        ],
    },
    "producer_provenance": {
        "actual_file_hashes": producer_file_hashes,
        "source_manifest_files": source_manifest["files"],
        "generator_manifest_files": {
            "klean_export.py": generator_manifest["exporter_sha256"],
            "klean.py": generator_manifest["klean_py_sha256"],
        },
        "file_hashes_match_source_manifest": (
            producer_file_hashes == source_manifest["files"]
        ),
        "file_hashes_match_generator_manifest": (
            producer_file_hashes
            == {
                "klean_export.py": generator_manifest["exporter_sha256"],
                "klean.py": generator_manifest["klean_py_sha256"],
            }
        ),
        "generator_image_id": generator_image_id,
        "source_manifest_image_id": source_manifest["generator_image_id"],
        "audit_input_producer_path_basename": Path(
            resolution["generation_producer_sources"]
        ).name,
        "image_matches_source_manifest": (
            source_manifest["generator_image_id"] == generator_image_id
        ),
        "image_matches_audit_input_path": (
            Path(resolution["generation_producer_sources"]).name
            == generator_image_key
        ),
    },
    "mode_shape": {
        "selected_stage4_status": resolution["selections"]["klean_generation"][
            "status"
        ],
        "candidate_exists": Path("/candidate").exists(),
        "target_in_audit_input": resolution["target"],
        "stage5_result_in_audit_input": resolution["stage5_result"],
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
