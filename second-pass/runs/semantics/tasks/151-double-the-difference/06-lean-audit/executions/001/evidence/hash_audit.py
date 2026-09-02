#!/usr/bin/env python3
"""Recompute launcher-recorded and Stage 4 producer hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): sha256_file(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


audit = json.loads(AUDIT_INPUT.read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]

expected_sources = resolution["stage1_source_hashes"]
actual_sources = regular_file_hashes(K_WORKSPACE)
missing_sources = sorted(set(expected_sources) - set(actual_sources))
extra_sources = sorted(set(actual_sources) - set(expected_sources))
mismatched_sources = {
    name: {"expected": expected_sources[name], "actual": actual_sources[name]}
    for name in sorted(set(expected_sources) & set(actual_sources))
    if expected_sources[name] != actual_sources[name]
}

generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
producer_hashes = {
    name: sha256_file(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
source_image_id = source_manifest["generator_image_id"]
audit_image_key = Path(resolution["generation_producer_sources"]).name

computed = {
    "discovery_manifest_sha256": sha256_file(DISCOVERY),
    "generated_tree_sha256": tree_digest(GENERATED),
    "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
    "k_audit_sha256": sha256_tree(K_AUDIT),
    "k_workspace_sha256": sha256_tree(K_WORKSPACE),
    "klean_generation_sha256": sha256_tree(GENERATION),
    "stage1_export_sha256": tree_digest(K_WORKSPACE),
}
comparisons = {
    name: {
        "recorded": recorded[name],
        "computed": computed[name],
        "match": recorded[name] == computed[name],
    }
    for name in computed
}

result = {
    "launcher_mode": resolution["mode"],
    "environment_mode": __import__("os").environ.get("AUDIT_MODE"),
    "recorded_null_stage5_hashes": {
        "lean_invocation_sha256": recorded["lean_invocation_sha256"],
        "lean_workspace_sha256": recorded["lean_workspace_sha256"],
    },
    "tree_and_file_hashes": comparisons,
    "stage1_source_hashes": {
        "recorded_count": len(expected_sources),
        "actual_count": len(actual_sources),
        "missing": missing_sources,
        "extra": extra_sources,
        "mismatched": mismatched_sources,
        "all_match": not (
            missing_sources or extra_sources or mismatched_sources
        ),
    },
    "producer_provenance": {
        "computed_file_hashes": producer_hashes,
        "generator_manifest_file_hashes": {
            "klean_export.py": generator_manifest["exporter_sha256"],
            "klean.py": generator_manifest["klean_py_sha256"],
        },
        "source_manifest_file_hashes": source_manifest["files"],
        "file_hashes_match_both_manifests": (
            producer_hashes
            == source_manifest["files"]
            == {
                "klean_export.py": generator_manifest["exporter_sha256"],
                "klean.py": generator_manifest["klean_py_sha256"],
            }
        ),
        "generator_manifest_image_id": generator_image_id,
        "source_manifest_image_id": source_image_id,
        "audit_input_image_key": audit_image_key,
        "image_ids_match": (
            generator_image_id
            == source_image_id
            == f"sha256:{audit_image_key}"
        ),
        "source_bundle_names": sorted(
            path.relative_to(PRODUCERS).as_posix()
            for path in PRODUCERS.iterdir()
        ),
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
