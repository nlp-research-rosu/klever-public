#!/usr/bin/env python3
import hashlib
import json
import stat
from pathlib import Path

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree

resolution = json.loads(Path("/audit-input.json").read_text())["resolution"]
expected = resolution["hashes"]
pipeline_roots = {
    "k_workspace_sha256": Path("/reference/k-proof"),
    "generation_producer_sources_sha256": Path("/reference/generation-tools"),
    "k_audit_sha256": Path("/reference/k-audit"),
    "klean_generation_sha256": Path("/reference/klean-generation"),
}
export_roots = {
    "stage1_export_sha256": Path("/reference/k-proof"),
    "generated_tree_sha256": Path("/reference/klean-generation/generated"),
}
for field, root in pipeline_roots.items():
    actual = sha256_tree(root)
    print(json.dumps({
        "field": field, "root": str(root), "expected": expected[field],
        "actual": actual, "match": actual == expected[field],
    }, sort_keys=True))
for field, root in export_roots.items():
    actual = tree_digest(root)
    print(json.dumps({
        "field": field, "root": str(root), "expected": expected[field],
        "actual": actual, "match": actual == expected[field],
    }, sort_keys=True))
discovery_actual = hashlib.sha256(
    Path("/reference/lemma-discovery.json").read_bytes()
).hexdigest()
print(json.dumps({
    "field": "discovery_manifest_sha256",
    "expected": expected["discovery_manifest_sha256"],
    "actual": discovery_actual,
    "match": discovery_actual == expected["discovery_manifest_sha256"],
}, sort_keys=True))

source_expected = resolution["stage1_source_hashes"]
source_actual = {}
nonregular = []
root = Path("/reference/k-proof")
for path in root.rglob("*"):
    relative = path.relative_to(root).as_posix()
    mode = path.lstat().st_mode
    if stat.S_ISREG(mode):
        source_actual[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    elif not stat.S_ISDIR(mode):
        nonregular.append(relative)
missing = sorted(set(source_expected) - set(source_actual))
extra = sorted(set(source_actual) - set(source_expected))
mismatch = sorted(
    key for key in set(source_expected) & set(source_actual)
    if source_expected[key] != source_actual[key]
)
print(json.dumps({
    "expected_count": len(source_expected),
    "actual_regular_count": len(source_actual),
    "missing": missing,
    "extra": extra,
    "mismatch": mismatch,
    "nonregular": nonregular,
}, indent=2, sort_keys=True))
