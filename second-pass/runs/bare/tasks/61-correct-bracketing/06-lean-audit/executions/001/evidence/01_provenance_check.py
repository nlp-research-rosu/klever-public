#!/usr/bin/env python3
"""Independent hash and audit-input checks using the trusted reference tools."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


document = json.loads(AUDIT_INPUT.read_text())
resolution, signed_digest = stage6_resolution_contract.verify_audit_input(document)
print(f"audit_input_envelope=PASS")
print(f"resolved_input_sha256={signed_digest}")
print(f"AUDIT_MODE={os.environ.get('AUDIT_MODE')}")
print(f"recorded_mode={resolution['mode']}")
assert os.environ.get("AUDIT_MODE") == resolution["mode"]

actual_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
    "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
    "discovery_manifest_sha256": file_sha256(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
for name, actual in actual_hashes.items():
    expected = resolution["hashes"][name]
    print(f"{name}: expected={expected} actual={actual} match={expected == actual}")
    assert expected == actual

for relative, expected in sorted(resolution["stage1_source_hashes"].items()):
    source = K_PROOF / relative
    actual = file_sha256(source)
    print(
        f"stage1_source_hash[{relative}]: "
        f"expected={expected} actual={actual} match={expected == actual}"
    )
    assert expected == actual

assert resolution["selections"]["k_audit"]["artifact_sha256"] == actual_hashes[
    "k_audit_sha256"
]
assert resolution["selections"]["klean_generation"][
    "artifact_sha256"
] == actual_hashes["klean_generation_sha256"]
print("selected_artifact_hashes=PASS")

generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
image_id = generator_manifest["provenance"]["generator_image_id"]
image_key = image_id.removeprefix("sha256:")
recorded_producer_key = Path(
    resolution["generation_producer_sources"]
).name
print(f"generator_manifest_image_id={image_id}")
print(f"source_manifest_image_id={source_manifest['generator_image_id']}")
print(f"audit_input_producer_path_key={recorded_producer_key}")
assert source_manifest["generator_image_id"] == image_id
assert recorded_producer_key == image_key

expected_producer_files = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
assert source_manifest == {
    "schema_version": 1,
    "generator_image_id": image_id,
    "files": expected_producer_files,
}
observed_names = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in PRODUCERS.iterdir()
)
print(f"producer_bundle_entries={observed_names}")
assert observed_names == ["klean.py", "klean_export.py", "source-manifest.json"]
for name, expected in expected_producer_files.items():
    source = PRODUCERS / name
    assert source.is_file() and not source.is_symlink()
    actual = file_sha256(source)
    print(
        f"producer_hash[{name}]: expected={expected} "
        f"source_manifest={source_manifest['files'][name]} actual={actual} "
        f"match={expected == actual}"
    )
    assert expected == source_manifest["files"][name] == actual
print("producer_source_gate=PASS")

recorded_preflight = json.loads((GENERATION / "preflight.json").read_text())
assert resolution["stage4_preflight"] == recorded_preflight
print("embedded_stage4_preflight_exact_match=PASS")

candidate = Path("/candidate")
assert not candidate.exists()
assert resolution["lean_workspace"] is None
assert resolution["lean_invocation"] is None
assert resolution["stage5_result"] is None
assert resolution["target"] is None
print("classification_only_candidate_absence=PASS")
print("OVERALL=PASS")
