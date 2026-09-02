#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.pipeline_contract import _walk_regular_files, sha256_file, sha256_tree
from tools.stage6_resolution_contract import canonical_json_sha256 as resolution_sha256
from tools.stage6_resolution_contract import verify_audit_input


def report(label, expected, actual):
    print(f"{label}: expected={expected} actual={actual} match={expected == actual}")
    if expected != actual:
        raise SystemExit(f"MISMATCH: {label}")


audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
resolution, signed_digest = verify_audit_input(audit)
report("resolved_input_sha256", audit["resolved_input_sha256"], resolution_sha256(resolution))
report("audit_mode_env", resolution["mode"], __import__("os").environ.get("AUDIT_MODE"))
report("problem_id_env", resolution["problem_id"], __import__("os").environ.get("AUDIT_PROBLEM_ID"))
report("condition_env", resolution["condition"], __import__("os").environ.get("AUDIT_CONDITION"))
report("semantics_mode_env", resolution["semantics_mode"], __import__("os").environ.get("AUDIT_SEMANTICS_MODE"))
report("mounted_audit_input_copy", sha256_file(audit_path), sha256_file(Path("/audit-output/audit-input.json")))

hashes = resolution["hashes"]
report("k_workspace_sha256", hashes["k_workspace_sha256"], sha256_tree(Path("/reference/k-proof")))
report("stage1_export_sha256", hashes["stage1_export_sha256"], klean_export.tree_digest(Path("/reference/k-proof")))
report("discovery_manifest_sha256", hashes["discovery_manifest_sha256"], sha256_file(Path("/reference/lemma-discovery.json")))
report("k_audit_sha256", hashes["k_audit_sha256"], sha256_tree(Path("/reference/k-audit")))
report("klean_generation_sha256", hashes["klean_generation_sha256"], sha256_tree(Path("/reference/klean-generation")))
report("generation_producer_sources_sha256", hashes["generation_producer_sources_sha256"], sha256_tree(Path("/reference/generation-tools")))
report("generated_tree_sha256", hashes["generated_tree_sha256"], klean_export.tree_digest(Path("/reference/klean-generation/generated")))
report("lean_workspace_sha256", hashes["lean_workspace_sha256"], None)
report("lean_invocation_sha256", hashes["lean_invocation_sha256"], None)

actual_source_hashes = {
    path.relative_to(Path("/reference/k-proof")).as_posix(): sha256_file(path)
    for path in _walk_regular_files(Path("/reference/k-proof"), "mounted Stage 1 source workspace")
}
expected_source_hashes = resolution["stage1_source_hashes"]
print(f"stage1_source_hash_count: expected={len(expected_source_hashes)} actual={len(actual_source_hashes)}")
missing = sorted(set(expected_source_hashes) - set(actual_source_hashes))
extra = sorted(set(actual_source_hashes) - set(expected_source_hashes))
changed = sorted(
    name for name in set(expected_source_hashes) & set(actual_source_hashes)
    if expected_source_hashes[name] != actual_source_hashes[name]
)
print(f"stage1_source_hash_mismatches: missing={missing} extra={extra} changed={changed}")
if missing or extra or changed:
    raise SystemExit("MISMATCH: Stage 1 source file hash map")

source_manifest = json.loads(Path("/reference/generation-tools/source-manifest.json").read_text())
generator_manifest = json.loads(Path("/reference/klean-generation/generator-manifest.json").read_text())
input_manifest = json.loads(Path("/reference/klean-generation/input-manifest.json").read_text())
export_result = json.loads(Path("/reference/klean-generation/export-result.json").read_text())
recorded_preflight = json.loads(Path("/reference/klean-generation/preflight.json").read_text())
trust_inventory_path = Path("/reference/klean-generation/trust-inventory.json")

report("producer_klean_export.py", generator_manifest["exporter_sha256"], sha256_file(Path("/reference/generation-tools/klean_export.py")))
report("producer_klean.py", generator_manifest["klean_py_sha256"], sha256_file(Path("/reference/generation-tools/klean.py")))
report("source_manifest_klean_export.py", source_manifest["files"]["klean_export.py"], generator_manifest["exporter_sha256"])
report("source_manifest_klean.py", source_manifest["files"]["klean.py"], generator_manifest["klean_py_sha256"])
image_id = generator_manifest["provenance"]["generator_image_id"]
report("source_manifest_generator_image_id", image_id, source_manifest["generator_image_id"])
report("audit_input_generator_image_id", image_id, "sha256:" + Path(resolution["generation_producer_sources"]).name)
report("producer_file_set", sorted(["source-manifest.json", "klean.py", "klean_export.py"]), sorted(path.name for path in Path("/reference/generation-tools").iterdir()))

inventory = inventory_verification(Path("/reference/k-proof"))
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
report("inventory_hash_vs_discovery", discovery["inventory_sha256"], inventory["inventory_sha256"])
report("inventory_hash_manual", inventory["inventory_sha256"], canonical_json_sha256(inventory["rules"]))
report("canonical_empty_inventory_hash", "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945", hashlib.sha256(b"[]").hexdigest())
report("inventory_rules_vs_discovery_rules", inventory["rules"], discovery["rules"])

report("input_manifest_stage1", hashes["stage1_export_sha256"], input_manifest["stage1_workspace_sha256"])
report("input_manifest_frozen", hashes["stage1_export_sha256"], input_manifest["frozen_input_sha256"])
report("input_manifest_discovery", hashes["discovery_manifest_sha256"], input_manifest["stage3_discovery_manifest_sha256"])
report("input_manifest_inventory", inventory["inventory_sha256"], input_manifest["inventory_sha256"])
report("input_manifest_verification", sha256_file(Path("/reference/k-proof/verification.k")), input_manifest["verification_sha256"])
report("generator_provenance_stage1", hashes["stage1_export_sha256"], generator_manifest["provenance"]["stage1_workspace_sha256"])
report("generator_provenance_discovery", hashes["discovery_manifest_sha256"], generator_manifest["provenance"]["stage3_discovery_manifest_sha256"])
report("generator_provenance_inventory", inventory["inventory_sha256"], generator_manifest["provenance"]["inventory_sha256"])
report("generator_tree", hashes["generated_tree_sha256"], generator_manifest["generated_tree_sha256"])
report("generator_toolchain_lock", json.loads(Path("/reference/klean-toolchain.lock.json").read_text()), generator_manifest["toolchain"])

report("export_result_stage1", hashes["stage1_export_sha256"], export_result["frozen_input_sha256"])
report("export_result_discovery", hashes["discovery_manifest_sha256"], export_result["stage3_discovery_manifest_sha256"])
report("export_result_tree", hashes["generated_tree_sha256"], export_result["generated_tree_sha256"])
report("export_result_trust_inventory", sha256_file(trust_inventory_path), export_result["trust_inventory_sha256"])
report("recorded_preflight_vs_audit_input", resolution["stage4_preflight"], recorded_preflight)
report("selection_k_audit", hashes["k_audit_sha256"], resolution["selections"]["k_audit"]["artifact_sha256"])
report("selection_generation", hashes["klean_generation_sha256"], resolution["selections"]["klean_generation"]["artifact_sha256"])

print("ALL_RECORDED_RESOLUTION_HASHES_MATCH")
