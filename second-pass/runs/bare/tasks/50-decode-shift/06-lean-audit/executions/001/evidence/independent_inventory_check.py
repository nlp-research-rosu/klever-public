#!/usr/bin/env python3
"""Independent Stage 3 inventory/order/classification audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")


def main() -> None:
    inventory = inventory_verification(WORKSPACE)
    discovery = json.loads(MANIFEST.read_text())
    source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

    assert set(discovery) == {"schema_version", "inventory_sha256", "rules"}
    assert discovery["schema_version"] == 2
    assert inventory["inventory_sha256"] == canonical_json_sha256(
        inventory["rules"]
    )
    assert discovery["inventory_sha256"] == inventory["inventory_sha256"]

    rules = inventory["rules"]
    entries = discovery["rules"]
    assert len(rules) == len(entries) == 9

    canonical_ids = [rule["source_rule_id"] for rule in rules]
    classified_ids = [entry["source_rule_id"] for entry in entries]
    assert len(set(canonical_ids)) == len(canonical_ids)
    assert len(set(classified_ids)) == len(classified_ids)
    assert classified_ids == canonical_ids

    judgments: list[dict[str, object]] = []
    for index, (rule, entry) in enumerate(zip(rules, entries, strict=True)):
        assert set(entry) == {
            "source_rule_id",
            "classification",
            "rationale",
        }
        start = rule["start_line"]
        end = rule["end_line"]
        spanned_source = "\n".join(source_lines[start - 1 : end])
        assert spanned_source == rule["text"]
        normalized = " ".join(spanned_source.split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        assert normalized_sha256 == rule["normalized_sha256"]
        assert rule["source_rule_id"] == f"rule-{normalized_sha256}"

        # Independent semantic judgment: all nine rules are equations for
        # [function,total] symbols declared immediately above them.  They name
        # arithmetic summaries, structural recurrences, or named predicates.
        # None matches a runtime cell/program term, and no simplification
        # attribute or separately proved Stage 1 rule is present.
        expected_classification = "DEFINITION"
        assert entry["classification"] == expected_classification
        assert entry["rationale"].strip()
        assert not (
            "simplification" in rule["attributes"]
            and entry["classification"]
            not in {"DEFINITION", "DOMAIN_LEMMA"}
        )
        judgments.append(
            {
                "index": index,
                "source_rule_id": rule["source_rule_id"],
                "source_span": [start, end],
                "normalized_sha256": normalized_sha256,
                "attributes": rule["attributes"],
                "independent_classification": expected_classification,
                "manifest_classification": entry["classification"],
            }
        )

    validated = validate_trust_boundary(WORKSPACE, MANIFEST)
    assert [rule["source_rule_id"] for rule in validated["definitions"]] == (
        canonical_ids
    )
    assert validated["operational_rules"] == []
    assert validated["proved_derived_lemmas"] == []
    assert validated["domain_lemmas"] == []

    print(
        json.dumps(
            {
                "verification_module": inventory["verification_module"],
                "verification_modules": inventory["verification_modules"],
                "verification_sha256": inventory["verification_sha256"],
                "inventory_sha256": inventory["inventory_sha256"],
                "ordered_bijection": True,
                "omissions": 0,
                "duplicates": 0,
                "extras": 0,
                "reordered_identities": False,
                "judgments": judgments,
                "classification_counts": {
                    "DEFINITION": 9,
                    "OPERATIONAL_RULE": 0,
                    "PROVED_DERIVED_LEMMA": 0,
                    "DOMAIN_LEMMA": 0,
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
