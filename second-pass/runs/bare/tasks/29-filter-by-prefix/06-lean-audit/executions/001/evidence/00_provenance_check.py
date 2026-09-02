#!/usr/bin/env python3
"""Independent hash and producer-provenance checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_audit_contract, klean_export, pipeline_contract


def load(path: str) -> dict:
    value = json.loads(Path(path).read_text())
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = load("/audit-input.json")
resolution, resolved_hash = klean_audit_contract.verify_stage6_audit_input(
    audit_input
)
assert resolved_hash == audit_input["resolved_input_sha256"]
assert os.environ.get("AUDIT_MODE") == resolution["mode"]
assert resolution["mode"] == "CLASSIFICATION_ONLY"
assert resolution["target"] is None
assert resolution["stage5_result"] is None
assert resolution["lean_workspace"] is None
assert resolution["lean_invocation"] is None
assert not Path("/candidate").exists()

generator = load("/reference/klean-generation/generator-manifest.json")
source_manifest = load("/reference/generation-tools/source-manifest.json")
provenance = generator["provenance"]
image_id = provenance["generator_image_id"]
expected_files = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
assert source_manifest == {
    "schema_version": 1,
    "generator_image_id": image_id,
    "files": expected_files,
}
recorded_source_path = Path(resolution["generation_producer_sources"])
assert recorded_source_path.name == image_id.removeprefix("sha256:")
observed_files = sorted(
    path.relative_to("/reference/generation-tools").as_posix()
    for path in Path("/reference/generation-tools").iterdir()
)
assert observed_files == ["klean.py", "klean_export.py", "source-manifest.json"]
for name, expected in expected_files.items():
    assert sha256(Path("/reference/generation-tools") / name) == expected

hashes = resolution["hashes"]
observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": sha256(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
assert observed_hashes == hashes

stage1_files = {
    path.relative_to("/reference/k-proof").as_posix(): sha256(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
assert stage1_files == resolution["stage1_source_hashes"]
assert sha256(Path("/reference/k-proof/verification.k")) == (
    resolution["stage1_source_hashes"]["verification.k"]
)
assert generator["generated_tree_sha256"] == hashes["generated_tree_sha256"]

print(
    json.dumps(
        {
            "status": "PASS",
            "audit_mode": resolution["mode"],
            "resolved_input_sha256": resolved_hash,
            "generator_image_id": image_id,
            "producer_files": expected_files,
            "observed_hashes": observed_hashes,
            "stage1_source_hashes": stage1_files,
            "candidate_present": Path("/candidate").exists(),
        },
        indent=2,
        sort_keys=True,
    )
)
