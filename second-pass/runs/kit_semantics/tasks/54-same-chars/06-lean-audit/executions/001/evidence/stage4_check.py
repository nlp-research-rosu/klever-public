from pathlib import Path
import hashlib
import json

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary

root = Path("/reference/klean-generation")
generated = root / "generated"
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
names = [
    "input-manifest.json",
    "generator-manifest.json",
    "export-result.json",
    "trust-inventory.json",
    "preflight.json",
]
files = {name: json.loads((root / name).read_text()) for name in names}
input_manifest = files["input-manifest.json"]
generator = files["generator-manifest.json"]
export = files["export-result.json"]
recorded_preflight = files["preflight.json"]
lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
map_path = generated / "obligation-map.json"
obligation_map = json.loads(map_path.read_text())
validated = validate_trust_boundary(
    Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
)
discovery_hash = hashlib.sha256(Path("/reference/lemma-discovery.json").read_bytes()).hexdigest()
source_rules = klean_export._domain_source_rules(validated, discovery_hash)
actual_target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
sidecar_hashes = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}
print("SIDECAR_SHA256:")
for name, digest in sidecar_hashes.items():
    print(name, digest)
observed_map_hash = hashlib.sha256(map_path.read_bytes()).hexdigest()
print("OBLIGATION_MAP_SHA256_OBSERVED:", observed_map_hash)
print("OBLIGATION_MAP_SHA256_GENERATOR:", generator["obligation_map_sha256"])
print("OBLIGATION_MAP_HASH_MATCH:", observed_map_hash == generator["obligation_map_sha256"])
print("TRUST_INVENTORY_SHA256_OBSERVED:", sidecar_hashes["trust-inventory.json"])
print("TRUST_INVENTORY_SHA256_EXPORT:", export["trust_inventory_sha256"])
print(
    "TRUST_INVENTORY_HASH_MATCH:",
    sidecar_hashes["trust-inventory.json"] == export["trust_inventory_sha256"],
)
print("TOOLCHAIN_EQUALS_LOCK:", generator["toolchain"] == lock)
print("INPUT_INVENTORY_MATCH:", input_manifest["inventory_sha256"] == validated["inventory_sha256"])
print(
    "GENERATOR_INVENTORY_MATCH:",
    generator["provenance"]["inventory_sha256"] == validated["inventory_sha256"],
)
print("INDEPENDENT_DOMAIN_SOURCE_RULES:", json.dumps(source_rules, sort_keys=True))
print("INPUT_SOURCE_RULES:", json.dumps(input_manifest["source_rules"], sort_keys=True))
print("MAP_SOURCE_RULES:", json.dumps(obligation_map["source_rules"], sort_keys=True))
print(
    "SOURCE_RULE_LISTS_EXACT_MATCH:",
    source_rules == input_manifest["source_rules"] == obligation_map["source_rules"],
)
expected_ids = [entry["source_rule_id"] for entry in source_rules]
observed_ids = [entry.get("source_rule_id") for entry in obligation_map["obligations"]]
print("EXPECTED_SOURCE_RULE_IDS:", expected_ids)
print("OBSERVED_OBLIGATION_IDS:", observed_ids)
print(
    "OBLIGATION_ID_ORDER_BIJECTION:",
    expected_ids == observed_ids and len(set(observed_ids)) == len(observed_ids),
)
print("OBLIGATION_COUNT_MAP:", len(obligation_map["obligations"]))
print("OBLIGATION_COUNT_GENERATOR:", generator["obligation_count"])
print("OBLIGATION_COUNT_EXPORT:", export["obligation_count"])
print("OBLIGATION_COUNT_PREFLIGHT:", recorded_preflight["obligation_count"])
print("TRUST_PARAMETERS:", json.dumps(obligation_map["trust_parameters"], sort_keys=True))
print("EXPECTED_TARGET_DEFINITION:", repr(expected_definition))
print("ACTUAL_TARGET:", json.dumps(actual_target, sort_keys=True))
print("GENERATOR_TARGET:", json.dumps(generator["target"], sort_keys=True))
print("AUDIT_INPUT_TARGET:", json.dumps(audit["target"], sort_keys=True))
print(
    "TARGETS_EXACT_MATCH:",
    actual_target == generator["target"] == audit["target"] and expected_definition is None,
)
print(
    "GENERATED_TREE_BINDINGS_MATCH:",
    generator["generated_tree_sha256"]
    == export["generated_tree_sha256"]
    == recorded_preflight["generated_tree_sha256"]
    == audit["hashes"]["generated_tree_sha256"],
)
print(
    "STATUS_CONSISTENT:",
    export["status"]
    == recorded_preflight["status"]
    == audit["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
)
print("RECORDED_PREFLIGHT_EQUALS_AUDIT_INPUT:", recorded_preflight == audit["stage4_preflight"])
print("TARGET_FILE_EXISTS:", (generated / "Klean54SameChars/Target.lean").exists())
print("CANDIDATE_EXISTS:", Path("/candidate").exists())
print("LEAN_WORKSPACE_JSON:", audit["lean_workspace"])
print("LEAN_INVOCATION_JSON:", audit["lean_invocation"])
print("LEAN_WORKSPACE_HASH_JSON:", audit["hashes"]["lean_workspace_sha256"])
print("LEAN_INVOCATION_HASH_JSON:", audit["hashes"]["lean_invocation_sha256"])
