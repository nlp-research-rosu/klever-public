#!/usr/bin/env python3
"""Independently check Stage 3-domain to Stage 4-obligation identity."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import (
    expected_target_definition,
    target_statement,
    tree_digest,
)


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def sha256_file(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


workspace = Path("/reference/k-proof")
generated = Path("/reference/klean-generation/generated")
inventory = inventory_verification(workspace)
discovery = load("/reference/lemma-discovery.json")
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
input_manifest = load("/reference/klean-generation/input-manifest.json")
generator_manifest = load(
    "/reference/klean-generation/generator-manifest.json"
)
export_result = load("/reference/klean-generation/export-result.json")
audit = load("/audit-input.json")["resolution"]

rules_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}
classification_by_id = {
    rule["source_rule_id"]: rule for rule in discovery["rules"]
}
domain_ids = [
    rule["source_rule_id"]
    for rule in discovery["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
obligations = obligation_map["obligations"]
obligation_ids = [item["source_rule_id"] for item in obligations]

print("DOMAIN/OBLIGATION ORDER")
print(json.dumps({"domain_ids": domain_ids, "obligation_ids": obligation_ids}, indent=2))

per_obligation = []
for index, obligation in enumerate(obligations):
    source_id = obligation["source_rule_id"]
    source = rules_by_id[source_id]
    conjunct = obligation["lean_conjunct"]
    entry = {
        "index": index,
        "source_rule_id": source_id,
        "classification": classification_by_id[source_id]["classification"],
        "source_span_recorded": obligation["source_span"],
        "source_span_reconstructed": {
            "start_line": source["start_line"],
            "end_line": source["end_line"],
        },
        "normalized_sha_recorded": obligation["normalized_sha256"],
        "normalized_sha_reconstructed": source["normalized_sha256"],
        "conjunct_sha_recorded": obligation["lean_conjunct_sha256"],
        "conjunct_sha_recomputed": hashlib.sha256(conjunct.encode()).hexdigest(),
        "discovery_sha_recorded": obligation[
            "discovery_manifest_sha256"
        ],
        "discovery_sha_actual": sha256_file(
            "/reference/lemma-discovery.json"
        ),
        "inventory_sha_recorded": obligation["inventory_sha256"],
        "inventory_sha_reconstructed": inventory["inventory_sha256"],
        "contains_true_as_standalone_conjunct": bool(
            re.search(r"(^|\s|[(])True($|\s|[)])", conjunct)
        ),
        "conjunct": conjunct,
        "source_text": source["text"],
    }
    entry["all_bindings_match"] = (
        entry["classification"] == "DOMAIN_LEMMA"
        and entry["source_span_recorded"]
        == entry["source_span_reconstructed"]
        and entry["normalized_sha_recorded"]
        == entry["normalized_sha_reconstructed"]
        and entry["conjunct_sha_recorded"]
        == entry["conjunct_sha_recomputed"]
        and entry["discovery_sha_recorded"]
        == entry["discovery_sha_actual"]
        and entry["inventory_sha_recorded"]
        == entry["inventory_sha_reconstructed"]
        and not entry["contains_true_as_standalone_conjunct"]
    )
    per_obligation.append(entry)
print("\nPER-OBLIGATION BINDINGS")
print(json.dumps(per_obligation, indent=2, sort_keys=True))

target = target_statement(generated)
expected_definition = expected_target_definition(obligation_map)
lemmas_text = (
    generated / "Klean106F" / "Lemmas.lean"
).read_text()
matches = list(
    re.finditer(
        r"(?ms)^\s*def\s+targetStatement\b.*?"
        r"(?=^\s*end\s+\S+\s*$)",
        lemmas_text,
    )
)
actual_definition = matches[0].group(0).strip() if len(matches) == 1 else None

input_domain_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
map_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
input_definition_ids = [
    rule["source_rule_id"] for rule in input_manifest["definitions"]
]
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
expected_definition_ids = [
    source_id for source_id in inventory_ids if source_id not in domain_ids
]

checks = {
    "domain_set_nonempty": len(domain_ids) == 4,
    "domain_ids_unique": len(domain_ids) == len(set(domain_ids)),
    "obligation_ids_unique": len(obligation_ids)
    == len(set(obligation_ids)),
    "domain_obligation_ordered_bijection": domain_ids == obligation_ids,
    "input_domain_ordered_bijection": domain_ids == input_domain_ids,
    "obligation_map_source_ordered_bijection": domain_ids
    == map_source_ids,
    "input_definitions_ordered_partition": input_definition_ids
    == expected_definition_ids,
    "input_classification_partition_bijective": set(
        input_domain_ids + input_definition_ids
    )
    == set(inventory_ids)
    and len(input_domain_ids + input_definition_ids) == len(inventory_ids),
    "all_obligation_bindings_match": all(
        item["all_bindings_match"] for item in per_obligation
    ),
    "obligation_count_generator": generator_manifest["obligation_count"]
    == len(domain_ids),
    "obligation_count_export": export_result["obligation_count"]
    == len(domain_ids),
    "export_status_ok": export_result["status"] == "OK",
    "obligation_map_hash": sha256_file(
        "/reference/klean-generation/generated/obligation-map.json"
    )
    == generator_manifest["obligation_map_sha256"],
    "generated_tree_hash": tree_digest(generated)
    == generator_manifest["generated_tree_sha256"]
    == audit["hashes"]["generated_tree_sha256"],
    "target_single_definition": len(matches) == 1,
    "target_definition_exactly_generated": actual_definition
    == expected_definition,
    "target_matches_generator": target == generator_manifest["target"],
    "target_matches_audit_input": target == audit["target"],
    "target_definition_sha": hashlib.sha256(
        actual_definition.encode()
    ).hexdigest()
    == target["definition_sha256"],
    "target_statement_sha": hashlib.sha256(
        target["statement"].encode()
    ).hexdigest()
    == target["statement_sha256"],
    "target_has_four_quantified_conjuncts": actual_definition.count("∀ ")
    == 4
    and actual_definition.count("\n    ∧ ") == 3,
    "target_has_no_true_false_or_iff_vacuity": not re.search(
        r"\b(?:True|False)\b|↔", actual_definition
    ),
}
print("\nTARGET")
print(json.dumps(target, indent=2, sort_keys=True))
print("\nEXPECTED TARGET DEFINITION")
print(expected_definition)
print("\nCHECKS")
print(json.dumps(checks, indent=2, sort_keys=True))
print("\nRESULT=" + ("PASS" if all(checks.values()) else "FAIL"))
raise SystemExit(0 if all(checks.values()) else 1)
