#!/usr/bin/env bash
set -eu

printf '%s\n' '$ printenv AUDIT_MODE'
printenv AUDIT_MODE

printf '%s\n' '$ sha256sum producer sources and immutable manifests'
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/klean-generation/export-result.json \
  /reference/klean-generation/preflight.json \
  /reference/klean-generation/trust-inventory.json \
  /reference/lemma-discovery.json \
  /audit-input.json

printf '%s\n' '$ PYTHONPATH=/reference python3 - (trusted digest functions and producer manifest checks)'
PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree

audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

observed_files = sorted(
    path.relative_to("/reference/generation-tools").as_posix()
    for path in Path("/reference/generation-tools").iterdir()
)
observed_hashes = {
    name: hashlib.sha256(
        (Path("/reference/generation-tools") / name).read_bytes()
    ).hexdigest()
    for name in ("klean_export.py", "klean.py")
}
expected_hashes = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
image_ids = {
    "generator_manifest": generator["provenance"]["generator_image_id"],
    "source_manifest": source_manifest["generator_image_id"],
    "audit_input_path_component": Path(
        resolution["generation_producer_sources"]
    ).name,
}
checks = {
    "source_manifest_exact_keys": set(source_manifest)
    == {"schema_version", "generator_image_id", "files"},
    "source_manifest_schema_1": source_manifest.get("schema_version") == 1,
    "bundle_exact_files": observed_files
    == ["klean.py", "klean_export.py", "source-manifest.json"],
    "per_file_hashes_match_generator": observed_hashes == expected_hashes,
    "per_file_hashes_match_source_manifest": observed_hashes
    == source_manifest["files"],
    "image_ids_match": image_ids["generator_manifest"]
    == image_ids["source_manifest"]
    == "sha256:" + image_ids["audit_input_path_component"],
}

digests = {
    "producer_bundle_pipeline_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "producer_bundle_expected_audit_input": resolution["hashes"][
        "generation_producer_sources_sha256"
    ],
    "stage1_klean_tree_digest": tree_digest(Path("/reference/k-proof")),
    "stage1_expected_export": resolution["hashes"]["stage1_export_sha256"],
    "generated_klean_tree_digest": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generated_expected_audit_input": resolution["hashes"][
        "generated_tree_sha256"
    ],
    "generation_pipeline_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_expected_audit_input": resolution["hashes"][
        "klean_generation_sha256"
    ],
}
checks.update(
    {
        "producer_aggregate_matches_audit_input": digests[
            "producer_bundle_pipeline_sha256"
        ]
        == digests["producer_bundle_expected_audit_input"],
        "stage1_export_matches_audit_input": digests["stage1_klean_tree_digest"]
        == digests["stage1_expected_export"],
        "generated_tree_matches_audit_input": digests[
            "generated_klean_tree_digest"
        ]
        == digests["generated_expected_audit_input"],
        "generation_tree_matches_audit_input": digests[
            "generation_pipeline_sha256"
        ]
        == digests["generation_expected_audit_input"],
    }
)

print(
    json.dumps(
        {
            "observed_files": observed_files,
            "observed_hashes": observed_hashes,
            "expected_hashes": expected_hashes,
            "image_ids": image_ids,
            "digests": digests,
            "checks": checks,
        },
        indent=2,
        sort_keys=True,
    )
)
if not all(checks.values()):
    raise SystemExit(1)
PY
