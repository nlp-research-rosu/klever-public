#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, klean_export


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


generation = Path("/reference/klean-generation")
generated = generation / "generated"
obligation_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_path.read_text())
generator = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
discovery_hash = sha256_file(Path("/reference/lemma-discovery.json"))
inventory = k_rule_inventory.inventory_verification(Path("/reference/k-proof"))
canonical = {r["source_rule_id"]: r for r in inventory["rules"]}
domain = input_manifest["source_rules"]
obligations = obligation_map["obligations"]

domain_ids = [r["source_rule_id"] for r in domain]
mapped_source_ids = [r["source_rule_id"] for r in obligation_map["source_rules"]]
obligation_ids = [r["source_rule_id"] for r in obligations]

per_obligation = []
for source, obligation in zip(domain, obligations, strict=True):
    canonical_rule = canonical[source["source_rule_id"]]
    per_obligation.append({
        "source_rule_id": source["source_rule_id"],
        "canonical_source_match": all(
            source.get(key) == canonical_rule.get(key)
            for key in (
                "source_rule_id", "module", "file", "start_line",
                "end_line", "normalized_sha256", "attributes", "text",
            )
        ),
        "obligation_source_id_match": (
            obligation["source_rule_id"] == source["source_rule_id"]
        ),
        "obligation_source_span_match": obligation["source_span"] == {
            "start_line": source["start_line"],
            "end_line": source["end_line"],
        },
        "obligation_normalized_hash_match": (
            obligation["normalized_sha256"] == source["normalized_sha256"]
        ),
        "obligation_inventory_hash_match": (
            obligation["inventory_sha256"] == inventory["inventory_sha256"]
        ),
        "obligation_discovery_hash_match": (
            obligation["discovery_manifest_sha256"] == discovery_hash
        ),
        "lean_conjunct_hash_actual": sha256_bytes(
            obligation["lean_conjunct"].encode()
        ),
        "lean_conjunct_hash_recorded": obligation[
            "lean_conjunct_sha256"
        ],
    })

actual_target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
print(json.dumps({
    "domain_rule_ids": domain_ids,
    "mapped_source_rule_ids": mapped_source_ids,
    "obligation_rule_ids": obligation_ids,
    "exact_ordered_bijection": (
        domain_ids == mapped_source_ids == obligation_ids
        and len(domain_ids) == len(set(domain_ids))
    ),
    "domain_count": len(domain_ids),
    "manifest_obligation_count": generator["obligation_count"],
    "export_obligation_count": export_result["obligation_count"],
    "per_obligation": per_obligation,
    "obligation_map_sha256_actual": sha256_file(obligation_path),
    "obligation_map_sha256_recorded": generator["obligation_map_sha256"],
    "expected_definition_sha256": sha256_bytes(
        expected_definition.encode()
    ),
    "actual_target": actual_target,
    "generator_target": generator["target"],
    "audit_input_target": audit["target"],
    "target_identity_all_match": (
        actual_target == generator["target"] == audit["target"]
    ),
    "generated_tree_sha256_actual": klean_export.tree_digest(generated),
    "generated_tree_sha256_generator": generator["generated_tree_sha256"],
    "generated_tree_sha256_audit": audit["hashes"]["generated_tree_sha256"],
    "discovery_sha256_actual": discovery_hash,
    "discovery_sha256_input_manifest": input_manifest[
        "stage3_discovery_manifest_sha256"
    ],
    "discovery_sha256_audit": audit["hashes"][
        "discovery_manifest_sha256"
    ],
    "inventory_sha256_actual": inventory["inventory_sha256"],
    "inventory_sha256_input_manifest": input_manifest["inventory_sha256"],
    "verification_sha256_actual": sha256_file(
        Path("/reference/k-proof/verification.k")
    ),
    "verification_sha256_input_manifest": input_manifest[
        "verification_sha256"
    ],
}, indent=2, sort_keys=True))
