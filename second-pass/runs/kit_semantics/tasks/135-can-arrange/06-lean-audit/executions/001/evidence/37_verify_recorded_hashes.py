#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]

observed = {
    "discovery_manifest_sha256": file_sha256(
        Path("/reference/lemma-discovery.json")
    ),
    "generated_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "klean_generation_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "lean_workspace_sha256": sha256_tree(Path("/candidate")),
    "stage1_export_sha256": tree_digest(Path("/reference/k-proof")),
}

for name, digest in observed.items():
    expected = recorded[name]
    print(
        f"{name}: expected={expected} observed={digest} "
        f"match={expected == digest}"
    )

source_expected = resolution["stage1_source_hashes"]
source_root = Path("/reference/k-proof")
source_observed = {
    path.relative_to(source_root).as_posix(): file_sha256(path)
    for path in source_root.rglob("*")
    if path.is_file() and not path.is_symlink()
}
missing = sorted(set(source_expected) - set(source_observed))
extra = sorted(set(source_observed) - set(source_expected))
mismatched = sorted(
    relative
    for relative in set(source_expected) & set(source_observed)
    if source_expected[relative] != source_observed[relative]
)
print(f"stage1_source_hash_count_expected={len(source_expected)}")
print(f"stage1_source_hash_count_observed={len(source_observed)}")
print(f"stage1_source_missing={missing}")
print(f"stage1_source_extra={extra}")
print(f"stage1_source_mismatched={mismatched}")

if (
    any(recorded[name] != digest for name, digest in observed.items())
    or missing
    or extra
    or mismatched
):
    raise SystemExit(1)
