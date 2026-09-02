#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)

checks = {}
observed_pipeline_trees = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "lean_workspace_sha256": sha256_tree(Path("/candidate")),
}
for key, value in observed_pipeline_trees.items():
    checks[f"audit_input.{key}"] = {
        "expected": recorded[key],
        "observed": value,
        "match": recorded[key] == value,
    }

observed_export_trees = {
    "stage1_export_sha256": tree_digest(Path("/reference/k-proof")),
    "generated_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
}
for key, value in observed_export_trees.items():
    checks[f"audit_input.{key}"] = {
        "expected": recorded[key],
        "observed": value,
        "match": recorded[key] == value,
    }

checks["audit_input.discovery_manifest_sha256"] = {
    "expected": recorded["discovery_manifest_sha256"],
    "observed": sha256_file(Path("/reference/lemma-discovery.json")),
    "match": recorded["discovery_manifest_sha256"]
    == sha256_file(Path("/reference/lemma-discovery.json")),
}

producer_files = {
    name: sha256_file(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
generator_expected_files = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
checks["producer.files_match_source_manifest"] = {
    "expected": source_manifest["files"],
    "observed": producer_files,
    "match": source_manifest["files"] == producer_files,
}
checks["producer.files_match_generator_manifest"] = {
    "expected": generator_expected_files,
    "observed": producer_files,
    "match": generator_expected_files == producer_files,
}
generator_image_id = generator["provenance"]["generator_image_id"]
checks["producer.image_matches_source_manifest"] = {
    "expected": generator_image_id,
    "observed": source_manifest["generator_image_id"],
    "match": generator_image_id == source_manifest["generator_image_id"],
}
audit_bundle_id = Path(
    resolution["generation_producer_sources"]
).name
checks["producer.image_matches_audit_input_bundle"] = {
    "expected": generator_image_id.removeprefix("sha256:"),
    "observed": audit_bundle_id,
    "match": generator_image_id.removeprefix("sha256:") == audit_bundle_id,
}
checks["producer.source_manifest_exact_keys"] = {
    "expected": ["files", "generator_image_id", "schema_version"],
    "observed": sorted(source_manifest),
    "match": set(source_manifest)
    == {"files", "generator_image_id", "schema_version"},
}
checks["generator.toolchain_matches_lock"] = {
    "expected": toolchain_lock,
    "observed": generator["toolchain"],
    "match": toolchain_lock == generator["toolchain"],
}
checks["generator.target_matches_audit_input"] = {
    "expected": resolution["target"],
    "observed": generator["target"],
    "match": resolution["target"] == generator["target"],
}

stage1_root = Path("/reference/k-proof")
observed_stage1_files = {
    path.relative_to(stage1_root).as_posix(): sha256_file(path)
    for path in sorted(stage1_root.rglob("*"))
    if path.is_file() and not path.is_symlink()
}
checks["stage1_source_hashes"] = {
    "expected_count": len(resolution["stage1_source_hashes"]),
    "observed_count": len(observed_stage1_files),
    "missing": sorted(
        set(resolution["stage1_source_hashes"]) - set(observed_stage1_files)
    ),
    "extra": sorted(
        set(observed_stage1_files) - set(resolution["stage1_source_hashes"])
    ),
    "mismatches": sorted(
        name
        for name in set(resolution["stage1_source_hashes"])
        & set(observed_stage1_files)
        if resolution["stage1_source_hashes"][name]
        != observed_stage1_files[name]
    ),
}
checks["stage1_source_hashes"]["match"] = not any(
    checks["stage1_source_hashes"][key]
    for key in ("missing", "extra", "mismatches")
)

checks["stage4_manifest_bindings"] = {
    "input_stage1": input_manifest["stage1_workspace_sha256"]
    == observed_export_trees["stage1_export_sha256"],
    "input_discovery": input_manifest[
        "stage3_discovery_manifest_sha256"
    ]
    == checks["audit_input.discovery_manifest_sha256"]["observed"],
    "generator_stage1": generator["provenance"]["stage1_workspace_sha256"]
    == observed_export_trees["stage1_export_sha256"],
    "generator_discovery": generator["provenance"][
        "stage3_discovery_manifest_sha256"
    ]
    == checks["audit_input.discovery_manifest_sha256"]["observed"],
    "generator_generated": generator["generated_tree_sha256"]
    == observed_export_trees["generated_tree_sha256"],
    "export_stage1": export_result["frozen_input_sha256"]
    == observed_export_trees["stage1_export_sha256"],
    "export_discovery": export_result[
        "stage3_discovery_manifest_sha256"
    ]
    == checks["audit_input.discovery_manifest_sha256"]["observed"],
    "export_generated": export_result["generated_tree_sha256"]
    == observed_export_trees["generated_tree_sha256"],
}
checks["stage4_manifest_bindings"]["match"] = all(
    checks["stage4_manifest_bindings"].values()
)

all_match = all(value.get("match", False) for value in checks.values())
print(json.dumps({"all_match": all_match, "checks": checks}, indent=2))
