#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and manifest comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
MANIFEST_PATH = Path("/reference/lemma-discovery.json")


def main() -> None:
    reconstructed = inventory_verification(WORKSPACE)
    manifest = json.loads(MANIFEST_PATH.read_text())
    source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

    per_rule = []
    for index, rule in enumerate(reconstructed["rules"]):
        exact_span = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        ).rstrip(" \t\r\n")
        normalized = " ".join(exact_span.split())
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        per_rule.append(
            {
                "index": index,
                "module": rule["module"],
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
                "span_exact_match": exact_span == rule["text"],
                "normalized_sha256": digest,
                "normalized_hash_match": digest == rule["normalized_sha256"],
                "source_rule_id": f"rule-{digest}",
                "source_rule_id_match": f"rule-{digest}" == rule["source_rule_id"],
                "attributes": rule["attributes"],
                "text": rule["text"],
            }
        )

    inventory_ids = [rule["source_rule_id"] for rule in reconstructed["rules"]]
    manifest_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
    classifications = {
        rule["source_rule_id"]: rule["classification"]
        for rule in manifest["rules"]
    }
    simplification_violations = [
        rule["source_rule_id"]
        for rule in reconstructed["rules"]
        if "simplification" in rule["attributes"]
        and classifications.get(rule["source_rule_id"])
        not in {"DEFINITION", "DOMAIN_LEMMA"}
    ]
    report = {
        "reconstructed": reconstructed,
        "checks": {
            "canonical_inventory_sha256_recomputed": canonical_json_sha256(
                reconstructed["rules"]
            ),
            "canonical_inventory_sha256_matches_reconstruction": (
                canonical_json_sha256(reconstructed["rules"])
                == reconstructed["inventory_sha256"]
            ),
            "manifest_inventory_sha256_matches": (
                manifest["inventory_sha256"]
                == reconstructed["inventory_sha256"]
            ),
            "inventory_count": len(inventory_ids),
            "manifest_count": len(manifest_ids),
            "inventory_ids_unique": len(inventory_ids) == len(set(inventory_ids)),
            "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
            "ordered_identities_exact": manifest_ids == inventory_ids,
            "omitted_from_manifest": sorted(set(inventory_ids) - set(manifest_ids)),
            "extra_in_manifest": sorted(set(manifest_ids) - set(inventory_ids)),
            "simplification_classification_violations": simplification_violations,
            "all_source_spans_exact": all(x["span_exact_match"] for x in per_rule),
            "all_normalized_hashes_exact": all(
                x["normalized_hash_match"] for x in per_rule
            ),
            "all_source_rule_ids_exact": all(
                x["source_rule_id_match"] for x in per_rule
            ),
        },
        "per_rule_recomputation": per_rule,
        "manifest_rules": manifest["rules"],
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    checks = report["checks"]
    required_bools = [
        "canonical_inventory_sha256_matches_reconstruction",
        "manifest_inventory_sha256_matches",
        "inventory_ids_unique",
        "manifest_ids_unique",
        "ordered_identities_exact",
        "all_source_spans_exact",
        "all_normalized_hashes_exact",
        "all_source_rule_ids_exact",
    ]
    if not all(checks[key] for key in required_bools):
        raise SystemExit(1)
    if (
        checks["omitted_from_manifest"]
        or checks["extra_in_manifest"]
        or checks["simplification_classification_violations"]
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
