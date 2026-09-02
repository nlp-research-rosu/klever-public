#!/usr/bin/env bash
set -euxo pipefail
sha256sum \
  /reference/k-proof/verification.k \
  /reference/k-proof/prove.sh \
  /reference/lemma-discovery.json
nl -ba /reference/k-proof/verification.k
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools import k_rule_inventory

workspace = Path("/reference/k-proof")
protected_path = Path("/reference/lemma-discovery.json")
reconstructed = k_rule_inventory.inventory_verification(workspace)
protected = json.loads(protected_path.read_text())

print("RECONSTRUCTED_INVENTORY")
print(json.dumps(reconstructed, indent=2, sort_keys=True))

inventory_rules = reconstructed["rules"]
classified_rules = protected["rules"]
inventory_ids = [entry["source_rule_id"] for entry in inventory_rules]
classified_ids = [entry["source_rule_id"] for entry in classified_rules]

comparisons = {
    "verification_sha256": reconstructed["verification_sha256"],
    "verification_module": reconstructed["verification_module"],
    "verification_modules": reconstructed["verification_modules"],
    "reconstructed_rule_count": len(inventory_rules),
    "protected_rule_count": len(classified_rules),
    "reconstructed_unique_ids": len(set(inventory_ids)),
    "protected_unique_ids": len(set(classified_ids)),
    "ordered_source_rule_ids_equal": inventory_ids == classified_ids,
    "inventory_sha256_reconstructed": reconstructed["inventory_sha256"],
    "inventory_sha256_protected": protected["inventory_sha256"],
    "inventory_sha256_equal": (
        reconstructed["inventory_sha256"] == protected["inventory_sha256"]
    ),
    "omitted_ids": sorted(set(inventory_ids) - set(classified_ids)),
    "extra_ids": sorted(set(classified_ids) - set(inventory_ids)),
}
comparisons["bijection_and_order_pass"] = (
    len(inventory_ids)
    == len(classified_ids)
    == len(set(inventory_ids))
    == len(set(classified_ids))
    and comparisons["ordered_source_rule_ids_equal"]
    and comparisons["inventory_sha256_equal"]
    and not comparisons["omitted_ids"]
    and not comparisons["extra_ids"]
)
print("BIJECTIVE_COMPARISON")
print(json.dumps(comparisons, indent=2, sort_keys=True))
assert comparisons["bijection_and_order_pass"]
PY
