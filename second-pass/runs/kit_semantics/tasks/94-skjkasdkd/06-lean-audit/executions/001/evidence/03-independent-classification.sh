#!/usr/bin/env bash
set -uo pipefail

PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification

# This audit classification is keyed by frozen source span, not copied from
# lemma-discovery.json.  Each tuple is (classification, audit rationale,
# source/postcondition relevance).
judgment = {
    9: ("DEFINITION", "Exact named syntax expansion of primeLoopBody.",
        "Names the source inner primality-loop body."),
    19: ("DEFINITION", "Exact named syntax expansion of scanBody.",
         "Names the source list-scan body."),
    38: ("DEFINITION", "Exact named syntax expansion of digitLoopBody.",
         "Names the source decimal-digit loop body."),
    46: ("DEFINITION", "Exact named syntax expansion of targetBody.",
         "Names the complete translated function body."),
    61: ("DEFINITION", "Empty-sequence base equation for allInts.",
         "States the source contract that every list element is an integer."),
    62: ("DEFINITION", "Structural recurrence for allInts.",
         "Propagates the integer-list source precondition."),
    69: ("DEFINITION", "Names cast-definedness as the generated Int sort test.",
         "Connects dynamic Val elements to source integer operations."),
    74: ("DOMAIN_LEMMA",
         "Unproved #Ceil characterization of the pre-existing Val-to-Int cast.",
         "Needed to discharge definedness of integer projections."),
    78: ("DEFINITION",
         "Primary guarded defining equation for fresh projectIntTotal.",
         "Names the integer projection used by the symbolic source summary."),
    82: ("DOMAIN_LEMMA",
         "Unproved reverse symbolic orientation from the pre-existing cast to "
         "the fresh projection; not a primary defining case.",
         "Makes symbolic dynamic integer elements usable by source arithmetic."),
    86: ("DEFINITION",
         "Defining collapse of the fresh total projection on an Int.",
         "Covers already-integer values in the source domain."),
    87: ("DOMAIN_LEMMA",
         "Unproved idempotence simplification for nested projection.",
         "Normalizes projections introduced by repeated symbolic dispatch."),
    93: ("DOMAIN_LEMMA",
         "Unproved guarded dispatch equality for dynamic-Val greater-than.",
         "Models value > largest and largest > 0 in the source loops."),
    98: ("DOMAIN_LEMMA",
         "Unproved guarded dispatch equality for dynamic-Val greater-or-equal.",
         "Models candidate initialization value >= 2."),
    103: ("DOMAIN_LEMMA",
          "Unproved guarded dispatch equality for Int less-than dynamic Val.",
          "Models divisor < value in the primality loop."),
    108: ("DOMAIN_LEMMA",
          "Unproved guarded dispatch equality for dynamic-Val modulo.",
          "Models value % divisor in primality testing."),
    113: ("DOMAIN_LEMMA",
          "Unproved guarded dispatch equality for dynamic-Val addition.",
          "Models the source value + 0 assignment through dynamic Val."),
    120: ("DEFINITION", "Totalization base case for fresh primeTail below 2.",
          "Defines the proof summary outside the source loop's reachable start."),
    122: ("DEFINITION", "Terminal base case for fresh primeTail at or beyond N.",
          "Defines exhaustion of the source divisor scan."),
    124: ("DEFINITION", "Primary recursive equation for fresh primeTail.",
          "Defines the source divisor-by-divisor primality summary."),
    133: ("DOMAIN_LEMMA",
          "Unproved zero-remainder shortcut derived from, rather than defining, "
          "the primary primeTail recurrence.",
          "Captures discovery of a divisor in the source primality loop."),
    138: ("DOMAIN_LEMMA",
          "Unproved backward fold of primeTail over a nondividing predecessor.",
          "Closes the source primality-loop invariant as divisor increments."),
    145: ("DEFINITION", "Defines fresh isPrime from its bound and primeTail.",
          "States the primality summary used by the list scan."),
    150: ("DEFINITION", "Positive guarded branch defining fresh selectPrime.",
          "Updates the maximum exactly when a larger prime is scanned."),
    152: ("DEFINITION", "Complementary guarded branch defining selectPrime.",
          "Retains the maximum on every other scan case."),
    157: ("DEFINITION", "Empty-sequence base equation for fresh largestPrime.",
          "Defines the list fold at exhaustion."),
    158: ("DEFINITION", "Integer-head recurrence for fresh largestPrime.",
          "Defines the source scan across integer elements."),
    161: ("DEFINITION", "Non-Int totalization branch for fresh largestPrime.",
          "Completes the summary, while the source theorem assumes allInts."),
    167: ("DEFINITION", "Nonpositive base equation for fresh digitSum.",
          "Defines termination/result after the source digit loop."),
    169: ("DEFINITION", "Primary positive decimal recurrence for fresh digitSum.",
          "Defines the source modulo/division digit loop."),
    174: ("DOMAIN_LEMMA",
          "Unproved reverse fold of the positive digitSum recurrence.",
          "Closes one source digit-loop iteration."),
    179: ("DOMAIN_LEMMA",
          "Unproved reverse fold after expanding pyMod to integer remainder.",
          "Matches the supplied semantics' modulo normalization in the digit loop."),
    185: ("DOMAIN_LEMMA",
          "Unproved accumulator-lifted digitSum fold plus addition reassociation.",
          "Connects repeated source total += largest % 10 updates to the result."),
}

