#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
)


def load(path: str):
    return json.loads(Path(path).read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load("/audit-input.json")
resolution = audit["resolution"]
discovery = load("/reference/lemma-discovery.json")
source_manifest = load("/reference/generation-tools/source-manifest.json")
generator_manifest = load("/reference/klean-generation/generator-manifest.json")

inventory = k_rule_inventory.inventory_verification(Path("/reference/k-proof"))
validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
)

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
assert canonical_ids == manifest_ids, "Stage 3 rule identities are reordered or differ"
assert len(canonical_ids) == len(set(canonical_ids)), "canonical duplicate rule"
assert len(manifest_ids) == len(set(manifest_ids)), "manifest duplicate rule"
assert discovery["inventory_sha256"] == inventory["inventory_sha256"]

print("AUDIT_MODE", resolution["mode"])
print("PROBLEM", resolution["problem_id"])
print("CONDITION", resolution["condition"])
print("SEMANTICS_MODE", resolution["semantics_mode"])
print("INVENTORY_SCHEMA", inventory["schema_version"])
print("VERIFICATION_SHA256", inventory["verification_sha256"])
print("VERIFICATION_MODULE", inventory["verification_module"])
print("VERIFICATION_MODULE_CLOSURE", json.dumps(inventory["verification_modules"]))
print("RULE_COUNT", len(inventory["rules"]))
print("INVENTORY_SHA256", inventory["inventory_sha256"])
print("MANIFEST_ORDER_AND_BIJECTION", "PASS")
print("TRUST_BOUNDARY_VALIDATOR", "PASS")
print()
print("CANONICAL_RULES")
classification_by_id = {
    item["source_rule_id"]: item for item in discovery["rules"]
}
for index, rule in enumerate(inventory["rules"], 1):
    classified = classification_by_id[rule["source_rule_id"]]
    assert rule["source_rule_id"] == "rule-" + rule["normalized_sha256"]
    print(json.dumps({
        "index": index,
        "module": rule["module"],
        "start_line": rule["start_line"],
        "end_line": rule["end_line"],
        "attributes": rule["attributes"],
        "normalized_sha256": rule["normalized_sha256"],
        "source_rule_id": rule["source_rule_id"],
        "classification": classified["classification"],
        "normalized_source": " ".join(rule["text"].split()),
    }, sort_keys=True))

producer_hashes = {
    name: sha(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
assert producer_hashes == source_manifest["files"]
assert producer_hashes["klean_export.py"] == generator_manifest["exporter_sha256"]
assert producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"]
source_image = source_manifest["generator_image_id"]
generator_image = generator_manifest["provenance"]["generator_image_id"]
audit_image = "sha256:" + Path(resolution["generation_producer_sources"]).name
assert source_image == generator_image == audit_image
producer_tree = pipeline_contract.sha256_tree(Path("/reference/generation-tools"))
assert producer_tree == resolution["hashes"]["generation_producer_sources_sha256"]
print()
print("PRODUCER_HASHES", json.dumps(producer_hashes, sort_keys=True))
print("PRODUCER_TREE_SHA256", producer_tree)
print("GENERATOR_IMAGE_ID", source_image)
print("PRODUCER_PROVENANCE", "PASS")

tree_checks = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(Path("/candidate")),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
    "generated_tree_sha256": klean_export.tree_digest(Path("/reference/klean-generation/generated")),
}
for key, observed in tree_checks.items():
    expected = resolution["hashes"][key]
    print("TREE_HASH", key, observed, "EXPECTED", expected, "MATCH", observed == expected)
    assert observed == expected

stage1_hashes = {}
for path in sorted(Path("/reference/k-proof").rglob("*")):
    if path.is_file() and not path.is_symlink():
        stage1_hashes[path.relative_to("/reference/k-proof").as_posix()] = sha(path)
assert stage1_hashes == resolution["stage1_source_hashes"]
print("STAGE1_SOURCE_HASH_COUNT", len(stage1_hashes))
print("STAGE1_SOURCE_HASHES", "PASS")
print("ALL_RECORDED_TREE_HASHES", "PASS")
