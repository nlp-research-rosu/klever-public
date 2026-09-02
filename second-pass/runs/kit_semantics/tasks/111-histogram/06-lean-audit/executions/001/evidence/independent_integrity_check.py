#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text())
    if not isinstance(document, dict):
        raise ValueError(f"not a JSON object: {path}")
    return document


def regular_file_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise ValueError(f"non-regular entry in source tree: {path}")
        hashes[path.relative_to(root).as_posix()] = sha256_file(path)
    return hashes


checks: dict[str, dict[str, Any]] = {}


def check(name: str, observed: Any, expected: Any) -> None:
    checks[name] = {
        "pass": observed == expected,
        "observed": observed,
        "expected": expected,
    }


audit = read_json(AUDIT_INPUT)
resolution, envelope_digest = stage6_resolution_contract.verify_audit_input(audit)
hashes = resolution["hashes"]
discovery = read_json(DISCOVERY)
generator = read_json(GENERATION / "generator-manifest.json")
input_manifest = read_json(GENERATION / "input-manifest.json")
obligation_map = read_json(GENERATED / "obligation-map.json")
export_result = read_json(GENERATION / "export-result.json")
preflight = read_json(GENERATION / "preflight.json")
source_manifest = read_json(PRODUCERS / "source-manifest.json")
toolchain = read_json(TOOLCHAIN_LOCK)
inventory = inventory_verification(K_WORKSPACE)
trust_inventory_hash = sha256_file(GENERATION / "trust-inventory.json")

