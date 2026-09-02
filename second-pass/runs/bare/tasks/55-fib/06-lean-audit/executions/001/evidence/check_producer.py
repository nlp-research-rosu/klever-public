#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
generation = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

bundle = Path("/reference/generation-tools")
observed_files = sorted(path.name for path in bundle.iterdir())
file_hashes = {
    name: hashlib.sha256((bundle / name).read_bytes()).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
image_id = generation["provenance"]["generator_image_id"]
audit_path_image = Path(audit["generation_producer_sources"]).name

checks = {
    "bundle_file_set_exact": observed_files
    == ["klean.py", "klean_export.py", "source-manifest.json"],
    "klean_export_matches_generator": file_hashes["klean_export.py"]
    == generation["exporter_sha256"],
    "klean_matches_generator": file_hashes["klean.py"]
    == generation["klean_py_sha256"],
    "file_hashes_match_source_manifest": file_hashes == source["files"],
    "image_matches_source_manifest": image_id == source["generator_image_id"],
    "image_matches_audit_path": image_id.removeprefix("sha256:")
    == audit_path_image,
    "bundle_tree_matches_audit": sha256_tree(bundle)
    == audit["hashes"]["generation_producer_sources_sha256"],
}

print(
    json.dumps(
        {
            "observed_file_hashes": file_hashes,
            "observed_bundle_tree_sha256": sha256_tree(bundle),
            "generator_image_id": image_id,
            "audit_path_image_id": audit_path_image,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(0 if all(checks.values()) else 1)
