#!/usr/bin/env python3
"""Independent mechanical reconstruction for the 35-max-element audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


ROOT = Path("/reference")
STAGE1 = ROOT / "k-proof"
DISCOVERY = ROOT / "lemma-discovery.json"
GENERATION = ROOT / "klean-generation"
GENERATED = GENERATION / "generated"
PRODUCERS = ROOT / "generation-tools"
CANDIDATE = Path("/candidate")
AUDIT_INPUT = Path("/audit-input.json")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> None:
    status = "PASS" if observed == expected else "FAIL"
    print(f"{status} {label}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if status == "FAIL":
        raise SystemExit(f"mismatch: {label}")


def main() -> None:
    audit_document = json.loads(AUDIT_INPUT.read_text())
    resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
        audit_document
    )
    hashes = resolution["hashes"]
    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    discovery_document = json.loads(DISCOVERY.read_text())

    print("== launcher identity ==")
    check("AUDIT_MODE env", os.environ.get("AUDIT_MODE"), resolution["mode"])
    check("audit mode", resolution["mode"], "CLASSIFICATION_AND_PROOF")
    check("problem", resolution["problem_id"], "35-max-element")
    check("condition", resolution["condition"], "kit-semantics")
    check("semantics mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")
    check(
        "resolved_input_sha256",
        resolved_digest,
        audit_document["resolved_input_sha256"],
    )

    print("\n== producer-source attestation ==")
    exporter_hash = sha(PRODUCERS / "klean_export.py")
    klean_hash = sha(PRODUCERS / "klean.py")
    image_id = generator_manifest["provenance"]["generator_image_id"]
    check("klean_export.py source-manifest hash", exporter_hash,
          source_manifest["files"]["klean_export.py"])
    check("klean_export.py generator-manifest hash", exporter_hash,
          generator_manifest["exporter_sha256"])
    check("klean.py source-manifest hash", klean_hash,
          source_manifest["files"]["klean.py"])
    check("klean.py generator-manifest hash", klean_hash,
          generator_manifest["klean_py_sha256"])
    check("source/generator image ID", source_manifest["generator_image_id"], image_id)
    check(
        "audit-input image ID via immutable source-bundle basename",
        "sha256:" + Path(resolution["generation_producer_sources"]).name,
        image_id,
    )
    producer_names = sorted(p.name for p in PRODUCERS.iterdir())
    check(
        "producer source exact file set",
        producer_names,
        ["klean.py", "klean_export.py", "source-manifest.json"],
    )
    check(
        "producer source tree hash",
        pipeline_contract.sha256_tree(PRODUCERS),
        hashes["generation_producer_sources_sha256"],
    )

    print("\n== all launcher-bound input hashes ==")
    check("Stage 1 pipeline tree", pipeline_contract.sha256_tree(STAGE1),
          hashes["k_workspace_sha256"])
    check("Stage 1 export tree", klean_export.tree_digest(STAGE1),
          hashes["stage1_export_sha256"])
    check("Stage 3 manifest", sha(DISCOVERY), hashes["discovery_manifest_sha256"])
    check("Stage 4 generation pipeline tree",
          pipeline_contract.sha256_tree(GENERATION), hashes["klean_generation_sha256"])
    check("Stage 4 generated export tree", klean_export.tree_digest(GENERATED),
          hashes["generated_tree_sha256"])
    check("Stage 5 candidate pipeline tree", pipeline_contract.sha256_tree(CANDIDATE),
          hashes["lean_workspace_sha256"])
    stage1_observed = {
        path.relative_to(STAGE1).as_posix(): sha(path)
        for path in pipeline_contract._walk_regular_files(STAGE1, "Stage 1")
    }
    check("Stage 1 source-file hash map", stage1_observed,
          resolution["stage1_source_hashes"])

    print("\n== canonical verification-rule inventory ==")
    inventory = k_rule_inventory.inventory_verification(STAGE1)
    validated = lemma_discovery_contract.validate_trust_boundary(STAGE1, DISCOVERY)
    check("verification SHA-256", inventory["verification_sha256"],
          sha(STAGE1 / "verification.k"))
    check("verification module", inventory["verification_module"], "VERIFICATION")
    check("local module closure", inventory["verification_modules"], ["VERIFICATION"])
    check("inventory hash", inventory["inventory_sha256"],
          discovery_document["inventory_sha256"])
    check("inventory hash in Stage 4", inventory["inventory_sha256"],
          input_manifest["inventory_sha256"])
    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    manifest_ids = [entry["source_rule_id"] for entry in discovery_document["rules"]]
    check("ordered Stage 3 identity sequence", manifest_ids, canonical_ids)
    check("unique Stage 3 identities", len(set(manifest_ids)), len(manifest_ids))
    by_id = {entry["source_rule_id"]: entry for entry in discovery_document["rules"]}
    counts: dict[str, int] = {
        "DEFINITION": 0,
        "DOMAIN_LEMMA": 0,
        "OPERATIONAL_RULE": 0,
        "PROVED_DERIVED_LEMMA": 0,
    }
    for index, rule in enumerate(inventory["rules"], 1):
        normalized = " ".join(rule["text"].split())
        normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
        check(f"rule {index:02d} normalized hash", normalized_hash,
              rule["normalized_sha256"])
        check(f"rule {index:02d} source_rule_id", "rule-" + normalized_hash,
              rule["source_rule_id"])
        classification = by_id[rule["source_rule_id"]]["classification"]
        counts[classification] = counts.get(classification, 0) + 1
        print(
            f"RULE {index:02d} {rule['module']}:{rule['start_line']}-{rule['end_line']} "
            f"{rule['source_rule_id']} {classification} attrs={rule['attributes']}"
        )
        print("  " + " ".join(rule["text"].split()))
    check(
        "classification counts",
        counts,
        {
            "DEFINITION": len(validated["definitions"]),
            "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
            "OPERATIONAL_RULE": len(validated["operational_rules"]),
            "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
        },
    )

    print("\n== Stage 4 structural identity ==")
    check("Stage 1 provenance", generator_manifest["provenance"]["stage1_workspace_sha256"],
          hashes["stage1_export_sha256"])
    check("Stage 3 provenance",
          generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
          hashes["discovery_manifest_sha256"])
    check("generated tree manifest", generator_manifest["generated_tree_sha256"],
          hashes["generated_tree_sha256"])
    target = klean_export.target_statement(GENERATED)
    check("generated target vs generator manifest", target, generator_manifest["target"])
    check("generated target vs audit input", target, resolution["target"])
    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = json.loads(obligation_map_path.read_text())
    check("obligation map hash", sha(obligation_map_path),
          generator_manifest["obligation_map_sha256"])
    source_ids = [rule["source_rule_id"] for rule in input_manifest["source_rules"]]
    obligation_ids = [item["source_rule_id"] for item in obligation_map["obligations"]]
    independently_classified_domain_ids = [
        rule["source_rule_id"] for rule in inventory["rules"]
        if by_id[rule["source_rule_id"]]["classification"] == "DOMAIN_LEMMA"
    ]
    check("Stage 3-domain/Stage 4-source ordered bijection", source_ids,
          independently_classified_domain_ids)
    check("source-rule/obligation ordered bijection", obligation_ids, source_ids)
    check("unique obligation identities", len(set(obligation_ids)), len(obligation_ids))
    check("obligation count", len(obligation_ids), generator_manifest["obligation_count"])
    expected_definition = klean_export.expected_target_definition(obligation_map)
    check("target definition hash", target["definition_sha256"],
          klean_export.sha256_text(expected_definition))
    for index, obligation in enumerate(obligation_map["obligations"], 1):
        source = input_manifest["source_rules"][index - 1]
        check(f"obligation {index:02d} source span", obligation["source_span"],
              {"start_line": source["start_line"], "end_line": source["end_line"]})
        check(f"obligation {index:02d} normalized hash",
              obligation["normalized_sha256"], source["normalized_sha256"])
        check(f"obligation {index:02d} inventory hash",
              obligation["inventory_sha256"], inventory["inventory_sha256"])
        check(f"obligation {index:02d} discovery hash",
              obligation["discovery_manifest_sha256"], sha(DISCOVERY))
        check(f"obligation {index:02d} conjunct hash",
              obligation["lean_conjunct_sha256"],
              klean_export.sha256_text(obligation["lean_conjunct"]))
        print(f"OBLIGATION {index:02d} {obligation['source_rule_id']}")
        print("  K:", " ".join(source["text"].split()))
        print("  Lean:", " ".join(obligation["lean_conjunct"].split()))

    print("\nALL MECHANICAL RECONSTRUCTION CHECKS PASSED")


if __name__ == "__main__":
    main()
