#!/usr/bin/env python3
"""Reviewer-authored, read-only recomputation of Stage 6 input hashes."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input_path = Path("/audit-input.json")
document = json.loads(audit_input_path.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(document)
print(f"audit_input_contract=PASS resolved_input_sha256={resolved_digest}")
print(f"env_AUDIT_MODE={os.environ.get('AUDIT_MODE')}")
print(f"recorded_mode={resolution['mode']}")
print(f"mode_match={os.environ.get('AUDIT_MODE') == resolution['mode']}")

checks = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": sha256(Path("/reference/lemma-discovery.json")),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
}
for name, observed in checks.items():
    expected = resolution["hashes"][name]
    print(
        f"{name}: expected={expected} observed={observed} "
        f"match={expected == observed}"
    )

workspace = Path("/reference/k-proof")
observed_sources = {
    path.relative_to(workspace).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "mounted Stage 1 source workspace"
    )
}
expected_sources = resolution["stage1_source_hashes"]
missing = sorted(set(expected_sources) - set(observed_sources))
extra = sorted(set(observed_sources) - set(expected_sources))
mismatched = sorted(
    name
    for name in set(expected_sources) & set(observed_sources)
    if expected_sources[name] != observed_sources[name]
)
print(f"stage1_source_hash_count_expected={len(expected_sources)}")
print(f"stage1_source_hash_count_observed={len(observed_sources)}")
print(f"stage1_source_missing={json.dumps(missing)}")
print(f"stage1_source_extra={json.dumps(extra)}")
print(f"stage1_source_mismatched={json.dumps(mismatched)}")

generation_tools = Path("/reference/generation-tools")
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads((generation_tools / "source-manifest.json").read_text())
producer_names = sorted(
    path.relative_to(generation_tools).as_posix()
    for path in pipeline_contract._walk_regular_files(
        generation_tools, "mounted Stage 4 producer source bundle"
    )
)
expected_names = ["klean.py", "klean_export.py", "source-manifest.json"]
image_id = generator_manifest["provenance"]["generator_image_id"]
path_image_key = Path(resolution["generation_producer_sources"]).name
print(f"producer_file_set={producer_names}")
print(f"producer_file_set_exact={producer_names == expected_names}")
print(f"generator_image_id={image_id}")
print(f"source_manifest_image_id={source_manifest.get('generator_image_id')}")
print(f"audit_input_image_key={path_image_key}")
print(
    "generator_image_identity_match="
    f"{source_manifest.get('generator_image_id') == image_id and image_id == 'sha256:' + path_image_key}"
)
producer_hashes = {
    "klean_export.py": sha256(generation_tools / "klean_export.py"),
    "klean.py": sha256(generation_tools / "klean.py"),
}
for name, observed in producer_hashes.items():
    manifest_field = "exporter_sha256" if name == "klean_export.py" else "klean_py_sha256"
    generator_expected = generator_manifest[manifest_field]
    source_expected = source_manifest["files"][name]
    print(
        f"producer_{name}: observed={observed} generator={generator_expected} "
        f"source_manifest={source_expected} "
        f"match={observed == generator_expected == source_expected}"
    )

all_hashes_match = all(
    observed == resolution["hashes"][name] for name, observed in checks.items()
)
all_sources_match = not missing and not extra and not mismatched
print(f"all_recorded_hashes_match={all_hashes_match}")
print(f"all_stage1_source_hashes_match={all_sources_match}")
