#!/usr/bin/env python3
"""Read-only independent hash, provenance, and Stage 4 structure audit."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")
CHECKER_LOCK = Path("/opt/humaneval/data/klean-audit-tools.lock.json")
TRUSTED_TOOLS = Path("/reference/tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[path.relative_to(root).as_posix()] = sha256_file(path)
            else:
                raise RuntimeError(f"non-regular tree entry: {path}")
    return dict(sorted(result.items()))


def main() -> int:
    audit_input = json.loads(AUDIT_INPUT.read_text())
    resolution = audit_input["resolution"]
    hashes = resolution["hashes"]
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    export_result = json.loads(
        (GENERATION / "export-result.json").read_text()
    )
    preflight = json.loads((GENERATION / "preflight.json").read_text())
    trust_inventory = json.loads(
        (GENERATION / "trust-inventory.json").read_text()
    )
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )
    discovery = json.loads(DISCOVERY.read_text())
    source_manifest = json.loads(
        (PRODUCERS / "source-manifest.json").read_text()
    )
    toolchain_lock = json.loads(TOOLCHAIN_LOCK.read_text())
    checker_lock = json.loads(CHECKER_LOCK.read_text())

    pipeline_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            PRODUCERS
        ),
    }
    export_hashes = {
        "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    }
    direct_hashes = {
        "discovery_manifest_sha256": sha256_file(DISCOVERY),
        "verification_sha256": sha256_file(K_PROOF / "verification.k"),
        "obligation_map_sha256": sha256_file(
            GENERATED / "obligation-map.json"
        ),
        "trust_inventory_sha256": sha256_file(
            GENERATION / "trust-inventory.json"
        ),
        "checker_lock_sha256": sha256_file(CHECKER_LOCK),
        "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
        "klean.py": sha256_file(PRODUCERS / "klean.py"),
    }
    inventory = inventory_verification(K_PROOF)
    actual_stage1_files = regular_files(K_PROOF)

    source_ids = [entry.get("source_rule_id") for entry in discovery["rules"]]
    mapped_source_ids = [
        entry.get("source_rule_id") for entry in obligation_map["source_rules"]
    ]
    obligation_ids = [
        entry.get("source_rule_id") for entry in obligation_map["obligations"]
    ]
    target_scan_count = 0
    for path in sorted(GENERATED.rglob("*.lean")):
        target_scan_count += len(
            re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text())
        )
    target = klean_export.target_statement(GENERATED)

    producer_image_from_input = (
        "sha256:"
        + Path(resolution["generation_producer_sources"]).name
    )
    checks = {
        "audit_mode_matches_environment": (
            resolution["mode"] == os.environ.get("AUDIT_MODE")
        ),
        "classification_only_mode": resolution["mode"] == "CLASSIFICATION_ONLY",
        "candidate_absent": not Path("/candidate").exists(),
        "lean_paths_and_hashes_null": all(
            value is None
            for value in (
                resolution["lean_workspace"],
                resolution["lean_invocation"],
                hashes["lean_workspace_sha256"],
                hashes["lean_invocation_sha256"],
            )
        ),
        "recorded_pipeline_tree_hashes_match": all(
            hashes[key] == value for key, value in pipeline_hashes.items()
        ),
        "recorded_export_tree_hashes_match": all(
            hashes[key] == value for key, value in export_hashes.items()
        ),
        "selected_k_audit_hash_matches": (
            resolution["selections"]["k_audit"]["artifact_sha256"]
            == pipeline_hashes["k_audit_sha256"]
        ),
        "selected_generation_hash_matches": (
            resolution["selections"]["klean_generation"]["artifact_sha256"]
            == pipeline_hashes["klean_generation_sha256"]
        ),
        "all_stage1_file_names_and_hashes_match": (
            resolution["stage1_source_hashes"] == actual_stage1_files
        ),
        "discovery_hash_matches_audit_input": (
            direct_hashes["discovery_manifest_sha256"]
            == hashes["discovery_manifest_sha256"]
        ),
        "verification_hash_matches_input_manifest": (
            direct_hashes["verification_sha256"]
            == input_manifest["verification_sha256"]
        ),
        "inventory_is_empty": inventory["rules"] == [],
        "empty_inventory_hash_recomputed": (
            inventory["inventory_sha256"]
            == canonical_json_sha256([])
            == discovery["inventory_sha256"]
            == input_manifest["inventory_sha256"]
            == generator_manifest["provenance"]["inventory_sha256"]
        ),
        "source_rule_lists_are_bijective_and_empty": (
            source_ids == mapped_source_ids == obligation_ids == []
            and len(set(source_ids)) == len(source_ids)
        ),
        "obligation_map_hash_matches": (
            direct_hashes["obligation_map_sha256"]
            == generator_manifest["obligation_map_sha256"]
        ),
        "obligation_counts_and_status_match": (
            generator_manifest["obligation_count"]
            == export_result["obligation_count"]
            == preflight["obligation_count"]
            == 0
            and export_result["status"]
            == preflight["status"]
            == resolution["selections"]["klean_generation"]["status"]
            == "KLEAN_NO_OBLIGATIONS"
        ),
        "target_absent_by_parser_and_scan": (
            target is None
            and target_scan_count == 0
            and generator_manifest["target"] is None
            and preflight["target"] is None
        ),
        "no_vacuous_conjunct_or_parameter": (
            obligation_map["obligations"] == []
            and obligation_map["trust_parameters"] == []
        ),
        "stage1_export_provenance_matches": all(
            value == export_hashes["stage1_export_sha256"]
            for value in (
                input_manifest["frozen_input_sha256"],
                input_manifest["stage1_workspace_sha256"],
                generator_manifest["provenance"]["stage1_workspace_sha256"],
                export_result["frozen_input_sha256"],
                preflight["frozen_input_sha256"],
            )
        ),
        "stage3_provenance_matches": all(
            value == direct_hashes["discovery_manifest_sha256"]
            for value in (
                input_manifest["stage3_discovery_manifest_sha256"],
                generator_manifest["provenance"][
                    "stage3_discovery_manifest_sha256"
                ],
                export_result["stage3_discovery_manifest_sha256"],
                preflight["stage3_discovery_manifest_sha256"],
            )
        ),
        "generated_tree_provenance_matches": all(
            value == export_hashes["generated_tree_sha256"]
            for value in (
                generator_manifest["generated_tree_sha256"],
                export_result["generated_tree_sha256"],
                preflight["generated_tree_sha256"],
            )
        ),
        "trust_inventory_hash_matches": (
            direct_hashes["trust_inventory_sha256"]
            == export_result["trust_inventory_sha256"]
        ),
        "trust_inventory_has_no_sorries": (
            trust_inventory["designated_sorries"] == 0
            and trust_inventory["other_sorries"] == 0
        ),
        "pinned_toolchain_matches_manifest": (
            generator_manifest["toolchain"] == toolchain_lock
        ),
        "producer_bundle_file_set_exact": (
            set(regular_files(PRODUCERS))
            == {"klean_export.py", "klean.py", "source-manifest.json"}
        ),
        "producer_file_hashes_match_manifest_and_source_manifest": (
            source_manifest["files"]
            == {
                "klean_export.py": direct_hashes["klean_export.py"],
                "klean.py": direct_hashes["klean.py"],
            }
            == {
                "klean_export.py": generator_manifest["exporter_sha256"],
                "klean.py": generator_manifest["klean_py_sha256"],
            }
        ),
        "producer_image_id_three_way_match": (
            source_manifest["generator_image_id"]
            == generator_manifest["provenance"]["generator_image_id"]
            == producer_image_from_input
        ),
        "producer_bundle_hash_matches_audit_input": (
            pipeline_hashes["generation_producer_sources_sha256"]
            == hashes["generation_producer_sources_sha256"]
        ),
        "checker_lock_hash_matches_audit_input": (
            direct_hashes["checker_lock_sha256"]
            == audit_input["audit"]["mechanical_checker_lock_sha256"]
        ),
        "every_checker_source_hash_matches_lock": all(
            sha256_file(Path("/reference") / relative) == expected
            for relative, expected in checker_lock["files"].items()
        ),
    }

    output = {
        "checks": checks,
        "counts": {
            "stage1_regular_files": len(actual_stage1_files),
            "inventory_rules": len(inventory["rules"]),
            "classified_rules": len(discovery["rules"]),
            "mapped_source_rules": len(obligation_map["source_rules"]),
            "obligations": len(obligation_map["obligations"]),
            "trust_parameters": len(obligation_map["trust_parameters"]),
            "target_declarations": target_scan_count,
            "generated_allowlisted_trust_declarations": len(
                trust_inventory["allowlist"]
            ),
        },
        "pipeline_hashes": pipeline_hashes,
        "export_hashes": export_hashes,
        "direct_hashes": direct_hashes,
        "inventory": inventory,
        "producer_image_from_audit_input_path": producer_image_from_input,
        "target": target,
        "failed_checks": [name for name, passed in checks.items() if not passed],
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 1 if output["failed_checks"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
