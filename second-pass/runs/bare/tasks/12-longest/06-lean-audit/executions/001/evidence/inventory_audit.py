#!/usr/bin/env python3
"""Independent Stage 3 inventory and classification comparison."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


def classify(text: str) -> tuple[str, str]:
    normalized = " ".join(text.split())
    definitions = {
        "rule longestLoopBody =>": "macro naming the translated loop body",
        "rule longestProgram =>": "macro naming the translated whole program",
        "rule stringList(SS) =>": "wrapper definition for the list conversion",
        "rule stringValues(.Strings) =>": "base equation of a structural conversion",
        "rule stringValues(S:String, SS:Strings)": "recursive equation of a structural conversion",
        "rule expectedLongest(.Strings) =>": "base equation of the contract summary",
        "rule expectedLongest(S:String, SS:Strings)": "seed equation of the contract summary",
        "rule firstLongest(BEST, .Strings) =>": "base equation of a named fold",
        "rule firstLongest(BEST, S:String, SS:Strings)": "guarded recurrence of a named fold",
        "rule firstInSeq(BEST, _ID, _I, N) =>": "base equation of a named symbolic-sequence fold",
        "rule firstInSeq(BEST, ID, I, N)": "guarded recurrence of a named symbolic-sequence fold",
    }
    for prefix, reason in definitions.items():
        if normalized.startswith(prefix):
            return "DEFINITION", reason

    operational = {
        "rule isEmpty(seqVal(": "ordinary empty/nonempty observation for the added seqVal value form",
        "rule head(seqVal(": "ordinary head observation for the added seqVal value form",
        "rule forValues(_, seqVal(": "ordinary loop-termination transition for seqVal",
        "rule <k> forValues(X, seqVal(": "ordinary one-step loop transition and environment update for seqVal",
    }
    for prefix, reason in operational.items():
        if normalized.startswith(prefix):
            return "OPERATIONAL_RULE", reason
    raise AssertionError(f"unclassified inventory rule: {normalized}")


inventory = inventory_verification(WORKSPACE)
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
manifest = json.loads(DISCOVERY.read_text())
source_lines = (WORKSPACE / "verification.k").read_text().splitlines()

manifest_ids = [entry["source_rule_id"] for entry in manifest["rules"]]
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
manifest_by_id = {entry["source_rule_id"]: entry for entry in manifest["rules"]}

records = []
for index, rule in enumerate(inventory["rules"]):
    span_text = "\n".join(
        source_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    independent_classification, reason = classify(rule["text"])
    manifest_entry = manifest_by_id[rule["source_rule_id"]]
    records.append(
        {
            "index": index,
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "source_span": {
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
            },
            "attributes": rule["attributes"],
            "normalized_sha256": rule["normalized_sha256"],
            "source_span_exact": span_text == rule["text"],
            "normalized_hash_exact": digest == rule["normalized_sha256"],
            "source_rule_id_exact": rule["source_rule_id"] == f"rule-{digest}",
            "independent_classification": independent_classification,
            "independent_reason": reason,
            "manifest_classification": manifest_entry["classification"],
            "classification_agrees": (
                independent_classification
                == manifest_entry["classification"]
            ),
        }
    )

summary = {
    "verification_file": inventory["verification_file"],
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "rule_count": len(inventory["rules"]),
    "inventory_sha256": inventory["inventory_sha256"],
    "recomputed_inventory_sha256": canonical_json_sha256(inventory["rules"]),
    "manifest_inventory_sha256": manifest["inventory_sha256"],
    "manifest_rule_count": len(manifest["rules"]),
    "manifest_unique_rule_count": len(set(manifest_ids)),
    "inventory_unique_rule_count": len(set(inventory_ids)),
    "ordered_identity_exact": manifest_ids == inventory_ids,
    "validated_definition_count": len(validated["definitions"]),
    "validated_operational_rule_count": len(validated["operational_rules"]),
    "validated_proved_derived_lemma_count": len(
        validated["proved_derived_lemmas"]
    ),
    "validated_domain_lemma_count": len(validated["domain_lemmas"]),
    "simplification_rule_count": sum(
        "simplification" in rule["attributes"]
        for rule in inventory["rules"]
    ),
    "all_span_hash_identity_checks_pass": all(
        record["source_span_exact"]
        and record["normalized_hash_exact"]
        and record["source_rule_id_exact"]
        for record in records
    ),
    "all_independent_classifications_agree": all(
        record["classification_agrees"] for record in records
    ),
}

print(json.dumps({"summary": summary, "rules": records}, indent=2, sort_keys=True))
