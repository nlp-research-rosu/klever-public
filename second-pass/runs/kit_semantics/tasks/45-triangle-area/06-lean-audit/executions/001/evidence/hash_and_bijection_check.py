#!/usr/bin/env python3
"""Independent hash, provenance, and zero-obligation checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, klean_export, pipeline_contract


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load("/audit-input.json")
resolution = audit["resolution"]
expected = resolution["hashes"]
source_manifest = load("/reference/generation-tools/source-manifest.json")
discovery = load("/reference/lemma-discovery.json")
input_manifest = load("/reference/klean-generation/input-manifest.json")
generator_manifest = load("/reference/klean-generation/generator-manifest.json")
export_result = load("/reference/klean-generation/export-result.json")
trust_inventory = load("/reference/klean-generation/trust-inventory.json")
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
toolchain_lock = load("/reference/klean-toolchain.lock.json")

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_invocation_sha256": None,
    "lean_workspace_sha256": None,
}

for key, value in observed.items():
    assert expected[key] == value, (key, expected[key], value)
print("AUDIT_INPUT_HASHES")
print(json.dumps(observed, indent=2, sort_keys=True))
print("AUDIT_INPUT_HASH_COMPARISON: PASS")

assert resolution["mode"] == "CLASSIFICATION_ONLY"
assert not Path("/candidate").exists()
for stage_key, hash_key in (
    ("k_audit", "k_audit_sha256"),
    ("klean_generation", "klean_generation_sha256"),
):
    selected = resolution["selections"][stage_key]
    assert selected["artifact_sha256"] == observed[hash_key]

producer_hashes = {
    name: file_sha(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
assert producer_hashes == source_manifest["files"]
assert generator_manifest["exporter_sha256"] == producer_hashes["klean_export.py"]
assert generator_manifest["klean_py_sha256"] == producer_hashes["klean.py"]
audit_producer_id = "sha256:" + Path(
    resolution["generation_producer_sources"]
).name
assert source_manifest["generator_image_id"] == audit_producer_id
assert (
    generator_manifest["provenance"]["generator_image_id"]
    == audit_producer_id
)
print("PRODUCER_PROVENANCE")
print(json.dumps({
    "files": producer_hashes,
    "generator_image_id": audit_producer_id,
    "producer_tree_sha256": observed["generation_producer_sources_sha256"],
}, indent=2, sort_keys=True))
print("PRODUCER_PROVENANCE_COMPARISON: PASS")

expected_source_hashes = resolution["stage1_source_hashes"]
actual_files = sorted(
    path for path in Path("/reference/k-proof").rglob("*") if path.is_file()
)
actual_relatives = {path.relative_to("/reference/k-proof").as_posix() for path in actual_files}
assert actual_relatives == set(expected_source_hashes), {
    "missing": sorted(set(expected_source_hashes) - actual_relatives),
    "extra": sorted(actual_relatives - set(expected_source_hashes)),
}
mismatches = []
for relative, digest in expected_source_hashes.items():
    actual = file_sha(Path("/reference/k-proof") / relative)
    if actual != digest:
        mismatches.append((relative, digest, actual))
assert not mismatches, mismatches
print(f"STAGE1_SOURCE_FILE_HASH_COUNT: {len(expected_source_hashes)}")
print("STAGE1_SOURCE_FILE_HASHES: PASS")

inventory = k_rule_inventory.inventory_verification(Path("/reference/k-proof"))
assert discovery["rules"] == inventory["rules"]
assert discovery["inventory_sha256"] == inventory["inventory_sha256"]
assert input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
assert input_manifest["source_rules"] == []
assert input_manifest["definitions"] == []
assert input_manifest["operational_rules"] == []
assert input_manifest["proved_derived_lemmas"] == []
assert input_manifest["summary_functions"] == []
assert obligation_map["source_rules"] == []
assert obligation_map["obligations"] == []
assert obligation_map["trust_parameters"] == []
assert generator_manifest["obligation_count"] == 0
assert export_result["obligation_count"] == 0
assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
assert generator_manifest["target"] is None
assert klean_export.expected_target_definition(obligation_map) is None
assert klean_export.target_statement(
    Path("/reference/klean-generation/generated")
) is None
print("SOURCE_RULE_OBLIGATION_BIJECTION: PASS (0 <-> 0)")
print("FIXED_GENERATED_TARGET: null")

stage1_export = observed["stage1_export_sha256"]
discovery_sha = observed["discovery_manifest_sha256"]
generated_sha = observed["generated_tree_sha256"]
verification_sha = file_sha(Path("/reference/k-proof/verification.k"))
obligation_map_sha = file_sha(
    Path("/reference/klean-generation/generated/obligation-map.json")
)
trust_inventory_sha = file_sha(
    Path("/reference/klean-generation/trust-inventory.json")
)
assert input_manifest["frozen_input_sha256"] == stage1_export
assert input_manifest["stage1_workspace_sha256"] == stage1_export
assert input_manifest["stage3_discovery_manifest_sha256"] == discovery_sha
assert input_manifest["verification_sha256"] == verification_sha
assert generator_manifest["generated_tree_sha256"] == generated_sha
assert generator_manifest["obligation_map_sha256"] == obligation_map_sha
assert generator_manifest["toolchain"] == toolchain_lock
assert generator_manifest["provenance"] == {
    "generator_image_id": audit_producer_id,
    "inventory_sha256": inventory["inventory_sha256"],
    "stage1_workspace_sha256": stage1_export,
    "stage3_discovery_manifest_sha256": discovery_sha,
}
assert export_result["frozen_input_sha256"] == stage1_export
assert export_result["stage3_discovery_manifest_sha256"] == discovery_sha
assert export_result["generated_tree_sha256"] == generated_sha
assert export_result["trust_inventory_sha256"] == trust_inventory_sha
assert trust_inventory["designated_sorries"] == 0
assert trust_inventory["other_sorries"] == 0
print("MANIFEST_CROSS_HASHES: PASS")
print(json.dumps({
    "verification_sha256": verification_sha,
    "obligation_map_sha256": obligation_map_sha,
    "trust_inventory_sha256": trust_inventory_sha,
}, indent=2, sort_keys=True))
