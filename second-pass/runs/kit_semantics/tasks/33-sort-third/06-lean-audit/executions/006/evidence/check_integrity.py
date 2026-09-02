#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_path = Path("/audit-input.json")
audit_document = json.loads(audit_path.read_text())
resolution, resolved_input_sha256 = stage6_resolution_contract.verify_audit_input(
    audit_document
)
expected = resolution["hashes"]
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)

producer_actual = {
    name: file_sha256(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
producer_expected_source_manifest = {
    name: source_manifest["files"][name]
    for name in ("klean_export.py", "klean.py")
}
producer_expected_generator_manifest = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
generator_image_ids = {
    "source_manifest": source_manifest.get("generator_image_id"),
    "generator_manifest": generator_manifest.get("provenance", {}).get(
        "generator_image_id"
    ),
    "audit_input_producer_path_basename": "sha256:"
    + Path(resolution["generation_producer_sources"]).name,
}

observed_hashes = {
    "discovery_manifest_sha256": file_sha256(
        Path("/reference/lemma-discovery.json")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(Path("/candidate")),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
}

stage1_mismatches = []
stage1_expected = resolution.get("stage1_source_hashes", {})
for relative, digest in stage1_expected.items():
    path = Path("/reference/k-proof") / relative
    if not path.is_file() or path.is_symlink():
        stage1_mismatches.append({
            "path": relative,
            "expected": digest,
            "observed": None,
            "reason": "missing_or_not_regular",
        })
        continue
    observed = file_sha256(path)
    if observed != digest:
        stage1_mismatches.append({
            "path": relative,
            "expected": digest,
            "observed": observed,
            "reason": "hash_mismatch",
        })

result = {
    "audit_mode_env": __import__("os").environ.get("AUDIT_MODE"),
    "audit_mode_recorded": resolution.get("mode"),
    "resolved_input_sha256": resolved_input_sha256,
    "producer_actual": producer_actual,
    "producer_expected_source_manifest": producer_expected_source_manifest,
    "producer_expected_generator_manifest": producer_expected_generator_manifest,
    "producer_hashes_all_match": (
        producer_actual == producer_expected_source_manifest
        == producer_expected_generator_manifest
    ),
    "generator_image_ids": generator_image_ids,
    "generator_image_ids_all_match": len(set(generator_image_ids.values())) == 1,
    "observed_hashes": observed_hashes,
    "expected_hashes": {key: expected.get(key) for key in observed_hashes},
    "all_mounted_top_level_hashes_match": all(
        observed == expected.get(key) for key, observed in observed_hashes.items()
    ),
    "unmounted_recorded_hashes": {
        "lean_invocation_sha256": expected.get("lean_invocation_sha256")
    },
    "stage1_source_hash_count": len(stage1_expected),
    "stage1_source_hash_mismatches": stage1_mismatches,
}
print(json.dumps(result, indent=2, sort_keys=True))
