#!/usr/bin/env python3
"""Reconstruct the canonical K rule inventory and compare Stage 3 bijectively."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")
OUTPUT = Path("/audit-output/evidence/reconstructed-inventory.json")


def main() -> int:
    inventory = inventory_verification(WORKSPACE)
    stage3 = json.loads(MANIFEST.read_text())
    OUTPUT.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n")

    canonical = inventory["rules"]
    classified = stage3["rules"]
    canonical_ids = [rule["source_rule_id"] for rule in canonical]
    classified_ids = [rule["source_rule_id"] for rule in classified]

    id_shape_failures = [
        rule["source_rule_id"]
        for rule in canonical
        if rule["source_rule_id"] != f"rule-{rule['normalized_sha256']}"
    ]
    source_span_failures: list[dict[str, object]] = []
    verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()
    for rule in canonical:
        observed = "\n".join(
            verification_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        if observed != rule["text"]:
            source_span_failures.append(
                {
                    "source_rule_id": rule["source_rule_id"],
                    "reported_text": rule["text"],
                    "source_slice": observed,
                }
            )

    duplicate_canonical = sorted(
        source_rule_id
        for source_rule_id, count in Counter(canonical_ids).items()
        if count != 1
    )
    duplicate_stage3 = sorted(
        source_rule_id
        for source_rule_id, count in Counter(classified_ids).items()
        if count != 1
    )
    omitted = [source_rule_id for source_rule_id in canonical_ids if source_rule_id not in classified_ids]
    extra = [source_rule_id for source_rule_id in classified_ids if source_rule_id not in canonical_ids]
    reordered = canonical_ids != classified_ids
    recomputed_inventory_hash = canonical_json_sha256(canonical)

    report = {
        "verification_file": inventory["verification_file"],
        "verification_sha256": inventory["verification_sha256"],
        "verification_module": inventory["verification_module"],
        "verification_modules_closure": inventory["verification_modules"],
        "canonical_rule_count": len(canonical),
        "classified_rule_count": len(classified),
        "canonical_inventory_sha256": inventory["inventory_sha256"],
        "independently_recomputed_inventory_sha256": recomputed_inventory_hash,
        "stage3_inventory_sha256": stage3["inventory_sha256"],
        "canonical_ids": canonical_ids,
        "stage3_ids": classified_ids,
        "duplicate_canonical_ids": duplicate_canonical,
        "duplicate_stage3_ids": duplicate_stage3,
        "omitted_stage3_ids": omitted,
        "extra_stage3_ids": extra,
        "reordered": reordered,
        "source_rule_id_shape_failures": id_shape_failures,
        "source_span_failures": source_span_failures,
    }
    failures = (
        duplicate_canonical
        or duplicate_stage3
        or omitted
        or extra
        or reordered
        or id_shape_failures
        or source_span_failures
        or recomputed_inventory_hash != inventory["inventory_sha256"]
        or stage3["inventory_sha256"] != inventory["inventory_sha256"]
    )
    report["status"] = "FAIL" if failures else "PASS"
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
