#!/usr/bin/env bash
set -euxo pipefail
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json
sed -n '1,220p' /reference/generation-tools/source-manifest.json
sed -n '1,260p' /reference/klean-generation/generator-manifest.json
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools import pipeline_contract, stage6_resolution_contract

audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
resolution, signed_digest = stage6_resolution_contract.verify_audit_input(audit)
bundle = Path("/reference/generation-tools")
generation = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source = json.loads((bundle / "source-manifest.json").read_text())

actual = {
    name: pipeline_contract.sha256_file(bundle / name)
    for name in ("klean_export.py", "klean.py")
}
expected = {
    "klean_export.py": generation["exporter_sha256"],
    "klean.py": generation["klean_py_sha256"],
}
image_id = generation["provenance"]["generator_image_id"]
audit_bundle_key = Path(resolution["generation_producer_sources"]).name
observed_files = sorted(
    path.relative_to(bundle).as_posix()
    for path in pipeline_contract._walk_regular_files(
        bundle, "mounted Stage 4 producer source bundle"
    )
)
result = {
    "audit_input_verified": True,
    "resolved_input_sha256": signed_digest,
    "producer_file_hashes_actual": actual,
    "producer_file_hashes_generator_manifest": expected,
    "producer_file_hashes_source_manifest": source["files"],
    "producer_file_hashes_match": actual == expected == source["files"],
    "generator_image_id_generator_manifest": image_id,
    "generator_image_id_source_manifest": source["generator_image_id"],
    "generator_image_id_audit_path_key": f"sha256:{audit_bundle_key}",
    "generator_image_ids_match": (
        image_id
        == source["generator_image_id"]
        == f"sha256:{audit_bundle_key}"
    ),
    "producer_bundle_files": observed_files,
    "producer_bundle_exact_file_set": observed_files
    == ["klean.py", "klean_export.py", "source-manifest.json"],
    "producer_bundle_sha256_actual": pipeline_contract.sha256_tree(bundle),
    "producer_bundle_sha256_audit_input": resolution["hashes"][
        "generation_producer_sources_sha256"
    ],
}
result["producer_bundle_sha256_match"] = (
    result["producer_bundle_sha256_actual"]
    == result["producer_bundle_sha256_audit_input"]
)
print(json.dumps(result, indent=2, sort_keys=True))
assert result["producer_file_hashes_match"]
assert result["generator_image_ids_match"]
assert result["producer_bundle_exact_file_set"]
assert result["producer_bundle_sha256_match"]
PY
