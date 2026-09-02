#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import pipeline_contract


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
bundle = Path("/reference/generation-tools")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


exporter = sha256(bundle / "klean_export.py")
klean = sha256(bundle / "klean.py")
generator_image_id = generator["provenance"]["generator_image_id"]
source_image_id = source["generator_image_id"]
audit_bundle_component = Path(
    audit["generation_producer_sources"]
).name
expected_files = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}

print(
    json.dumps(
        {
            "bundle_entries": sorted(
                path.relative_to(bundle).as_posix()
                for path in bundle.iterdir()
            ),
            "bundle_tree_sha256": {
                "observed": pipeline_contract.sha256_tree(bundle),
                "expected": audit["hashes"][
                    "generation_producer_sources_sha256"
                ],
            },
            "generator_image_id": {
                "generator_manifest": generator_image_id,
                "source_manifest": source_image_id,
                "audit_input_path_component": audit_bundle_component,
                "all_match": (
                    generator_image_id == source_image_id
                    and generator_image_id.removeprefix("sha256:")
                    == audit_bundle_component
                ),
            },
            "producer_files": {
                "klean_export.py": {
                    "observed": exporter,
                    "generator_manifest": generator["exporter_sha256"],
                    "source_manifest": source["files"]["klean_export.py"],
                    "all_match": (
                        exporter
                        == generator["exporter_sha256"]
                        == source["files"]["klean_export.py"]
                    ),
                },
                "klean.py": {
                    "observed": klean,
                    "generator_manifest": generator["klean_py_sha256"],
                    "source_manifest": source["files"]["klean.py"],
                    "all_match": (
                        klean
                        == generator["klean_py_sha256"]
                        == source["files"]["klean.py"]
                    ),
                },
            },
            "source_manifest_exact_file_map": source["files"]
            == expected_files,
        },
        indent=2,
        sort_keys=True,
    )
)
