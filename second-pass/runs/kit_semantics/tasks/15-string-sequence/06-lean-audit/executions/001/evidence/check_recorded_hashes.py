#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools import pipeline_contract
from tools.klean_export import tree_digest

audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
expected = resolution["hashes"]

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": hashlib.sha256(
        Path("/reference/lemma-discovery.json").read_bytes()
    ).hexdigest(),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}

recorded_source_hashes = resolution["stage1_source_hashes"]
observed_source_hashes = {
    path.relative_to("/reference/k-proof").as_posix():
        pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
source_missing = sorted(set(recorded_source_hashes) - set(observed_source_hashes))
source_extra = sorted(set(observed_source_hashes) - set(recorded_source_hashes))
source_changed = sorted(
    name
    for name in set(recorded_source_hashes) & set(observed_source_hashes)
    if recorded_source_hashes[name] != observed_source_hashes[name]
)

checks = {
    name: observed[name] == expected[name]
    for name in observed
}
checks["stage1_source_hash_map_exact"] = not (
    source_missing or source_extra or source_changed
)

print(
    json.dumps(
        {
            "observed": observed,
            "expected": {name: expected[name] for name in observed},
            "checks": checks,
            "stage1_source_hash_count_recorded": len(recorded_source_hashes),
            "stage1_source_hash_count_observed": len(observed_source_hashes),
            "stage1_source_hash_missing": source_missing,
            "stage1_source_hash_extra": source_extra,
            "stage1_source_hash_changed": source_changed,
            "unmounted_recorded_hashes": {
                "lean_invocation_sha256": expected.get(
                    "lean_invocation_sha256"
                )
            },
            "all_mounted_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
