#!/usr/bin/env bash
set -eu

printf '%s\n' '$ nl -ba /reference/k-proof/verification.k'
nl -ba /reference/k-proof/verification.k

printf '%s\n' '$ sed -n 1,260p /reference/lemma-discovery.json'
sed -n '1,260p' /reference/lemma-discovery.json

printf '%s\n' '$ PYTHONPATH=/reference python3 - (trusted inventory, independent span/hash recomputation, exact ordered bijection)'
PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary

workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
discovery_path = Path("/reference/lemma-discovery.json")
audit_path = Path("/audit-input.json")

inventory = inventory_verification(workspace)
validated = validate_trust_boundary(workspace, discovery_path)
discovery = json.loads(discovery_path.read_text())
audit = json.loads(audit_path.read_text())
lines = verification.read_text().splitlines()

manual_rules = []
for rule in inventory["rules"]:
    text = "\n".join(lines[rule["start_line"] - 1 : rule["end_line"]])
    normalized = " ".join(text.split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    manual_rules.append(
        {
            "source_rule_id": f"rule-{digest}",
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "normalized_sha256": digest,
            "attributes": rule["attributes"],
            "text": text,
        }
    )

expected_source_hashes = audit["resolution"]["stage1_source_hashes"]
observed_source_hashes = {}
for relative in expected_source_hashes:
    path = workspace / relative
    observed_source_hashes[relative] = (
        hashlib.sha256(path.read_bytes()).hexdigest()
        if path.is_file() and not path.is_symlink()
        else None
    )

canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
checks = {
    "verification_sha256_matches_audit_input": inventory[
        "verification_sha256"
    ]
    == expected_source_hashes["verification.k"],
    "all_stage1_source_hashes_match_audit_input": observed_source_hashes
    == expected_source_hashes,
    "manual_rules_equal_trusted_inventory": manual_rules
    == inventory["rules"],
    "manual_inventory_hash_matches": canonical_json_sha256(manual_rules)
    == inventory["inventory_sha256"],
    "discovery_inventory_hash_matches": discovery["inventory_sha256"]
    == inventory["inventory_sha256"],
    "ordered_identity_bijection": discovery_ids == canonical_ids,
    "no_duplicate_discovery_ids": len(discovery_ids) == len(set(discovery_ids)),
    "validated_rule_count_matches": len(validated["rules"])
    == len(inventory["rules"]),
}

print(
    json.dumps(
        {
            "trusted_inventory": inventory,
            "manual_rules": manual_rules,
            "discovery_order": discovery_ids,
            "classification_buckets": {
                "definitions": [
                    item["source_rule_id"] for item in validated["definitions"]
                ],
                "operational_rules": [
                    item["source_rule_id"]
                    for item in validated["operational_rules"]
                ],
                "proved_derived_lemmas": [
                    item["source_rule_id"]
                    for item in validated["proved_derived_lemmas"]
                ],
                "domain_lemmas": [
                    item["source_rule_id"]
                    for item in validated["domain_lemmas"]
                ],
            },
            "observed_stage1_source_hashes": observed_source_hashes,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
if not all(checks.values()):
    raise SystemExit(1)
PY
