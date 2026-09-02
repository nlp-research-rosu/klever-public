#!/usr/bin/env python3
"""Independent Stage 3 inventory reconstruction and strict manifest comparison."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    manifest = json.loads(MANIFEST.read_text())
    source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    classified_ids = [rule["source_rule_id"] for rule in manifest["rules"]]
    manifest_by_id = {
        rule["source_rule_id"]: rule for rule in manifest["rules"]
    }

    reconstructed = []
    span_checks = []
    for rule in inventory["rules"]:
        normalized = " ".join(rule["text"].split())
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        span_text = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        span_matches = span_text == rule["text"]
        hash_matches = digest == rule["normalized_sha256"]
        id_matches = rule["source_rule_id"] == f"rule-{digest}"
        span_checks.append(span_matches and hash_matches and id_matches)
        reconstructed.append(
            {
                **rule,
                "span_text_matches": span_matches,
                "recomputed_normalized_sha256": digest,
                "normalized_hash_matches": hash_matches,
                "source_rule_id_matches": id_matches,
                "classification": manifest_by_id.get(
                    rule["source_rule_id"], {}
                ).get("classification"),
                "rationale": manifest_by_id.get(
                    rule["source_rule_id"], {}
                ).get("rationale"),
            }
        )

    duplicate_manifest_ids = sorted(
        {
            source_rule_id
            for source_rule_id in classified_ids
            if classified_ids.count(source_rule_id) > 1
        }
    )
    canonical_set = set(canonical_ids)
    classified_set = set(classified_ids)
    report = {
        "workspace": str(WORKSPACE),
        "verification_file": inventory["verification_file"],
        "verification_sha256": inventory["verification_sha256"],
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
        "rule_count": len(inventory["rules"]),
        "canonical_rule_ids": canonical_ids,
        "manifest_rule_ids": classified_ids,
        "strict_order_match": classified_ids == canonical_ids,
        "duplicate_manifest_ids": duplicate_manifest_ids,
        "omitted_manifest_ids": [
            item for item in canonical_ids if item not in classified_set
        ],
        "extra_manifest_ids": [
            item for item in classified_ids if item not in canonical_set
        ],
        "inventory_sha256": inventory["inventory_sha256"],
        "recomputed_inventory_sha256": canonical_json_sha256(
            inventory["rules"]
        ),
        "manifest_inventory_sha256": manifest.get("inventory_sha256"),
        "inventory_hashes_match": (
            inventory["inventory_sha256"]
            == canonical_json_sha256(inventory["rules"])
            == manifest.get("inventory_sha256")
        ),
        "all_span_hash_id_checks_pass": all(span_checks),
        "rules": reconstructed,
    }
    report["bijection_pass"] = (
        report["strict_order_match"]
        and not report["duplicate_manifest_ids"]
        and not report["omitted_manifest_ids"]
        and not report["extra_manifest_ids"]
        and report["inventory_hashes_match"]
        and report["all_span_hash_id_checks_pass"]
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
