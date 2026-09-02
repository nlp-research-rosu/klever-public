#!/usr/bin/env python3
"""Recompute launcher-recorded file and tree hashes from mounted inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit = json.loads(AUDIT_INPUT.read_text())
    resolution = audit["resolution"]
    expected = resolution["hashes"]

    computed = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
        "discovery_manifest_sha256": sha256(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    comparisons = {
        name: {
            "expected": expected.get(name),
            "computed": value,
            "match": expected.get(name) == value,
        }
        for name, value in computed.items()
    }

    computed_sources = {
        path.relative_to(K_WORKSPACE).as_posix(): pipeline_contract.sha256_file(
            path
        )
        for path in pipeline_contract._walk_regular_files(
            K_WORKSPACE, "mounted Stage 1 workspace"
        )
    }
    expected_sources = resolution["stage1_source_hashes"]
    missing = sorted(set(expected_sources) - set(computed_sources))
    extra = sorted(set(computed_sources) - set(expected_sources))
    changed = sorted(
        path
        for path in set(expected_sources) & set(computed_sources)
        if expected_sources[path] != computed_sources[path]
    )

    sidecars = {
        relative: sha256(GENERATION / relative)
        for relative in (
            "input-manifest.json",
            "generator-manifest.json",
            "trust-inventory.json",
            "export-result.json",
            "generated/obligation-map.json",
        )
    }
    document = {
        "launcher_mode": resolution["mode"],
        "environment_mode": os.environ.get("AUDIT_MODE"),
        "mode_exact": (
            resolution["mode"] == os.environ.get("AUDIT_MODE")
            == "CLASSIFICATION_ONLY"
        ),
        "hash_comparisons": comparisons,
        "all_launcher_hashes_exact": all(
            entry["match"] for entry in comparisons.values()
        ),
        "stage1_source_hashes": {
            "expected_count": len(expected_sources),
            "computed_count": len(computed_sources),
            "missing": missing,
            "extra": extra,
            "changed": changed,
            "all_exact": not missing and not extra and not changed,
        },
        "selected_artifact_hashes": {
            "k_audit_selection_matches": (
                resolution["selections"]["k_audit"]["artifact_sha256"]
                == computed["k_audit_sha256"]
            ),
            "klean_generation_selection_matches": (
                resolution["selections"]["klean_generation"][
                    "artifact_sha256"
                ]
                == computed["klean_generation_sha256"]
            ),
        },
        "sidecar_sha256": sidecars,
        "candidate_exists": Path("/candidate").exists(),
        "audit_input_target": resolution.get("target"),
        "audit_input_stage4_status": resolution["selections"][
            "klean_generation"
        ]["status"],
    }
    print(json.dumps(document, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
