#!/usr/bin/env python3
"""Recompute immutable-input, producer, tree, and manifest bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_audit_contract, klean_export, pipeline_contract


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK = Path("/reference/klean-toolchain.lock.json")


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, verified_input_hash = klean_audit_contract.verify_stage6_audit_input(
    audit_document
)
hashes = resolution["hashes"]
generator = json.loads((GENERATION / "generator-manifest.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
lock = json.loads(LOCK.read_text())

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "discovery_manifest_sha256": file_hash(DISCOVERY),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
}

print("audit_input_verified_sha256:", verified_input_hash)
print("audit_input_recorded_sha256:", audit_document["resolved_input_sha256"])
assert verified_input_hash == audit_document["resolved_input_sha256"]

for name, digest in observed.items():
    print(f"{name}: {digest}")
    print(f"{name}_recorded: {hashes[name]}")
    assert digest == hashes[name], f"mismatch: {name}"

for relative, expected in resolution["stage1_source_hashes"].items():
    actual = file_hash(K_WORKSPACE / relative)
    print(f"stage1_source {relative}: {actual}")
    assert actual == expected, f"Stage 1 source mismatch: {relative}"

producer_files = {
    path.relative_to(PRODUCERS).as_posix()
    for path in PRODUCERS.iterdir()
    if path.is_file()
}
assert producer_files == {
    "klean.py",
    "klean_export.py",
    "source-manifest.json",
}
assert set(source_manifest) == {"schema_version", "generator_image_id", "files"}
assert source_manifest["schema_version"] == 1
assert source_manifest["files"] == {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
for producer_name, expected in source_manifest["files"].items():
    actual = file_hash(PRODUCERS / producer_name)
    print(f"producer {producer_name}: {actual}")
    print(f"producer {producer_name} recorded: {expected}")
    assert actual == expected

generator_image_id = generator["provenance"]["generator_image_id"]
print("generator_image_id:", generator_image_id)
print("source_manifest_image_id:", source_manifest["generator_image_id"])
print(
    "audit_input_producer_path_id:",
    Path(resolution["generation_producer_sources"]).name,
)
assert source_manifest["generator_image_id"] == generator_image_id
assert Path(resolution["generation_producer_sources"]).name == (
    generator_image_id.removeprefix("sha256:")
)

assert generator["toolchain"] == lock
assert generator["generated_tree_sha256"] == observed["generated_tree_sha256"]
assert (
    generator["provenance"]["stage1_workspace_sha256"]
    == observed["stage1_export_sha256"]
)
assert (
    generator["provenance"]["stage3_discovery_manifest_sha256"]
    == observed["discovery_manifest_sha256"]
)
assert input_manifest["frozen_input_sha256"] == observed["stage1_export_sha256"]
assert (
    input_manifest["stage1_workspace_sha256"]
    == observed["stage1_export_sha256"]
)
assert (
    input_manifest["stage3_discovery_manifest_sha256"]
    == observed["discovery_manifest_sha256"]
)
assert preflight == resolution["stage4_preflight"]
assert resolution["mode"] == "CLASSIFICATION_ONLY"
assert resolution["target"] is None
assert resolution["stage5_result"] is None
assert resolution["lean_workspace"] is None
assert resolution["lean_invocation"] is None
assert not Path("/candidate").exists()

print("toolchain_lock_match: true")
print("stage4_preflight_matches_audit_input: true")
print("classification_only_absence_checks: true")
print("RESULT: PASS")
