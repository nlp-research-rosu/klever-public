#!/usr/bin/env python3
"""Independent ordered/bijective checks over the trusted K inventory output."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


workspace = Path("/reference/k-proof")
manifest_path = Path("/reference/lemma-discovery.json")
inventory = inventory_verification(workspace)
manifest = json.loads(manifest_path.read_text())
source = (workspace / "verification.k").read_text()
source_lines = source.splitlines()

canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]

checks: dict[str, object] = {
    "canonical_rule_count": len(canonical_ids),
    "manifest_rule_count": len(manifest_ids),
    "canonical_ids_unique": len(canonical_ids) == len(set(canonical_ids)),
    "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
    "ordered_identity_match": canonical_ids == manifest_ids,
    "set_identity_match": set(canonical_ids) == set(manifest_ids),
    "inventory_hash_recomputed": canonical_json_sha256(inventory["rules"]),
    "inventory_hash_recorded_by_tool": inventory["inventory_sha256"],
    "inventory_hash_in_manifest": manifest["inventory_sha256"],
    "verification_sha256_recomputed": hashlib.sha256(
        (workspace / "verification.k").read_bytes()
    ).hexdigest(),
    "verification_sha256_recorded_by_tool": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_module_closure": inventory["verification_modules"],
    "rules": [],
}

for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    span = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    checks["rules"].append(
        {
            "source_rule_id": rule["source_rule_id"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "span_exact": span == rule["text"],
            "normalized_sha256_recomputed": normalized_sha256,
            "normalized_sha256_recorded": rule["normalized_sha256"],
            "id_is_hash_derived": (
                rule["source_rule_id"] == f"rule-{normalized_sha256}"
            ),
        }
    )

required_true = [
    checks["canonical_ids_unique"],
    checks["manifest_ids_unique"],
    checks["ordered_identity_match"],
    checks["set_identity_match"],
    (
        checks["inventory_hash_recomputed"]
        == checks["inventory_hash_recorded_by_tool"]
        == checks["inventory_hash_in_manifest"]
    ),
    (
        checks["verification_sha256_recomputed"]
        == checks["verification_sha256_recorded_by_tool"]
    ),
    all(
        entry["span_exact"]
        and entry["normalized_sha256_recomputed"]
        == entry["normalized_sha256_recorded"]
        and entry["id_is_hash_derived"]
        for entry in checks["rules"]
    ),
]
checks["all_checks_pass"] = all(required_true)
print(json.dumps(checks, indent=2, sort_keys=True))
raise SystemExit(0 if checks["all_checks_pass"] else 1)
