#!/usr/bin/env python3
"""Independent immutable-input, inventory, and Stage 4 structural checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object, results: dict) -> None:
    passed = observed == expected
    results[label] = {
        "expected": expected,
        "observed": observed,
        "pass": passed,
    }
    if not passed:
        raise AssertionError(f"{label}: {observed!r} != {expected!r}")


def main() -> None:
    audit_input = json.loads(Path("/audit-input.json").read_text())
    resolution = audit_input["resolution"]
    recorded = resolution["hashes"]
    generation = Path("/reference/klean-generation")
    generated = generation / "generated"
    k_proof = Path("/reference/k-proof")
    k_audit = Path("/reference/k-audit")
    discovery_path = Path("/reference/lemma-discovery.json")
    producers = Path("/reference/generation-tools")
    results: dict[str, object] = {}

    check("mode_env_contract", resolution["mode"], "CLASSIFICATION_ONLY", results)
    check("lean_workspace_null", resolution["lean_workspace"], None, results)
    check("lean_invocation_null", resolution["lean_invocation"], None, results)
    check("candidate_absent", Path("/candidate").exists(), False, results)

    check(
        "k_workspace_sha256",
        pipeline_contract.sha256_tree(k_proof),
        recorded["k_workspace_sha256"],
        results,
    )
    check(
        "stage1_export_sha256",
        klean_export.tree_digest(k_proof),
        recorded["stage1_export_sha256"],
        results,
    )
    check(
        "k_audit_sha256",
        pipeline_contract.sha256_tree(k_audit),
        recorded["k_audit_sha256"],
        results,
    )
    check(
        "klean_generation_sha256",
        pipeline_contract.sha256_tree(generation),
        recorded["klean_generation_sha256"],
        results,
    )
    check(
        "generated_tree_sha256",
        klean_export.tree_digest(generated),
        recorded["generated_tree_sha256"],
        results,
    )
    check(
        "generation_producer_sources_sha256",
        pipeline_contract.sha256_tree(producers),
        recorded["generation_producer_sources_sha256"],
        results,
    )
    check(
        "discovery_manifest_sha256",
        sha256(discovery_path),
        recorded["discovery_manifest_sha256"],
        results,
    )
    check("lean_workspace_sha256_null", recorded["lean_workspace_sha256"], None, results)
    check("lean_invocation_sha256_null", recorded["lean_invocation_sha256"], None, results)

    actual_source_hashes = {
        path.relative_to(k_proof).as_posix(): sha256(path)
        for path in pipeline_contract._walk_regular_files(k_proof, "Stage 1 source workspace")
    }
    recorded_source_hashes = resolution["stage1_source_hashes"]
    source_hash_mismatches = sorted(
        name
        for name in actual_source_hashes.keys() & recorded_source_hashes.keys()
        if actual_source_hashes[name] != recorded_source_hashes[name]
    )
    missing_source_hashes = sorted(recorded_source_hashes.keys() - actual_source_hashes.keys())
    extra_source_hashes = sorted(actual_source_hashes.keys() - recorded_source_hashes.keys())
    results["stage1_source_hashes"] = {
        "expected_count": len(recorded_source_hashes),
        "observed_count": len(actual_source_hashes),
        "mismatches": source_hash_mismatches,
        "missing": missing_source_hashes,
        "extra": extra_source_hashes,
        "pass": not source_hash_mismatches and not missing_source_hashes and not extra_source_hashes,
    }
    if not results["stage1_source_hashes"]["pass"]:
        raise AssertionError("Stage 1 per-file source hashes differ")
    results["stage1_source_hash_count"] = len(actual_source_hashes)

    source_manifest = json.loads((producers / "source-manifest.json").read_text())
    generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
    source_files = {
        "klean.py": sha256(producers / "klean.py"),
        "klean_export.py": sha256(producers / "klean_export.py"),
    }
    check("producer_files_source_manifest", source_files, source_manifest["files"], results)
    check(
        "producer_exporter_generator_manifest",
        source_files["klean_export.py"],
        generator_manifest["exporter_sha256"],
        results,
    )
    check(
        "producer_klean_generator_manifest",
        source_files["klean.py"],
        generator_manifest["klean_py_sha256"],
        results,
    )
    generator_image = generator_manifest["provenance"]["generator_image_id"]
    check("generator_image_source_manifest", source_manifest["generator_image_id"], generator_image, results)
    audit_path_image = "sha256:" + Path(resolution["generation_producer_sources"]).name
    check("generator_image_audit_input_path", audit_path_image, generator_image, results)
    check(
        "producer_bundle_exact_files",
        sorted(path.relative_to(producers).as_posix() for path in producers.iterdir()),
        ["klean.py", "klean_export.py", "source-manifest.json"],
        results,
    )

    inventory = inventory_verification(k_proof)
    validated = validate_trust_boundary(k_proof, discovery_path)
    discovery = json.loads(discovery_path.read_text())
    check("inventory_hash_discovery", inventory["inventory_sha256"], discovery["inventory_sha256"], results)
    check("inventory_hash_validated", inventory["inventory_sha256"], validated["inventory_sha256"], results)
    reconstructed_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
    check("inventory_rule_id_order", reconstructed_ids, discovery_ids, results)
    check("inventory_no_duplicate_ids", len(set(reconstructed_ids)), len(reconstructed_ids), results)
    check("inventory_verification_module", inventory["verification_module"], "VERIFICATION", results)
    check("inventory_module_closure", inventory["verification_modules"], ["VERIFICATION"], results)
    results["reconstructed_inventory"] = inventory

    independent_classes = {
        reconstructed_ids[0]: "DEFINITION",
        reconstructed_ids[1]: "DEFINITION",
        reconstructed_ids[2]: "DEFINITION",
        reconstructed_ids[3]: "DEFINITION",
    }
    observed_classes = {
        rule["source_rule_id"]: rule["classification"] for rule in discovery["rules"]
    }
    check("independent_classifications", observed_classes, independent_classes, results)
    independent_domain_ids = [
        source_rule_id
        for source_rule_id, classification in independent_classes.items()
        if classification == "DOMAIN_LEMMA"
    ]
    check("independent_domain_ids", independent_domain_ids, [], results)
    check(
        "no_simplification_attributes",
        [rule["source_rule_id"] for rule in inventory["rules"] if "simplification" in rule["attributes"]],
        [],
        results,
    )

    input_manifest = json.loads((generation / "input-manifest.json").read_text())
    obligation_map_path = generated / "obligation-map.json"
    obligation_map = json.loads(obligation_map_path.read_text())
    export_result = json.loads((generation / "export-result.json").read_text())
    trust_inventory_path = generation / "trust-inventory.json"
    trust_inventory = json.loads(trust_inventory_path.read_text())
    lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())

    check("input_inventory_hash", input_manifest["inventory_sha256"], inventory["inventory_sha256"], results)
    check(
        "input_verification_hash",
        input_manifest["verification_sha256"],
        sha256(k_proof / "verification.k"),
        results,
    )
    check("input_definitions_ids", [r["source_rule_id"] for r in input_manifest["definitions"]], reconstructed_ids, results)
    check("input_source_rules", input_manifest["source_rules"], [], results)
    check("obligation_map_source_rules", obligation_map["source_rules"], [], results)
    check("obligation_map_obligations", obligation_map["obligations"], [], results)
    check("obligation_map_trust_parameters", obligation_map["trust_parameters"], [], results)
    check("generator_obligation_count", generator_manifest["obligation_count"], 0, results)
    check("export_obligation_count", export_result["obligation_count"], 0, results)
    check("export_status", export_result["status"], "KLEAN_NO_OBLIGATIONS", results)
    check(
        "obligation_map_sha256",
        sha256(obligation_map_path),
        generator_manifest["obligation_map_sha256"],
        results,
    )
    check(
        "trust_inventory_sha256",
        sha256(trust_inventory_path),
        export_result["trust_inventory_sha256"],
        results,
    )
    check("generator_toolchain", generator_manifest["toolchain"], lock, results)
    check("generator_target_null", generator_manifest["target"], None, results)
    check("actual_target_null", klean_export.target_statement(generated), None, results)
    check("generated_tree_manifest", generator_manifest["generated_tree_sha256"], klean_export.tree_digest(generated), results)
    check("export_generated_tree", export_result["generated_tree_sha256"], klean_export.tree_digest(generated), results)
    check("trust_designated_sorries", trust_inventory["designated_sorries"], 0, results)
    check("trust_other_sorries", trust_inventory["other_sorries"], 0, results)
    results["trust_allowlist_count"] = len(trust_inventory["allowlist"])
    results["all_checks_pass"] = all(
        not isinstance(value, dict) or value.get("pass") is not False
        for value in results.values()
    )
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
