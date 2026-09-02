#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.pipeline_contract import sha256_tree


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
stage1 = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

observed_source_hashes = {
    path.relative_to(stage1).as_posix(): file_sha256(path)
    for path in sorted(stage1.rglob("*"))
    if path.is_file()
}
expected_source_hashes = audit["stage1_source_hashes"]

observed = {
    "k_workspace_sha256_pipeline_contract": sha256_tree(stage1),
    "stage1_export_sha256_klean_tree_digest": klean_export.tree_digest(stage1),
    "discovery_manifest_sha256": file_sha256(Path("/reference/lemma-discovery.json")),
    "k_audit_sha256_pipeline_contract": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256_pipeline_contract": sha256_tree(generation),
    "generated_tree_sha256_klean_tree_digest": klean_export.tree_digest(generated),
}
expected = {
    "k_workspace_sha256_pipeline_contract": audit["hashes"]["k_workspace_sha256"],
    "stage1_export_sha256_klean_tree_digest": audit["hashes"]["stage1_export_sha256"],
    "discovery_manifest_sha256": audit["hashes"]["discovery_manifest_sha256"],
    "k_audit_sha256_pipeline_contract": audit["hashes"]["k_audit_sha256"],
    "klean_generation_sha256_pipeline_contract": audit["hashes"]["klean_generation_sha256"],
    "generated_tree_sha256_klean_tree_digest": audit["hashes"]["generated_tree_sha256"],
}
checks = {
    key: observed[key] == expected[key]
    for key in observed
}
checks.update(
    {
        "stage1_source_file_set_exact": (
            set(observed_source_hashes) == set(expected_source_hashes)
        ),
        "stage1_source_hashes_exact": (
            observed_source_hashes == expected_source_hashes
        ),
    }
)

result = {
    "observed": observed,
    "expected": expected,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "stage1_source_missing": sorted(
        set(expected_source_hashes) - set(observed_source_hashes)
    ),
    "stage1_source_extra": sorted(
        set(observed_source_hashes) - set(expected_source_hashes)
    ),
    "stage1_source_mismatches": {
        name: {
            "observed": observed_source_hashes.get(name),
            "expected": expected_source_hashes.get(name),
        }
        for name in sorted(set(observed_source_hashes) | set(expected_source_hashes))
        if observed_source_hashes.get(name) != expected_source_hashes.get(name)
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
