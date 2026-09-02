import hashlib
import json
import os
from pathlib import Path

from tools.klean_audit_contract import verify_stage6_audit_input
from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


audit_path = Path("/audit-input.json")
document = json.loads(audit_path.read_text())
audit = document["resolution"]
resolution, resolved_digest = verify_stage6_audit_input(document)
source = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
producer_files = [
    Path("/reference/generation-tools/klean_export.py"),
    Path("/reference/generation-tools/klean.py"),
]
actual_producers = {
    path.name: hashlib.sha256(path.read_bytes()).hexdigest()
    for path in producer_files
}
path_image = (
    "sha256:" + Path(audit["generation_producer_sources"]).name
)
source_hashes = {
    path.name: hashlib.sha256(path.read_bytes()).hexdigest()
    for path in sorted(Path("/reference/k-proof").iterdir())
    if path.is_file()
}
artifact_paths = {
    "generation_producer_sources": Path("/reference/generation-tools"),
    "k_workspace": Path("/reference/k-proof"),
    "k_audit": Path("/reference/k-audit"),
    "klean_generation": Path("/reference/klean-generation"),
}
artifact_hash_fields = {
    "generation_producer_sources": "generation_producer_sources_sha256",
    "k_workspace": "k_workspace_sha256",
    "k_audit": "k_audit_sha256",
    "klean_generation": "klean_generation_sha256",
}
artifact_hashes = {}
for name, path in artifact_paths.items():
    actual = sha256_tree(path)
    recorded = audit["hashes"][artifact_hash_fields[name]]
    artifact_hashes[name] = {
        "actual": actual,
        "recorded": recorded,
        "match": actual == recorded,
    }

export_hashes = {
    "stage1_export_sha256": {
        "actual": tree_digest(Path("/reference/k-proof")),
        "recorded": audit["hashes"]["stage1_export_sha256"],
    },
    "generated_tree_sha256": {
        "actual": tree_digest(
            Path("/reference/klean-generation/generated")
        ),
        "recorded": audit["hashes"]["generated_tree_sha256"],
    },
    "discovery_manifest_sha256": {
        "actual": hashlib.sha256(
            Path("/reference/lemma-discovery.json").read_bytes()
        ).hexdigest(),
        "recorded": audit["hashes"]["discovery_manifest_sha256"],
    },
}
for entry in export_hashes.values():
    entry["match"] = entry["actual"] == entry["recorded"]

result = {
    "mode": {
        "AUDIT_MODE": os.environ.get("AUDIT_MODE"),
        "resolved_mode": resolution["mode"],
        "classification_only_has_null_target": resolution["target"] is None,
        "classification_only_has_no_stage5": (
            resolution["stage5_result"] is None
            and resolution["lean_workspace"] is None
            and resolution["lean_invocation"] is None
        ),
    },
    "audit_input": {
        "resolved_sha256_recorded": document["resolved_input_sha256"],
        "resolved_sha256_recomputed": resolved_digest,
        "resolved_hash_match": (
            resolved_digest == document["resolved_input_sha256"]
        ),
        "mounted_and_output_copies_identical": (
            audit_path.read_bytes()
            == Path("/audit-output/audit-input.json").read_bytes()
        ),
    },
    "producer_authentication": {
        "actual_file_sha256": actual_producers,
        "source_manifest_file_sha256": source["files"],
        "generator_manifest_exporter_sha256": generator["exporter_sha256"],
        "generator_manifest_klean_py_sha256": generator["klean_py_sha256"],
        "source_manifest_generator_image_id": source["generator_image_id"],
        "generator_manifest_generator_image_id": (
            generator["provenance"]["generator_image_id"]
        ),
        "audit_input_path_generator_image_id": path_image,
        "all_file_hashes_match": (
            actual_producers == source["files"]
            and actual_producers["klean_export.py"]
            == generator["exporter_sha256"]
            and actual_producers["klean.py"]
            == generator["klean_py_sha256"]
        ),
        "all_image_ids_match": (
            source["generator_image_id"]
            == generator["provenance"]["generator_image_id"]
            == path_image
        ),
    },
    "artifact_tree_hashes": artifact_hashes,
    "export_tree_and_manifest_hashes": export_hashes,
    "stage1_source_hashes": {
        "actual": source_hashes,
        "recorded": audit["stage1_source_hashes"],
        "match": source_hashes == audit["stage1_source_hashes"],
    },
}
print(json.dumps(result, indent=2, sort_keys=True))

assert result["mode"]["AUDIT_MODE"] == "CLASSIFICATION_ONLY"
assert result["mode"]["resolved_mode"] == "CLASSIFICATION_ONLY"
assert result["mode"]["classification_only_has_null_target"]
assert result["mode"]["classification_only_has_no_stage5"]
assert result["audit_input"]["resolved_hash_match"]
assert result["audit_input"]["mounted_and_output_copies_identical"]
assert result["producer_authentication"]["all_file_hashes_match"]
assert result["producer_authentication"]["all_image_ids_match"]
assert all(entry["match"] for entry in artifact_hashes.values())
assert all(entry["match"] for entry in export_hashes.values())
assert result["stage1_source_hashes"]["match"]
