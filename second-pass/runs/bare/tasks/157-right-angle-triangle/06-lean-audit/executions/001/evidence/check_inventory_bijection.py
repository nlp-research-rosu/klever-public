#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import (
    canonical_json_sha256,
    inventory_verification,
)


workspace = Path("/reference/k-proof")
verification_lines = (
    workspace / "verification.k"
).read_text().splitlines()

# These two source spans are independently delimited from the two outer
# `rule` sentences in VERIFICATION (the only local module in the closure).
manual_spans = [(8, 14), (19, 47)]
manual_rules = []
for start_line, end_line in manual_spans:
    text = "\n".join(
        verification_lines[start_line - 1 : end_line]
    )
    normalized_sha256 = hashlib.sha256(
        " ".join(text.split()).encode()
    ).hexdigest()
    manual_rules.append(
        {
            "source_rule_id": f"rule-{normalized_sha256}",
            "module": "VERIFICATION",
            "start_line": start_line,
            "end_line": end_line,
            "normalized_sha256": normalized_sha256,
            "attributes": [],
            "text": text,
        }
    )

trusted_inventory = inventory_verification(workspace)
discovery = json.loads(
    Path("/reference/lemma-discovery.json").read_text()
)
discovery_ids = [
    entry["source_rule_id"] for entry in discovery["rules"]
]
manual_ids = [entry["source_rule_id"] for entry in manual_rules]

independent_classification = [
    {
        "source_rule_id": manual_ids[0],
        "classification": "DEFINITION",
        "judgment": (
            "Equation for the declared total function rightTriangle; "
            "it names and unfolds the mathematical postcondition summary."
        ),
        "domain_lemma": False,
        "operational_rule": False,
        "proved_derived_lemma": False,
    },
    {
        "source_rule_id": manual_ids[1],
        "classification": "DEFINITION",
        "judgment": (
            "Equation for the declared nullary function solutionProgram; "
            "it expands a named proof term to the exact translated program AST."
        ),
        "domain_lemma": False,
        "operational_rule": False,
        "proved_derived_lemma": False,
    },
]
classification_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in independent_classification
}
discovery_classification_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}

checks = {
    "manual rules == trusted reconstructed rules": (
        manual_rules == trusted_inventory["rules"]
    ),
    "manual inventory hash == trusted inventory hash": (
        canonical_json_sha256(manual_rules)
        == trusted_inventory["inventory_sha256"]
    ),
    "trusted inventory hash == discovery inventory hash": (
        trusted_inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
    ),
    "discovery IDs preserve exact order": discovery_ids == manual_ids,
    "manual IDs are unique": len(manual_ids) == len(set(manual_ids)),
    "discovery IDs are unique": (
        len(discovery_ids) == len(set(discovery_ids))
    ),
    "discovery has no omitted or extra IDs": (
        set(discovery_ids) == set(manual_ids)
        and len(discovery_ids) == len(manual_ids)
    ),
    "independent classifications == discovery": (
        classification_by_id == discovery_classification_by_id
    ),
    "all simplification rules are definition/domain lemma": all(
        "simplification" not in rule["attributes"]
        or classification_by_id[rule["source_rule_id"]]
        in {"DEFINITION", "DOMAIN_LEMMA"}
        for rule in manual_rules
    ),
    "domain set genuinely empty": all(
        entry["classification"] != "DOMAIN_LEMMA"
        for entry in independent_classification
    ),
}

print(
    json.dumps(
        {
            "verification_module_closure": ["VERIFICATION"],
            "manual_source_spans": manual_spans,
            "manual_rules": manual_rules,
            "manual_inventory_sha256": canonical_json_sha256(manual_rules),
            "trusted_inventory_sha256": trusted_inventory[
                "inventory_sha256"
            ],
            "discovery_inventory_sha256": discovery[
                "inventory_sha256"
            ],
            "independent_classification": independent_classification,
            "discovery_rules": discovery["rules"],
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
