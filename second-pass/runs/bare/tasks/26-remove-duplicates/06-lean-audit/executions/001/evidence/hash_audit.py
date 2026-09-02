#!/usr/bin/env python3
"""Independent hash/provenance comparison for the mounted audit inputs."""

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


def check(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{status}: {label}")
    print(f"  observed: {observed}")
    print(f"  expected: {expected}")
    if status != "MATCH":
        raise SystemExit(1)


document = json.loads(AUDIT_INPUT.read_bytes())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    document
)
print(f"MATCH: signed audit-input envelope ({resolved_digest})")

check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
check(
    "AUDIT_PROBLEM_ID",
    os.environ.get("AUDIT_PROBLEM_ID"),
    resolution["problem_id"],
)
check(
    "AUDIT_CONDITION",
    os.environ.get("AUDIT_CONDITION"),
    resolution["condition"],
)
check(
    "AUDIT_SEMANTICS_MODE",
    os.environ.get("AUDIT_SEMANTICS_MODE"),
    resolution["semantics_mode"],
)

hashes = resolution["hashes"]
check(
    "Stage 1 pipeline tree",
    pipeline_contract.sha256_tree(K_PROOF),
    hashes["k_workspace_sha256"],
)
check(
    "Stage 1 deterministic-export tree",
    klean_export.tree_digest(K_PROOF),
    hashes["stage1_export_sha256"],
)
check(
    "Stage 2 selected-audit tree",
    pipeline_contract.sha256_tree(K_AUDIT),
    hashes["k_audit_sha256"],
)
check(
    "Stage 3 discovery file",
    file_sha256(DISCOVERY),
    hashes["discovery_manifest_sha256"],
)
check(
    "Stage 4 selected-generation tree",
    pipeline_contract.sha256_tree(GENERATION),
    hashes["klean_generation_sha256"],
)
check(
    "Stage 4 generated-project tree",
    klean_export.tree_digest(GENERATED),
    hashes["generated_tree_sha256"],
)
check(
    "producer-source bundle tree",
    pipeline_contract.sha256_tree(PRODUCERS),
    hashes["generation_producer_sources_sha256"],
)
check("Lean workspace absent hash", None, hashes["lean_workspace_sha256"])
check("Lean invocation absent hash", None, hashes["lean_invocation_sha256"])

observed_stage1_files = {
    path.relative_to(K_PROOF).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        K_PROOF, "mounted Stage 1 source workspace"
    )
}
check(
    "all Stage 1 source-file hashes",
    observed_stage1_files,
    resolution["stage1_source_hashes"],
)

source_manifest = json.loads(
    (PRODUCERS / "source-manifest.json").read_bytes()
)
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_bytes()
)
image_id = generator_manifest["provenance"]["generator_image_id"]
check(
    "producer source manifest image ID",
    source_manifest["generator_image_id"],
    image_id,
)
check(
    "audit-input producer path image ID",
    Path(resolution["generation_producer_sources"]).name,
    image_id.removeprefix("sha256:"),
)
check(
    "producer source manifest exact file set",
    sorted(source_manifest["files"]),
    ["klean.py", "klean_export.py"],
)
check(
    "klean_export.py producer hash",
    file_sha256(PRODUCERS / "klean_export.py"),
    generator_manifest["exporter_sha256"],
)
check(
    "klean.py producer hash",
    file_sha256(PRODUCERS / "klean.py"),
    generator_manifest["klean_py_sha256"],
)
check(
    "source-manifest klean_export.py hash",
    source_manifest["files"]["klean_export.py"],
    generator_manifest["exporter_sha256"],
)
check(
    "source-manifest klean.py hash",
    source_manifest["files"]["klean.py"],
    generator_manifest["klean_py_sha256"],
)

input_manifest = json.loads((GENERATION / "input-manifest.json").read_bytes())
check(
    "input-manifest Stage 1 tree",
    input_manifest["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "input-manifest frozen tree",
    input_manifest["frozen_input_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "input-manifest Stage 3 discovery",
    input_manifest["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check(
    "input-manifest verification.k",
    input_manifest["verification_sha256"],
    resolution["stage1_source_hashes"]["verification.k"],
)
check(
    "generator provenance Stage 1",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "generator provenance Stage 3",
    generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ],
    hashes["discovery_manifest_sha256"],
)
check(
    "generator generated-project hash",
    generator_manifest["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)
check(
    "generator toolchain lock",
    generator_manifest["toolchain"],
    json.loads(Path("/reference/klean-toolchain.lock.json").read_bytes()),
)

preflight = resolution["stage4_preflight"]
check(
    "signed preflight Stage 1",
    preflight["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "signed preflight Stage 3",
    preflight["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check(
    "signed preflight generated tree",
    preflight["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)

print("PASS: all launcher-recorded mounted-input hashes and producer bindings match")
