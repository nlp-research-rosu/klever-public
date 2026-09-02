#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from tools import pipeline_contract


def load_producer():
    path = Path("/reference/generation-tools/klean_export.py")
    spec = importlib.util.spec_from_file_location(
        "generation_time_klean_export", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
expected = audit["hashes"]
producer = load_producer()

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": producer.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_hash(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": producer.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}
checks = {
    name: observed[name] == expected[name] for name in observed
}

workspace = Path("/reference/k-proof")
observed_sources = {
    path.relative_to(workspace).as_posix(): file_hash(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "mounted Stage 1 workspace"
    )
}
expected_sources = audit["stage1_source_hashes"]
checks["stage1_source_hash_map_exact"] = observed_sources == expected_sources

result = {
    "observed": observed,
    "expected": {name: expected[name] for name in observed},
    "checks": checks,
    "stage1_source_file_count": len(observed_sources),
    "stage1_expected_source_file_count": len(expected_sources),
    "unmounted_recorded_hashes": {
        "lean_invocation_sha256": expected.get("lean_invocation_sha256")
    },
    "overall": "PASS" if all(checks.values()) else "FAIL",
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if all(checks.values()) else 1)
