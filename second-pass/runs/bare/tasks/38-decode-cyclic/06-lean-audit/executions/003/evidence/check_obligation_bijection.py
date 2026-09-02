#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


inventory = inventory_verification(Path("/reference/k-proof"))
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
assert inventory_ids == discovery_ids == source_ids == obligation_ids
assert len(inventory_ids) == len(set(inventory_ids)) == 3

expected_conjuncts = {
    inventory_ids[0]: (
        "∀ (V' : SortKItem) (K : SortKItem) (M : SortMap) "
        "(V : SortKItem), ((«Map:update» M K V : SortMap) = "
        "(«Map:update» M K V' : SortMap)) ↔ "
        "((V : SortKItem) = (V' : SortKItem))"
    ),
    inventory_ids[1]: (
        "∀ (_S : SortString), («_<=Int_» 0 "
        "(«lengthString(_)_STRING-COMMON_Int_String» _S) : SortBool) "
        "= (true : SortBool)"
    ),
    inventory_ids[2]: (
        "∀ (S : SortString), "
        "(«substrString(_,_,_)_STRING-COMMON_String_String_Int_Int» "
        "S 0 («lengthString(_)_STRING-COMMON_Int_String» S) : "
        "SortString) = (S : SortString)"
    ),
}

for source_rule, obligation in zip(
    inventory["rules"], obligation_map["obligations"], strict=True
):
    rule_id = source_rule["source_rule_id"]
    assert obligation["source_span"] == {
        "start_line": source_rule["start_line"],
        "end_line": source_rule["end_line"],
    }
    assert (
        obligation["normalized_sha256"]
        == source_rule["normalized_sha256"]
    )
    assert obligation["inventory_sha256"] == inventory["inventory_sha256"]
    assert obligation["lean_conjunct"] == expected_conjuncts[rule_id]
    assert (
        obligation["lean_conjunct_sha256"]
        == sha256_text(obligation["lean_conjunct"])
    )
    print(
        "PASS",
        rule_id,
        f"lines {source_rule['start_line']}-{source_rule['end_line']}",
        obligation["lean_conjunct_sha256"],
    )

expected_links = {
    "«_<=Int_»": {inventory_ids[1]},
    "«Map:update»": {inventory_ids[0]},
    "«lengthString(_)_STRING-COMMON_Int_String»": {
        inventory_ids[1],
        inventory_ids[2],
    },
    "«substrString(_,_,_)_STRING-COMMON_String_String_Int_Int»": {
        inventory_ids[2]
    },
}
observed_links = {
    parameter["name"]: set(parameter["source_rule_ids"])
    for parameter in obligation_map["trust_parameters"]
}
assert observed_links == expected_links
print("PASS exact trust-parameter/source-rule links")
print("PASS three nonempty, universally quantified, nonvacuous conjuncts")
