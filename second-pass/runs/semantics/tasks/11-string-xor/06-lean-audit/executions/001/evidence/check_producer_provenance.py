#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


AUDIT_INPUT = Path("/audit-input.json")
GENERATION = Path("/reference/klean-generation")
PRODUCERS = Path("/reference/generation-tools")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = json.loads(AUDIT_INPUT.read_text())
generator = json.loads((GENERATION / "generator-manifest.json").read_text())
source = json.loads((PRODUCERS / "source-manifest.json").read_text())
resolution = audit_input["resolution"]

exporter = sha256(PRODUCERS / "klean_export.py")
klean = sha256(PRODUCERS / "klean.py")
bundle = sha256_tree(PRODUCERS)
audit_bundle = resolution["hashes"]["generation_producer_sources_sha256"]
audit_image_key = Path(resolution["generation_producer_sources"]).name
audit_image_id = f"sha256:{audit_image_key}"
generator_image_id = generator["provenance"]["generator_image_id"]
source_image_id = source["generator_image_id"]

checks = {
    "bundle_sha256_matches_audit_input": bundle == audit_bundle,
    "exporter_matches_generator_manifest": exporter == generator["exporter_sha256"],
    "exporter_matches_source_manifest": exporter == source["files"]["klean_export.py"],
    "klean_matches_generator_manifest": klean == generator["klean_py_sha256"],
    "klean_matches_source_manifest": klean == source["files"]["klean.py"],
    "generator_image_matches_source_manifest": generator_image_id == source_image_id,
    "generator_image_matches_audit_input_path": generator_image_id == audit_image_id,
    "source_manifest_file_set_exact": set(source["files"]) == {"klean_export.py", "klean.py"},
    "producer_bundle_file_set_exact": {
        path.relative_to(PRODUCERS).as_posix()
        for path in PRODUCERS.rglob("*")
        if path.is_file()
    } == {"klean_export.py", "klean.py", "source-manifest.json"},
}

result = {
    "observed": {
        "producer_bundle_sha256_pipeline_contract": bundle,
        "klean_export.py_sha256": exporter,
        "klean.py_sha256": klean,
        "generator_manifest_image_id": generator_image_id,
        "source_manifest_image_id": source_image_id,
        "audit_input_image_id_from_bundle_path": audit_image_id,
    },
    "expected": {
        "audit_input_producer_bundle_sha256": audit_bundle,
        "generator_manifest_exporter_sha256": generator["exporter_sha256"],
        "generator_manifest_klean_py_sha256": generator["klean_py_sha256"],
        "source_manifest_files": source["files"],
    },
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(result, indent=2, sort_keys=True))
