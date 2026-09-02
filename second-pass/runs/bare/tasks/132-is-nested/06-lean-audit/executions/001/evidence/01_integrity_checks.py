#!/usr/bin/env python3
"""Independent hash and provenance checks for the mounted Stage 3/4 inputs."""

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
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def emit(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{label}: {status}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")


document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(document)
print("audit input envelope: VALID")
emit("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
emit(
    "resolved_input_sha256",
    stage6_resolution_contract.canonical_json_sha256(resolution),
    resolved_digest,
)

source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
toolchain_lock = json.loads(TOOLCHAIN_LOCK.read_text())

producer_expected = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
emit("producer manifest file map", source_manifest["files"], producer_expected)
for name, expected in producer_expected.items():
    observed = sha256_file(PRODUCERS / name)
    emit(f"producer file {name} vs generator-manifest", observed, expected)
    emit(f"producer file {name} vs source-manifest", observed, source_manifest["files"][name])

generator_image_id = generator_manifest["provenance"]["generator_image_id"]
emit("generator image IDs", source_manifest["generator_image_id"], generator_image_id)
emit(
    "generator image ID vs audit-input source-path basename",
    generator_image_id.removeprefix("sha256:"),
    Path(resolution["generation_producer_sources"]).name,
)
emit(
    "generation_producer_sources_sha256",
    pipeline_contract.sha256_tree(PRODUCERS),
    resolution["hashes"]["generation_producer_sources_sha256"],
)

emit(
    "k_workspace_sha256",
    pipeline_contract.sha256_tree(K_PROOF),
    resolution["hashes"]["k_workspace_sha256"],
)
emit(
    "stage1_export_sha256",
    klean_export.tree_digest(K_PROOF),
    resolution["hashes"]["stage1_export_sha256"],
)
emit(
    "k_audit_sha256",
    pipeline_contract.sha256_tree(K_AUDIT),
    resolution["hashes"]["k_audit_sha256"],
)
emit(
    "klean_generation_sha256",
    pipeline_contract.sha256_tree(GENERATION),
    resolution["hashes"]["klean_generation_sha256"],
)
emit(
    "generated_tree_sha256",
    klean_export.tree_digest(GENERATED),
    resolution["hashes"]["generated_tree_sha256"],
)
emit(
    "discovery_manifest_sha256",
    sha256_file(DISCOVERY),
    resolution["hashes"]["discovery_manifest_sha256"],
)
emit(
    "selected k-audit artifact_sha256",
    resolution["hashes"]["k_audit_sha256"],
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
emit(
    "selected generation artifact_sha256",
    resolution["hashes"]["klean_generation_sha256"],
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)

observed_stage1_sources = {
    path.relative_to(K_PROOF).as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(K_PROOF, "Stage 1 workspace")
}
emit("stage1_source_hashes", observed_stage1_sources, resolution["stage1_source_hashes"])

stage1_export = klean_export.tree_digest(K_PROOF)
discovery_hash = sha256_file(DISCOVERY)
generated_hash = klean_export.tree_digest(GENERATED)
emit("input-manifest frozen_input_sha256", input_manifest["frozen_input_sha256"], stage1_export)
emit("input-manifest stage1_workspace_sha256", input_manifest["stage1_workspace_sha256"], stage1_export)
emit(
    "input-manifest discovery hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    discovery_hash,
)
emit(
    "generator provenance Stage 1 hash",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    stage1_export,
)
emit(
    "generator provenance Stage 3 hash",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    discovery_hash,
)
emit("generator generated tree hash", generator_manifest["generated_tree_sha256"], generated_hash)
emit("generator toolchain lock", generator_manifest["toolchain"], toolchain_lock)

emit("preflight frozen input hash", preflight["frozen_input_sha256"], stage1_export)
emit("preflight Stage 1 hash", preflight["stage1_workspace_sha256"], stage1_export)
emit("preflight Stage 3 hash", preflight["stage3_discovery_manifest_sha256"], discovery_hash)
emit("preflight generated tree hash", preflight["generated_tree_sha256"], generated_hash)
emit(
    "audit-input embedded preflight",
    resolution["stage4_preflight"],
    preflight,
)
emit("export frozen input hash", export_result["frozen_input_sha256"], stage1_export)
emit("export Stage 3 hash", export_result["stage3_discovery_manifest_sha256"], discovery_hash)
emit("export generated tree hash", export_result["generated_tree_sha256"], generated_hash)

emit("audit-input mode selected from status", resolution["mode"], "CLASSIFICATION_ONLY")
emit("audit-input target", resolution["target"], None)
emit("generator target", generator_manifest["target"], None)
emit("mechanically parsed generated target", klean_export.target_statement(GENERATED), None)
emit("audit-input Stage 5 result", resolution["stage5_result"], None)
emit("audit-input Lean workspace hash", resolution["hashes"]["lean_workspace_sha256"], None)
emit("audit-input Lean invocation hash", resolution["hashes"]["lean_invocation_sha256"], None)
print(f"/candidate exists: {Path('/candidate').exists()}")
