#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


domain_ids = [
    "rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43"
]
inventory = inventory_verification(Path("/reference/k-proof"))
inventory_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}
mapping_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
mapping = json.loads(mapping_path.read_text())
manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)

mapped_source_ids = [
    rule["source_rule_id"] for rule in mapping["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"] for obligation in mapping["obligations"]
]
print(f"independent_domain_ids={domain_ids}")
print(f"mapped_source_ids={mapped_source_ids}")
print(f"obligation_ids={obligation_ids}")
print(
    "ordered_bijection="
    + str(
        domain_ids == mapped_source_ids == obligation_ids
        and len(set(obligation_ids)) == len(obligation_ids)
    )
)

for source_rule, obligation in zip(
    mapping["source_rules"], mapping["obligations"], strict=True
):
    frozen = inventory_by_id[source_rule["source_rule_id"]]
    expected_span = {
        "start_line": frozen["start_line"],
        "end_line": frozen["end_line"],
    }
    print("\nSOURCE/OBLIGATION")
    print(f"source_rule_id={source_rule['source_rule_id']}")
    print(f"source_text_equal={source_rule['text'] == frozen['text']}")
    print(
        "normalized_hash_equal="
        + str(
            source_rule["normalized_sha256"]
            == obligation["normalized_sha256"]
            == frozen["normalized_sha256"]
        )
    )
    print(
        f"source_span_expected={expected_span} "
        f"source_span_observed={obligation['source_span']} "
        f"match={expected_span == obligation['source_span']}"
    )
    actual_conjunct_hash = hashlib.sha256(
        obligation["lean_conjunct"].encode()
    ).hexdigest()
    print(f"lean_conjunct={obligation['lean_conjunct']}")
    print(
        f"lean_conjunct_hash_recorded={obligation['lean_conjunct_sha256']} "
        f"actual={actual_conjunct_hash} "
        f"match={obligation['lean_conjunct_sha256'] == actual_conjunct_hash}"
    )

actual_map_hash = hashlib.sha256(mapping_path.read_bytes()).hexdigest()
print("\nOBLIGATION MAP")
print(f"recorded_sha256={manifest['obligation_map_sha256']}")
print(f"actual_sha256={actual_map_hash}")
print(
    f"hash_match={manifest['obligation_map_sha256'] == actual_map_hash}"
)
print(f"manifest_obligation_count={manifest['obligation_count']}")
print(f"actual_obligation_count={len(mapping['obligations'])}")

expected_conjunct = (
    "∀ (V : SortVal), "
    "((«project:Int?» (SortK.kseq ((@inj SortVal SortKItem) V) "
    "SortK.dotk)).isSome = true) ↔ "
    "(((«definedProjectInt(_)_MAX-FILL-SUMMARY_Bool_Val» V : "
    "SortBool) = (true : SortBool)) ∧ (True))"
)
print("\nINDEPENDENT EXPECTED CONJUNCT")
print(expected_conjunct)
print(
    "exact_conjunct_match="
    + str(mapping["obligations"][0]["lean_conjunct"] == expected_conjunct)
)
print(
    "semantic_reading=the partial Val-to-Int projection is defined iff "
    "the Val is an Int; the final True is the direct image of source "
    "#Ceil(@V), because a bound SortVal variable is defined"
)
