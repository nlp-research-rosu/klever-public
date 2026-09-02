import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.pipeline_contract import sha256_tree


generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]
discovery = Path("/reference/lemma-discovery.json")
verification = Path("/reference/k-proof/verification.k")

expected_ids = [
    "rule-bb0819476c6343e9119c99a78b2ae8eb72ebad42dbc170a9eaa3c4af6f39f115",
    "rule-79c1c8d9ff74acff507b7b4a319ee7d9d034df3550afdf9196f29291297713c8",
]
observed_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
source_ids = [
    source_rule["source_rule_id"]
    for source_rule in obligation_map["source_rules"]
]

checks = {
    "stage1_tree": (
        klean_export.tree_digest(Path("/reference/k-proof"))
        == input_manifest["frozen_input_sha256"]
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
        == audit_input["hashes"]["stage1_export_sha256"]
    ),
    "discovery_file": (
        hashlib.sha256(discovery.read_bytes()).hexdigest()
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == export_result["stage3_discovery_manifest_sha256"]
        == audit_input["hashes"]["discovery_manifest_sha256"]
    ),
    "verification_file": (
        hashlib.sha256(verification.read_bytes()).hexdigest()
        == input_manifest["verification_sha256"]
        == audit_input["stage1_source_hashes"]["verification.k"]
    ),
    "generated_tree": (
        klean_export.tree_digest(generated)
        == generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
        == audit_input["hashes"]["generated_tree_sha256"]
    ),
    "obligation_map_file": (
        hashlib.sha256((generated / "obligation-map.json").read_bytes())
        .hexdigest()
        == generator_manifest["obligation_map_sha256"]
    ),
    "trust_inventory_file": (
        hashlib.sha256((generation / "trust-inventory.json").read_bytes())
        .hexdigest()
        == export_result["trust_inventory_sha256"]
    ),
    "producer_tree": (
        sha256_tree(Path("/reference/generation-tools"))
        == audit_input["hashes"]["generation_producer_sources_sha256"]
    ),
    "exporter_file": (
        hashlib.sha256(
            Path("/reference/generation-tools/klean_export.py").read_bytes()
        ).hexdigest()
        == source_manifest["files"]["klean_export.py"]
        == generator_manifest["exporter_sha256"]
    ),
    "klean_file": (
        hashlib.sha256(
            Path("/reference/generation-tools/klean.py").read_bytes()
        ).hexdigest()
        == source_manifest["files"]["klean.py"]
        == generator_manifest["klean_py_sha256"]
    ),
    "generator_image": (
        source_manifest["generator_image_id"]
        == generator_manifest["provenance"]["generator_image_id"]
        == "sha256:" + Path(audit_input["generation_producer_sources"]).name
    ),
    "obligation_ids_exact_order": observed_ids == expected_ids,
    "source_ids_exact_order": source_ids == expected_ids,
    "obligation_ids_unique": len(observed_ids) == len(set(observed_ids)),
    "source_ids_unique": len(source_ids) == len(set(source_ids)),
    "obligation_conjunct_hashes": all(
        hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest()
        == obligation["lean_conjunct_sha256"]
        for obligation in obligation_map["obligations"]
    ),
    "obligation_source_hashes": all(
        obligation["source_rule_id"]
        == "rule-" + obligation["normalized_sha256"]
        for obligation in obligation_map["obligations"]
    ),
    "target_exact_definition": (
        klean_export.target_statement(generated)["definition_sha256"]
        == klean_export.sha256_text(
            klean_export.expected_target_definition(obligation_map)
        )
    ),
    "target_generator_audit": (
        klean_export.target_statement(generated)
        == generator_manifest["target"]
        == audit_input["target"]
    ),
    "obligation_count": (
        len(observed_ids)
        == generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == 2
    ),
}

print(json.dumps(checks, indent=2, sort_keys=True))
print("all_checks", all(checks.values()))
print("observed_ids", observed_ids)
print("target_statement", generator_manifest["target"]["statement"])
print(
    "target_definition_sha256",
    generator_manifest["target"]["definition_sha256"],
)
print(
    "target_statement_sha256",
    generator_manifest["target"]["statement_sha256"],
)
