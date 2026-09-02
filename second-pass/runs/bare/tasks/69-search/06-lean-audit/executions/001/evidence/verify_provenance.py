#!/usr/bin/env python3
"""Recompute the launcher, source, producer, and generated-artifact hashes."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(label: str, condition: bool) -> None:
    if not condition:
        raise SystemExit(f"MISMATCH: {label}")
    print(f"MATCH: {label}")


audit_document = json.loads(AUDIT_INPUT.read_bytes())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
generator = json.loads((GENERATION / "generator-manifest.json").read_bytes())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_bytes())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_bytes())
export_result = json.loads((GENERATION / "export-result.json").read_bytes())
preflight = json.loads((GENERATION / "preflight.json").read_bytes())
trust_inventory = GENERATION / "trust-inventory.json"
obligation_map = GENERATED / "obligation-map.json"
lock = json.loads(TOOLCHAIN_LOCK.read_bytes())

require(
    "AUDIT_MODE equals signed resolution mode",
    os.environ.get("AUDIT_MODE") == resolution["mode"] == "CLASSIFICATION_ONLY",
)
require(
    "signed resolution canonical digest",
    resolved_digest == audit_document["resolved_input_sha256"],
)
require("problem ID", resolution["problem_id"] == "69-search")
require("condition", resolution["condition"] == "bare")
require(
    "semantics mode",
    resolution["semantics_mode"] == "GENERATED_SEMANTICS",
)

observed_pipeline_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        PRODUCERS
    ),
}
for key, observed in observed_pipeline_hashes.items():
    require(
        f"audit-input {key}",
        observed == resolution["hashes"][key],
    )

stage1_export_hash = klean_export.tree_digest(K_WORKSPACE)
generated_tree_hash = klean_export.tree_digest(GENERATED)
discovery_hash = sha256(DISCOVERY)
require(
    "Stage 1 export tree hash across audit/input/generator",
    stage1_export_hash
    == resolution["hashes"]["stage1_export_sha256"]
    == input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == generator["provenance"]["stage1_workspace_sha256"]
    == preflight["stage1_workspace_sha256"]
    == preflight["frozen_input_sha256"]
    == export_result["frozen_input_sha256"],
)
require(
    "Stage 3 manifest hash across audit/input/generator",
    discovery_hash
    == resolution["hashes"]["discovery_manifest_sha256"]
    == input_manifest["stage3_discovery_manifest_sha256"]
    == generator["provenance"]["stage3_discovery_manifest_sha256"]
    == preflight["stage3_discovery_manifest_sha256"]
    == export_result["stage3_discovery_manifest_sha256"],
)
require(
    "generated project tree hash across audit/generator/preflight/export",
    generated_tree_hash
    == resolution["hashes"]["generated_tree_sha256"]
    == generator["generated_tree_sha256"]
    == preflight["generated_tree_sha256"]
    == export_result["generated_tree_sha256"],
)
require(
    "trust inventory hash in export result",
    sha256(trust_inventory) == export_result["trust_inventory_sha256"],
)
require(
    "obligation map hash in generator manifest",
    sha256(obligation_map) == generator["obligation_map_sha256"],
)
require("pinned toolchain manifest", generator["toolchain"] == lock)
require(
    "selected K audit artifact hash",
    resolution["selections"]["k_audit"]["artifact_sha256"]
    == resolution["hashes"]["k_audit_sha256"],
)
require(
    "selected Klean generation artifact hash",
    resolution["selections"]["klean_generation"]["artifact_sha256"]
    == resolution["hashes"]["klean_generation_sha256"],
)
require(
    "signed Stage 4 preflight is byte-for-byte JSON-equivalent",
    resolution["stage4_preflight"] == preflight,
)

observed_stage1_sources = {
    path.relative_to(K_WORKSPACE).as_posix(): sha256(path)
    for path in sorted(K_WORKSPACE.rglob("*"))
    if path.is_file() and not path.is_symlink()
}
require(
    "complete Stage 1 per-file source hash map",
    observed_stage1_sources == resolution["stage1_source_hashes"],
)

producer_hashes = {
    "klean_export.py": sha256(PRODUCERS / "klean_export.py"),
    "klean.py": sha256(PRODUCERS / "klean.py"),
}
expected_producer_hashes = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
require(
    "producer file hashes match generator manifest",
    producer_hashes == expected_producer_hashes,
)
require(
    "producer file hashes match source manifest",
    producer_hashes == source_manifest["files"],
)
generator_image_id = generator["provenance"]["generator_image_id"]
require(
    "generator image ID matches source manifest",
    generator_image_id == source_manifest["generator_image_id"],
)
require(
    "generator image ID matches audit-input producer path",
    generator_image_id.removeprefix("sha256:")
    == Path(resolution["generation_producer_sources"]).name,
)
require(
    "producer bundle contains exactly the immutable expected files",
    sorted(path.name for path in PRODUCERS.iterdir())
    == ["klean.py", "klean_export.py", "source-manifest.json"],
)
require(
    "producer source manifest has exact schema",
    set(source_manifest)
    == {"schema_version", "generator_image_id", "files"}
    and source_manifest["schema_version"] == 1,
)

require(
    "no-obligation target identity",
    resolution["target"] is None
    and generator["target"] is None
    and preflight["target"] is None,
)
require(
    "no Stage 5 inputs in classification-only mode",
    resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["hashes"]["lean_workspace_sha256"] is None
    and resolution["hashes"]["lean_invocation_sha256"] is None
    and resolution["stage5_result"] is None
    and not Path("/candidate").exists(),
)

print(
    json.dumps(
        {
            "producer_file_sha256": producer_hashes,
            "producer_bundle_pipeline_sha256": observed_pipeline_hashes[
                "generation_producer_sources_sha256"
            ],
            "generator_image_id": generator_image_id,
            "stage1_pipeline_sha256": observed_pipeline_hashes[
                "k_workspace_sha256"
            ],
            "stage1_export_sha256": stage1_export_hash,
            "stage3_manifest_sha256": discovery_hash,
            "generated_tree_sha256": generated_tree_hash,
            "generation_pipeline_sha256": observed_pipeline_hashes[
                "klean_generation_sha256"
            ],
            "resolved_input_sha256": resolved_digest,
        },
        indent=2,
        sort_keys=True,
    )
)
