#!/usr/bin/env python3
"""Read-only recomputation of hashes bound into the Stage 6 audit input."""

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
LOCK = Path("/reference/klean-toolchain.lock.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(document)
checks: dict[str, dict[str, object]] = {}


def check(name: str, observed: object, expected: object) -> None:
    checks[name] = {
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }


hashes = resolution["hashes"]
check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
check(
    "resolved_input_sha256",
    resolved_digest,
    document["resolved_input_sha256"],
)
check(
    "k_workspace_sha256",
    pipeline_contract.sha256_tree(K_PROOF),
    hashes["k_workspace_sha256"],
)
check(
    "stage1_export_sha256",
    klean_export.tree_digest(K_PROOF),
    hashes["stage1_export_sha256"],
)
check(
    "discovery_manifest_sha256",
    file_sha256(DISCOVERY),
    hashes["discovery_manifest_sha256"],
)
check(
    "k_audit_sha256",
    pipeline_contract.sha256_tree(K_AUDIT),
    hashes["k_audit_sha256"],
)
check(
    "klean_generation_sha256",
    pipeline_contract.sha256_tree(GENERATION),
    hashes["klean_generation_sha256"],
)
check(
    "generation_producer_sources_sha256",
    pipeline_contract.sha256_tree(PRODUCERS),
    hashes["generation_producer_sources_sha256"],
)
check(
    "generated_tree_sha256",
    klean_export.tree_digest(GENERATED),
    hashes["generated_tree_sha256"],
)
check("lean_workspace_sha256", None, hashes["lean_workspace_sha256"])
check("lean_invocation_sha256", None, hashes["lean_invocation_sha256"])

observed_sources = {
    path.relative_to(K_PROOF).as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        K_PROOF, "Stage 1 source workspace"
    )
}
check(
    "stage1_source_hashes",
    observed_sources,
    resolution["stage1_source_hashes"],
)

generator = json.loads((GENERATION / "generator-manifest.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
recorded_preflight = json.loads((GENERATION / "preflight.json").read_text())
trust_inventory = GENERATION / "trust-inventory.json"
obligation_map = GENERATED / "obligation-map.json"

check(
    "producer_klean_export.py",
    file_sha256(PRODUCERS / "klean_export.py"),
    generator["exporter_sha256"],
)
check(
    "producer_klean.py",
    file_sha256(PRODUCERS / "klean.py"),
    generator["klean_py_sha256"],
)
check(
    "source_manifest_files",
    source_manifest["files"],
    {
        "klean.py": generator["klean_py_sha256"],
        "klean_export.py": generator["exporter_sha256"],
    },
)
check(
    "producer_image_id",
    source_manifest["generator_image_id"],
    generator["provenance"]["generator_image_id"],
)
check(
    "producer_image_id_audit_path",
    Path(resolution["generation_producer_sources"]).name,
    generator["provenance"]["generator_image_id"].removeprefix("sha256:"),
)
check(
    "generator_generated_tree",
    generator["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)
check(
    "generator_stage1",
    generator["provenance"]["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "generator_stage3",
    generator["provenance"]["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check(
    "input_manifest_stage1",
    input_manifest["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "input_manifest_frozen",
    input_manifest["frozen_input_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "input_manifest_stage3",
    input_manifest["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check(
    "generator_input_inventory",
    generator["provenance"]["inventory_sha256"],
    input_manifest["inventory_sha256"],
)
check("generator_toolchain_lock", generator["toolchain"], json.loads(LOCK.read_text()))
check(
    "obligation_map_sha256",
    file_sha256(obligation_map),
    generator["obligation_map_sha256"],
)
check(
    "export_trust_inventory_sha256",
    export_result["trust_inventory_sha256"],
    file_sha256(trust_inventory),
)
check(
    "audit_recorded_preflight",
    resolution["stage4_preflight"],
    recorded_preflight,
)
check(
    "stage4_selection_hash",
    resolution["selections"]["klean_generation"]["artifact_sha256"],
    hashes["klean_generation_sha256"],
)
check(
    "stage2_selection_hash",
    resolution["selections"]["k_audit"]["artifact_sha256"],
    hashes["k_audit_sha256"],
)
check(
    "classification_only_no_target",
    (resolution["target"], generator["target"], recorded_preflight["target"]),
    (None, None, None),
)

candidate = Path("/candidate")
candidate_files = (
    [p.relative_to(candidate).as_posix() for p in candidate.rglob("*") if p.is_file()]
    if candidate.is_dir()
    else []
)
check("classification_only_no_candidate_files", candidate_files, [])

result = {
    "all_match": all(item["match"] for item in checks.values()),
    "checks": checks,
}
print(json.dumps(result, indent=2, sort_keys=True))
