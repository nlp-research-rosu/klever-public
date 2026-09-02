#!/usr/bin/env python3
"""Independent hash, obligation-bijection, and fixed-target checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    klean_final_gate,
    pipeline_contract,
)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
expected_hashes = resolution["hashes"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
candidate = Path("/candidate")
frozen = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
discovery = json.loads(discovery_path.read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(frozen),
    "stage1_export_sha256": klean_export.tree_digest(frozen),
    "discovery_manifest_sha256": file_hash(discovery_path),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(candidate),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
}
print("MOUNTED HASHES")
for name, observed in observed_hashes.items():
    print(name, "observed=", observed, "expected=", expected_hashes[name],
          "match=", observed == expected_hashes[name])
    assert observed == expected_hashes[name]

expected_stage1_files = resolution["stage1_source_hashes"]
actual_stage1_files = {
    path.relative_to(frozen).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(frozen, "Stage 1 workspace")
}
print("STAGE1_FILE_COUNT expected=", len(expected_stage1_files),
      "actual=", len(actual_stage1_files))
print("STAGE1_FILE_HASH_MAP_MATCH=", actual_stage1_files == expected_stage1_files)
assert actual_stage1_files == expected_stage1_files

inventory = k_rule_inventory.inventory_verification(frozen)
inventory_by_id = {rule["source_rule_id"]: rule for rule in inventory["rules"]}
class_by_id = {rule["source_rule_id"]: rule for rule in discovery["rules"]}
domain_ids = [
    rule["source_rule_id"]
    for rule in discovery["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
map_source_ids = [rule["source_rule_id"] for rule in obligation_map["source_rules"]]
obligation_ids = [rule["source_rule_id"] for rule in obligation_map["obligations"]]
print("DOMAIN_IDS=", domain_ids)
print("MAP_SOURCE_IDS=", map_source_ids)
print("OBLIGATION_IDS=", obligation_ids)
assert domain_ids == map_source_ids == obligation_ids
assert len(domain_ids) == len(set(domain_ids)) == 5

for source, obligation in zip(obligation_map["source_rules"], obligation_map["obligations"]):
    source_id = source["source_rule_id"]
    frozen_rule = inventory_by_id[source_id]
    classified = class_by_id[source_id]
    assert source["classification"] == classified["classification"] == "DOMAIN_LEMMA"
    for key in ("module", "start_line", "end_line", "normalized_sha256", "attributes", "text"):
        assert source[key] == frozen_rule[key]
    assert obligation["normalized_sha256"] == frozen_rule["normalized_sha256"]
    assert obligation["source_span"] == {
        "start_line": frozen_rule["start_line"],
        "end_line": frozen_rule["end_line"],
    }
    assert obligation["inventory_sha256"] == inventory["inventory_sha256"]
    assert obligation["discovery_manifest_sha256"] == file_hash(discovery_path)
    assert obligation["lean_conjunct_sha256"] == klean_export.sha256_text(
        obligation["lean_conjunct"]
    )
print("SOURCE_OBLIGATION_BIJECTION_MATCH=true")

assert input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
assert generator_manifest["obligation_count"] == len(domain_ids)
assert generator_manifest["obligation_map_sha256"] == file_hash(
    generated / "obligation-map.json"
)

target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
assert target is not None and expected_definition is not None
print("EXPECTED_TARGET_DEFINITION")
print(expected_definition)
print("EXTRACTED_TARGET")
print(json.dumps(target, indent=2, sort_keys=True))
assert target["definition_sha256"] == klean_export.sha256_text(expected_definition)
assert target == generator_manifest["target"]
assert target == resolution["target"]
assert target == resolution["stage4_preflight"]["target"]
assert target["statement_sha256"] == klean_export.sha256_text(target["statement"])
print("FIXED_TARGET_MATCH=true")

# The trusted mechanical candidate gate checks one exact definition for every
# target binding and exact textual identity of theorem Proof.final's type.
klean_final_gate._candidate_gate(candidate, target)
print("CANDIDATE_EXACT_BINDINGS_AND_FINAL_TYPE=true")

copied_base = Path("/tmp/audit-work/69-search-proof-audit/Base")
print("COPIED_BASE_TREE_SHA256=", klean_export.tree_digest(copied_base))
print("GENERATED_TREE_SHA256=", klean_export.tree_digest(generated))
assert klean_export.tree_digest(copied_base) == klean_export.tree_digest(generated)
assert klean_export.target_statement(copied_base) == target
print("COPIED_BASE_UNCHANGED=true")
