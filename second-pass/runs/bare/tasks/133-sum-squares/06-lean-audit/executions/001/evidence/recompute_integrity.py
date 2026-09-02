#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import k_rule_inventory
from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def print_json(label: str, value: object) -> None:
    print(label)
    print(json.dumps(value, indent=2, sort_keys=True))


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]

inventory = k_rule_inventory.inventory_verification(
    Path("/reference/k-proof")
)
validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)

producer_files = {
    name: sha256_file(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)

producer_checks = {
    "environment_mode": os.environ.get("AUDIT_MODE"),
    "audit_input_mode": resolution["mode"],
    "producer_file_hashes": producer_files,
    "source_manifest_files": source_manifest["files"],
    "generator_manifest_files": {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    },
    "source_manifest_image_id": source_manifest["generator_image_id"],
    "generator_manifest_image_id": generator_manifest["provenance"][
        "generator_image_id"
    ],
    "audit_input_producer_bundle_path_tail": Path(
        resolution["generation_producer_sources"]
    ).name,
    "producer_tree_pipeline_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "audit_input_producer_tree_sha256": resolution["hashes"][
        "generation_producer_sources_sha256"
    ],
}

tree_checks = {
    "stage1_export_klean_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "stage1_export_recorded_sha256": resolution["hashes"][
        "stage1_export_sha256"
    ],
    "stage1_pipeline_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_pipeline_recorded_sha256": resolution["hashes"][
        "k_workspace_sha256"
    ],
    "k_audit_pipeline_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "k_audit_pipeline_recorded_sha256": resolution["hashes"][
        "k_audit_sha256"
    ],
    "generation_pipeline_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_pipeline_recorded_sha256": resolution["hashes"][
        "klean_generation_sha256"
    ],
    "generated_klean_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generated_klean_recorded_sha256": resolution["hashes"][
        "generated_tree_sha256"
    ],
    "discovery_file_sha256": sha256_file(
        Path("/reference/lemma-discovery.json")
    ),
    "discovery_recorded_sha256": resolution["hashes"][
        "discovery_manifest_sha256"
    ],
}

stage1_source_hashes = {
    path.relative_to(Path("/reference/k-proof")).as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}

print_json("PRODUCER_CHECKS", producer_checks)
print_json("TREE_CHECKS", tree_checks)
print_json("STAGE1_SOURCE_HASHES", stage1_source_hashes)
print_json(
    "STAGE1_SOURCE_HASHES_RECORDED", resolution["stage1_source_hashes"]
)
print_json("CANONICAL_INVENTORY", inventory)
print_json("VALIDATED_DISCOVERY", validated)
