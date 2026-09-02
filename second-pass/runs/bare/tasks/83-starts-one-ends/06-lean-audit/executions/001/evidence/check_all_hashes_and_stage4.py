#!/usr/bin/env python3
import hashlib
import json
import os
import re
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.stage6_resolution_contract import verify_audit_input


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK = Path("/reference/klean-toolchain.lock.json")


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return value


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = read_json(AUDIT_INPUT)
resolution, resolved_digest = verify_audit_input(audit_document)
recorded_hashes = resolution["hashes"]

computed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
    "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
    "discovery_manifest_sha256": file_sha256(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        PRODUCERS
    ),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
assert computed_hashes == recorded_hashes

source_hashes = {
    path.relative_to(K_PROOF).as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        K_PROOF, "Stage 1 source workspace"
    )
}
assert source_hashes == resolution["stage1_source_hashes"]

input_manifest = read_json(GENERATION / "input-manifest.json")
generator_manifest = read_json(GENERATION / "generator-manifest.json")
obligation_map = read_json(GENERATED / "obligation-map.json")
export_result = read_json(GENERATION / "export-result.json")
preflight = read_json(GENERATION / "preflight.json")
trust_inventory = read_json(GENERATION / "trust-inventory.json")
toolchain_lock = read_json(LOCK)

assert generator_manifest["toolchain"] == toolchain_lock
assert toolchain_lock == pipeline_contract.FROZEN_TOOLCHAIN_LOCK
assert preflight == resolution["stage4_preflight"]
assert generator_manifest["generated_tree_sha256"] == computed_hashes[
    "generated_tree_sha256"
]
assert generator_manifest["obligation_map_sha256"] == file_sha256(
    GENERATED / "obligation-map.json"
)
assert export_result["trust_inventory_sha256"] == file_sha256(
    GENERATION / "trust-inventory.json"
)

for document in (input_manifest, generator_manifest["provenance"]):
    assert document["stage1_workspace_sha256"] == computed_hashes[
        "stage1_export_sha256"
    ]
    assert document["stage3_discovery_manifest_sha256"] == computed_hashes[
        "discovery_manifest_sha256"
    ]
assert input_manifest["frozen_input_sha256"] == computed_hashes[
    "stage1_export_sha256"
]
assert export_result["frozen_input_sha256"] == computed_hashes[
    "stage1_export_sha256"
]
assert export_result["stage3_discovery_manifest_sha256"] == computed_hashes[
    "discovery_manifest_sha256"
]
assert export_result["generated_tree_sha256"] == computed_hashes[
    "generated_tree_sha256"
]

# Independent semantic classification found no DOMAIN_LEMMA entries.
true_domain_rule_ids: list[str] = []
mapped_source_rule_ids = [
    item["source_rule_id"] for item in obligation_map["source_rules"]
]
obligation_source_rule_ids = [
    item["source_rule_id"] for item in obligation_map["obligations"]
]
assert mapped_source_rule_ids == true_domain_rule_ids
assert obligation_source_rule_ids == true_domain_rule_ids
assert obligation_map["trust_parameters"] == []
assert input_manifest["source_rules"] == []
assert input_manifest["operational_rules"] == []
assert input_manifest["proved_derived_lemmas"] == []
assert len(input_manifest["definitions"]) == 6

target_from_sources = klean_export.target_statement(GENERATED)
lean_sources = sorted(GENERATED.rglob("*.lean"))
theorem_lines = []
for source in lean_sources:
    for line_no, line in enumerate(source.read_text().splitlines(), start=1):
        if re.match(r"^\s*theorem\b", line):
            theorem_lines.append(
                f"{source.relative_to(GENERATED)}:{line_no}:{line.strip()}"
            )

assert generator_manifest["obligation_count"] == 0
assert export_result["obligation_count"] == 0
assert preflight["obligation_count"] == 0
assert obligation_map["obligations"] == []
assert target_from_sources is None
assert theorem_lines == []
assert generator_manifest["target"] is None
assert preflight["target"] is None
assert resolution["target"] is None
assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
assert preflight["status"] == "KLEAN_NO_OBLIGATIONS"
assert resolution["selections"]["klean_generation"]["status"] == (
    "KLEAN_NO_OBLIGATIONS"
)
assert resolution["mode"] == os.environ["AUDIT_MODE"] == "CLASSIFICATION_ONLY"
assert resolution["stage5_result"] is None
assert resolution["lean_workspace"] is None
assert resolution["lean_invocation"] is None
assert not Path("/candidate").exists()

print("resolved_input_sha256 =", resolved_digest)
print(
    "recorded_and_computed_hashes =",
    json.dumps(computed_hashes, indent=2, sort_keys=True),
)
print(
    "stage1_source_hash_count =",
    len(source_hashes),
    "all_match =",
    True,
)
print("toolchain_lock_matches_generator =", True)
print("generator_obligation_map_sha256 =", file_sha256(
    GENERATED / "obligation-map.json"
))
print("trust_inventory_sha256 =", file_sha256(
    GENERATION / "trust-inventory.json"
))
print("true_domain_rule_ids =", true_domain_rule_ids)
print("mapped_source_rule_ids =", mapped_source_rule_ids)
print("obligation_source_rule_ids =", obligation_source_rule_ids)
print("target_from_generated_sources =", target_from_sources)
print("generated_theorem_lines =", theorem_lines)
print("stage4_status =", export_result["status"])
print("stage5_candidate_absent =", not Path("/candidate").exists())
print("trust_allowlist_count =", len(trust_inventory["allowlist"]))
print("RESULT: PASS")
