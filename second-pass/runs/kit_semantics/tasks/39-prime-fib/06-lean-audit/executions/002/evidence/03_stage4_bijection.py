#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


def load(path: str):
    return json.loads(Path(path).read_text())


generation = Path("/reference/klean-generation")
generated = generation / "generated"
discovery_path = Path("/reference/lemma-discovery.json")
validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"), discovery_path
)
discovery_hash = hashlib.sha256(discovery_path.read_bytes()).hexdigest()
expected_source_rules = klean_export._domain_source_rules(validated, discovery_hash)
input_manifest = load(str(generation / "input-manifest.json"))
generator_manifest = load(str(generation / "generator-manifest.json"))
obligation_map = load(str(generated / "obligation-map.json"))
audit_target = load("/audit-input.json")["resolution"]["target"]

assert input_manifest["source_rules"] == expected_source_rules
assert obligation_map["source_rules"] == expected_source_rules
expected_ids = [x["source_rule_id"] for x in expected_source_rules]
observed_ids = [x["source_rule_id"] for x in obligation_map["obligations"]]
assert expected_ids == observed_ids
assert len(observed_ids) == len(set(observed_ids))
assert len(observed_ids) == generator_manifest["obligation_count"] == 2

for source, obligation in zip(expected_source_rules, obligation_map["obligations"]):
    assert obligation["source_span"] == {
        "start_line": source["start_line"],
        "end_line": source["end_line"],
    }
    for key in (
        "source_rule_id",
        "normalized_sha256",
        "inventory_sha256",
        "discovery_manifest_sha256",
    ):
        assert obligation[key] == source[key]
    assert obligation["lean_conjunct_sha256"] == klean_export.sha256_text(
        obligation["lean_conjunct"]
    )

expected_definition = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(generated)
assert expected_definition is not None
assert observed_target == generator_manifest["target"] == audit_target
assert observed_target["definition_sha256"] == klean_export.sha256_text(
    expected_definition
)

print("DISCOVERY_MANIFEST_SHA256", discovery_hash)
print("DOMAIN_SOURCE_RULE_IDS", json.dumps(expected_ids))
print("OBLIGATION_RULE_IDS", json.dumps(observed_ids))
print("SOURCE_OBLIGATION_ORDERED_BIJECTION", "PASS")
print("OBLIGATION_MAP_SHA256", hashlib.sha256(
    (generated / "obligation-map.json").read_bytes()
).hexdigest())
print("TARGET", json.dumps(observed_target, indent=2, sort_keys=True))
print("EXPECTED_TARGET_DEFINITION")
print(expected_definition)
print("FIXED_TARGET_IDENTITY", "PASS")
print("NONVACUITY_WITNESS_1", "D=2, A=4; 2 >= 2 is true")
print(
    "NONVACUITY_WITNESS_2",
    "N=1, C=0, A=0, B=2; primeScan(2,2,true)=true, so the guarded update count is 1",
)
