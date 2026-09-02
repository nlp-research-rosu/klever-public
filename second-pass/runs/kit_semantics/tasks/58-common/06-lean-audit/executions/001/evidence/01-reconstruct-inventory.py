import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
inventory = inventory_verification(workspace)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in discovery["rules"]]

print("verification_module", inventory["verification_module"])
print("verification_modules", inventory["verification_modules"])
print("verification_sha256", inventory["verification_sha256"])
print("inventory_sha256_reconstructed", inventory["inventory_sha256"])
print("inventory_sha256_protected", discovery["inventory_sha256"])
print("inventory_count", len(inventory_ids))
print("classification_count", len(classified_ids))
print("same_order", inventory_ids == classified_ids)
print("unique_inventory", len(inventory_ids) == len(set(inventory_ids)))
print("unique_classification", len(classified_ids) == len(set(classified_ids)))
print("omitted", sorted(set(inventory_ids) - set(classified_ids)))
print("extra", sorted(set(classified_ids) - set(inventory_ids)))

classification_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
for index, rule in enumerate(inventory["rules"], 1):
    normalized = " ".join(rule["text"].split())
    recomputed_hash = hashlib.sha256(normalized.encode()).hexdigest()
    print(
        "rule",
        index,
        rule["source_rule_id"],
        f"{rule['module']}:{rule['start_line']}-{rule['end_line']}",
        f"attributes={rule['attributes']}",
        f"normalized_sha256={rule['normalized_sha256']}",
        f"normalized_hash_recomputed={recomputed_hash}",
        f"classification={classification_by_id[rule['source_rule_id']]}",
    )
    print(rule["text"])

independent_domain_ids = [
    "rule-cd11c71e1459d61e91176cc439f01696c9d8116dd9313d8d67eb714d1144a5b0"
]
source_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
print("independent_domain_ids", independent_domain_ids)
print("mapped_source_rule_ids", source_rule_ids)
print("mapped_obligation_ids", obligation_ids)
print(
    "domain_source_obligation_bijection",
    independent_domain_ids == source_rule_ids == obligation_ids
    and len(obligation_ids) == len(set(obligation_ids)),
)
for source_rule, obligation in zip(
    obligation_map["source_rules"],
    obligation_map["obligations"],
    strict=True,
):
    print(
        "obligation_provenance_exact",
        obligation["source_span"]
        == {
            "start_line": source_rule["start_line"],
            "end_line": source_rule["end_line"],
        }
        and obligation["normalized_sha256"]
        == source_rule["normalized_sha256"]
        and obligation["inventory_sha256"]
        == source_rule["inventory_sha256"]
        and obligation["discovery_manifest_sha256"]
        == source_rule["discovery_manifest_sha256"],
    )
    print(
        "lean_conjunct_hash_exact",
        hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest()
        == obligation["lean_conjunct_sha256"],
    )
    print("lean_conjunct", obligation["lean_conjunct"])
