#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.pipeline_contract import sha256_tree


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
recorded = audit["hashes"]

k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_sources = Path("/reference/generation-tools")
candidate = Path("/candidate")

observed = {
    "k_workspace_sha256": sha256_tree(k_workspace),
    "stage1_export_sha256": klean_export.tree_digest(k_workspace),
    "discovery_manifest_sha256": file_hash(discovery_path),
    "k_audit_sha256": sha256_tree(k_audit),
    "klean_generation_sha256": sha256_tree(generation),
    "generation_producer_sources_sha256": sha256_tree(producer_sources),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": sha256_tree(candidate),
}
for name, value in observed.items():
    assert recorded[name] == value, (name, recorded[name], value)

# The invocation transcript is not mounted as an independent input. Its hash
# remains explicitly outside the set re-hashable from the launcher mounts.
assert isinstance(recorded["lean_invocation_sha256"], str)

observed_stage1_files = {
    path.relative_to(k_workspace).as_posix(): file_hash(path)
    for path in k_workspace.rglob("*")
    if path.is_file() and not path.is_symlink()
}
assert observed_stage1_files == audit["stage1_source_hashes"]

input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
export_result = json.loads((generation / "export-result.json").read_text())

assert input_manifest["stage1_workspace_sha256"] == observed["stage1_export_sha256"]
assert input_manifest["stage3_discovery_manifest_sha256"] == observed[
    "discovery_manifest_sha256"
]
assert generator_manifest["generated_tree_sha256"] == observed[
    "generated_tree_sha256"
]
assert generator_manifest["provenance"]["stage1_workspace_sha256"] == observed[
    "stage1_export_sha256"
]
assert generator_manifest["provenance"][
    "stage3_discovery_manifest_sha256"
] == observed["discovery_manifest_sha256"]
assert generator_manifest["obligation_map_sha256"] == file_hash(obligation_map_path)
assert export_result["trust_inventory_sha256"] == file_hash(
    generation / "trust-inventory.json"
)

source_rules = input_manifest["source_rules"]
obligations = obligation_map["obligations"]
assert len(source_rules) == len(obligations) == generator_manifest["obligation_count"] == 1
assert len({rule["source_rule_id"] for rule in source_rules}) == 1
assert len({obligation["source_rule_id"] for obligation in obligations}) == 1

for source_rule, obligation in zip(source_rules, obligations, strict=True):
    assert source_rule["classification"] == "DOMAIN_LEMMA"
    assert obligation["source_rule_id"] == source_rule["source_rule_id"]
    assert obligation["source_span"] == {
        "start_line": source_rule["start_line"],
        "end_line": source_rule["end_line"],
    }
    for key in (
        "normalized_sha256",
        "inventory_sha256",
        "discovery_manifest_sha256",
    ):
        assert obligation[key] == source_rule[key]
    assert obligation["lean_conjunct_sha256"] == klean_export.sha256_text(
        obligation["lean_conjunct"]
    )

expected_definition = klean_export.expected_target_definition(obligation_map)
actual_target = klean_export.target_statement(generated)
assert expected_definition is not None
assert actual_target == generator_manifest["target"]
assert actual_target == audit["target"]
assert actual_target == audit["stage4_preflight"]["target"]
assert actual_target["definition_sha256"] == klean_export.sha256_text(
    expected_definition
)
assert actual_target["statement_sha256"] == klean_export.sha256_text(
    actual_target["statement"]
)
assert obligation_map["trust_parameters"] == actual_target["parameters"]

print(
    json.dumps(
        {
            "status": "PASS",
            "observed_hashes": observed,
            "verified_stage1_file_count": len(observed_stage1_files),
            "unmounted_recorded_hashes": {
                "lean_invocation_sha256": recorded["lean_invocation_sha256"]
            },
            "source_rule_ids": [rule["source_rule_id"] for rule in source_rules],
            "obligation_ids": [rule["source_rule_id"] for rule in obligations],
            "target": actual_target,
        },
        indent=2,
        sort_keys=True,
    )
)
