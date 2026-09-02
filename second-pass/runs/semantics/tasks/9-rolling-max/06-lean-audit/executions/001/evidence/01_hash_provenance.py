#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_file, sha256_tree
from tools.stage6_resolution_contract import canonical_json_sha256


AUDIT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")


def match(observed: object, expected: object) -> dict[str, object]:
    return {
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }


audit = json.loads(AUDIT.read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)

producer_files = {
    name: sha256_file(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
producer_image_key = PurePosixPath(
    resolution["generation_producer_sources"]
).name
producer_image = f"sha256:{producer_image_key}"

observed_source_hashes = {
    path.relative_to(K_PROOF).as_posix(): sha256_file(path)
    for path in sorted(K_PROOF.rglob("*"))
    if path.is_file() and not path.is_symlink()
}

checks = {
    "audit_mode_env": match(os.environ.get("AUDIT_MODE"), resolution["mode"]),
    "resolved_input_sha256": match(
        canonical_json_sha256(resolution),
        audit["resolved_input_sha256"],
    ),
    "k_workspace_sha256": match(
        sha256_tree(K_PROOF), recorded["k_workspace_sha256"]
    ),
    "stage1_export_sha256": match(
        tree_digest(K_PROOF), recorded["stage1_export_sha256"]
    ),
    "stage1_source_hashes": match(
        observed_source_hashes, resolution["stage1_source_hashes"]
    ),
    "discovery_manifest_sha256": match(
        sha256_file(DISCOVERY), recorded["discovery_manifest_sha256"]
    ),
    "k_audit_sha256": match(
        sha256_tree(K_AUDIT), recorded["k_audit_sha256"]
    ),
    "klean_generation_sha256": match(
        sha256_tree(GENERATION), recorded["klean_generation_sha256"]
    ),
    "generated_tree_sha256": match(
        tree_digest(GENERATED), recorded["generated_tree_sha256"]
    ),
    "generation_producer_sources_sha256": match(
        sha256_tree(PRODUCERS),
        recorded["generation_producer_sources_sha256"],
    ),
    "lean_workspace_sha256": match(
        sha256_tree(CANDIDATE), recorded["lean_workspace_sha256"]
    ),
    "stage5_result_workspace_sha256": match(
        sha256_tree(CANDIDATE),
        resolution["stage5_result"]["outputs"]["workspace_sha256"],
    ),
    "producer_klean_export_source_manifest": match(
        producer_files["klean_export.py"],
        source_manifest["files"]["klean_export.py"],
    ),
    "producer_klean_source_manifest": match(
        producer_files["klean.py"],
        source_manifest["files"]["klean.py"],
    ),
    "producer_klean_export_generator_manifest": match(
        producer_files["klean_export.py"],
        generator_manifest["exporter_sha256"],
    ),
    "producer_klean_generator_manifest": match(
        producer_files["klean.py"],
        generator_manifest["klean_py_sha256"],
    ),
    "producer_image_source_vs_generator_manifest": match(
        source_manifest["generator_image_id"],
        generator_manifest["provenance"]["generator_image_id"],
    ),
    "producer_image_audit_path_vs_source_manifest": match(
        producer_image,
        source_manifest["generator_image_id"],
    ),
}

result = {
    "checks": checks,
    "producer_files": producer_files,
    "producer_bundle_entries": sorted(
        path.relative_to(PRODUCERS).as_posix()
        for path in PRODUCERS.rglob("*")
    ),
    "recorded_but_unmounted": {
        "lean_invocation_sha256": recorded["lean_invocation_sha256"],
        "reason": (
            "The launcher mounted /candidate (the Stage 5 workspace), "
            "but no Stage 5 invocation/evidence tree."
        ),
    },
}
result["all_mounted_checks_match"] = all(
    item["match"] for item in checks.values()
)
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["all_mounted_checks_match"] else 1)
