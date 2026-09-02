#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


audit = load("/audit-input.json")
source = load("/reference/generation-tools/source-manifest.json")
generator = load("/reference/klean-generation/generator-manifest.json")

actual_files = {
    name: hashlib.sha256(
        Path("/reference/generation-tools", name).read_bytes()
    ).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
audit_resolution = audit["resolution"]
audit_source_path = Path(
    audit_resolution["generation_producer_sources"]
)
audit_image_id = f"sha256:{audit_source_path.name}"
actual_tree = sha256_tree(Path("/reference/generation-tools"))
actual_bundle_files = sorted(
    path.relative_to("/reference/generation-tools").as_posix()
    for path in Path("/reference/generation-tools").rglob("*")
    if path.is_file() and not path.is_symlink()
)

checks = {
    "actual_files_equal_source_manifest": actual_files == source["files"],
    "exporter_equal_generator_manifest": (
        actual_files["klean_export.py"] == generator["exporter_sha256"]
    ),
    "klean_equal_generator_manifest": (
        actual_files["klean.py"] == generator["klean_py_sha256"]
    ),
    "source_image_equal_generator_manifest": (
        source["generator_image_id"]
        == generator["provenance"]["generator_image_id"]
    ),
    "source_image_equal_audit_input_path_binding": (
        source["generator_image_id"] == audit_image_id
    ),
    "producer_tree_equal_audit_input": (
        actual_tree
        == audit_resolution["hashes"]["generation_producer_sources_sha256"]
    ),
    "producer_bundle_file_set_is_exact": actual_bundle_files
    == ["klean.py", "klean_export.py", "source-manifest.json"],
    "source_manifest_schema_is_exact": (
        set(source)
        == {"schema_version", "generator_image_id", "files"}
        and source["schema_version"] == 1
    ),
}

print(
    json.dumps(
        {
            "actual_files": actual_files,
            "source_manifest_files": source["files"],
            "generator_exporter_sha256": generator["exporter_sha256"],
            "generator_klean_py_sha256": generator["klean_py_sha256"],
            "actual_producer_tree_sha256": actual_tree,
            "audit_producer_tree_sha256": audit_resolution["hashes"][
                "generation_producer_sources_sha256"
            ],
            "actual_bundle_files": actual_bundle_files,
            "source_manifest_generator_image_id": source[
                "generator_image_id"
            ],
            "generator_manifest_generator_image_id": generator[
                "provenance"
            ]["generator_image_id"],
            "audit_input_path_bound_generator_image_id": audit_image_id,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
