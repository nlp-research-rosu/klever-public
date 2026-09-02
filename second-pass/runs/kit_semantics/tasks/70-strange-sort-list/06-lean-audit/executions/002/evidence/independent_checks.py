import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.klean_export import (
    expected_target_definition,
    sha256_text,
    target_statement,
    tree_digest,
)
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import verify_audit_input


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(Path("/audit-input.json").read_text())
verified_resolution, verified_resolution_hash = verify_audit_input(
    audit_document
)
audit = audit_document["resolution"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)
inventory = inventory_verification(Path("/reference/k-proof"))
validated = validate_trust_boundary(
    Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
)
target = target_statement(
    Path("/reference/klean-generation/generated")
)
expected_definition = expected_target_definition(obligation_map)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
source_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]

result = {
    "audit_mode": audit["mode"],
    "audit_input_contract": {
        "verified_resolution_sha256": verified_resolution_hash,
        "recorded_resolution_sha256": audit_document[
            "resolved_input_sha256"
        ],
        "verified_mode": verified_resolution["mode"],
        "verified_problem_id": verified_resolution["problem_id"],
    },
    "producer": {
        "audit_bundle_tree_expected": audit["hashes"][
            "generation_producer_sources_sha256"
        ],
        "audit_bundle_tree_observed": sha256_tree(
            Path("/reference/generation-tools")
        ),
        "audit_image_from_bundle_path": "sha256:"
        + Path(audit["generation_producer_sources"]).name,
        "generator_image": generator["provenance"]["generator_image_id"],
        "source_manifest_image": source_manifest["generator_image_id"],
        "files": {
            name: {
                "observed": file_sha256(
                    Path("/reference/generation-tools") / name
                ),
                "source_manifest": source_manifest["files"][name],
                "generator_manifest": generator[
                    "exporter_sha256"
                    if name == "klean_export.py"
                    else "klean_py_sha256"
                ],
            }
            for name in ("klean_export.py", "klean.py")
        },
    },
    "frozen_hashes": {
        "stage1_pipeline_expected": audit["hashes"]["k_workspace_sha256"],
        "stage1_pipeline_observed": sha256_tree(
            Path("/reference/k-proof")
        ),
        "stage1_export_expected": audit["hashes"]["stage1_export_sha256"],
        "stage1_export_observed": tree_digest(Path("/reference/k-proof")),
        "discovery_expected": audit["hashes"][
            "discovery_manifest_sha256"
        ],
        "discovery_observed": file_sha256(
            Path("/reference/lemma-discovery.json")
        ),
        "generation_pipeline_expected": audit["hashes"][
            "klean_generation_sha256"
        ],
        "generation_pipeline_observed": sha256_tree(
            Path("/reference/klean-generation")
        ),
        "generated_export_expected": audit["hashes"][
            "generated_tree_sha256"
        ],
        "generated_export_observed": tree_digest(
            Path("/reference/klean-generation/generated")
        ),
        "candidate_pipeline_expected": audit["hashes"][
            "lean_workspace_sha256"
        ],
        "candidate_pipeline_observed": sha256_tree(Path("/candidate")),
    },
    "inventory": {
        "count": len(inventory_ids),
        "ids": inventory_ids,
        "manifest_ids": discovery_ids,
        "manifest_entries": discovery["rules"],
        "ordered_identity_equal": inventory_ids == discovery_ids,
        "unique_inventory": len(inventory_ids) == len(set(inventory_ids)),
        "unique_manifest": len(discovery_ids) == len(set(discovery_ids)),
        "inventory_sha256_observed": inventory["inventory_sha256"],
        "inventory_sha256_manifest": discovery["inventory_sha256"],
        "verification_sha256": inventory["verification_sha256"],
        "verification_modules": inventory["verification_modules"],
        "validated_bucket_counts": {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(
                validated["proved_derived_lemmas"]
            ),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
        "rules": inventory["rules"],
    },
    "bijection": {
        "domain_source_ids": source_rule_ids,
        "obligation_ids": obligation_ids,
        "exact_ordered_bijection": source_rule_ids == obligation_ids,
        "unique_obligations": len(obligation_ids) == len(set(obligation_ids)),
        "obligation_count": len(obligation_ids),
        "conjuncts": [
            {
                "source_rule_id": item["source_rule_id"],
                "lean_conjunct": item["lean_conjunct"],
                "recorded_sha256": item["lean_conjunct_sha256"],
                "observed_sha256": sha256_text(item["lean_conjunct"]),
            }
            for item in obligation_map["obligations"]
        ],
    },
    "target": {
        "observed": target,
        "generator_manifest": generator["target"],
        "audit_input": audit["target"],
        "expected_definition_sha256": (
            sha256_text(expected_definition)
            if expected_definition is not None
            else None
        ),
        "all_equal": target == generator["target"] == audit["target"],
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