check("audit_envelope_digest", envelope_digest, audit["resolved_input_sha256"])
check("mode_environment", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("mode", resolution["mode"], "CLASSIFICATION_ONLY")
check("semantics_mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")
check("condition", resolution["condition"], "kit-semantics")
check("problem", resolution["problem_id"], "111-histogram")

stage1_artifact_hash = pipeline_contract.sha256_tree(K_WORKSPACE)
stage1_export_hash = klean_export.tree_digest(K_WORKSPACE)
k_audit_hash = pipeline_contract.sha256_tree(K_AUDIT)
generation_hash = pipeline_contract.sha256_tree(GENERATION)
producer_tree_hash = pipeline_contract.sha256_tree(PRODUCERS)
generated_hash = klean_export.tree_digest(GENERATED)
discovery_hash = sha256_file(DISCOVERY)

check("k_workspace_tree", stage1_artifact_hash, hashes["k_workspace_sha256"])
check("stage1_export_tree", stage1_export_hash, hashes["stage1_export_sha256"])
check("k_audit_tree", k_audit_hash, hashes["k_audit_sha256"])
check("klean_generation_tree", generation_hash, hashes["klean_generation_sha256"])
check(
    "generation_producer_tree",
    producer_tree_hash,
    hashes["generation_producer_sources_sha256"],
)
check("generated_tree", generated_hash, hashes["generated_tree_sha256"])
check("discovery_file", discovery_hash, hashes["discovery_manifest_sha256"])
check("lean_workspace_hash_absent", hashes["lean_workspace_sha256"], None)
check("lean_invocation_hash_absent", hashes["lean_invocation_sha256"], None)
check("selected_k_audit_tree", resolution["selections"]["k_audit"]["artifact_sha256"], k_audit_hash)
check("selected_generation_tree", resolution["selections"]["klean_generation"]["artifact_sha256"], generation_hash)
check("embedded_stage4_preflight", resolution["stage4_preflight"], preflight)

observed_stage1_files = regular_file_hashes(K_WORKSPACE)
expected_stage1_files = resolution["stage1_source_hashes"]
stage1_missing = sorted(set(expected_stage1_files) - set(observed_stage1_files))
stage1_extra = sorted(set(observed_stage1_files) - set(expected_stage1_files))
stage1_changed = sorted(
    name
    for name in set(observed_stage1_files) & set(expected_stage1_files)
    if observed_stage1_files[name] != expected_stage1_files[name]
)
check("stage1_file_count", len(observed_stage1_files), len(expected_stage1_files))
check("stage1_missing_files", stage1_missing, [])
check("stage1_extra_files", stage1_extra, [])
check("stage1_changed_files", stage1_changed, [])

producer_names = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in PRODUCERS.iterdir()
)
check(
    "producer_file_set",
    producer_names,
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
producer_hashes = {
    "klean.py": sha256_file(PRODUCERS / "klean.py"),
    "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
}
check("producer_hashes_source_manifest", producer_hashes, source_manifest["files"])
check(
    "producer_exporter_generator_manifest",
    producer_hashes["klean_export.py"],
    generator["exporter_sha256"],
)
check(
    "producer_klean_generator_manifest",
    producer_hashes["klean.py"],
    generator["klean_py_sha256"],
)
generator_image_id = generator["provenance"]["generator_image_id"]
check("producer_image_source_manifest", source_manifest["generator_image_id"], generator_image_id)
check(
    "producer_image_audit_input_path",
    Path(resolution["generation_producer_sources"]).name,
    generator_image_id.removeprefix("sha256:"),
)

check("generator_toolchain", generator["toolchain"], toolchain)
check("generator_generated_tree", generator["generated_tree_sha256"], generated_hash)
check("input_frozen_tree", input_manifest["frozen_input_sha256"], stage1_export_hash)
check("input_stage1_tree", input_manifest["stage1_workspace_sha256"], stage1_export_hash)
check("input_discovery_hash", input_manifest["stage3_discovery_manifest_sha256"], discovery_hash)
check("input_verification_hash", input_manifest["verification_sha256"], sha256_file(K_WORKSPACE / "verification.k"))
check("generator_stage1_provenance", generator["provenance"]["stage1_workspace_sha256"], stage1_export_hash)
check("generator_discovery_provenance", generator["provenance"]["stage3_discovery_manifest_sha256"], discovery_hash)
check("export_frozen_tree", export_result["frozen_input_sha256"], stage1_export_hash)
check("export_generated_tree", export_result["generated_tree_sha256"], generated_hash)
check("export_discovery_hash", export_result["stage3_discovery_manifest_sha256"], discovery_hash)
check("export_trust_inventory_hash", export_result["trust_inventory_sha256"], trust_inventory_hash)

reconstructed_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
check("inventory_hash_discovery", inventory["inventory_sha256"], discovery["inventory_sha256"])
check("inventory_hash_input_manifest", inventory["inventory_sha256"], input_manifest["inventory_sha256"])
check("inventory_hash_generator", inventory["inventory_sha256"], generator["provenance"]["inventory_sha256"])
check("classified_identity_order", classified_ids, reconstructed_ids)
check("classified_identity_uniqueness", len(set(classified_ids)), len(classified_ids))
check("reconstructed_identity_uniqueness", len(set(reconstructed_ids)), len(reconstructed_ids))
check("verification_module", inventory["verification_module"], input_manifest["verification_module"])
check("verification_module_closure", inventory["verification_modules"], ["COUNT-SUMMARY", "VERIFICATION"])

discovery_by_id = {rule["source_rule_id"]: rule for rule in discovery["rules"]}
enriched = []
for rule in inventory["rules"]:
    classification = discovery_by_id[rule["source_rule_id"]]
    enriched.append({
        **rule,
        "classification": classification["classification"],
        "rationale": classification["rationale"],
    })
check("enriched_definition_bijection", input_manifest["definitions"], enriched)
check("operational_rule_set", input_manifest["operational_rules"], [])
check("proved_derived_lemma_set", input_manifest["proved_derived_lemmas"], [])
check("domain_source_rule_set", input_manifest["source_rules"], [])
check("obligation_map_source_rule_set", obligation_map["source_rules"], [])
check("obligation_set", obligation_map["obligations"], [])
check("trust_parameter_set", obligation_map["trust_parameters"], [])
check("generator_obligation_count", generator["obligation_count"], 0)
check("export_obligation_count", export_result["obligation_count"], 0)
check("preflight_obligation_count", preflight["obligation_count"], 0)
check("obligation_map_hash", sha256_file(GENERATED / "obligation-map.json"), generator["obligation_map_sha256"])

target = klean_export.target_statement(GENERATED)
check("detected_target", target, None)
check("generator_target", generator["target"], None)
check("audit_target", resolution["target"], None)
check("preflight_target", preflight["target"], None)
check("stage5_result", resolution["stage5_result"], None)
check("candidate_absent", Path("/candidate").exists(), False)
check("generation_status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
check("export_status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check("preflight_status", preflight["status"], "KLEAN_NO_OBLIGATIONS")

failed = sorted(name for name, result in checks.items() if not result["pass"])
summary = {
    "schema_version": 1,
    "pass": not failed,
    "check_count": len(checks),
    "failed_checks": failed,
    "inventory_rule_count": len(inventory["rules"]),
    "stage1_regular_file_count": len(observed_stage1_files),
    "checks": checks,
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(0 if not failed else 1)
