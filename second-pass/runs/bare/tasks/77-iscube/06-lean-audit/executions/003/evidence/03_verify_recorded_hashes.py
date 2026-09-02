import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.stage6_resolution_contract import verify_audit_input


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = verify_audit_input(audit_input)
recorded = resolution["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)


def file_sha(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha(
        "/reference/lemma-discovery.json"
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}

producer_files = {
    name: file_sha(f"/reference/generation-tools/{name}")
    for name in ("klean_export.py", "klean.py")
}
image_id = generator["provenance"]["generator_image_id"]
image_key = image_id.removeprefix("sha256:")
audit_bundle_key = Path(
    resolution["generation_producer_sources"]
).name

report = {
    "audit_input_envelope_valid": True,
    "resolved_input_sha256": resolved_digest,
    "recorded_hashes": recorded,
    "observed_accessible_hashes": observed,
    "accessible_hash_comparisons": {
        key: {
            "recorded": recorded[key],
            "observed": value,
            "matches": recorded[key] == value,
        }
        for key, value in observed.items()
    },
    "producer_authentication": {
        "observed_file_hashes": producer_files,
        "generator_manifest_hashes": {
            "klean_export.py": generator["exporter_sha256"],
            "klean.py": generator["klean_py_sha256"],
        },
        "source_manifest_hashes": source_manifest["files"],
        "file_hashes_match_both_manifests": (
            producer_files
            == source_manifest["files"]
            == {
                "klean_export.py": generator["exporter_sha256"],
                "klean.py": generator["klean_py_sha256"],
            }
        ),
        "generator_manifest_image_id": image_id,
        "source_manifest_image_id": source_manifest["generator_image_id"],
        "audit_input_bundle_key": audit_bundle_key,
        "image_id_matches_all_three": (
            image_id == source_manifest["generator_image_id"]
            and image_key == audit_bundle_key
        ),
        "bundle_exact_regular_files": sorted(
            path.name
            for path in Path("/reference/generation-tools").iterdir()
            if path.is_file() and not path.is_symlink()
        ),
    },
}

print(json.dumps(report, indent=2, sort_keys=True))
