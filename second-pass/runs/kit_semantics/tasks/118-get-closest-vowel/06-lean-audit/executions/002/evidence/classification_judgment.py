#!/usr/bin/env python3
"""Independent semantic classification of every canonical inventory entry."""

from __future__ import annotations

import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


WORKSPACE = Path("/reference/k-proof")
MANIFEST = Path("/reference/lemma-discovery.json")

# These judgments are authored from the frozen rules and supplied operational
# semantics.  They are deliberately not derived from the protected labels.
JUDGMENTS = {
    "rule-c20cac6fc636336fce2d7dbc24f7aa987c09ce9dd8b4b8e10851db71031a2574": (
        "PROVED_DERIVED_LEMMA",
        "Exact loop/return/frame-pop execution theorem, freshly reproved before the VERIFICATION rule is installed; compiled ordinary LHS/RHS/guard/cells match.",
    ),
    "rule-284c4c4d20e7564f3b85f9ae093aa32298e088fc96aae41906f05d8ef3f0ef15": (
        "PROVED_DERIVED_LEMMA",
        "Exact true-result helper execution theorem, freshly reproved against FOUNDATION before HELPER-VERIFICATION is installed.",
    ),
    "rule-08d6a79c00e8974a6bd055b18bc2d39ca1d25c682c2008be19c209f460d89d5d": (
        "PROVED_DERIVED_LEMMA",
        "Exact false-result helper execution theorem, freshly reproved against FOUNDATION before HELPER-VERIFICATION is installed.",
    ),
    "rule-9750751be23de63eea428066c5f2315f3bebcc22fe43dddf5e6d79c43915d75b": (
        "DEFINITION",
        "Macro equation defining the named helper-body proof term.",
    ),
    "rule-9f040a569fbdef71fcf41191a36aa87b4a12a1408da3cb7e8e4fd521f3142050": (
        "DEFINITION",
        "Macro equation defining the named loop-body proof term.",
    ),
    "rule-b469237f699e183d197e8af26b5fe59f2f7ee10feb5e2cae653d35fa6db3b18e": (
        "DEFINITION",
        "Macro equation defining the named get_closest_vowel body proof term.",
    ),
    "rule-bda9325d20b98ccb8ea35f87db6a25e30467c4fdc5a3795dff9cc7b0fad1df95": (
        "DEFINITION",
        "Macro equation defining the named two-function program proof term.",
    ),
    "rule-f92258ede26e827ded78066798d36a19faf667c244668896801918a553460f73": (
        "DEFINITION",
        "Equation defining closestCandidate as a singleton IntSeq at the selected index.",
    ),
    "rule-b53c8b783e2e5811d5637116208c57afb5dff0bec4c0f204437b0d5e025b40bf": (
        "DEFINITION",
        "Equation defining vowelPred by exactly ten ASCII vowel code points.",
    ),
    "rule-4ffa001d0025dfc39e75914c4018aec5fc84882a251347e2f7d3411147df71c2": (
        "DEFINITION",
        "Positive guarded equation of the fresh total isVowelCode predicate.",
    ),
    "rule-d4475acafd5ccc48b928bf84e40a47c36c492090891bdaac93fb21beb3dd6a08": (
        "DEFINITION",
        "Complementary negative guarded equation of the fresh total isVowelCode predicate.",
    ),
    "rule-3ece48af78d3f7d2f9eaef5f4a84518a114cf9815cb9dbeb7d46bd3102033d68": (
        "DEFINITION",
        "Equation defining closestQualifies from current and adjacent vowel tests.",
    ),
    "rule-438d7cc7c496278810f0bb993f58a64eacd19276c70d0f101e30bc6b5084c96f": (
        "DEFINITION",
        "Guarded base equation of the closestScan recurrence.",
    ),
    "rule-44428f2a6174cdcf211cfdd4a90819eb05c02a3189ffc69f34a0c1f6958959a7": (
        "DEFINITION",
        "Descending found=true equation of the closestScan recurrence.",
    ),
    "rule-a7036ead5012afd996265af2ec30eed7ee568c6f0416cf2e867b9ee5977d169c": (
        "DEFINITION",
        "Descending qualifying-vowel equation of the closestScan recurrence.",
    ),
    "rule-faba90d09a0cbb9fce0409db469110529b83cdc311057d00d3f26b64c3f6667f": (
        "DEFINITION",
        "Descending current-nonvowel equation of the closestScan recurrence.",
    ),
    "rule-460633535e62fabbd09b552246be723a3c6834d4c684d42e87597492b2b6ab1f": (
        "DEFINITION",
        "Descending current-and-left-vowels equation of the closestScan recurrence.",
    ),
    "rule-2dd28623449f964e93ee34df5544e991e09c1d1d901864a6c0da8b6e223cb7c7": (
        "DEFINITION",
        "Descending current-vowel/left-nonvowel/right-vowel equation of closestScan.",
    ),
    "rule-b246dcd7d7a81de803c8f1e6ffff14aa138826f5bc035c9b59b2b595f75d9202": (
        "DEFINITION",
        "Equation defining closestVowel by initializing closestScan at length minus two.",
    ),
    "rule-1cad334b6905baf03866113ddd1797f5714a455f71cedf67b42074759ca10ca7": (
        "DOMAIN_LEMMA",
        "Unproved but true and relevant guarded #Ceil fact: constructor length bounds make intSeqAt descend to an existing head.",
    ),
    "rule-3cb106e69fb9d49b1f6233a47205ceacbe2aee414ced90880b1ceb6cbb0782e5": (
        "DOMAIN_LEMMA",
        "Unproved but true and relevant guarded #Ceil fact: closestScan has an exhaustive Boolean case partition and strictly decreases I to its base case while all indexed neighbors remain in bounds.",
    ),
}

inventory = inventory_verification(WORKSPACE)
protected = json.loads(MANIFEST.read_text())
protected_by_id = {entry["source_rule_id"]: entry for entry in protected["rules"]}

rows = []
for index, rule in enumerate(inventory["rules"]):
    source_rule_id = rule["source_rule_id"]
    classification, basis = JUDGMENTS[source_rule_id]
    protected_entry = protected_by_id[source_rule_id]
    rows.append(
        {
            "index": index,
            "source_rule_id": source_rule_id,
            "file": rule.get("file", inventory["verification_file"]),
            "span": [rule["start_line"], rule["end_line"]],
            "attributes": rule["attributes"],
            "independent_classification": classification,
            "protected_classification": protected_entry["classification"],
            "classification_matches": (
                classification == protected_entry["classification"]
            ),
            "independent_basis": basis,
            "simplification_policy_satisfied": (
                "simplification" not in rule["attributes"]
                or classification in {"DEFINITION", "DOMAIN_LEMMA"}
            ),
        }
    )

counts = {
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
result = {
    "inventory_sha256": inventory["inventory_sha256"],
    "counts": counts,
    "all_protected_classifications_match": all(
        row["classification_matches"] for row in rows
    ),
    "all_simplification_rules_satisfy_policy": all(
        row["simplification_policy_satisfied"] for row in rows
    ),
    "rows": rows,
}
print(json.dumps(result, indent=2, sort_keys=True))

if not (
    set(JUDGMENTS) == {rule["source_rule_id"] for rule in inventory["rules"]}
    and result["all_protected_classifications_match"]
    and result["all_simplification_rules_satisfy_policy"]
    and counts
    == {
        "DEFINITION": 16,
        "OPERATIONAL_RULE": 0,
        "PROVED_DERIVED_LEMMA": 3,
        "DOMAIN_LEMMA": 2,
    }
):
    raise SystemExit(1)
