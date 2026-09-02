#!/usr/bin/env python3
"""Read-only cross-check of the launcher, Stage 3, and Stage 4 hashes."""

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


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{label}: {status}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if observed != expected:
        raise SystemExit(f"hash/provenance audit failed at {label}")


document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    document
)
print(f"audit-input-envelope: VALID ({resolved_digest})")
check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])

recorded_hashes = resolution["hashes"]
check(
    "k_workspace_sha256",
    pipeline_contract.sha256_tree(K_WORKSPACE),
    recorded_hashes["k_workspace_sha256"],
)
check(
    "stage1_export_sha256",
    klean_export.tree_digest(K_WORKSPACE),
    recorded_hashes["stage1_export_sha256"],
)
check(
    "discovery_manifest_sha256",
    file_sha256(DISCOVERY),
    recorded_hashes["discovery_manifest_sha256"],
)
check(
    "k_audit_sha256",
    pipeline_contract.sha256_tree(K_AUDIT),
    recorded_hashes["k_audit_sha256"],
)
check(
    "klean_generation_sha256",
    pipeline_contract.sha256_tree(GENERATION),
    recorded_hashes["klean_generation_sha256"],
)
check(
    "generation_producer_sources_sha256",
    pipeline_contract.sha256_tree(PRODUCERS),
    recorded_hashes["generation_producer_sources_sha256"],
)
check(
    "generated_tree_sha256",
    klean_export.tree_digest(GENERATED),
    recorded_hashes["generated_tree_sha256"],
)

observed_stage1_sources = {
    path.relative_to(K_WORKSPACE).as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        K_WORKSPACE, "mounted Stage 1 workspace"
    )
}
check(
    "stage1_source_hashes",
    observed_stage1_sources,
    resolution["stage1_source_hashes"],
)

generator = json.loads((GENERATION / "generator-manifest.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
discovery_document = json.loads(DISCOVERY.read_text())

producer_hashes = {
    "klean_export.py": file_sha256(PRODUCERS / "klean_export.py"),
    "klean.py": file_sha256(PRODUCERS / "klean.py"),
}
check("producer source-manifest hashes", producer_hashes, source_manifest["files"])
check(
    "producer exporter hash",
    producer_hashes["klean_export.py"],
    generator["exporter_sha256"],
)
check(
    "producer klean.py hash",
    producer_hashes["klean.py"],
    generator["klean_py_sha256"],
)
check(
    "producer generator image ID",
    source_manifest["generator_image_id"],
    generator["provenance"]["generator_image_id"],
)
image_hex = generator["provenance"]["generator_image_id"].removeprefix("sha256:")
check(
    "audit-input producer path image key",
    Path(resolution["generation_producer_sources"]).name,
    image_hex,
)

check(
    "generator generated tree",
    generator["generated_tree_sha256"],
    recorded_hashes["generated_tree_sha256"],
)
check(
    "generator Stage 1 provenance",
    generator["provenance"]["stage1_workspace_sha256"],
    recorded_hashes["stage1_export_sha256"],
)
check(
    "generator Stage 3 provenance",
    generator["provenance"]["stage3_discovery_manifest_sha256"],
    recorded_hashes["discovery_manifest_sha256"],
)
check(
    "generator inventory provenance",
    generator["provenance"]["inventory_sha256"],
    discovery_document["inventory_sha256"],
)
check(
    "input manifest inventory",
    input_manifest["inventory_sha256"],
    discovery_document["inventory_sha256"],
)
check(
    "input manifest verification hash",
    input_manifest["verification_sha256"],
    file_sha256(K_WORKSPACE / "verification.k"),
)
check(
    "input manifest source rules",
    input_manifest["source_rules"],
    [],
)
check("generator target", generator["target"], resolution["target"])
check("generator obligation count", generator["obligation_count"], 0)
check("candidate absence", Path("/candidate").exists(), False)

verification_lines = (K_WORKSPACE / "verification.k").read_text().splitlines()
rule_text = "\n".join(verification_lines[9:16])
normalized_hash = hashlib.sha256(" ".join(rule_text.split()).encode()).hexdigest()
rule = discovery_document["rules"][0]
check("manual source span start", rule["source_rule_id"], f"rule-{normalized_hash}")
check(
    "manual normalized source hash",
    normalized_hash,
    "c3ab2878674aa2f645784b82238d257700a7250a3ecf4a8047ddb95328b1fdc9",
)

print("ALL HASH AND PROVENANCE CHECKS PASSED")
