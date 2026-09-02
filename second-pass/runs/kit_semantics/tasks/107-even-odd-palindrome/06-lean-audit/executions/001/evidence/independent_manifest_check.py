#!/usr/bin/env python3
"""Independent hash, manifest, obligation, and target consistency audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import klean_export
from tools.k_rule_inventory import inventory_verification
from tools.pipeline_contract import _walk_regular_files, sha256_file, sha256_tree


REFERENCE = Path("/reference")
K_PROOF = REFERENCE / "k-proof"
K_AUDIT = REFERENCE / "k-audit"
GENERATION = REFERENCE / "klean-generation"
GENERATED = GENERATION / "generated"
PRODUCERS = REFERENCE / "generation-tools"


def load(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text())
    if not isinstance(document, dict):
        raise TypeError(f"{path} is not a JSON object")
    return document


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: list[tuple[str, bool, object]] = []


def check(name: str, condition: bool, observed: object) -> None:
    checks.append((name, condition, observed))
    print(f"{name}={'PASS' if condition else 'FAIL'} observed={observed!r}")


audit = load(Path("/audit-input.json"))
resolution = audit["resolution"]
discovery = load(REFERENCE / "lemma-discovery.json")
inventory = inventory_verification(K_PROOF)
input_manifest = load(GENERATION / "input-manifest.json")
generator = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
shipped_preflight = load(GENERATION / "preflight.json")
returned_preflight = load(Path("/audit-output/evidence/07-preflight-returned.json"))
trust_inventory = load(GENERATION / "trust-inventory.json")
obligation_map = load(GENERATED / "obligation-map.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
toolchain_lock = load(REFERENCE / "klean-toolchain.lock.json")

resolution_hashes = {
    "k_workspace_sha256": sha256_tree(K_PROOF),
    "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
    "discovery_manifest_sha256": file_hash(REFERENCE / "lemma-discovery.json"),
    "k_audit_sha256": sha256_tree(K_AUDIT),
    "klean_generation_sha256": sha256_tree(GENERATION),
    "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
check(
    "audit_input_resolution_hashes",
    resolution_hashes == resolution["hashes"],
    resolution_hashes,
)

stage1_source_hashes = {
    path.relative_to(K_PROOF).as_posix(): sha256_file(path)
    for path in _walk_regular_files(K_PROOF, "Stage 1 source workspace")
}
source_hash_diff = {
    "missing": sorted(set(resolution["stage1_source_hashes"]) - set(stage1_source_hashes)),
    "extra": sorted(set(stage1_source_hashes) - set(resolution["stage1_source_hashes"])),
    "changed": sorted(
        name
        for name in set(stage1_source_hashes) & set(resolution["stage1_source_hashes"])
        if stage1_source_hashes[name] != resolution["stage1_source_hashes"][name]
    ),
    "count": len(stage1_source_hashes),
}
check(
    "stage1_source_hash_bijection",
    stage1_source_hashes == resolution["stage1_source_hashes"],
    source_hash_diff,
)

selection_hashes = {
    "k_audit": resolution_hashes["k_audit_sha256"],
    "klean_generation": resolution_hashes["klean_generation_sha256"],
}
check(
    "selection_artifact_hashes",
    all(
        resolution["selections"][name]["artifact_sha256"] == digest
        for name, digest in selection_hashes.items()
    ),
    selection_hashes,
)

producer_files = {
    name: file_hash(PRODUCERS / name)
    for name in ("klean.py", "klean_export.py")
}
generator_files = {
    "klean.py": generator["klean_py_sha256"],
    "klean_export.py": generator["exporter_sha256"],
}
audit_image = "sha256:" + Path(resolution["generation_producer_sources"]).name
producer_names = sorted(path.name for path in PRODUCERS.iterdir())
check(
    "producer_file_image_binding",
    producer_names == ["klean.py", "klean_export.py", "source-manifest.json"]
    and producer_files == source_manifest["files"] == generator_files
    and source_manifest["generator_image_id"]
    == generator["provenance"]["generator_image_id"]
    == audit_image,
    {
        "names": producer_names,
        "files": producer_files,
        "image": audit_image,
    },
)

discovery_ids = [entry.get("source_rule_id") for entry in discovery["rules"]]
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
check(
    "stage3_ordered_rule_bijection",
    inventory_ids == discovery_ids
    and len(discovery_ids) == len(set(discovery_ids))
    and inventory["inventory_sha256"] == discovery["inventory_sha256"],
    {
        "inventory_ids": inventory_ids,
        "discovery_ids": discovery_ids,
        "inventory_sha256": inventory["inventory_sha256"],
    },
)

expected_definitions = []
for source, classified in zip(inventory["rules"], discovery["rules"], strict=True):
    expected_definitions.append(
        source
        | {
            "classification": classified["classification"],
            "rationale": classified["rationale"],
        }
    )
check(
    "input_manifest_definition_identity",
    input_manifest["definitions"] == expected_definitions,
    {"definition_count": len(input_manifest["definitions"])},
)

# This set is independently determined by the classification audit: the sole
# source rule is an exact named closure definition, not a domain proposition.
independent_domain_ids: list[str] = []
stage4_source_ids = [entry["source_rule_id"] for entry in input_manifest["source_rules"]]
mapped_source_ids = [entry["source_rule_id"] for entry in obligation_map["source_rules"]]
obligation_ids = [entry["source_rule_id"] for entry in obligation_map["obligations"]]
check(
    "domain_source_obligation_bijection",
    independent_domain_ids == stage4_source_ids == mapped_source_ids == obligation_ids
    and len(obligation_ids) == len(set(obligation_ids)),
    {
        "independent_domain_ids": independent_domain_ids,
        "input_manifest_ids": stage4_source_ids,
        "obligation_map_source_ids": mapped_source_ids,
        "obligation_ids": obligation_ids,
    },
)
check(
    "zero_obligation_sidecars",
    obligation_map["trust_parameters"] == []
    and generator["obligation_count"] == 0
    and export_result["obligation_count"] == 0
    and returned_preflight["obligation_count"] == 0,
    {
        "generator": generator["obligation_count"],
        "export": export_result["obligation_count"],
        "returned_preflight": returned_preflight["obligation_count"],
    },
)

expected_target = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(GENERATED)
check(
    "fixed_target_absence",
    expected_target is None
    and observed_target is None
    and generator["target"] is None
    and resolution.get("target") is None
    and shipped_preflight["target"] is None
    and returned_preflight["target"] is None,
    {
        "expected_definition": expected_target,
        "observed_target": observed_target,
        "generator_target": generator["target"],
        "audit_target": resolution.get("target"),
    },
)

sidecar_bindings = {
    "verification_sha256": file_hash(K_PROOF / "verification.k"),
    "inventory_sha256": inventory["inventory_sha256"],
    "stage1_workspace_sha256": resolution_hashes["stage1_export_sha256"],
    "stage3_discovery_manifest_sha256": resolution_hashes[
        "discovery_manifest_sha256"
    ],
    "generated_tree_sha256": resolution_hashes["generated_tree_sha256"],
    "obligation_map_sha256": file_hash(GENERATED / "obligation-map.json"),
    "trust_inventory_sha256": file_hash(GENERATION / "trust-inventory.json"),
}
sidecar_ok = (
    input_manifest["verification_sha256"] == sidecar_bindings["verification_sha256"]
    and input_manifest["inventory_sha256"] == sidecar_bindings["inventory_sha256"]
    and input_manifest["stage1_workspace_sha256"]
    == sidecar_bindings["stage1_workspace_sha256"]
    and input_manifest["frozen_input_sha256"]
    == sidecar_bindings["stage1_workspace_sha256"]
    and input_manifest["stage3_discovery_manifest_sha256"]
    == sidecar_bindings["stage3_discovery_manifest_sha256"]
    and generator["generated_tree_sha256"]
    == sidecar_bindings["generated_tree_sha256"]
    and generator["obligation_map_sha256"]
    == sidecar_bindings["obligation_map_sha256"]
    and generator["provenance"]["inventory_sha256"]
    == sidecar_bindings["inventory_sha256"]
    and generator["provenance"]["stage1_workspace_sha256"]
    == sidecar_bindings["stage1_workspace_sha256"]
    and generator["provenance"]["stage3_discovery_manifest_sha256"]
    == sidecar_bindings["stage3_discovery_manifest_sha256"]
    and export_result["frozen_input_sha256"]
    == sidecar_bindings["stage1_workspace_sha256"]
    and export_result["stage3_discovery_manifest_sha256"]
    == sidecar_bindings["stage3_discovery_manifest_sha256"]
    and export_result["generated_tree_sha256"]
    == sidecar_bindings["generated_tree_sha256"]
    and export_result["trust_inventory_sha256"]
    == sidecar_bindings["trust_inventory_sha256"]
)
check("manifest_sidecar_hash_bindings", sidecar_ok, sidecar_bindings)

check(
    "toolchain_lock_identity",
    generator["toolchain"] == toolchain_lock,
    toolchain_lock,
)
check(
    "preflight_return_identity",
    returned_preflight == shipped_preflight
    and returned_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
    and all(entry["exit_code"] == 0 for entry in returned_preflight["diagnostics"]),
    {
        "equal_to_shipped": returned_preflight == shipped_preflight,
        "status": returned_preflight["status"],
        "exit_codes": [entry["exit_code"] for entry in returned_preflight["diagnostics"]],
    },
)
check(
    "classification_only_stage5_absence",
    os.environ.get("AUDIT_MODE") == "CLASSIFICATION_ONLY"
    and resolution["mode"] == "CLASSIFICATION_ONLY"
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and not Path("/candidate").exists(),
    {
        "env_mode": os.environ.get("AUDIT_MODE"),
        "input_mode": resolution["mode"],
        "candidate_exists": Path("/candidate").exists(),
    },
)
check(
    "no_vacuous_conjunct_or_target",
    not obligation_map["obligations"]
    and expected_target is None
    and observed_target is None,
    {"obligations": obligation_map["obligations"], "target": observed_target},
)

failed = [name for name, passed, _observed in checks if not passed]
print(f"check_count={len(checks)}")
print(f"failed_checks={failed!r}")
print("INDEPENDENT_MANIFEST_AUDIT=" + ("PASS" if not failed else "FAIL"))
raise SystemExit(0 if not failed else 1)
