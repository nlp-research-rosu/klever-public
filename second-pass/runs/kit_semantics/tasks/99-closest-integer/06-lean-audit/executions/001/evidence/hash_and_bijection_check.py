#!/usr/bin/env python3
import hashlib
import json
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(root: Path) -> set[str]:
    result = set()
    for path in root.rglob("*"):
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            result.add(path.relative_to(root).as_posix())
        elif not stat.S_ISDIR(mode):
            raise RuntimeError(f"unsupported entry: {path}")
    return result


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
recorded = resolution["hashes"]

pipeline_trees = {
    "k_workspace_sha256": Path("/reference/k-proof"),
    "k_audit_sha256": Path("/reference/k-audit"),
    "klean_generation_sha256": Path("/reference/klean-generation"),
    "generation_producer_sources_sha256": Path("/reference/generation-tools"),
}
for field, path in pipeline_trees.items():
    actual = pipeline_contract.sha256_tree(path)
    print(f"{field}: recorded={recorded[field]} actual={actual} match={actual == recorded[field]}")

stage1_export = klean_export.tree_digest(Path("/reference/k-proof"))
print(
    "stage1_export_sha256: "
    f"recorded={recorded['stage1_export_sha256']} actual={stage1_export} "
    f"match={stage1_export == recorded['stage1_export_sha256']}"
)

generated_tree = klean_export.tree_digest(Path("/reference/klean-generation/generated"))
print(
    "generated_tree_sha256: "
    f"recorded={recorded['generated_tree_sha256']} actual={generated_tree} "
    f"match={generated_tree == recorded['generated_tree_sha256']}"
)

discovery_hash = file_hash(Path("/reference/lemma-discovery.json"))
print(
    "discovery_manifest_sha256: "
    f"recorded={recorded['discovery_manifest_sha256']} actual={discovery_hash} "
    f"match={discovery_hash == recorded['discovery_manifest_sha256']}"
)

workspace = Path("/reference/k-proof")
expected_source_hashes = resolution["stage1_source_hashes"]
actual_files = regular_files(workspace)
expected_files = set(expected_source_hashes)
mismatches = []
for relative in sorted(expected_files & actual_files):
    actual = file_hash(workspace / relative)
    if actual != expected_source_hashes[relative]:
        mismatches.append((relative, expected_source_hashes[relative], actual))
print(f"stage1_source_hash_count_recorded={len(expected_files)}")
print(f"stage1_regular_file_count_actual={len(actual_files)}")
print(f"stage1_source_hash_missing={sorted(expected_files - actual_files)}")
print(f"stage1_source_hash_extra={sorted(actual_files - expected_files)}")
print(f"stage1_source_hash_mismatches={mismatches}")

discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
input_manifest = json.loads(Path("/reference/klean-generation/input-manifest.json").read_text())
generator_manifest = json.loads(Path("/reference/klean-generation/generator-manifest.json").read_text())
obligation_map_path = Path("/reference/klean-generation/generated/obligation-map.json")
obligation_map = json.loads(obligation_map_path.read_text())
export_result = json.loads(Path("/reference/klean-generation/export-result.json").read_text())
source_manifest = json.loads(Path("/reference/generation-tools/source-manifest.json").read_text())
toolchain_lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())

print(f"discovery_rules={discovery['rules']}")
print(f"input_source_rules={input_manifest['source_rules']}")
print(f"input_definitions={input_manifest['definitions']}")
print(f"input_operational_rules={input_manifest['operational_rules']}")
print(f"input_proved_derived_lemmas={input_manifest['proved_derived_lemmas']}")
print(f"obligation_map={json.dumps(obligation_map, sort_keys=True)}")
print(f"generator_obligation_count={generator_manifest['obligation_count']}")
print(f"export_obligation_count={export_result['obligation_count']}")
print(f"generator_target={generator_manifest['target']}")
print(f"audit_target={resolution['target']}")
print(f"derived_target={klean_export.target_statement(Path('/reference/klean-generation/generated'))}")
print(f"selected_stage4_status={resolution['selections']['klean_generation']['status']}")
print(f"audit_mode={resolution['mode']}")
print(f"lean_workspace={resolution['lean_workspace']}")
print(f"lean_invocation={resolution['lean_invocation']}")

obligation_file_hash = file_hash(obligation_map_path)
print(
    "obligation_map_sha256: "
    f"recorded={generator_manifest['obligation_map_sha256']} actual={obligation_file_hash} "
    f"match={obligation_file_hash == generator_manifest['obligation_map_sha256']}"
)
print(f"toolchain_lock_matches_generator={toolchain_lock == generator_manifest['toolchain']}")
print(
    "producer_exporter_hash_matches_all="
    + str(
        file_hash(Path("/reference/generation-tools/klean_export.py"))
        == source_manifest["files"]["klean_export.py"]
        == generator_manifest["exporter_sha256"]
    )
)
print(
    "producer_klean_hash_matches_all="
    + str(
        file_hash(Path("/reference/generation-tools/klean.py"))
        == source_manifest["files"]["klean.py"]
        == generator_manifest["klean_py_sha256"]
    )
)
print(
    "generator_image_id_matches_source_manifest="
    + str(generator_manifest["provenance"]["generator_image_id"] == source_manifest["generator_image_id"])
)
print(
    "generator_image_id_matches_audit_path="
    + str(
        generator_manifest["provenance"]["generator_image_id"]
        == "sha256:" + Path(resolution["generation_producer_sources"]).name
    )
)

cross_checks = {
    "inventory_discovery_to_input": discovery["inventory_sha256"] == input_manifest["inventory_sha256"],
    "inventory_input_to_generator": input_manifest["inventory_sha256"] == generator_manifest["provenance"]["inventory_sha256"],
    "stage1_input_to_generator": input_manifest["stage1_workspace_sha256"] == generator_manifest["provenance"]["stage1_workspace_sha256"],
    "discovery_input_to_generator": input_manifest["stage3_discovery_manifest_sha256"] == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    "generated_generator_to_export": generator_manifest["generated_tree_sha256"] == export_result["generated_tree_sha256"],
    "status_selected_to_export": resolution["selections"]["klean_generation"]["status"] == export_result["status"],
}
print(f"cross_checks={json.dumps(cross_checks, sort_keys=True)}")
print(f"all_cross_checks={all(cross_checks.values())}")
