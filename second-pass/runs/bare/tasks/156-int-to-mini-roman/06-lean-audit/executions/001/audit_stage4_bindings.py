#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
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
LOCK = Path("/reference/klean-toolchain.lock.json")
MECHANICAL_LOCK = Path("/opt/humaneval/data/klean-audit-tools.lock.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise TypeError(f"{path} is not an object")
    return value


def main() -> int:
    audit_document = load(AUDIT_INPUT)
    resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
        audit_document
    )
    discovery = load(DISCOVERY)
    input_manifest = load(GENERATION / "input-manifest.json")
    generator_manifest = load(GENERATION / "generator-manifest.json")
    export_result = load(GENERATION / "export-result.json")
    preflight = load(GENERATION / "preflight.json")
    trust_inventory = load(GENERATION / "trust-inventory.json")
    obligation_map = load(GENERATED / "obligation-map.json")
    source_manifest = load(PRODUCERS / "source-manifest.json")
    lock = load(LOCK)
    mechanical_lock = load(MECHANICAL_LOCK)
    inventory = inventory_verification(K_WORKSPACE)

    observed_source_hashes = {
        path.relative_to(K_WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
        for path in pipeline_contract._walk_regular_files(
            K_WORKSPACE, "mounted Stage 1 source workspace"
        )
    }
    observed_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
        "discovery_manifest_sha256": file_sha256(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            PRODUCERS
        ),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }

    producer_hashes = {
        "klean_export.py": file_sha256(PRODUCERS / "klean_export.py"),
        "klean.py": file_sha256(PRODUCERS / "klean.py"),
    }
    producer_image_id = generator_manifest["provenance"]["generator_image_id"]
    producer_image_key = producer_image_id.removeprefix("sha256:")
    recorded_bundle_key = Path(
        resolution["generation_producer_sources"]
    ).name

    source_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    discovered_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
    definition_ids = [
        rule["source_rule_id"] for rule in input_manifest["definitions"]
    ]
    exported_source_ids = [
        rule["source_rule_id"] for rule in obligation_map["source_rules"]
    ]
    obligation_ids = [
        obligation["source_rule_id"] for obligation in obligation_map["obligations"]
    ]

    # Independent classification judgment: both local-closure rules are
    # definitions, so the mathematically required DOMAIN_LEMMA set is empty.
    independently_classified_domain_ids: list[str] = []

    lean_declarations: list[dict[str, str]] = []
    for source in sorted(GENERATED.rglob("*.lean")):
        for line_number, line in enumerate(source.read_text().splitlines(), 1):
            match = re.match(
                r"^\s*(theorem|lemma)\s+([A-Za-z0-9_'.«»]+)", line
            )
            if match:
                lean_declarations.append(
                    {
                        "file": source.relative_to(GENERATED).as_posix(),
                        "line": str(line_number),
                        "kind": match.group(1),
                        "name": match.group(2),
                    }
                )

    preflight_log_lines = (
        GENERATION / "preflight.log"
    ).read_text().splitlines()
    export_log_lines = (GENERATION / "export.log").read_text().splitlines()

    checks = {
        "mechanical_checker_lock": {
            "recorded_lock_sha256": audit_document["audit"][
                "mechanical_checker_lock_sha256"
            ],
            "observed_lock_sha256": file_sha256(MECHANICAL_LOCK),
            "file_hashes": {
                relative: {
                    "recorded": expected,
                    "observed": file_sha256(Path("/reference") / relative),
                    "match": expected
                    == file_sha256(Path("/reference") / relative),
                }
                for relative, expected in mechanical_lock["files"].items()
            },
            "match": (
                audit_document["audit"]["mechanical_checker_lock_sha256"]
                == file_sha256(MECHANICAL_LOCK)
                and all(
                    expected == file_sha256(Path("/reference") / relative)
                    for relative, expected in mechanical_lock["files"].items()
                )
            ),
        },
        "audit_input_envelope_digest": {
            "recorded": audit_document["resolved_input_sha256"],
            "recomputed": resolved_digest,
            "match": audit_document["resolved_input_sha256"] == resolved_digest,
        },
        "launcher_identity": {
            "audit_mode_env": os.environ.get("AUDIT_MODE"),
            "recorded_mode": resolution["mode"],
            "problem": resolution["problem_id"],
            "condition": resolution["condition"],
            "semantics_mode": resolution["semantics_mode"],
            "match": (
                os.environ.get("AUDIT_MODE") == resolution["mode"]
                and resolution["mode"] == "CLASSIFICATION_ONLY"
                and resolution["problem_id"] == "156-int-to-mini-roman"
                and resolution["condition"] == "bare"
                and resolution["semantics_mode"] == "GENERATED_SEMANTICS"
            ),
        },
        "all_resolution_hashes": {
            key: {
                "recorded": resolution["hashes"][key],
                "observed": value,
                "match": resolution["hashes"][key] == value,
            }
            for key, value in observed_hashes.items()
        },
        "stage1_source_hashes": {
            "recorded_count": len(resolution["stage1_source_hashes"]),
            "observed_count": len(observed_source_hashes),
            "match": resolution["stage1_source_hashes"] == observed_source_hashes,
        },
        "selection_artifact_hashes": {
            "k_audit": (
                resolution["selections"]["k_audit"]["artifact_sha256"]
                == observed_hashes["k_audit_sha256"]
            ),
            "klean_generation": (
                resolution["selections"]["klean_generation"]["artifact_sha256"]
                == observed_hashes["klean_generation_sha256"]
            ),
            "match": (
                resolution["selections"]["k_audit"]["artifact_sha256"]
                == observed_hashes["k_audit_sha256"]
                and resolution["selections"]["klean_generation"][
                    "artifact_sha256"
                ]
                == observed_hashes["klean_generation_sha256"]
            ),
        },
        "producer_authentication": {
            "observed_file_hashes": producer_hashes,
            "source_manifest_file_hashes": source_manifest["files"],
            "generator_exporter_hash": generator_manifest["exporter_sha256"],
            "generator_klean_hash": generator_manifest["klean_py_sha256"],
            "source_manifest_image_id": source_manifest["generator_image_id"],
            "generator_image_id": producer_image_id,
            "audit_input_bundle_key": recorded_bundle_key,
            "expected_image_key": producer_image_key,
            "exact_bundle_files": sorted(
                path.name for path in PRODUCERS.iterdir()
            ),
            "match": (
                producer_hashes == source_manifest["files"]
                and producer_hashes["klean_export.py"]
                == generator_manifest["exporter_sha256"]
                and producer_hashes["klean.py"]
                == generator_manifest["klean_py_sha256"]
                and source_manifest["generator_image_id"] == producer_image_id
                and recorded_bundle_key == producer_image_key
                and sorted(path.name for path in PRODUCERS.iterdir())
                == ["klean.py", "klean_export.py", "source-manifest.json"]
            ),
        },
        "inventory_bindings": {
            "reconstructed_inventory_sha256": inventory["inventory_sha256"],
            "discovery_inventory_sha256": discovery["inventory_sha256"],
            "input_manifest_inventory_sha256": input_manifest["inventory_sha256"],
            "generator_inventory_sha256": generator_manifest["provenance"][
                "inventory_sha256"
            ],
            "source_ids": source_ids,
            "discovered_ids": discovered_ids,
            "definition_ids": definition_ids,
            "match": (
                source_ids == discovered_ids == definition_ids
                and inventory["inventory_sha256"]
                == discovery["inventory_sha256"]
                == input_manifest["inventory_sha256"]
                == generator_manifest["provenance"]["inventory_sha256"]
            ),
        },
        "obligation_bijection": {
            "independent_domain_ids": independently_classified_domain_ids,
            "input_manifest_source_rules": [
                rule["source_rule_id"]
                for rule in input_manifest["source_rules"]
            ],
            "exported_source_ids": exported_source_ids,
            "obligation_ids": obligation_ids,
            "obligation_count_manifest": generator_manifest["obligation_count"],
            "obligation_count_export_result": export_result["obligation_count"],
            "obligation_map_sha256_recorded": generator_manifest[
                "obligation_map_sha256"
            ],
            "obligation_map_sha256_observed": file_sha256(
                GENERATED / "obligation-map.json"
            ),
            "match": (
                independently_classified_domain_ids
                == [
                    rule["source_rule_id"]
                    for rule in input_manifest["source_rules"]
                ]
                == exported_source_ids
                == obligation_ids
                and generator_manifest["obligation_count"] == 0
                and export_result["obligation_count"] == 0
                and generator_manifest["obligation_map_sha256"]
                == file_sha256(GENERATED / "obligation-map.json")
            ),
        },
        "fixed_target": {
            "generator_manifest": generator_manifest["target"],
            "preflight": preflight["target"],
            "audit_input": resolution["target"],
            "mechanically_parsed": klean_export.target_statement(GENERATED),
            "lean_theorem_or_lemma_declarations": lean_declarations,
            "candidate_present": Path("/candidate").exists(),
            "match": (
                generator_manifest["target"] is None
                and preflight["target"] is None
                and resolution["target"] is None
                and klean_export.target_statement(GENERATED) is None
                and not lean_declarations
                and not Path("/candidate").exists()
            ),
        },
        "toolchain_lock": {
            "match": generator_manifest["toolchain"] == lock,
            "value": lock,
        },
        "sidecar_and_log_bindings": {
            "export_result_trust_hash_matches": (
                export_result["trust_inventory_sha256"]
                == file_sha256(GENERATION / "trust-inventory.json")
            ),
            "export_result_generated_hash_matches": (
                export_result["generated_tree_sha256"]
                == observed_hashes["generated_tree_sha256"]
            ),
            "export_result_stage1_hash_matches": (
                export_result["frozen_input_sha256"]
                == observed_hashes["stage1_export_sha256"]
            ),
            "audit_preflight_exact_match": resolution["stage4_preflight"]
            == preflight,
            "preflight_log_embeds_export_result": (
                len(preflight_log_lines) == 2
                and json.loads(preflight_log_lines[0]) == export_result
            ),
            "preflight_log_embeds_preflight": (
                len(preflight_log_lines) == 2
                and json.loads(preflight_log_lines[1]) == preflight
            ),
            "export_log_exact_match": (
                len(export_log_lines) == 1
                and json.loads(export_log_lines[0]) == export_result
            ),
            "recorded_clean_output_hash_matches": (
                preflight["diagnostics"][0]["output_sha256"]
                == hashlib.sha256(
                    preflight["diagnostics"][0]["output_tail"].encode()
                ).hexdigest()
            ),
            "recorded_build_output_hash_matches": (
                preflight["diagnostics"][1]["output_sha256"]
                == hashlib.sha256(
                    preflight["diagnostics"][1]["output_tail"].encode()
                ).hexdigest()
            ),
            "match": (
                export_result["trust_inventory_sha256"]
                == file_sha256(GENERATION / "trust-inventory.json")
                and export_result["generated_tree_sha256"]
                == observed_hashes["generated_tree_sha256"]
                and export_result["frozen_input_sha256"]
                == observed_hashes["stage1_export_sha256"]
                and resolution["stage4_preflight"] == preflight
                and len(preflight_log_lines) == 2
                and json.loads(preflight_log_lines[0]) == export_result
                and json.loads(preflight_log_lines[1]) == preflight
                and len(export_log_lines) == 1
                and json.loads(export_log_lines[0]) == export_result
                and preflight["diagnostics"][0]["output_sha256"]
                == hashlib.sha256(
                    preflight["diagnostics"][0]["output_tail"].encode()
                ).hexdigest()
                and preflight["diagnostics"][1]["output_sha256"]
                == hashlib.sha256(
                    preflight["diagnostics"][1]["output_tail"].encode()
                ).hexdigest()
            ),
        },
        "status_consistency": {
            "selection": resolution["selections"]["klean_generation"]["status"],
            "preflight": preflight["status"],
            "export_result": export_result["status"],
            "match": (
                resolution["selections"]["klean_generation"]["status"]
                == preflight["status"]
                == export_result["status"]
                == "KLEAN_NO_OBLIGATIONS"
            ),
        },
        "trust_inventory_summary": {
            "allowlist_count": len(trust_inventory["allowlist"]),
            "designated_sorries": trust_inventory["designated_sorries"],
            "other_sorries": trust_inventory["other_sorries"],
        },
    }

    print(json.dumps(checks, indent=2, sort_keys=True))

    def all_true(value: Any) -> bool:
        if isinstance(value, dict):
            local_match = value.get("match")
            if local_match is False:
                return False
            return all(all_true(child) for child in value.values())
        if isinstance(value, list):
            return all(all_true(child) for child in value)
        return True

    return 0 if all_true(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
