#!/usr/bin/env python3
import hashlib
import json
import stat
from pathlib import Path

from tools import pipeline_contract
from tools.klean_export import tree_digest


producer_dir = Path("/reference/generation-tools")
source_manifest_path = producer_dir / "source-manifest.json"
generator_manifest_path = Path("/reference/klean-generation/generator-manifest.json")
audit_input_path = Path("/audit-input.json")

source_manifest = json.loads(source_manifest_path.read_text())
generator_manifest = json.loads(generator_manifest_path.read_text())
audit_input = json.loads(audit_input_path.read_text())
resolution = audit_input["resolution"]

actual_hashes = {}
regular_files = {}
for name in ("klean_export.py", "klean.py"):
    path = producer_dir / name
    mode = path.stat(follow_symlinks=False).st_mode
    regular_files[name] = stat.S_ISREG(mode)
    actual_hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()

image_id = source_manifest["generator_image_id"]
image_digest = image_id.removeprefix("sha256:")
audit_source_path = Path(resolution["generation_producer_sources"])
actual_tree_hash = pipeline_contract.sha256_tree(producer_dir)
klean_tree_hash = tree_digest(producer_dir)

checks = {
    "producer_files_regular": all(regular_files.values()),
    "source_manifest_schema_1": source_manifest.get("schema_version") == 1,
    "file_hashes_match_source_manifest": actual_hashes == source_manifest.get("files"),
    "exporter_hash_matches_generator_manifest": actual_hashes["klean_export.py"] == generator_manifest.get("exporter_sha256"),
    "klean_hash_matches_generator_manifest": actual_hashes["klean.py"] == generator_manifest.get("klean_py_sha256"),
    "image_matches_generator_manifest": image_id == generator_manifest.get("provenance", {}).get("generator_image_id"),
    "image_matches_audit_input_path": audit_source_path.name == image_digest,
    "source_tree_matches_audit_input": actual_tree_hash == resolution["hashes"].get("generation_producer_sources_sha256"),
}
result = {
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "actual_file_sha256": actual_hashes,
    "source_manifest_file_sha256": source_manifest["files"],
    "generator_manifest_file_sha256": {
        "klean_export.py": generator_manifest.get("exporter_sha256"),
        "klean.py": generator_manifest.get("klean_py_sha256"),
    },
    "generator_image_id": image_id,
    "audit_input_producer_path": str(audit_source_path),
    "actual_producer_tree_sha256": actual_tree_hash,
    "informational_klean_tree_digest": klean_tree_hash,
    "audit_input_producer_tree_sha256": resolution["hashes"].get("generation_producer_sources_sha256"),
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["all_checks_pass"] else 1)
