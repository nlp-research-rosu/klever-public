#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.pipeline_contract import sha256_tree


def load_json(path: Path):
    return json.loads(path.read_text())


producer_path = Path("/reference/generation-tools/klean_export.py")
spec = importlib.util.spec_from_file_location("generation_klean_export", producer_path)
producer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = producer
spec.loader.exec_module(producer)

stage1 = Path("/reference/k-proof")
stage3 = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = load_json(Path("/audit-input.json"))["resolution"]
input_manifest = load_json(generation / "input-manifest.json")
generator_manifest = load_json(generation / "generator-manifest.json")
source_manifest = load_json(Path("/reference/generation-tools/source-manifest.json"))
obligation_map = load_json(generated / "obligation-map.json")
export_result = load_json(generation / "export-result.json")
trust_inventory = load_json(generation / "trust-inventory.json")
inventory = inventory_verification(stage1)

independent_domain_ids = [
    "rule-684bef72ba46103ebf75024cdc1fa13051bb1bec81e5c3ebfd659638388ad8f2",
    "rule-a1197a694d8ff7aa6e41e81faf447c740a45b12fc2bad596cbef040446551918",
    "rule-d101e72bc8dee6c43ac06d55f47939cef9e5ae630efb965cc680c40d10bb36f9",
]
obligation_ids = [entry["source_rule_id"] for entry in obligation_map["obligations"]]
source_rule_ids = [entry["source_rule_id"] for entry in obligation_map["source_rules"]]
input_source_rule_ids = [entry["source_rule_id"] for entry in input_manifest["source_rules"]]

conjunct_checks = []
for obligation in obligation_map["obligations"]:
    conjunct = obligation["lean_conjunct"]
    conjunct_checks.append(
        {
            "source_rule_id": obligation["source_rule_id"],
            "computed_sha256": hashlib.sha256(conjunct.encode()).hexdigest(),
            "recorded_sha256": obligation["lean_conjunct_sha256"],
            "matches": hashlib.sha256(conjunct.encode()).hexdigest()
            == obligation["lean_conjunct_sha256"],
        }
    )

expected_definition = producer.expected_target_definition(obligation_map)
observed_target = producer.target_statement(generated)
producer_hashes = {
    name: hashlib.sha256(
        (Path("/reference/generation-tools") / name).read_bytes()
    ).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
sidecar_hashes = {
    name: hashlib.sha256((generation / name).read_bytes()).hexdigest()
    for name in (
        "input-manifest.json",
        "generator-manifest.json",
        "trust-inventory.json",
        "export-result.json",
    )
}

result = {
    "producer_hashes": producer_hashes,
    "producer_hashes_match_source_manifest": producer_hashes
    == source_manifest["files"],
    "producer_hashes_match_generator_manifest": {
        "klean_export.py": producer_hashes["klean_export.py"]
        == generator_manifest["exporter_sha256"],
        "klean.py": producer_hashes["klean.py"]
        == generator_manifest["klean_py_sha256"],
    },
    "producer_image_id_source_manifest": source_manifest["generator_image_id"],
    "producer_image_id_generator_manifest": generator_manifest["provenance"][
        "generator_image_id"
    ],
    "producer_image_id_audit_input_path_component": Path(
        audit["generation_producer_sources"]
    ).name,
    "pipeline_tree_hashes": {
        "generation_producer_sources": sha256_tree(
            Path("/reference/generation-tools")
        ),
        "klean_generation": sha256_tree(generation),
        "stage1_workspace": sha256_tree(stage1),
        "candidate": sha256_tree(Path("/candidate")),
    },
    "recorded_pipeline_tree_hashes": {
        "generation_producer_sources": audit["hashes"][
            "generation_producer_sources_sha256"
        ],
        "klean_generation": audit["hashes"]["klean_generation_sha256"],
        "stage1_workspace": audit["hashes"]["k_workspace_sha256"],
        "candidate": audit["hashes"]["lean_workspace_sha256"],
    },
    "producer_tree_hashes": {
        "stage1_workspace": producer.tree_digest(stage1),
        "generated": producer.tree_digest(generated),
    },
    "recorded_producer_tree_hashes": {
        "stage1_workspace": generator_manifest["provenance"][
            "stage1_workspace_sha256"
        ],
        "generated_manifest": generator_manifest["generated_tree_sha256"],
        "generated_audit_input": audit["hashes"]["generated_tree_sha256"],
    },
    "sidecar_sha256": sidecar_hashes,
    "stage3_sha256": hashlib.sha256(stage3.read_bytes()).hexdigest(),
    "verification_sha256": hashlib.sha256(
        (stage1 / "verification.k").read_bytes()
    ).hexdigest(),
    "inventory_sha256": inventory["inventory_sha256"],
    "independent_domain_ids": independent_domain_ids,
    "input_manifest_source_rule_ids": input_source_rule_ids,
    "obligation_map_source_rule_ids": source_rule_ids,
    "obligation_ids": obligation_ids,
    "source_rule_bijection_exact": (
        independent_domain_ids
        == input_source_rule_ids
        == source_rule_ids
        == obligation_ids
        and len(set(obligation_ids)) == len(obligation_ids)
    ),
    "conjunct_hash_checks": conjunct_checks,
    "expected_target_definition": expected_definition,
    "expected_target_definition_sha256": hashlib.sha256(
        expected_definition.encode()
    ).hexdigest(),
    "observed_target": observed_target,
    "generator_manifest_target": generator_manifest["target"],
    "audit_input_target": audit["target"],
    "target_identity_exact": observed_target
    == generator_manifest["target"]
    == audit["target"],
    "obligation_counts": {
        "map": len(obligation_map["obligations"]),
        "generator_manifest": generator_manifest["obligation_count"],
        "export_result": export_result["obligation_count"],
    },
    "obligation_map_sha256_computed": hashlib.sha256(
        (generated / "obligation-map.json").read_bytes()
    ).hexdigest(),
    "obligation_map_sha256_recorded": generator_manifest[
        "obligation_map_sha256"
    ],
    "trust_inventory_sha256_computed": hashlib.sha256(
        (generation / "trust-inventory.json").read_bytes()
    ).hexdigest(),
    "trust_inventory_sha256_export_result": export_result[
        "trust_inventory_sha256"
    ],
    "trust_allowlist_count": len(trust_inventory["allowlist"]),
}

print(json.dumps(result, indent=2, sort_keys=True))
