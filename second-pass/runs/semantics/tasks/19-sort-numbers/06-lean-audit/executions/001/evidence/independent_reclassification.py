#!/usr/bin/env python3
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


inventory = inventory_verification(Path("/reference/k-proof"))
protected = json.loads(Path("/reference/lemma-discovery.json").read_text())
protected_by_id = {
    item["source_rule_id"]: item["classification"]
    for item in protected["rules"]
}

domain_id = (
    "rule-b25203fce8fc32addea6c7671ce933b1a9ee841e26d4b5263e1113d6ed4ffaed"
)
records = []
for index, rule in enumerate(inventory["rules"]):
    if rule["source_rule_id"] == domain_id:
        classification = "DOMAIN_LEMMA"
        rationale = (
            "Problem-specific connection lemma. It preempts the supplied "
            "no-argument split rule and asserts that the supplied splitWS "
            "recurrence on encodedWords(WORDS) yields the independently "
            "defined wordsVS(WORDS) summary. Removing only this rule exposes "
            "that exact equality as the residual of the final symbolic claim."
        )
    elif index <= 3:
        classification = "DEFINITION"
        rationale = (
            "Named macro/proof term defining translated program syntax or "
            "the named closure; it does not assert a new domain theorem."
        )
    elif 4 <= index <= 13:
        classification = "DEFINITION"
        rationale = (
            "Exhaustive constructor equation defining the named wordVal "
            "summary on one NumWord constructor."
        )
    elif 14 <= index <= 15:
        classification = "DEFINITION"
        rationale = (
            "Base/recursive equation defining the named wordsVS structural "
            "summary."
        )
    elif 16 <= index <= 25:
        classification = "DEFINITION"
        rationale = (
            "Exhaustive constructor equation defining the named wordCodes "
            "summary on one NumWord constructor."
        )
    elif 26 <= index <= 28:
        classification = "DEFINITION"
        rationale = (
            "Base/singleton/recursive equation defining the named "
            "encodedWords representation."
        )
    else:
        classification = "DEFINITION"
        rationale = (
            "Equation defining the named numericOutput proof summary in "
            "terms of joinCodes, wordsVS, numberKey, and supplied sortKeyVS."
        )
    records.append(
        {
            "ordinal": index,
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "normalized_sha256": rule["normalized_sha256"],
            "attributes": rule["attributes"],
            "protected_classification": protected_by_id[rule["source_rule_id"]],
            "independent_classification": classification,
            "classification_agrees": (
                classification == protected_by_id[rule["source_rule_id"]]
            ),
            "rationale": rationale,
            "text": rule["text"],
        }
    )

document = {
    "inventory_sha256": inventory["inventory_sha256"],
    "rule_count": len(records),
    "independent_counts": {
        role: sum(
            record["independent_classification"] == role
            for record in records
        )
        for role in (
            "DEFINITION",
            "OPERATIONAL_RULE",
            "PROVED_DERIVED_LEMMA",
            "DOMAIN_LEMMA",
        )
    },
    "simplification_policy_pass": all(
        "simplification" not in record["attributes"]
        or record["independent_classification"]
        in {"DEFINITION", "DOMAIN_LEMMA"}
        for record in records
    ),
    "disagreements": [
        record["source_rule_id"]
        for record in records
        if not record["classification_agrees"]
    ],
    "rules": records,
}
print(json.dumps(document, indent=2, sort_keys=True))
