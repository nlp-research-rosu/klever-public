#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools import klean_export


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


stage1 = Path("/reference/k-proof")
discovery = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
input_manifest = json.loads(
    (generation / "input-manifest.json").read_text()
)
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = generated / "obligation-map.json"
trust_inventory = generation / "trust-inventory.json"
target = klean_export.target_statement(generated)

observed = {
    "stage1_export_sha256": klean_export.tree_digest(stage1),
    "discovery_sha256": file_hash(discovery),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "obligation_map_sha256": file_hash(obligation_map),
    "trust_inventory_sha256": file_hash(trust_inventory),
}
checks = {
    "input_manifest_frozen_input": (
        input_manifest["frozen_input_sha256"]
        == observed["stage1_export_sha256"]
    ),
    "input_manifest_stage1": (
        input_manifest["stage1_workspace_sha256"]
        == observed["stage1_export_sha256"]
    ),
    "input_manifest_discovery": (
        input_manifest["stage3_discovery_manifest_sha256"]
        == observed["discovery_sha256"]
    ),
    "generator_generated_tree": (
        generator_manifest["generated_tree_sha256"]
        == observed["generated_tree_sha256"]
    ),
    "generator_obligation_map": (
        generator_manifest["obligation_map_sha256"]
        == observed["obligation_map_sha256"]
    ),
    "generator_stage1_provenance": (
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == observed["stage1_export_sha256"]
    ),
    "generator_discovery_provenance": (
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == observed["discovery_sha256"]
    ),
    "export_stage1": (
        export_result["frozen_input_sha256"]
        == observed["stage1_export_sha256"]
    ),
    "export_discovery": (
        export_result["stage3_discovery_manifest_sha256"]
        == observed["discovery_sha256"]
    ),
    "export_generated_tree": (
        export_result["generated_tree_sha256"]
        == observed["generated_tree_sha256"]
    ),
    "export_trust_inventory": (
        export_result["trust_inventory_sha256"]
        == observed["trust_inventory_sha256"]
    ),
    "target_equals_generator_manifest": (
        target == generator_manifest["target"]
    ),
}
print(
    json.dumps(
        {
            "observed": observed,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
            "target": target,
        },
        indent=2,
        sort_keys=True,
    )
)
