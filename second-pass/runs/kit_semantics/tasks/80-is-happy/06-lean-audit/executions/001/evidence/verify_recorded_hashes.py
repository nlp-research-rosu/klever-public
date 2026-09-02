#!/usr/bin/env python3
"""Recompute every launcher-recorded source/tree hash and producer binding."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import pipeline_contract
from tools.klean_export import tree_digest


AUDIT = json.loads(Path("/audit-input.json").read_text())
RESOLUTION = AUDIT["resolution"]
HASHES = RESOLUTION["hashes"]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report(name: str, observed: object, expected: object) -> bool:
    matched = observed == expected
    print(
        f"{name}: matched={matched} observed={observed!r} expected={expected!r}"
    )
    return matched


checks: list[bool] = []
checks.append(report("AUDIT_MODE", os.environ.get("AUDIT_MODE"), RESOLUTION["mode"]))
checks.append(report("problem_id", RESOLUTION["problem_id"], "80-is-happy"))
checks.append(report("condition", RESOLUTION["condition"], "kit-semantics"))
checks.append(
    report("semantics_mode", RESOLUTION["semantics_mode"], "SUPPLIED_SEMANTICS")
)

pipeline_trees = {
    "k_workspace_sha256": Path("/reference/k-proof"),
    "k_audit_sha256": Path("/reference/k-audit"),
    "klean_generation_sha256": Path("/reference/klean-generation"),
    "generation_producer_sources_sha256": Path("/reference/generation-tools"),
}
for field, path in pipeline_trees.items():
    checks.append(report(field, pipeline_contract.sha256_tree(path), HASHES[field]))

checks.append(
    report(
        "stage1_export_sha256",
        tree_digest(Path("/reference/k-proof")),
        HASHES["stage1_export_sha256"],
    )
)
checks.append(
    report(
        "generated_tree_sha256",
        tree_digest(Path("/reference/klean-generation/generated")),
        HASHES["generated_tree_sha256"],
    )
)
checks.append(
    report(
        "discovery_manifest_sha256",
        file_sha256(Path("/reference/lemma-discovery.json")),
        HASHES["discovery_manifest_sha256"],
    )
)

checks.append(report("lean_workspace_sha256", HASHES["lean_workspace_sha256"], None))
checks.append(report("lean_invocation_sha256", HASHES["lean_invocation_sha256"], None))
checks.append(report("lean_workspace_path", RESOLUTION["lean_workspace"], None))
checks.append(report("lean_invocation_path", RESOLUTION["lean_invocation"], None))
checks.append(report("candidate_absent", Path("/candidate").exists(), False))

checks.append(
    report(
        "selected_k_audit_artifact",
        RESOLUTION["selections"]["k_audit"]["artifact_sha256"],
        HASHES["k_audit_sha256"],
    )
)
checks.append(
    report(
        "selected_generation_artifact",
        RESOLUTION["selections"]["klean_generation"]["artifact_sha256"],
        HASHES["klean_generation_sha256"],
    )
)

workspace = Path("/reference/k-proof")
observed_source_hashes = {
    path.relative_to(workspace).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "mounted frozen Stage 1 source workspace"
    )
}
expected_source_hashes = RESOLUTION["stage1_source_hashes"]
missing_source_paths = sorted(set(expected_source_hashes) - set(observed_source_hashes))
extra_source_paths = sorted(set(observed_source_hashes) - set(expected_source_hashes))
changed_source_paths = sorted(
    path
    for path in set(expected_source_hashes) & set(observed_source_hashes)
    if expected_source_hashes[path] != observed_source_hashes[path]
)
print(f"stage1_source_hash_count_observed={len(observed_source_hashes)}")
print(f"stage1_source_hash_count_expected={len(expected_source_hashes)}")
print(f"stage1_source_missing_paths={missing_source_paths}")
print(f"stage1_source_extra_paths={extra_source_paths}")
print(f"stage1_source_changed_paths={changed_source_paths}")
checks.append(
    report(
        "stage1_source_hash_bijection",
        not (missing_source_paths or extra_source_paths or changed_source_paths),
        True,
    )
)

source_bundle = Path("/reference/generation-tools")
source_manifest = json.loads((source_bundle / "source-manifest.json").read_text())
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
observed_bundle_names = sorted(
    path.relative_to(source_bundle).as_posix()
    for path in pipeline_contract._walk_regular_files(
        source_bundle, "mounted Stage 4 producer source bundle"
    )
)
expected_bundle_names = ["klean.py", "klean_export.py", "source-manifest.json"]
checks.append(report("producer_bundle_exact_files", observed_bundle_names, expected_bundle_names))

observed_producer_files = {
    name: file_sha256(source_bundle / name)
    for name in ("klean.py", "klean_export.py")
}
checks.append(
    report("producer_files_vs_source_manifest", observed_producer_files, source_manifest["files"])
)
checks.append(
    report(
        "producer_exporter_vs_generator_manifest",
        observed_producer_files["klean_export.py"],
        generator_manifest["exporter_sha256"],
    )
)
checks.append(
    report(
        "producer_klean_vs_generator_manifest",
        observed_producer_files["klean.py"],
        generator_manifest["klean_py_sha256"],
    )
)

generator_image = generator_manifest["provenance"]["generator_image_id"]
audit_path_image = "sha256:" + Path(
    RESOLUTION["generation_producer_sources"]
).name
checks.append(
    report(
        "generator_image_source_vs_generator_manifest",
        source_manifest["generator_image_id"],
        generator_image,
    )
)
checks.append(
    report(
        "generator_image_audit_input_vs_generator_manifest",
        audit_path_image,
        generator_image,
    )
)

checks.append(
    report(
        "generator_generated_tree",
        generator_manifest["generated_tree_sha256"],
        HASHES["generated_tree_sha256"],
    )
)
checks.append(
    report(
        "generator_stage1_provenance",
        generator_manifest["provenance"]["stage1_workspace_sha256"],
        HASHES["stage1_export_sha256"],
    )
)
checks.append(
    report(
        "generator_stage3_provenance",
        generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
        HASHES["discovery_manifest_sha256"],
    )
)

print(f"ALL_RECORDED_HASH_AND_PRODUCER_CHECKS_PASS={all(checks)}")