inventory = inventory_verification(Path("/reference/k-proof"))
manifest = json.loads(Path("/reference/lemma-discovery.json").read_text())
manifest_by_id = {
    entry["source_rule_id"]: entry for entry in manifest["rules"]
}
rows = []
for rule in inventory["rules"]:
    role, rationale, relevance = judgment[rule["start_line"]]
    recorded = manifest_by_id[rule["source_rule_id"]]["classification"]
    rows.append({
        "source_rule_id": rule["source_rule_id"],
        "source_span": {
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
        },
        "attributes": rule["attributes"],
        "independent_classification": role,
        "recorded_classification": recorded,
        "classification_matches": role == recorded,
        "audit_rationale": rationale,
        "source_or_postcondition_relevance": relevance,
    })

counts = {}
for row in rows:
    role = row["independent_classification"]
    counts[role] = counts.get(role, 0) + 1
simplification_valid = all(
    row["independent_classification"] in {"DEFINITION", "DOMAIN_LEMMA"}
    for row in rows
    if any(
        attr == "simplification" or attr.startswith("simplification(")
        for attr in row["attributes"]
    )
)
domain_relevance_nonempty = all(
    bool(row["source_or_postcondition_relevance"].strip())
    for row in rows
    if row["independent_classification"] == "DOMAIN_LEMMA"
)
print(json.dumps({
    "rows": rows,
    "counts": counts,
    "checks": {
        "all_33_spans_classified_once": (
            len(rows) == 33
            and len(judgment) == 33
            and set(judgment) == {r["start_line"] for r in inventory["rules"]}
        ),
        "all_classifications_match_manifest": all(
            row["classification_matches"] for row in rows
        ),
        "all_simplification_rules_are_definition_or_domain_lemma":
            simplification_valid,
        "all_domain_lemmas_have_source_or_postcondition_relevance":
            domain_relevance_nonempty,
        "no_claimed_proved_derived_lemma": (
            counts.get("PROVED_DERIVED_LEMMA", 0) == 0
        ),
        "no_local_ordinary_operational_rule": (
            counts.get("OPERATIONAL_RULE", 0) == 0
        ),
    },
    "stage1_proof_sequence_observation": (
        "prove.sh compiles verification.k once with every rule already present; "
        "no exact inventory rule is first proved against a module omitting it "
        "and then installed for a later proof."
    ),
}, indent=2, sort_keys=True))
PY
