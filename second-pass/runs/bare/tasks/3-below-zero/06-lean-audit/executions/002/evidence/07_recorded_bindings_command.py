#!/usr/bin/env python3
"""Enumerate and recompute every hash with a mounted artifact referent."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
inventory = inventory_verification(workspace)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
recorded_preflight = json.loads((generation / "preflight.json").read_text())
rerun_preflight = json.loads(
    Path("/audit-output/evidence/03_preflight_result.json").read_text()
)
trust_inventory_path = generation / "trust-inventory.json"
obligation_map_path = generated / "obligation-map.json"

stage1_export_hash = klean_export.tree_digest(workspace)
stage1_pipeline_hash = pipeline_contract.sha256_tree(workspace)
discovery_hash = hashlib.sha256(discovery_path.read_bytes()).hexdigest()
generated_hash = klean_export.tree_digest(generated)
generation_hash = pipeline_contract.sha256_tree(generation)
k_audit_hash = pipeline_contract.sha256_tree(Path("/reference/k-audit"))
verification_hash = hashlib.sha256(
    (workspace / "verification.k").read_bytes()
).hexdigest()
obligation_map_hash = hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
trust_inventory_hash = hashlib.sha256(
    trust_inventory_path.read_bytes()
).hexdigest()

checks: list[dict[str, object]] = []


def check(label: str, recorded: object, recomputed: object) -> None:
    checks.append(
        {
            "label": label,
            "recorded": recorded,
            "recomputed": recomputed,
            "matches": recorded == recomputed,
        }
    )


check(
    "audit resolution k_workspace_sha256",
    resolution["hashes"]["k_workspace_sha256"],
    stage1_pipeline_hash,
)
check(
    "audit resolution stage1_export_sha256",
    resolution["hashes"]["stage1_export_sha256"],
    stage1_export_hash,
)
check(
    "audit resolution discovery_manifest_sha256",
    resolution["hashes"]["discovery_manifest_sha256"],
    discovery_hash,
)
check(
    "audit resolution k_audit_sha256",
    resolution["hashes"]["k_audit_sha256"],
    k_audit_hash,
)
check(
    "audit resolution klean_generation_sha256",
    resolution["hashes"]["klean_generation_sha256"],
    generation_hash,
)
check(
    "audit resolution generated_tree_sha256",
    resolution["hashes"]["generated_tree_sha256"],
    generated_hash,
)
check(
    "selected Stage 2 artifact_sha256",
    resolution["selections"]["k_audit"]["artifact_sha256"],
    k_audit_hash,
)
check(
    "selected Stage 4 artifact_sha256",
    resolution["selections"]["klean_generation"]["artifact_sha256"],
    generation_hash,
)
check(
    "Stage 3 inventory_sha256",
    json.loads(discovery_path.read_text())["inventory_sha256"],
    inventory["inventory_sha256"],
)

for index, (recorded_rule, canonical_rule) in enumerate(
    zip(input_manifest["definitions"], inventory["rules"], strict=True)
):
    normalized = " ".join(canonical_rule["text"].split())
    check(
        f"input manifest definition {index} normalized_sha256",
        recorded_rule["normalized_sha256"],
        hashlib.sha256(normalized.encode()).hexdigest(),
    )

for label, recorded, recomputed in [
    (
        "input manifest frozen_input_sha256",
        input_manifest["frozen_input_sha256"],
        stage1_export_hash,
    ),
    (
        "input manifest stage1_workspace_sha256",
        input_manifest["stage1_workspace_sha256"],
        stage1_export_hash,
    ),
    (
        "input manifest stage3_discovery_manifest_sha256",
        input_manifest["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    (
        "input manifest inventory_sha256",
        input_manifest["inventory_sha256"],
        inventory["inventory_sha256"],
    ),
    (
        "input manifest verification_sha256",
        input_manifest["verification_sha256"],
        verification_hash,
    ),
    (
        "generator manifest generated_tree_sha256",
        generator_manifest["generated_tree_sha256"],
        generated_hash,
    ),
    (
        "generator manifest obligation_map_sha256",
        generator_manifest["obligation_map_sha256"],
        obligation_map_hash,
    ),
    (
        "generator provenance stage1_workspace_sha256",
        generator_manifest["provenance"]["stage1_workspace_sha256"],
        stage1_export_hash,
    ),
    (
        "generator provenance stage3_discovery_manifest_sha256",
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ],
        discovery_hash,
    ),
    (
        "generator provenance inventory_sha256",
        generator_manifest["provenance"]["inventory_sha256"],
        inventory["inventory_sha256"],
    ),
    (
        "export result frozen_input_sha256",
        export_result["frozen_input_sha256"],
        stage1_export_hash,
    ),
    (
        "export result generated_tree_sha256",
        export_result["generated_tree_sha256"],
        generated_hash,
    ),
    (
        "export result stage3_discovery_manifest_sha256",
        export_result["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    (
        "export result trust_inventory_sha256",
        export_result["trust_inventory_sha256"],
        trust_inventory_hash,
    ),
    (
        "recorded preflight frozen_input_sha256",
        recorded_preflight["frozen_input_sha256"],
        stage1_export_hash,
    ),
    (
        "recorded preflight stage1_workspace_sha256",
        recorded_preflight["stage1_workspace_sha256"],
        stage1_export_hash,
    ),
    (
        "recorded preflight stage3_discovery_manifest_sha256",
        recorded_preflight["stage3_discovery_manifest_sha256"],
        discovery_hash,
    ),
    (
        "recorded preflight generated_tree_sha256",
        recorded_preflight["generated_tree_sha256"],
        generated_hash,
    ),
]:
    check(label, recorded, recomputed)

for index, diagnostic in enumerate(rerun_preflight["diagnostics"]):
    check(
        f"rerun preflight diagnostic {index} output_sha256",
        diagnostic["output_sha256"],
        hashlib.sha256(diagnostic["output_tail"].encode()).hexdigest(),
    )

result = {
    "command": (
        "PYTHONPATH=/reference python3 "
        "/audit-output/evidence/07_recorded_bindings_command.py"
    ),
    "checks": checks,
    "check_count": len(checks),
    "all_mounted_bindings_match": all(
        bool(entry["matches"]) for entry in checks
    ),
    "rerun_preflight_semantically_equals_recorded": (
        rerun_preflight == recorded_preflight
    ),
    "source_attestations_without_mounted_generator-source_referent": {
        "generator_manifest.exporter_sha256": generator_manifest[
            "exporter_sha256"
        ],
        "generator_manifest.klean_py_sha256": generator_manifest[
            "klean_py_sha256"
        ],
        "generator_manifest.provenance.generator_image_id": (
            generator_manifest["provenance"]["generator_image_id"]
        ),
        "audit.image_id": audit["audit"]["image_id"],
        "note": (
            "These attest generator/audit images or source versions, not a "
            "mounted artifact path. The current mounted audit tools are bound "
            "separately by the verified mechanical-checker lock."
        ),
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
