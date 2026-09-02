#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

producer_files = {
    name: file_sha256(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
observed_bundle_hash = sha256_tree(Path("/reference/generation-tools"))
image_ids = {
    "generator_manifest": generator["provenance"]["generator_image_id"],
    "source_manifest": source["generator_image_id"],
    "audit_input_path_key": "sha256:"
    + Path(audit["generation_producer_sources"]).name,
}
checks = {
    "klean_export_matches_generator": (
        producer_files["klean_export.py"] == generator["exporter_sha256"]
    ),
    "klean_export_matches_source_manifest": (
        producer_files["klean_export.py"] == source["files"]["klean_export.py"]
    ),
    "klean_matches_generator": (
        producer_files["klean.py"] == generator["klean_py_sha256"]
    ),
    "klean_matches_source_manifest": (
        producer_files["klean.py"] == source["files"]["klean.py"]
    ),
    "image_ids_all_equal": len(set(image_ids.values())) == 1,
    "bundle_matches_audit_input": (
        observed_bundle_hash
        == audit["hashes"]["generation_producer_sources_sha256"]
    ),
}
print(
    json.dumps(
        {
            "producer_files": producer_files,
            "generator_hashes": {
                "klean_export.py": generator["exporter_sha256"],
                "klean.py": generator["klean_py_sha256"],
            },
            "source_manifest_files": source["files"],
            "image_ids": image_ids,
            "observed_pipeline_tree_sha256": observed_bundle_hash,
            "audit_input_pipeline_tree_sha256": audit["hashes"][
                "generation_producer_sources_sha256"
            ],
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
