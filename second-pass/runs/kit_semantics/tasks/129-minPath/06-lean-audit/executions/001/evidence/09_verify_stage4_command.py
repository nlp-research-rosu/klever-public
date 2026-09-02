import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import expected_target_definition, target_statement, tree_digest
from tools.pipeline_contract import sha256_file, sha256_tree


def j(path):
    return json.loads(Path(path).read_text())


audit = j("/audit-input.json")["resolution"]
manifest = j("/reference/klean-generation/generator-manifest.json")
input_manifest = j("/reference/klean-generation/input-manifest.json")
obmap = j("/reference/klean-generation/generated/obligation-map.json")
export = j("/reference/klean-generation/export-result.json")
discovery = j("/reference/lemma-discovery.json")
inventory = inventory_verification("/reference/k-proof")
generated = Path("/reference/klean-generation/generated")

print("MOUNTED HASH RECOMPUTATION")
pipeline_trees = {
    "k_workspace_sha256": Path("/reference/k-proof"),
    "k_audit_sha256": Path("/reference/k-audit"),
    "klean_generation_sha256": Path("/reference/klean-generation"),
    "generation_producer_sources_sha256": Path("/reference/generation-tools"),
    "lean_workspace_sha256": Path("/candidate"),
}
all_hashes_ok = True
for key, path in pipeline_trees.items():
    actual = sha256_tree(path)
    expected = audit["hashes"][key]
    ok = actual == expected
    all_hashes_ok &= ok
    print(key, "actual=", actual, "recorded=", expected, "match=", ok)
file_hash = sha256_file(Path("/reference/lemma-discovery.json"))
print("discovery_manifest_sha256", file_hash, audit["hashes"]["discovery_manifest_sha256"], file_hash == audit["hashes"]["discovery_manifest_sha256"])
all_hashes_ok &= file_hash == audit["hashes"]["discovery_manifest_sha256"]
stage1_export = tree_digest(Path("/reference/k-proof"))
generated_tree = tree_digest(generated)
print("stage1_export_sha256", stage1_export, audit["hashes"]["stage1_export_sha256"], stage1_export == audit["hashes"]["stage1_export_sha256"])
print("generated_tree_sha256", generated_tree, audit["hashes"]["generated_tree_sha256"], generated_tree == audit["hashes"]["generated_tree_sha256"])
all_hashes_ok &= stage1_export == audit["hashes"]["stage1_export_sha256"]
all_hashes_ok &= generated_tree == audit["hashes"]["generated_tree_sha256"]

source_missing = []
source_mismatch = []
for relative, expected in audit["stage1_source_hashes"].items():
    path = Path("/reference/k-proof") / relative
    if not path.is_file():
        source_missing.append(relative)
    elif sha256_file(path) != expected:
        source_mismatch.append((relative, sha256_file(path), expected))
mounted_files = {p.relative_to('/reference/k-proof').as_posix() for p in Path('/reference/k-proof').rglob('*') if p.is_file()}
recorded_files = set(audit["stage1_source_hashes"])
print("stage1_source_hash_count", len(recorded_files))
print("stage1_source_missing", source_missing)
print("stage1_source_mismatch", source_mismatch)
print("stage1_unrecorded_mounted_files", sorted(mounted_files - recorded_files))
print("stage1_all_recorded_files_match", not source_missing and not source_mismatch)
all_hashes_ok &= not source_missing and not source_mismatch
print("all_recomputable_mounted_audit_hashes_match", all_hashes_ok)
print("lean_invocation_sha256_recomputable", False, "reason=launcher did not mount the Stage 5 invocation directory; it is not a candidate input")

print("\nSOURCE-RULE / OBLIGATION BIJECTION")
inv_by_id = {r["source_rule_id"]: r for r in inventory["rules"]}
discovery_cls = {r["source_rule_id"]: r["classification"] for r in discovery["rules"]}
domain_ids = [r["source_rule_id"] for r in inventory["rules"] if discovery_cls[r["source_rule_id"]] == "DOMAIN_LEMMA"]
source_ids = [r["source_rule_id"] for r in obmap["source_rules"]]
obligation_ids = [r["source_rule_id"] for r in obmap["obligations"]]
print("independently_confirmed_domain_ids", json.dumps(domain_ids, indent=2))
print("obligation_ids", json.dumps(obligation_ids, indent=2))
print("source_rule_ids", json.dumps(source_ids, indent=2))
print("exact_ordered_domain_to_obligation_bijection", domain_ids == obligation_ids == source_ids)
print("counts", len(domain_ids), len(obligation_ids), len(source_ids), "unique_obligations", len(set(obligation_ids)))

entry_errors = []
for i, (source, obligation) in enumerate(zip(obmap["source_rules"], obmap["obligations"]), 1):
    frozen = inv_by_id[obligation["source_rule_id"]]
    conjunct_hash = hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest()
    checks = {
        "id": source["source_rule_id"] == obligation["source_rule_id"] == frozen["source_rule_id"],
        "span": source["start_line"] == obligation["source_span"]["start_line"] == frozen["start_line"] and source["end_line"] == obligation["source_span"]["end_line"] == frozen["end_line"],
        "normalized_hash": source["normalized_sha256"] == obligation["normalized_sha256"] == frozen["normalized_sha256"],
        "inventory_hash": source["inventory_sha256"] == obligation["inventory_sha256"] == inventory["inventory_sha256"],
        "discovery_hash": source["discovery_manifest_sha256"] == obligation["discovery_manifest_sha256"] == sha256_file(Path("/reference/lemma-discovery.json")),
        "conjunct_hash": conjunct_hash == obligation["lean_conjunct_sha256"],
    }
    print(f"obligation_{i}", obligation["source_rule_id"], checks)
    print(" lean_conjunct=", obligation["lean_conjunct"])
    if not all(checks.values()):
        entry_errors.append((i, checks))
print("obligation_entry_errors", entry_errors)

print("\nFIXED TARGET RECONSTRUCTION")
actual_target = target_statement(generated)
expected_definition = expected_target_definition(obmap)
expected_definition_hash = hashlib.sha256(expected_definition.encode()).hexdigest()
actual_source = (generated / actual_target["file"]).read_text()
actual_definition_present = expected_definition in actual_source
print("expected_definition=\n" + expected_definition)
print("expected_definition_sha256", expected_definition_hash)
print("trusted_extracted_target", json.dumps(actual_target, indent=2, sort_keys=True))
print("expected_definition_occurs_exactly_once", actual_source.count(expected_definition) == 1)
print("definition_hash_matches_reconstruction", expected_definition_hash == actual_target["definition_sha256"])
print("target_equals_generator_manifest", actual_target == manifest["target"])
print("target_equals_audit_input", actual_target == audit["target"])
print("target_equals_preflight", actual_target == audit["stage4_preflight"]["target"])
print("manifest_obligation_count", manifest["obligation_count"], "actual", len(obligation_ids))
print("manifest_generated_tree_match", manifest["generated_tree_sha256"] == generated_tree)
print("export_generated_tree_match", export["generated_tree_sha256"] == generated_tree)
print("obligation_map_file_hash_match", sha256_file(generated / "obligation-map.json") == manifest["obligation_map_sha256"])
print("status_is_nonempty_generation", export["status"], "obligation_count", export["obligation_count"], "target_present", actual_target is not None)
