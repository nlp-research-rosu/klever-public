#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


document = json.loads(AUDIT_INPUT.read_text())
resolution = document["resolution"]
expected_hashes = resolution["hashes"]

inventory = k_rule_inventory.inventory_verification(K_PROOF)
protected = json.loads(DISCOVERY.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(K_PROOF, DISCOVERY)

print("INVENTORY_RECONSTRUCTION")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("PROTECTED_STAGE3")
print(json.dumps(protected, indent=2, sort_keys=True))
print("BIJECTION")
print("inventory_hash_match=", protected["inventory_sha256"] == inventory["inventory_sha256"])
print("ordered_ids_inventory=", [rule["source_rule_id"] for rule in inventory["rules"]])
print("ordered_ids_manifest=", [rule["source_rule_id"] for rule in protected["rules"]])
print(
    "validated_counts=",
    {
        key: len(validated[key])
        for key in (
            "rules",
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
    },
)

source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
producer_files = {
    name: hashlib.sha256((PRODUCERS / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
generator_files = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
audit_image = "sha256:" + Path(resolution["generation_producer_sources"]).name

print("PRODUCER_PROVENANCE")
print("producer_files=", json.dumps(producer_files, sort_keys=True))
print("source_manifest_files=", json.dumps(source_manifest["files"], sort_keys=True))
print("generator_manifest_files=", json.dumps(generator_files, sort_keys=True))
print("file_hashes_all_match=", producer_files == source_manifest["files"] == generator_files)
print("image_source_manifest=", source_manifest["generator_image_id"])
print("image_generator_manifest=", generator_manifest["provenance"]["generator_image_id"])
print("image_audit_input_path=", audit_image)
print(
    "image_ids_all_match=",
    source_manifest["generator_image_id"]
    == generator_manifest["provenance"]["generator_image_id"]
    == audit_image,
)
print("bundle_entries=", sorted(path.name for path in PRODUCERS.iterdir()))

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
    "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
    "discovery_manifest_sha256": hashlib.sha256(DISCOVERY.read_bytes()).hexdigest(),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

print("HASH_LEDGER")
for key, observed in observed_hashes.items():
    expected = expected_hashes[key]
    print(f"{key}: observed={observed} expected={expected} match={observed == expected}")

actual_source_hashes = {
    path.relative_to(K_PROOF).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(K_PROOF, "mounted Stage 1 workspace")
}
expected_source_hashes = resolution["stage1_source_hashes"]
print(
    "stage1_source_hashes:",
    f"observed_count={len(actual_source_hashes)}",
    f"expected_count={len(expected_source_hashes)}",
    f"missing={sorted(set(expected_source_hashes) - set(actual_source_hashes))}",
    f"extra={sorted(set(actual_source_hashes) - set(expected_source_hashes))}",
    "mismatched="
    + repr(
        sorted(
            key
            for key in set(actual_source_hashes) & set(expected_source_hashes)
            if actual_source_hashes[key] != expected_source_hashes[key]
        )
    ),
    f"exact={actual_source_hashes == expected_source_hashes}",
)
resolved_digest = stage6_resolution_contract.canonical_json_sha256(resolution)
print(
    "resolved_input_sha256:",
    f"observed={resolved_digest}",
    f"expected={document['resolved_input_sha256']}",
    f"match={resolved_digest == document['resolved_input_sha256']}",
)

input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
toolchain_lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
independent_domain_ids = [
    rule["source_rule_id"] for rule in validated["domain_lemmas"]
]
source_ids = [rule["source_rule_id"] for rule in obligation_map["source_rules"]]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]

print("STAGE4_IDENTITY")
print("independent_domain_ids=", independent_domain_ids)
print("input_manifest_source_rules=", input_manifest["source_rules"])
print("obligation_map_source_rules=", obligation_map["source_rules"])
print("obligation_ids=", obligation_ids)
print("trust_parameters=", obligation_map["trust_parameters"])
print(
    "exact_empty_bijection=",
    independent_domain_ids == source_ids == obligation_ids
    and len(set(obligation_ids)) == len(obligation_ids),
)
print("obligation_count_manifest=", generator_manifest["obligation_count"])
print("obligation_count_export=", export_result["obligation_count"])
observed_map_hash = hashlib.sha256((GENERATED / "obligation-map.json").read_bytes()).hexdigest()
print("obligation_map_sha_observed=", observed_map_hash)
print("obligation_map_sha_manifest=", generator_manifest["obligation_map_sha256"])
print("target_statement_observed=", klean_export.target_statement(GENERATED))
print("target_definition_expected=", klean_export.expected_target_definition(obligation_map))
print("target_generator_manifest=", generator_manifest["target"])
print("target_audit_input=", resolution["target"])
print("status_export_result=", export_result["status"])
print("status_selected=", resolution["selections"]["klean_generation"]["status"])
print("toolchain_lock_exact=", generator_manifest["toolchain"] == toolchain_lock)
print("inventory_input_manifest=", input_manifest["inventory_sha256"])
print("inventory_generator_provenance=", generator_manifest["provenance"]["inventory_sha256"])
print("verification_sha_observed=", hashlib.sha256((K_PROOF / "verification.k").read_bytes()).hexdigest())
print("verification_sha_input_manifest=", input_manifest["verification_sha256"])
print("candidate_exists=", Path("/candidate").exists())
print("audit_mode=", resolution["mode"])
print("audit_lean_workspace=", resolution["lean_workspace"])
print("audit_lean_invocation=", resolution["lean_invocation"])
