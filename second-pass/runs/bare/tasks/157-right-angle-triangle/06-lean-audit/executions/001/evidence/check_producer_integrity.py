#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)

exporter = Path("/reference/generation-tools/klean_export.py")
klean = Path("/reference/generation-tools/klean.py")
actual_exporter = hashlib.sha256(exporter.read_bytes()).hexdigest()
actual_klean = hashlib.sha256(klean.read_bytes()).hexdigest()
actual_tree = sha256_tree(Path("/reference/generation-tools"))

source_image = source_manifest["generator_image_id"]
generator_image = generator_manifest["provenance"]["generator_image_id"]
audit_source_path_id = "sha256:" + Path(
    audit_input["generation_producer_sources"]
).name

checks = {
    "klean_export.py == source-manifest": (
        actual_exporter == source_manifest["files"]["klean_export.py"]
    ),
    "klean_export.py == generator-manifest": (
        actual_exporter == generator_manifest["exporter_sha256"]
    ),
    "klean.py == source-manifest": (
        actual_klean == source_manifest["files"]["klean.py"]
    ),
    "klean.py == generator-manifest": (
        actual_klean == generator_manifest["klean_py_sha256"]
    ),
    "producer tree == audit-input": (
        actual_tree
        == audit_input["hashes"]["generation_producer_sources_sha256"]
    ),
    "image == source-manifest": source_image == generator_image,
    "image == audit-input source path": source_image == audit_source_path_id,
}

print(
    json.dumps(
        {
            "actual": {
                "klean_export.py": actual_exporter,
                "klean.py": actual_klean,
                "producer_tree": actual_tree,
                "generator_image_id": source_image,
            },
            "recorded": {
                "source_manifest_files": source_manifest["files"],
                "generator_manifest_exporter_sha256": generator_manifest[
                    "exporter_sha256"
                ],
                "generator_manifest_klean_py_sha256": generator_manifest[
                    "klean_py_sha256"
                ],
                "audit_input_producer_tree": audit_input["hashes"][
                    "generation_producer_sources_sha256"
                ],
                "source_manifest_image_id": source_image,
                "generator_manifest_image_id": generator_image,
                "audit_input_source_path_image_id": audit_source_path_id,
            },
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
