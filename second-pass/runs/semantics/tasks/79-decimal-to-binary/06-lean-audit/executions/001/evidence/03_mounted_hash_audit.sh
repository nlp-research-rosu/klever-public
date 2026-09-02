#!/usr/bin/env bash
set -euo pipefail

echo '$ PYTHONPATH=/reference python3 - <<PY  # independently recompute launcher and manifest hashes'
PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
import os
from pathlib import Path
from tools.klean_export import (
    expected_target_definition,
    sha256_text,
    target_statement,
    tree_digest,
)
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import verify_audit_input

audit_document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = verify_audit_input(audit_document)
hashes = resolution["hashes"]

observed = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": hashlib.sha256(
        Path("/reference/lemma-discovery.json").read_bytes()
    ).hexdigest(),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(Path("/reference/klean-generation")),
    "generation_producer_sources_sha256": sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": sha256_tree(Path("/candidate")),
}
for key, digest in observed.items():
    print(f"{key}: expected={hashes[key]} observed={digest} match={hashes[key] == digest}")
    assert hashes[key] == digest

print("resolved_input_sha256: expected=",
      audit_document["resolved_input_sha256"],
      "observed=", resolved_digest,
      "match=", audit_document["resolved_input_sha256"] == resolved_digest)
assert audit_document["resolved_input_sha256"] == resolved_digest

expected_source_hashes = resolution["stage1_source_hashes"]
actual_source_hashes = {}
for root, dirs, files in os.walk("/reference/k-proof"):
    dirs.sort()
    files.sort()
    for filename in files:
        path = Path(root) / filename
        assert path.is_file() and not path.is_symlink()
        relative = path.relative_to("/reference/k-proof").as_posix()
        actual_source_hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
print("stage1_source_hash_count: expected=", len(expected_source_hashes),
      "observed=", len(actual_source_hashes),
      "exact_match=", expected_source_hashes == actual_source_hashes)
assert expected_source_hashes == actual_source_hashes

generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
target = target_statement(generated)
expected_definition = expected_target_definition(obligation_map)

print("generator.generated_tree_sha256 =", generator_manifest["generated_tree_sha256"])
print("actual.generated_tree_sha256 =", observed["generated_tree_sha256"])
assert generator_manifest["generated_tree_sha256"] == observed["generated_tree_sha256"]
print("generator.obligation_map_sha256 =", generator_manifest["obligation_map_sha256"])
actual_obligation_map_hash = hashlib.sha256((generated / "obligation-map.json").read_bytes()).hexdigest()
print("actual.obligation_map_sha256 =", actual_obligation_map_hash)
assert generator_manifest["obligation_map_sha256"] == actual_obligation_map_hash
print("input.verification_sha256 =", input_manifest["verification_sha256"])
actual_verification_hash = hashlib.sha256(Path("/reference/k-proof/verification.k").read_bytes()).hexdigest()
print("actual.verification_sha256 =", actual_verification_hash)
assert input_manifest["verification_sha256"] == actual_verification_hash
print("recomputed.target =", json.dumps(target, sort_keys=True))
print("manifest.target =", json.dumps(generator_manifest["target"], sort_keys=True))
print("audit_input.target =", json.dumps(resolution["target"], sort_keys=True))
assert target == generator_manifest["target"] == resolution["target"]
assert target["definition_sha256"] == sha256_text(expected_definition)
print("expected_target_definition =")
print(expected_definition)
print("MOUNTED_HASH_AND_TARGET_CHECK = PASS")

print("NOTE: lean_invocation_sha256 is launcher-recorded but its invocation tree is not mounted;")
print("      the audit-input envelope and all mounted source/project hashes are verified above.")
PY
