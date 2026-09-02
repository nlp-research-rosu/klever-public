#!/usr/bin/env python3
"""Read-only independent hash, inventory, and manifest checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.stage6_resolution_contract import verify_audit_input


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                hashes[path.relative_to(root).as_posix()] = sha256_file(path)
            else:
                raise RuntimeError(f"unsafe tree entry: {path}")
    return dict(sorted(hashes.items()))


def comparison(expected: object, observed: object) -> dict[str, object]:
    return {"expected": expected, "observed": observed, "match": expected == observed}


def main() -> None:
    audit_document = json.loads(AUDIT_INPUT.read_text())
    resolution = audit_document["resolution"]
    recorded_hashes = resolution["hashes"]

    verified_resolution, binding_digest = verify_audit_input(audit_document)
    print("AUDIT INPUT CONTRACT")
    print(json.dumps({
        "binding_sha256": binding_digest,
        "verified_mode": verified_resolution["mode"],
        "verified_problem_id": verified_resolution["problem_id"],
        "verified_semantics_mode": verified_resolution["semantics_mode"],
    }, indent=2, sort_keys=True))

    observed_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
        "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
        "discovery_manifest_sha256": sha256_file(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    print("RECORDED TREE/FILE HASHES")
    print(json.dumps({
        key: comparison(recorded_hashes.get(key), observed)
        for key, observed in observed_hashes.items()
    }, indent=2, sort_keys=True))

    expected_source_hashes = resolution["stage1_source_hashes"]
    observed_source_hashes = regular_file_hashes(K_PROOF)
    expected_names = set(expected_source_hashes)
    observed_names = set(observed_source_hashes)
    mismatches = {
        name: comparison(expected_source_hashes[name], observed_source_hashes[name])
        for name in sorted(expected_names & observed_names)
        if expected_source_hashes[name] != observed_source_hashes[name]
    }
    print("STAGE 1 PER-FILE HASHES")
    print(json.dumps({
        "expected_count": len(expected_source_hashes),
        "observed_count": len(observed_source_hashes),
        "missing": sorted(expected_names - observed_names),
        "extra": sorted(observed_names - expected_names),
        "mismatches": mismatches,
        "all_match": not (expected_names ^ observed_names) and not mismatches,
    }, indent=2, sort_keys=True))

    inventory = inventory_verification(K_PROOF)
    discovery = json.loads(DISCOVERY.read_text())
    validated = validate_trust_boundary(K_PROOF, DISCOVERY)
    canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
    manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    classifications = {
        entry["source_rule_id"]: entry["classification"]
        for entry in discovery["rules"]
    }
    reconstructed_rules = []
    for index, rule in enumerate(inventory["rules"]):
        normalized = " ".join(rule["text"].split())
        independently_hashed = hashlib.sha256(normalized.encode()).hexdigest()
        reconstructed_rules.append({
            "index": index,
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "attributes": rule["attributes"],
            "normalized_sha256": rule["normalized_sha256"],
            "independent_normalized_sha256": independently_hashed,
            "normalized_hash_match": independently_hashed == rule["normalized_sha256"],
            "source_rule_id": rule["source_rule_id"],
            "source_rule_id_match": rule["source_rule_id"] == f"rule-{independently_hashed}",
            "manifest_classification": classifications.get(rule["source_rule_id"]),
            "text": rule["text"],
        })
    print("CANONICAL RULE INVENTORY")
    print(json.dumps({
        "schema_version": inventory["schema_version"],
        "verification_file": inventory["verification_file"],
        "verification_sha256": inventory["verification_sha256"],
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
        "inventory_sha256": inventory["inventory_sha256"],
        "manifest_inventory_sha256": discovery["inventory_sha256"],
        "inventory_hash_match": inventory["inventory_sha256"] == discovery["inventory_sha256"],
        "canonical_count": len(canonical_ids),
        "manifest_count": len(manifest_ids),
        "canonical_ids_unique": len(canonical_ids) == len(set(canonical_ids)),
        "manifest_ids_unique": len(manifest_ids) == len(set(manifest_ids)),
        "ordered_identity_match": canonical_ids == manifest_ids,
        "omitted_ids": sorted(set(canonical_ids) - set(manifest_ids)),
        "extra_ids": sorted(set(manifest_ids) - set(canonical_ids)),
        "validated_counts": {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
        "rules": reconstructed_rules,
    }, indent=2, sort_keys=True))

    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
    producer_hashes = {
        "klean.py": sha256_file(PRODUCERS / "klean.py"),
        "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
    }
    image_from_audit_path = "sha256:" + Path(
        resolution["generation_producer_sources"]
    ).name
    print("GENERATOR PRODUCER PROVENANCE")
    print(json.dumps({
        "bundle_regular_files": sorted(regular_file_hashes(PRODUCERS)),
        "producer_hashes": producer_hashes,
        "source_manifest_files": source_manifest.get("files"),
        "source_manifest_files_match": producer_hashes == source_manifest.get("files"),
        "generator_exporter_match": producer_hashes["klean_export.py"] == generator_manifest.get("exporter_sha256"),
        "generator_klean_match": producer_hashes["klean.py"] == generator_manifest.get("klean_py_sha256"),
        "source_manifest_image_id": source_manifest.get("generator_image_id"),
        "generator_manifest_image_id": generator_manifest.get("provenance", {}).get("generator_image_id"),
        "audit_input_path_image_id": image_from_audit_path,
        "image_ids_match": len({
            source_manifest.get("generator_image_id"),
            generator_manifest.get("provenance", {}).get("generator_image_id"),
            image_from_audit_path,
        }) == 1,
        "producer_tree_hash": comparison(
            recorded_hashes["generation_producer_sources_sha256"],
            pipeline_contract.sha256_tree(PRODUCERS),
        ),
    }, indent=2, sort_keys=True))

    preflight_sidecar = json.loads((GENERATION / "preflight.json").read_text())
    print("AUDIT INPUT EMBEDDED BINDINGS")
    print(json.dumps({
        "stage4_preflight_exact_match": resolution.get("stage4_preflight") == preflight_sidecar,
        "target_exact_match": resolution.get("target") == generator_manifest.get("target"),
        "target": resolution.get("target"),
        "stage5_result": resolution.get("stage5_result"),
        "candidate_exists": Path("/candidate").exists(),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
