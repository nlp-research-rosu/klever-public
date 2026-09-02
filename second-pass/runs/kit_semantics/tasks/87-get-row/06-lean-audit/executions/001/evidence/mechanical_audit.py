#!/usr/bin/env python3
"""Independent mechanical reconstruction and Stage 4 preflight evidence."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_audit_contract,
    klean_export,
    klean_preflight,
    lemma_discovery_contract,
    pipeline_contract,
)


OUT = Path("/audit-output/evidence")
AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(name: str, document: object) -> None:
    (OUT / name).write_text(
        json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    )


def all_regular_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"symlink in immutable tree: {path}")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = sha256_file(path)
        elif not path.is_dir():
            raise RuntimeError(f"unsupported entry in immutable tree: {path}")
    return result


def main() -> int:
    audit_document = json.loads(AUDIT_INPUT.read_text())
    resolution = audit_document["resolution"]
    hashes = resolution["hashes"]

    verified_resolution, audit_input_hash = (
        klean_audit_contract.verify_stage6_audit_input(audit_document)
    )

    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    producer_file_hashes = {
        name: sha256_file(PRODUCERS / name)
        for name in ("klean_export.py", "klean.py")
    }
    producer_tree_hash = pipeline_contract.sha256_tree(PRODUCERS)
    audit_image_from_path = "sha256:" + Path(
        resolution["generation_producer_sources"]
    ).name
    producer_checks = {
        "producer_file_hashes": producer_file_hashes,
        "source_manifest_file_hashes": source_manifest.get("files"),
        "generator_manifest_exporter_sha256": generator_manifest.get(
            "exporter_sha256"
        ),
        "generator_manifest_klean_py_sha256": generator_manifest.get(
            "klean_py_sha256"
        ),
        "source_manifest_generator_image_id": source_manifest.get(
            "generator_image_id"
        ),
        "generator_manifest_generator_image_id": generator_manifest.get(
            "provenance", {}
        ).get("generator_image_id"),
        "audit_input_generator_image_id_from_path": audit_image_from_path,
        "producer_tree_sha256": producer_tree_hash,
        "audit_input_producer_tree_sha256": hashes[
            "generation_producer_sources_sha256"
        ],
    }
    producer_checks["all_match"] = (
        producer_file_hashes == source_manifest.get("files")
        and producer_file_hashes["klean_export.py"]
        == generator_manifest.get("exporter_sha256")
        and producer_file_hashes["klean.py"]
        == generator_manifest.get("klean_py_sha256")
        and source_manifest.get("generator_image_id")
        == generator_manifest.get("provenance", {}).get("generator_image_id")
        == audit_image_from_path
        and producer_tree_hash
        == hashes["generation_producer_sources_sha256"]
    )
    write_json("producer-authentication.json", producer_checks)

    actual_stage1_sources = all_regular_hashes(K_PROOF)
    expected_stage1_sources = resolution["stage1_source_hashes"]
    source_hash_check = {
        "expected_count": len(expected_stage1_sources),
        "actual_count": len(actual_stage1_sources),
        "missing": sorted(set(expected_stage1_sources) - set(actual_stage1_sources)),
        "extra": sorted(set(actual_stage1_sources) - set(expected_stage1_sources)),
        "mismatches": {
            key: {
                "expected": expected_stage1_sources[key],
                "actual": actual_stage1_sources.get(key),
            }
            for key in expected_stage1_sources
            if actual_stage1_sources.get(key) != expected_stage1_sources[key]
        },
    }
    source_hash_check["all_match"] = not (
        source_hash_check["missing"]
        or source_hash_check["extra"]
        or source_hash_check["mismatches"]
    )
    write_json("stage1-source-hashes.json", source_hash_check)

    actual_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
        "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
        "discovery_manifest_sha256": sha256_file(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(
            Path("/reference/k-audit")
        ),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": producer_tree_hash,
        "generated_tree_sha256": klean_export.tree_digest(
            GENERATION / "generated"
        ),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    hash_comparison = {
        "audit_input_sha256": audit_input_hash,
        "audit_mode_environment": os.environ.get("AUDIT_MODE"),
        "audit_mode_document": resolution.get("mode"),
        "verified_resolution_matches_document": (
            verified_resolution == resolution
        ),
        "expected": hashes,
        "actual": actual_hashes,
        "mismatches": {
            key: {"expected": hashes.get(key), "actual": actual_hashes.get(key)}
            for key in sorted(set(hashes) | set(actual_hashes))
            if hashes.get(key) != actual_hashes.get(key)
        },
        "selection_hash_checks": {
            "k_audit": resolution["selections"]["k_audit"]["artifact_sha256"]
            == actual_hashes["k_audit_sha256"],
            "klean_generation": resolution["selections"]["klean_generation"][
                "artifact_sha256"
            ]
            == actual_hashes["klean_generation_sha256"],
        },
    }
    hash_comparison["all_match"] = (
        not hash_comparison["mismatches"]
        and all(hash_comparison["selection_hash_checks"].values())
        and hash_comparison["audit_mode_environment"]
        == hash_comparison["audit_mode_document"]
    )
    write_json("recorded-hash-comparison.json", hash_comparison)

    inventory = k_rule_inventory.inventory_verification(K_PROOF)
    write_json("reconstructed-inventory.json", inventory)
    validated = lemma_discovery_contract.validate_trust_boundary(
        K_PROOF, DISCOVERY
    )
    discovery_document = json.loads(DISCOVERY.read_text())
    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    discovery_ids = [rule["source_rule_id"] for rule in discovery_document["rules"]]
    span_hash_checks: list[dict[str, object]] = []
    verification_lines = (K_PROOF / "verification.k").read_text().splitlines()
    for rule in inventory["rules"]:
        source_slice = "\n".join(
            verification_lines[rule["start_line"] - 1 : rule["end_line"]]
        ).rstrip(" \t\r\n")
        normalized = " ".join(source_slice.split())
        normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
        span_hash_checks.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
                "text_exact": source_slice == rule["text"],
                "normalized_sha256": normalized_sha256,
                "normalized_hash_matches": normalized_sha256
                == rule["normalized_sha256"],
                "source_rule_id_matches": rule["source_rule_id"]
                == "rule-" + normalized_sha256,
            }
        )
    inventory_comparison = {
        "rule_count": len(canonical_ids),
        "discovery_rule_count": len(discovery_ids),
        "canonical_ids": canonical_ids,
        "discovery_ids": discovery_ids,
        "ordered_identity_match": canonical_ids == discovery_ids,
        "canonical_unique": len(canonical_ids) == len(set(canonical_ids)),
        "discovery_unique": len(discovery_ids) == len(set(discovery_ids)),
        "inventory_hash_recomputed": k_rule_inventory.canonical_json_sha256(
            inventory["rules"]
        ),
        "inventory_hash_inventory": inventory["inventory_sha256"],
        "inventory_hash_discovery": discovery_document["inventory_sha256"],
        "span_hash_checks": span_hash_checks,
        "validated_classification_counts": {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
    }
    inventory_comparison["all_match"] = (
        inventory_comparison["ordered_identity_match"]
        and inventory_comparison["canonical_unique"]
        and inventory_comparison["discovery_unique"]
        and inventory_comparison["inventory_hash_recomputed"]
        == inventory_comparison["inventory_hash_inventory"]
        == inventory_comparison["inventory_hash_discovery"]
        and all(
            check["text_exact"]
            and check["normalized_hash_matches"]
            and check["source_rule_id_matches"]
            for check in span_hash_checks
        )
    )
    write_json("inventory-bijection.json", inventory_comparison)

    preflight = klean_preflight.check_generation(
        K_PROOF,
        DISCOVERY,
        GENERATION,
        toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    )
    write_json("preflight-returned-evidence.json", preflight)

    summary = {
        "trusted_module_paths": {
            "k_rule_inventory": str(Path(k_rule_inventory.__file__).resolve()),
            "klean_preflight": str(Path(klean_preflight.__file__).resolve()),
        },
        "producer_authentication": producer_checks["all_match"],
        "recorded_hashes": hash_comparison["all_match"],
        "stage1_source_hashes": source_hash_check["all_match"],
        "inventory_bijection": inventory_comparison["all_match"],
        "preflight_status": preflight["status"],
        "preflight_obligation_count": preflight["obligation_count"],
        "preflight_target": preflight["target"],
    }
    write_json("mechanical-summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if all(
        (
            summary["producer_authentication"],
            summary["recorded_hashes"],
            summary["stage1_source_hashes"],
            summary["inventory_bijection"],
            summary["preflight_status"] == "KLEAN_NO_OBLIGATIONS",
            summary["preflight_obligation_count"] == 0,
            summary["preflight_target"] is None,
        )
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
