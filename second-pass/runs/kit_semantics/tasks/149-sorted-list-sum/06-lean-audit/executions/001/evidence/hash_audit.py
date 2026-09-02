#!/usr/bin/env python3
"""Independently recompute launcher and Stage 4 provenance hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
STAGE1 = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): file_sha256(path)
        for path in pipeline_contract._walk_regular_files(root, str(root))
    }


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
expected = resolution["hashes"]
generator = json.loads((GENERATION / "generator-manifest.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(STAGE1),
    "stage1_export_sha256": klean_export.tree_digest(STAGE1),
    "discovery_manifest_sha256": file_sha256(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        PRODUCERS
    ),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(CANDIDATE),
}

producer_files = {
    name: file_sha256(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
generator_image_id = generator["provenance"]["generator_image_id"]
launcher_image_id = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)

recorded_stage1_files = resolution["stage1_source_hashes"]
observed_stage1_files = file_hashes(STAGE1)
stage1_missing = sorted(set(recorded_stage1_files) - set(observed_stage1_files))
stage1_extra = sorted(set(observed_stage1_files) - set(recorded_stage1_files))
stage1_mismatched = sorted(
    name
    for name in set(recorded_stage1_files) & set(observed_stage1_files)
    if recorded_stage1_files[name] != observed_stage1_files[name]
)

report = {
    "signed_resolution": {
        "recorded": audit_document["resolved_input_sha256"],
        "recomputed": resolved_digest,
        "match": audit_document["resolved_input_sha256"] == resolved_digest,
    },
    "recorded_hash_comparisons": {
        name: {
            "recorded": expected[name],
            "recomputed": digest,
            "match": expected[name] == digest,
        }
        for name, digest in observed.items()
    },
    "unmounted_lean_invocation_hash": expected["lean_invocation_sha256"],
    "stage1_source_hashes": {
        "recorded_count": len(recorded_stage1_files),
        "observed_count": len(observed_stage1_files),
        "missing": stage1_missing,
        "extra": stage1_extra,
        "mismatched": stage1_mismatched,
        "match": not (stage1_missing or stage1_extra or stage1_mismatched),
    },
    "producer_provenance": {
        "recomputed_files": producer_files,
        "generator_manifest_files": {
            "klean_export.py": generator["exporter_sha256"],
            "klean.py": generator["klean_py_sha256"],
        },
        "source_manifest_files": source_manifest["files"],
        "file_hashes_match_both_manifests": (
            producer_files
            == source_manifest["files"]
            == {
                "klean_export.py": generator["exporter_sha256"],
                "klean.py": generator["klean_py_sha256"],
            }
        ),
        "generator_manifest_image_id": generator_image_id,
        "source_manifest_image_id": source_manifest["generator_image_id"],
        "launcher_producer_path_image_id": launcher_image_id,
        "image_ids_match": (
            generator_image_id
            == source_manifest["generator_image_id"]
            == launcher_image_id
        ),
        "observed_bundle_names": sorted(
            path.relative_to(PRODUCERS).as_posix()
            for path in pipeline_contract._walk_regular_files(
                PRODUCERS, str(PRODUCERS)
            )
        ),
    },
}

print(json.dumps(report, indent=2, sort_keys=True))
