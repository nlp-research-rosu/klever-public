#!/usr/bin/env bash
set -uo pipefail

sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /audit-input.json

PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree

audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
source = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
actual = {
    name: hashlib.sha256(
        Path("/reference/generation-tools", name).read_bytes()
    ).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
producer_tree = sha256_tree(Path("/reference/generation-tools"))
image_id = source["generator_image_id"]
audit_source_path_id = (
    "sha256:" + Path(audit["generation_producer_sources"]).name
)
checks = {
    "klean_export_matches_source_manifest":
        actual["klean_export.py"] == source["files"]["klean_export.py"],
    "klean_export_matches_generator_manifest":
        actual["klean_export.py"] == generator["exporter_sha256"],
    "klean_matches_source_manifest":
        actual["klean.py"] == source["files"]["klean.py"],
    "klean_matches_generator_manifest":
        actual["klean.py"] == generator["klean_py_sha256"],
    "producer_tree_matches_audit_input":
        producer_tree
        == audit["hashes"]["generation_producer_sources_sha256"],
    "image_matches_generator_manifest":
        image_id == generator["provenance"]["generator_image_id"],
    "image_matches_audit_input_source_path":
        image_id == audit_source_path_id,
}
print(json.dumps({
    "actual_file_sha256": actual,
    "producer_tree_sha256": producer_tree,
    "source_manifest_generator_image_id": image_id,
    "generator_manifest_generator_image_id":
        generator["provenance"]["generator_image_id"],
    "audit_input_source_path_image_id": audit_source_path_id,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}, indent=2, sort_keys=True))
PY
