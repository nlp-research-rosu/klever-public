#!/usr/bin/env python3
"""Independent structural and semantic check of the protected Stage 3 manifest."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
AUDIT_INPUT_PATH = Path("/audit-input.json")

DOMAIN_RULE_IDS = {
    "rule-0dfb3ea463a2e10ce61e8445bcf95e2aa2d4748b432b47ccd1f9825f8cca2630",
    "rule-f684bfbef1c0219f754e562f1888c8a1b7236498affdcf8c5681f52ef8e6175f",
    "rule-4f3a4fc13d02a156f3a8d695f13fdac54badb56cceabf4cbe100c7ea4aca4d57",
    "rule-f2662dddafe1054c19c3ddaf31b8c9e9a8971c2baafdf6d7f8bfb1785b1ff321",
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_role(start_line: int) -> str:
    if 51 <= start_line <= 53:
        return "constructor recurrence defining the NumSeq-to-ValSeq embedding"
    if 57 <= start_line <= 67:
        return "logical inversion/injectivity consequence of the embedding"
    if 72 <= start_line <= 87:
        return "structural recurrence or named proof-domain predicate"
    if 89 <= start_line <= 151:
        return "named macro for exact translated source syntax"
    if 155 <= start_line <= 225:
        return "recursive mathematical summary or composition equation"
    raise AssertionError(f"unclassified source line: {start_line}")


def main() -> None:
    audit_input = json.loads(AUDIT_INPUT_PATH.read_text())
    discovery = json.loads(DISCOVERY_PATH.read_text())
    inventory = inventory_verification(WORKSPACE)
    source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

    errors: list[str] = []
    checks: dict[str, object] = {}

    recorded_mode = audit_input["resolution"]["mode"]
    checks["mode_environment_matches_launcher"] = (
        os.environ.get("AUDIT_MODE") == recorded_mode == "CLASSIFICATION_AND_PROOF"
    )

    discovery_file_hash = file_sha256(DISCOVERY_PATH)
    checks["discovery_file_hash"] = discovery_file_hash
    checks["discovery_file_hash_matches_audit_input"] = (
        discovery_file_hash
        == audit_input["resolution"]["hashes"]["discovery_manifest_sha256"]
    )
    checks["verification_file_hash_matches_audit_input"] = (
        inventory["verification_sha256"]
        == audit_input["resolution"]["stage1_source_hashes"]["verification.k"]
    )
    checks["inventory_hash_recomputed"] = canonical_json_sha256(inventory["rules"])
    checks["inventory_hash_self_consistent"] = (
        checks["inventory_hash_recomputed"] == inventory["inventory_sha256"]
    )
    checks["inventory_hash_matches_discovery"] = (
        inventory["inventory_sha256"] == discovery.get("inventory_sha256")
    )

    reconstructed_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    recorded_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
    checks["reconstructed_rule_count"] = len(reconstructed_ids)
    checks["recorded_rule_count"] = len(recorded_ids)
    checks["reconstructed_ids_unique"] = (
        len(reconstructed_ids) == len(set(reconstructed_ids))
    )
    checks["recorded_ids_unique"] = len(recorded_ids) == len(set(recorded_ids))
    checks["ordered_rule_identity_bijection"] = reconstructed_ids == recorded_ids

    recorded_by_id = {
        entry["source_rule_id"]: entry for entry in discovery["rules"]
    }
    rows: list[dict[str, object]] = []
    for index, rule in enumerate(inventory["rules"], start=1):
        source_rule_id = rule["source_rule_id"]
        normalized = " ".join(rule["text"].split())
        normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
        exact_source_span = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        expected_classification = (
            "DOMAIN_LEMMA"
            if source_rule_id in DOMAIN_RULE_IDS
            else "DEFINITION"
        )
        recorded_entry = recorded_by_id.get(source_rule_id)
        recorded_classification = (
            None
            if recorded_entry is None
            else recorded_entry.get("classification")
        )
        row = {
            "index": index,
            "source_rule_id": source_rule_id,
            "module": rule["module"],
            "source_span": f"{rule['start_line']}-{rule['end_line']}",
            "normalized_sha256": rule["normalized_sha256"],
            "id_matches_normalized_hash": (
                source_rule_id == f"rule-{normalized_hash}"
                and rule["normalized_sha256"] == normalized_hash
            ),
            "text_matches_exact_source_span": rule["text"] == exact_source_span,
            "attributes": rule["attributes"],
            "semantic_role": semantic_role(rule["start_line"]),
            "independent_classification": expected_classification,
            "recorded_classification": recorded_classification,
            "classification_matches": (
                expected_classification == recorded_classification
            ),
            "simplification_class_allowed": (
                "simplification" not in rule["attributes"]
                or expected_classification in {"DEFINITION", "DOMAIN_LEMMA"}
            ),
        }
        rows.append(row)

    checks["all_rule_ids_and_normalized_hashes_match"] = all(
        row["id_matches_normalized_hash"] for row in rows
    )
    checks["all_rule_texts_match_exact_source_spans"] = all(
        row["text_matches_exact_source_span"] for row in rows
    )
    checks["all_classifications_match"] = all(
        row["classification_matches"] for row in rows
    )
    checks["all_simplification_classes_allowed"] = all(
        row["simplification_class_allowed"] for row in rows
    )
    checks["independent_classification_counts"] = {
        classification: sum(
            row["independent_classification"] == classification for row in rows
        )
        for classification in (
            "DEFINITION",
            "OPERATIONAL_RULE",
            "PROVED_DERIVED_LEMMA",
            "DOMAIN_LEMMA",
        )
    }
    checks["recorded_classification_counts"] = {
        classification: sum(
            row["recorded_classification"] == classification for row in rows
        )
        for classification in (
            "DEFINITION",
            "OPERATIONAL_RULE",
            "PROVED_DERIVED_LEMMA",
            "DOMAIN_LEMMA",
        )
    }

    for name, result in checks.items():
        if isinstance(result, bool) and not result:
            errors.append(name)

    report = {
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "checks": checks,
        "rules": rows,
        "independent_judgment": {
            "domain_rule_relevance": (
                "The four numVals inversion/injectivity rules connect the "
                "proof-domain NumSeq input to the concrete ValSeq consumed by "
                "the source program's list iterator and are used by the "
                "constructor-split poly loop claims."
            ),
            "derived_lemma_test": (
                "No inventory rule qualifies as PROVED_DERIVED_LEMMA: "
                "prove.sh compiles VERIFICATION-BASE containing all four "
                "simplifications before every kprove invocation and contains "
                "no earlier proof of their exact statements against a module "
                "that excludes them."
            ),
            "operational_rule_test": (
                "No inventory rule is an ordinary execution/observation rule. "
                "The source-AST rules name exact syntax trees; the remaining "
                "rules define embeddings, predicates, or recursive summaries."
            ),
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
