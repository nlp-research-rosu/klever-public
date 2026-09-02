#!/usr/bin/env bash
set -uo pipefail

PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary

workspace = Path("/reference/k-proof")
verification = workspace / "verification.k"
manifest_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
validated = validate_trust_boundary(workspace, manifest_path)
source_lines = verification.read_text().splitlines()

per_rule_checks = []
for rule in inventory["rules"]:
    span_text = "\n".join(
        source_lines[rule["start_line"] - 1:rule["end_line"]]
    )
    normalized_sha256 = hashlib.sha256(
        " ".join(rule["text"].split()).encode()
    ).hexdigest()
    per_rule_checks.append({
        "source_rule_id": rule["source_rule_id"],
        "source_span_matches_text": span_text == rule["text"],
        "normalized_hash_recomputed": normalized_sha256,
        "normalized_hash_matches": (
            normalized_sha256 == rule["normalized_sha256"]
        ),
        "source_rule_id_matches": (
            rule["source_rule_id"] == "rule-" + normalized_sha256
        ),
    })

canonical_ids = [r["source_rule_id"] for r in inventory["rules"]]
manifest_ids = [r["source_rule_id"] for r in manifest["rules"]]
checks = {
    "inventory_hash_recomputed": (
        canonical_json_sha256(inventory["rules"])
        == inventory["inventory_sha256"]
    ),
    "inventory_hash_matches_manifest": (
        inventory["inventory_sha256"] == manifest["inventory_sha256"]
    ),
    "manifest_ordered_identity_bijection": canonical_ids == manifest_ids,
    "manifest_has_no_duplicates": len(manifest_ids) == len(set(manifest_ids)),
    "manifest_rule_count_matches": len(canonical_ids) == len(manifest_ids),
    "contract_validation_succeeded": (
        validated["inventory_sha256"] == inventory["inventory_sha256"]
    ),
    "all_source_spans_match": all(
        c["source_span_matches_text"] for c in per_rule_checks
    ),
    "all_normalized_hashes_match": all(
        c["normalized_hash_matches"] for c in per_rule_checks
    ),
    "all_source_rule_ids_match": all(
        c["source_rule_id_matches"] for c in per_rule_checks
    ),
}
print(json.dumps({
    "inventory": inventory,
    "manifest_classifications": manifest["rules"],
    "per_rule_checks": per_rule_checks,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}, indent=2, sort_keys=True))
PY
