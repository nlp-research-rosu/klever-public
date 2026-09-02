import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree


root_input = json.loads(Path("/audit-input.json").read_text())["resolution"]
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
inventory = inventory_verification(Path("/reference/k-proof"))
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
print("INVENTORY_DISCOVERY_BIJECTION")
print("inventory_count=", len(inventory_ids))
print("discovery_count=", len(discovery_ids))
print("inventory_duplicates=", len(inventory_ids) - len(set(inventory_ids)))
print("discovery_duplicates=", len(discovery_ids) - len(set(discovery_ids)))
print("ordered_identity_match=", inventory_ids == discovery_ids)
print("missing_from_discovery=", sorted(set(inventory_ids) - set(discovery_ids)))
print("extra_in_discovery=", sorted(set(discovery_ids) - set(inventory_ids)))
print("inventory_hash_recomputed=", inventory["inventory_sha256"])
print("inventory_hash_recorded=", discovery["inventory_sha256"])

class_by_id = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}
manifest_sections = [
    "definitions",
    "operational_rules",
    "proved_derived_lemmas",
    "source_rules",
]
manifest_entries = [
    entry for section in manifest_sections for entry in input_manifest[section]
]
manifest_ids = [entry["source_rule_id"] for entry in manifest_entries]
field_mismatches = []
for rule in inventory["rules"]:
    source_id = rule["source_rule_id"]
    matches = [
        entry
        for entry in manifest_entries
        if entry["source_rule_id"] == source_id
    ]
    if len(matches) != 1:
        field_mismatches.append((source_id, "multiplicity", len(matches)))
        continue
    expected = dict(rule)
    expected.update(class_by_id[source_id])
    for field in [
        "source_rule_id",
        "module",
        "start_line",
        "end_line",
        "normalized_sha256",
        "attributes",
        "text",
        "classification",
        "rationale",
    ]:
        if matches[0].get(field) != expected.get(field):
            field_mismatches.append(
                (
                    source_id,
                    field,
                    matches[0].get(field),
                    expected.get(field),
                )
            )
print("STAGE4_INPUT_MANIFEST")
print(
    "section_counts=",
    {section: len(input_manifest[section]) for section in manifest_sections},
)
print("manifest_total=", len(manifest_ids))
print("manifest_duplicates=", len(manifest_ids) - len(set(manifest_ids)))
print("manifest_inventory_set_match=", set(manifest_ids) == set(inventory_ids))
print("manifest_source_order_match=", manifest_ids == inventory_ids)
print("manifest_field_mismatches=", field_mismatches)

obligations = obligation_map["obligations"]
obligation_ids = [entry.get("source_rule_id") for entry in obligations]
domain_ids = [
    entry["source_rule_id"] for entry in input_manifest["source_rules"]
]
print("OBLIGATION_BIJECTION_AND_TARGET")
print("domain_rule_ids=", domain_ids)
print("obligation_rule_ids=", obligation_ids)
print(
    "obligation_duplicates=",
    len(obligation_ids) - len(set(obligation_ids)),
)
print("domain_obligation_bijection=", domain_ids == obligation_ids)
print("obligation_map_source_rules=", obligation_map["source_rules"])
print(
    "obligation_map_trust_parameters=", obligation_map["trust_parameters"]
)
print("generator_obligation_count=", generator["obligation_count"])
print("generator_target=", generator["target"])
print(
    "parsed_generated_target=",
    target_statement(Path("/reference/klean-generation/generated")),
)

actual_stage1_files = sorted(
    path.relative_to("/reference/k-proof").as_posix()
    for path in Path("/reference/k-proof").rglob("*")
    if path.is_file()
)
recorded_stage1_files = sorted(root_input["stage1_source_hashes"])
file_hash_mismatches = []
for relative, expected_hash in root_input["stage1_source_hashes"].items():
    path = Path("/reference/k-proof") / relative
    actual_hash = (
        hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
    )
    if actual_hash != expected_hash:
        file_hash_mismatches.append((relative, actual_hash, expected_hash))
print("RECORDED_HASHES")
print("stage1_file_count_recorded=", len(recorded_stage1_files))
print("stage1_file_count_actual=", len(actual_stage1_files))
print(
    "stage1_missing=",
    sorted(set(recorded_stage1_files) - set(actual_stage1_files)),
)
print(
    "stage1_extra=",
    sorted(set(actual_stage1_files) - set(recorded_stage1_files)),
)
print("stage1_file_hash_mismatches=", file_hash_mismatches)
computed = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "stage1_export_sha256": tree_digest(Path("/reference/k-proof")),
    "generated_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "discovery_manifest_sha256": hashlib.sha256(
        Path("/reference/lemma-discovery.json").read_bytes()
    ).hexdigest(),
}
for name, actual in computed.items():
    print(
        name,
        "actual=",
        actual,
        "recorded=",
        root_input["hashes"][name],
        "match=",
        actual == root_input["hashes"][name],
    )
print("lean_invocation_sha256=", root_input["hashes"]["lean_invocation_sha256"])
print("lean_workspace_sha256=", root_input["hashes"]["lean_workspace_sha256"])

actual_exporter = hashlib.sha256(
    Path("/reference/generation-tools/klean_export.py").read_bytes()
).hexdigest()
actual_klean = hashlib.sha256(
    Path("/reference/generation-tools/klean.py").read_bytes()
).hexdigest()
input_image_id = "sha256:" + Path(
    root_input["generation_producer_sources"]
).name
print("PRODUCER_AUTHENTICATION")
print("klean_export_actual=", actual_exporter)
print(
    "klean_export_source_manifest=",
    source_manifest["files"]["klean_export.py"],
)
print("klean_export_generator_manifest=", generator["exporter_sha256"])
print(
    "klean_export_all_match=",
    len(
        {
            actual_exporter,
            source_manifest["files"]["klean_export.py"],
            generator["exporter_sha256"],
        }
    )
    == 1,
)
print("klean_actual=", actual_klean)
print("klean_source_manifest=", source_manifest["files"]["klean.py"])
print("klean_generator_manifest=", generator["klean_py_sha256"])
print(
    "klean_all_match=",
    len(
        {
            actual_klean,
            source_manifest["files"]["klean.py"],
            generator["klean_py_sha256"],
        }
    )
    == 1,
)
print("generator_image_audit_input=", input_image_id)
print(
    "generator_image_source_manifest=", source_manifest["generator_image_id"]
)
print(
    "generator_image_generator_manifest=",
    generator["provenance"]["generator_image_id"],
)
print(
    "generator_image_all_match=",
    len(
        {
            input_image_id,
            source_manifest["generator_image_id"],
            generator["provenance"]["generator_image_id"],
        }
    )
    == 1,
)
