#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory, lemma_discovery_contract


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def report(label: str, observed, expected) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{status} {label}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")
    if observed != expected:
        raise SystemExit(1)


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
verification = workspace / "verification.k"
inventory = k_rule_inventory.inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, manifest_path
)

print("RECONSTRUCTED_INVENTORY_JSON")
print(json.dumps(inventory, indent=2, sort_keys=True))
print("PROTECTED_CLASSIFICATION_JSON")
print(json.dumps(manifest, indent=2, sort_keys=True))

report("inventory schema_version", inventory["schema_version"], 2)
report("verification file", inventory["verification_file"], "verification.k")
report("verification main module", inventory["verification_module"], "VERIFICATION")
report(
    "local verification-module closure",
    inventory["verification_modules"],
    ["VERIFICATION"],
)
report("inventory rule count", len(inventory["rules"]), 4)

source_lines = verification.read_text().splitlines()
for index, rule in enumerate(inventory["rules"]):
    extracted = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(extracted.split())
    digest = sha256_text(normalized)
    print(f"RULE {index}")
    print(f"  span={rule['start_line']}..{rule['end_line']}")
    print(f"  attributes={rule['attributes']}")
    print(f"  normalized={normalized}")
    report(f"rule {index} exact source span", extracted, rule["text"])
    report(f"rule {index} normalized_sha256", digest, rule["normalized_sha256"])
    report(f"rule {index} source_rule_id", f"rule-{digest}", rule["source_rule_id"])

canonical_inventory_hash = sha256_text(
    json.dumps(
        inventory["rules"],
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
)
report(
    "whole inventory_sha256",
    canonical_inventory_hash,
    inventory["inventory_sha256"],
)
report(
    "protected whole inventory_sha256",
    inventory["inventory_sha256"],
    manifest["inventory_sha256"],
)

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
report("exact source-rule identity order", manifest_ids, canonical_ids)
report("canonical IDs unique", len(set(canonical_ids)), len(canonical_ids))
report("classified IDs unique", len(set(manifest_ids)), len(manifest_ids))
report("exact inventory/classification cardinality", len(manifest_ids), len(canonical_ids))

independent_roles = {
    "rule-d095c8888afcb3dd088fdc3c664435491743c78be0a54a41138084f98215f5e0": "DEFINITION",
    "rule-4a53979712cc9f4bc859fe5870bc02792a9f2614c0ffbd65fb212ab383807457": "OPERATIONAL_RULE",
    "rule-9dd6dbfcce1300ea93b427dc414913c5a4ca13d4f90781207d2a75f3181ad8e0": "DEFINITION",
    "rule-6aad8f4cafb083a2584e89e9e7ced610b42247ea1e1eadf1af9063b72ec8e2cd": "DEFINITION",
}
report("independent role ID set", sorted(independent_roles), sorted(canonical_ids))
for entry in manifest["rules"]:
    source_rule_id = entry["source_rule_id"]
    report(
        f"independent classification {source_rule_id}",
        entry["classification"],
        independent_roles[source_rule_id],
    )

simplification_ids = [
    rule["source_rule_id"]
    for rule in inventory["rules"]
    if "simplification" in rule["attributes"]
]
domain_ids = [
    rule["source_rule_id"]
    for rule in validated["domain_lemmas"]
]
derived_ids = [
    rule["source_rule_id"]
    for rule in validated["proved_derived_lemmas"]
]
report("simplification rule set", simplification_ids, [])
report("independently true DOMAIN_LEMMA set", domain_ids, [])
report("PROVED_DERIVED_LEMMA set", derived_ids, [])
report("validated definition count", len(validated["definitions"]), 3)
report("validated operational-rule count", len(validated["operational_rules"]), 1)
print("BIJECTION_AND_INDEPENDENT_CLASSIFICATION_PASS")
