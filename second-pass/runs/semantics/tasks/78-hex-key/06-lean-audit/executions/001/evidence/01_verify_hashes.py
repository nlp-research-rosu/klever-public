#!/usr/bin/env python3
"""Independent hash and provenance checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.stage6_resolution_contract import verify_audit_input


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


failures: list[str] = []


def check(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{status}: {label}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if observed != expected:
        failures.append(label)


audit_path = Path("/audit-input.json")
audit_document = json.loads(audit_path.read_text())
resolution, resolved_digest = verify_audit_input(audit_document)
print(f"PASS: audit-input envelope and resolved digest {resolved_digest}")
check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("problem", resolution["problem_id"], "78-hex-key")
check("condition", resolution["condition"], "semantics")
check("semantics mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")

proof = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")
discovery_path = Path("/reference/lemma-discovery.json")

generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
source_manifest = json.loads((producer / "source-manifest.json").read_text())
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
stored_preflight = json.loads((generation / "preflight.json").read_text())

producer_hashes = {
    name: sha256_file(producer / name)
    for name in ("klean_export.py", "klean.py")
}
check(
    "producer klean_export.py hash vs source manifest",
    producer_hashes["klean_export.py"],
    source_manifest["files"]["klean_export.py"],
)
check(
    "producer klean.py hash vs source manifest",
    producer_hashes["klean.py"],
    source_manifest["files"]["klean.py"],
)
check(
    "producer klean_export.py hash vs generator manifest",
    producer_hashes["klean_export.py"],
    generator_manifest["exporter_sha256"],
)
check(
    "producer klean.py hash vs generator manifest",
    producer_hashes["klean.py"],
    generator_manifest["klean_py_sha256"],
)

image_id = source_manifest["generator_image_id"]
check(
    "immutable image ID vs generator manifest",
    image_id,
    generator_manifest["provenance"]["generator_image_id"],
)
check(
    "immutable image ID vs audit-input producer path",
    image_id.removeprefix("sha256:"),
    Path(resolution["generation_producer_sources"]).name,
)

tree_checks = (
    (
        "Stage 1 pipeline tree",
        pipeline_contract.sha256_tree(proof),
        resolution["hashes"]["k_workspace_sha256"],
    ),
    (
        "Stage 1 export tree",
        klean_export.tree_digest(proof),
        resolution["hashes"]["stage1_export_sha256"],
    ),
    (
        "Stage 2 audit tree",
        pipeline_contract.sha256_tree(k_audit),
        resolution["hashes"]["k_audit_sha256"],
    ),
    (
        "Stage 4 generation tree",
        pipeline_contract.sha256_tree(generation),
        resolution["hashes"]["klean_generation_sha256"],
    ),
    (
        "producer source tree",
        pipeline_contract.sha256_tree(producer),
        resolution["hashes"]["generation_producer_sources_sha256"],
    ),
    (
        "generated Lean tree",
        klean_export.tree_digest(generated),
        resolution["hashes"]["generated_tree_sha256"],
    ),
)
for label, observed, expected in tree_checks:
    check(label, observed, expected)

discovery_hash = sha256_file(discovery_path)
check(
    "Stage 3 discovery file",
    discovery_hash,
    resolution["hashes"]["discovery_manifest_sha256"],
)

actual_stage1_files = {
    path.relative_to(proof).as_posix(): sha256_file(path)
    for path in proof.rglob("*")
    if path.is_file() and not path.is_symlink()
}
check(
    "Stage 1 exact source-file path set",
    sorted(actual_stage1_files),
    sorted(resolution["stage1_source_hashes"]),
)
for relative, expected in sorted(resolution["stage1_source_hashes"].items()):
    check(
        f"Stage 1 source hash {relative}",
        actual_stage1_files.get(relative),
        expected,
    )

stage1_export_hash = klean_export.tree_digest(proof)
generated_hash = klean_export.tree_digest(generated)
check(
    "input manifest frozen input",
    input_manifest["frozen_input_sha256"],
    stage1_export_hash,
)
check(
    "input manifest Stage 1 workspace",
    input_manifest["stage1_workspace_sha256"],
    stage1_export_hash,
)
check(
    "input manifest discovery",
    input_manifest["stage3_discovery_manifest_sha256"],
    discovery_hash,
)
check(
    "input manifest verification.k",
    input_manifest["verification_sha256"],
    sha256_file(proof / "verification.k"),
)
check(
    "generator manifest generated tree",
    generator_manifest["generated_tree_sha256"],
    generated_hash,
)
check(
    "generator manifest toolchain lock",
    generator_manifest["toolchain"],
    toolchain_lock,
)
check(
    "generator provenance Stage 1",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    stage1_export_hash,
)
check(
    "generator provenance Stage 3",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    discovery_hash,
)
check(
    "generator provenance inventory",
    generator_manifest["provenance"]["inventory_sha256"],
    input_manifest["inventory_sha256"],
)

obligation_map_hash = sha256_file(generated / "obligation-map.json")
trust_inventory_hash = sha256_file(generation / "trust-inventory.json")
check(
    "generator obligation-map hash",
    generator_manifest["obligation_map_sha256"],
    obligation_map_hash,
)
check(
    "export generated tree",
    export_result["generated_tree_sha256"],
    generated_hash,
)
check(
    "export Stage 1",
    export_result["frozen_input_sha256"],
    stage1_export_hash,
)
check(
    "export Stage 3",
    export_result["stage3_discovery_manifest_sha256"],
    discovery_hash,
)
check(
    "export trust inventory",
    export_result["trust_inventory_sha256"],
    trust_inventory_hash,
)

check(
    "audit-input embedded Stage 4 preflight",
    resolution["stage4_preflight"],
    stored_preflight,
)
check(
    "Stage 2 selected artifact hash",
    resolution["selections"]["k_audit"]["artifact_sha256"],
    resolution["hashes"]["k_audit_sha256"],
)
check(
    "Stage 4 selected artifact hash",
    resolution["selections"]["klean_generation"]["artifact_sha256"],
    resolution["hashes"]["klean_generation_sha256"],
)
check("classification-only Stage 5 result", resolution["stage5_result"], None)
check("classification-only target", resolution["target"], None)
check("classification-only Lean workspace hash", resolution["hashes"]["lean_workspace_sha256"], None)
check("classification-only Lean invocation hash", resolution["hashes"]["lean_invocation_sha256"], None)
check("classification-only /candidate absence", Path("/candidate").exists(), False)

print(f"TOTAL_FAILURES={len(failures)}")
if failures:
    print("FAILED_LABELS=" + json.dumps(failures))
    raise SystemExit(1)
