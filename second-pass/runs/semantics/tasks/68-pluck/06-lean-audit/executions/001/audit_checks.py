#!/usr/bin/env python3
"""Independent mechanical cross-checks for the 68-pluck Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

from tools import k_rule_inventory
from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract
from tools import stage6_resolution_contract


ROOT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
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
                result[path.relative_to(root).as_posix()] = file_sha256(path)
            else:
                raise RuntimeError(f"unsupported tree entry: {path}")
    return dict(sorted(result.items()))


def mismatch(expected: Any, actual: Any) -> dict[str, Any]:
    return {
        "expected": expected,
        "actual": actual,
        "match": expected == actual,
    }


def main() -> None:
    envelope = json.loads(ROOT_INPUT.read_text())
    resolution, signed_digest = stage6_resolution_contract.verify_audit_input(
        envelope
    )
    recorded_hashes = resolution["hashes"]

    inventory = k_rule_inventory.inventory_verification(WORKSPACE)
    validated = lemma_discovery_contract.validate_trust_boundary(
        WORKSPACE, DISCOVERY
    )
    discovery = json.loads(DISCOVERY.read_text())
    inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
    source_lines = (WORKSPACE / "verification.k").read_text().splitlines()
    span_checks: list[dict[str, Any]] = []
    for rule in inventory["rules"]:
        extracted = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        normalized_sha256 = hashlib.sha256(
            " ".join(extracted.split()).encode()
        ).hexdigest()
        span_checks.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "span": [rule["start_line"], rule["end_line"]],
                "text_exact": extracted == rule["text"],
                "normalized_sha256": mismatch(
                    rule["normalized_sha256"], normalized_sha256
                ),
                "source_rule_id_recomputed": mismatch(
                    rule["source_rule_id"], f"rule-{normalized_sha256}"
                ),
            }
        )

    source_manifest = json.loads(
        (PRODUCERS / "source-manifest.json").read_text()
    )
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    preflight = json.loads((GENERATION / "preflight.json").read_text())
    trust_inventory = json.loads(
        (GENERATION / "trust-inventory.json").read_text()
    )
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )
    toolchain_lock = json.loads(
        Path("/reference/klean-toolchain.lock.json").read_text()
    )

    actual_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(WORKSPACE),
        "discovery_manifest_sha256": file_sha256(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(
            Path("/reference/k-audit")
        ),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": (
            pipeline_contract.sha256_tree(PRODUCERS)
        ),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    recorded_source_hashes = resolution["stage1_source_hashes"]
    actual_source_hashes = regular_file_hashes(WORKSPACE)

    manifest_classified = {
        "definitions": input_manifest.get("definitions"),
        "operational_rules": input_manifest.get("operational_rules"),
        "proved_derived_lemmas": input_manifest.get("proved_derived_lemmas"),
        "source_rules": input_manifest.get("source_rules"),
    }
    validated_classified = {
        "definitions": validated["definitions"],
        "operational_rules": validated["operational_rules"],
        "proved_derived_lemmas": validated["proved_derived_lemmas"],
        "source_rules": validated["domain_lemmas"],
    }
    producer_image = generator_manifest["provenance"]["generator_image_id"]
    producer_key = producer_image.removeprefix("sha256:")
    producer_checks = {
        "source_manifest_exact_keys": (
            set(source_manifest)
            == {"schema_version", "generator_image_id", "files"}
        ),
        "source_bundle_exact_files": (
            set(regular_file_hashes(PRODUCERS))
            == {"klean.py", "klean_export.py", "source-manifest.json"}
        ),
        "image_source_vs_generator": mismatch(
            source_manifest.get("generator_image_id"), producer_image
        ),
        "image_audit_path_vs_generator": mismatch(
            Path(resolution["generation_producer_sources"]).name, producer_key
        ),
        "exporter_file_vs_source_manifest": mismatch(
            source_manifest["files"]["klean_export.py"],
            file_sha256(PRODUCERS / "klean_export.py"),
        ),
        "exporter_file_vs_generator_manifest": mismatch(
            generator_manifest["exporter_sha256"],
            file_sha256(PRODUCERS / "klean_export.py"),
        ),
        "klean_file_vs_source_manifest": mismatch(
            source_manifest["files"]["klean.py"],
            file_sha256(PRODUCERS / "klean.py"),
        ),
        "klean_file_vs_generator_manifest": mismatch(
            generator_manifest["klean_py_sha256"],
            file_sha256(PRODUCERS / "klean.py"),
        ),
        "producer_tree_vs_audit_input": mismatch(
            recorded_hashes["generation_producer_sources_sha256"],
            actual_hashes["generation_producer_sources_sha256"],
        ),
    }

    simplification_violations = [
        entry["source_rule_id"]
        for entry, rule in zip(discovery["rules"], inventory["rules"], strict=True)
        if "simplification" in rule["attributes"]
        and entry["classification"] not in {"DEFINITION", "DOMAIN_LEMMA"}
    ]
    report = {
        "audit_envelope": {
            "verified": True,
            "signed_resolution_sha256": signed_digest,
            "mode": resolution["mode"],
            "audit_mode_environment": os.environ.get("AUDIT_MODE"),
            "mode_match": resolution["mode"] == os.environ.get("AUDIT_MODE"),
        },
        "producer_gate": producer_checks,
        "recorded_hash_checks": {
            key: mismatch(recorded_hashes[key], actual_hashes[key])
            for key in recorded_hashes
        },
        "stage1_source_hashes": {
            "recorded_count": len(recorded_source_hashes),
            "actual_count": len(actual_source_hashes),
            "exact_path_and_hash_match": (
                recorded_source_hashes == actual_source_hashes
            ),
            "missing_from_actual": sorted(
                set(recorded_source_hashes) - set(actual_source_hashes)
            ),
            "extra_in_actual": sorted(
                set(actual_source_hashes) - set(recorded_source_hashes)
            ),
            "changed": sorted(
                name
                for name in set(recorded_source_hashes) & set(actual_source_hashes)
                if recorded_source_hashes[name] != actual_source_hashes[name]
            ),
        },
        "inventory": {
            "verification_module": inventory["verification_module"],
            "verification_modules": inventory["verification_modules"],
            "verification_sha256": inventory["verification_sha256"],
            "rule_count": len(inventory["rules"]),
            "unique_id_count": len(set(inventory_ids)),
            "inventory_sha256": inventory["inventory_sha256"],
            "inventory_sha256_recomputed": (
                k_rule_inventory.canonical_json_sha256(inventory["rules"])
            ),
            "manifest_inventory_sha256": discovery["inventory_sha256"],
            "manifest_rule_count": len(discovery["rules"]),
            "ordered_bijection": inventory_ids == discovery_ids,
            "omitted_ids": sorted(set(inventory_ids) - set(discovery_ids)),
            "extra_ids": sorted(set(discovery_ids) - set(inventory_ids)),
            "duplicate_manifest_ids": (
                len(discovery_ids) - len(set(discovery_ids))
            ),
            "span_hash_id_checks": span_checks,
            "simplification_classification_violations": (
                simplification_violations
            ),
        },
        "classification_counts": {
            "DEFINITION": len(validated["definitions"]),
            "OPERATIONAL_RULE": len(validated["operational_rules"]),
            "PROVED_DERIVED_LEMMA": len(
                validated["proved_derived_lemmas"]
            ),
            "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
        },
        "stage4_bijection": {
            "input_manifest_matches_validated_classification": (
                manifest_classified == validated_classified
            ),
            "input_inventory_sha256": mismatch(
                inventory["inventory_sha256"],
                input_manifest.get("inventory_sha256"),
            ),
            "input_verification_sha256": mismatch(
                inventory["verification_sha256"],
                input_manifest.get("verification_sha256"),
            ),
            "source_rules": obligation_map.get("source_rules"),
            "obligations": obligation_map.get("obligations"),
            "trust_parameters": obligation_map.get("trust_parameters"),
            "obligation_map_sha256": mismatch(
                generator_manifest["obligation_map_sha256"],
                file_sha256(GENERATED / "obligation-map.json"),
            ),
            "target_statement_from_generated": (
                klean_export.target_statement(GENERATED)
            ),
            "generator_target": generator_manifest.get("target"),
            "audit_input_target": resolution.get("target"),
            "export_status": export_result.get("status"),
            "preflight_status": preflight.get("status"),
            "selection_status": resolution["selections"][
                "klean_generation"
            ]["status"],
            "obligation_count_generator": generator_manifest.get(
                "obligation_count"
            ),
            "obligation_count_export": export_result.get("obligation_count"),
            "obligation_count_preflight": preflight.get("obligation_count"),
            "toolchain_lock_match": (
                generator_manifest.get("toolchain") == toolchain_lock
            ),
            "stage4_preflight_matches_audit_input": (
                preflight == resolution["stage4_preflight"]
            ),
            "trust_inventory_designated_sorries": trust_inventory.get(
                "designated_sorries"
            ),
            "trust_inventory_other_sorries": trust_inventory.get(
                "other_sorries"
            ),
        },
        "classification_only_constraints": {
            "candidate_exists": Path("/candidate").exists(),
            "lean_workspace": resolution["lean_workspace"],
            "lean_invocation": resolution["lean_invocation"],
            "stage5_result": resolution["stage5_result"],
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
