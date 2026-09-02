#!/usr/bin/env python3
"""Independent read-only structural checks for the 161-solve audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, lemma_discovery_contract, pipeline_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


K_PROOF = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    document = json.loads(path.read_text())
    assert isinstance(document, dict)
    return document


def check(condition: bool, label: str) -> dict[str, object]:
    return {"check": label, "pass": bool(condition)}


def main() -> None:
    audit = load(AUDIT_INPUT)["resolution"]
    source_manifest = load(PRODUCERS / "source-manifest.json")
    generator_manifest = load(GENERATION / "generator-manifest.json")
    input_manifest = load(GENERATION / "input-manifest.json")
    obligation_map = load(GENERATED / "obligation-map.json")
    discovery_document = load(DISCOVERY)

    image_id = generator_manifest["provenance"]["generator_image_id"]
    expected_image_key = image_id.removeprefix("sha256:")
    producer_hashes = {
        name: sha256_file(PRODUCERS / name)
        for name in ("klean_export.py", "klean.py")
    }
    producer_checks = [
        check(
            producer_hashes == source_manifest["files"],
            "producer file hashes equal source-manifest files",
        ),
        check(
            producer_hashes["klean_export.py"]
            == generator_manifest["exporter_sha256"],
            "klean_export.py hash equals generator-manifest exporter_sha256",
        ),
        check(
            producer_hashes["klean.py"]
            == generator_manifest["klean_py_sha256"],
            "klean.py hash equals generator-manifest klean_py_sha256",
        ),
        check(
            source_manifest["generator_image_id"] == image_id,
            "source and generator manifests identify the same immutable image",
        ),
        check(
            Path(audit["generation_producer_sources"]).name
            == expected_image_key,
            "audit-input producer path basename identifies the same image",
        ),
        check(
            pipeline_contract.sha256_tree(PRODUCERS)
            == audit["hashes"]["generation_producer_sources_sha256"],
            "producer bundle tree equals audit-input hash",
        ),
        check(
            {p.name for p in PRODUCERS.iterdir()}
            == {"klean_export.py", "klean.py", "source-manifest.json"},
            "producer bundle contains exactly the authenticated source set",
        ),
    ]

    inventory = inventory_verification(K_PROOF)
    validated = lemma_discovery_contract.validate_trust_boundary(
        K_PROOF, DISCOVERY
    )
    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    classified_ids = [
        rule["source_rule_id"] for rule in discovery_document["rules"]
    ]
    verification_lines = (
        (K_PROOF / "verification.k").read_text().splitlines()
    )
    per_rule = []
    for rule in inventory["rules"]:
        normalized = " ".join(rule["text"].split())
        span_text = "\n".join(
            verification_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        per_rule.append(
            {
                "source_rule_id": rule["source_rule_id"],
                "module": rule["module"],
                "start_line": rule["start_line"],
                "end_line": rule["end_line"],
                "attributes": rule["attributes"],
                "normalized_sha256": rule["normalized_sha256"],
                "checks": [
                    check(
                        sha256_file(K_PROOF / "verification.k")
                        == inventory["verification_sha256"],
                        "verification file hash",
                    ),
                    check(
                        hashlib.sha256(normalized.encode()).hexdigest()
                        == rule["normalized_sha256"],
                        "normalized text hash",
                    ),
                    check(
                        rule["source_rule_id"]
                        == f"rule-{rule['normalized_sha256']}",
                        "source_rule_id derived from normalized hash",
                    ),
                    check(
                        span_text == rule["text"],
                        "reported source span is exact",
                    ),
                ],
                "text": rule["text"],
            }
        )
    inventory_checks = [
        check(
            canonical_json_sha256(inventory["rules"])
            == inventory["inventory_sha256"],
            "whole inventory canonical hash",
        ),
        check(
            inventory["inventory_sha256"]
            == discovery_document["inventory_sha256"],
            "discovery whole-inventory hash",
        ),
        check(
            len(canonical_ids) == len(set(canonical_ids)),
            "canonical IDs have no duplicates",
        ),
        check(
            len(classified_ids) == len(set(classified_ids)),
            "classified IDs have no duplicates",
        ),
        check(
            classified_ids == canonical_ids,
            "classified identities are a bijection in canonical source order",
        ),
        check(
            inventory["verification_module"] == "VERIFICATION",
            "selected verification module",
        ),
        check(
            inventory["verification_modules"] == ["VERIFICATION"],
            "local verification-module closure",
        ),
    ]

    discovery_hash = sha256_file(DISCOVERY)
    expected_domain_rules = klean_export._domain_source_rules(
        validated, discovery_hash
    )
    obligations = obligation_map["obligations"]
    observed_obligation_ids = [
        obligation["source_rule_id"] for obligation in obligations
    ]
    expected_domain_ids = [
        rule["source_rule_id"] for rule in expected_domain_rules
    ]
    per_obligation = []
    for index, obligation in enumerate(obligations):
        source_rule = expected_domain_rules[index]
        per_obligation.append(
            {
                "source_rule_id": obligation["source_rule_id"],
                "lean_conjunct": obligation["lean_conjunct"],
                "checks": [
                    check(
                        obligation["source_rule_id"]
                        == source_rule["source_rule_id"],
                        "obligation source identity",
                    ),
                    check(
                        obligation["source_span"]
                        == {
                            "start_line": source_rule["start_line"],
                            "end_line": source_rule["end_line"],
                        },
                        "obligation source span",
                    ),
                    check(
                        obligation["normalized_sha256"]
                        == source_rule["normalized_sha256"],
                        "obligation normalized source hash",
                    ),
                    check(
                        obligation["inventory_sha256"]
                        == source_rule["inventory_sha256"],
                        "obligation inventory hash",
                    ),
                    check(
                        obligation["discovery_manifest_sha256"]
                        == source_rule["discovery_manifest_sha256"],
                        "obligation discovery hash",
                    ),
                    check(
                        klean_export.sha256_text(obligation["lean_conjunct"])
                        == obligation["lean_conjunct_sha256"],
                        "Lean conjunct hash",
                    ),
                ],
            }
        )

    expected_definition = klean_export.expected_target_definition(
        obligation_map
    )
    observed_target = klean_export.target_statement(GENERATED)
    stage4_checks = [
        check(
            pipeline_contract.sha256_tree(K_PROOF)
            == audit["hashes"]["k_workspace_sha256"],
            "Stage 1 selected workspace tree hash",
        ),
        check(
            klean_export.tree_digest(K_PROOF)
            == audit["hashes"]["stage1_export_sha256"],
            "Stage 1 deterministic-export tree hash",
        ),
        check(
            sha256_file(DISCOVERY)
            == audit["hashes"]["discovery_manifest_sha256"],
            "Stage 3 discovery file hash",
        ),
        check(
            pipeline_contract.sha256_tree(GENERATION)
            == audit["hashes"]["klean_generation_sha256"],
            "Stage 4 selected generation tree hash",
        ),
        check(
            klean_export.tree_digest(GENERATED)
            == audit["hashes"]["generated_tree_sha256"],
            "generated project deterministic tree hash",
        ),
        check(
            input_manifest["source_rules"] == expected_domain_rules,
            "input-manifest source rules equal independently selected domain set",
        ),
        check(
            obligation_map["source_rules"] == expected_domain_rules,
            "obligation-map source rules equal independently selected domain set",
        ),
        check(
            observed_obligation_ids == expected_domain_ids
            and len(observed_obligation_ids)
            == len(set(observed_obligation_ids)),
            "exact source-rule/obligation bijection in source order",
        ),
        check(
            generator_manifest["obligation_count"] == len(obligations),
            "generator obligation count",
        ),
        check(
            sha256_file(GENERATED / "obligation-map.json")
            == generator_manifest["obligation_map_sha256"],
            "obligation-map file hash",
        ),
        check(
            expected_definition is not None
            and klean_export.sha256_text(expected_definition)
            == generator_manifest["target"]["definition_sha256"],
            "fixed target is exact conjunction of obligations",
        ),
        check(
            observed_target == generator_manifest["target"],
            "generated target equals generator manifest",
        ),
        check(
            observed_target == audit["target"],
            "generated target equals audit input",
        ),
    ]

    result = {
        "audit_mode_environment": os.environ.get("AUDIT_MODE"),
        "audit_mode_recorded": audit["mode"],
        "producer_authentication": {
            "observed_file_sha256": producer_hashes,
            "source_manifest": source_manifest,
            "generator_image_id": image_id,
            "audit_input_image_key": Path(
                audit["generation_producer_sources"]
            ).name,
            "observed_bundle_tree_sha256": pipeline_contract.sha256_tree(
                PRODUCERS
            ),
            "checks": producer_checks,
        },
        "inventory": {
            "schema_version": inventory["schema_version"],
            "verification_sha256": inventory["verification_sha256"],
            "verification_module": inventory["verification_module"],
            "verification_modules": inventory["verification_modules"],
            "inventory_sha256": inventory["inventory_sha256"],
            "canonical_ids": canonical_ids,
            "classified_ids": classified_ids,
            "checks": inventory_checks,
            "rules": per_rule,
        },
        "validated_classification_counts": {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(
                validated["proved_derived_lemmas"]
            ),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
        "stage4": {
            "expected_domain_ids": expected_domain_ids,
            "observed_obligation_ids": observed_obligation_ids,
            "obligation_count": len(obligations),
            "per_obligation": per_obligation,
            "expected_target_definition": expected_definition,
            "observed_target": observed_target,
            "checks": stage4_checks,
        },
    }
    all_checks = (
        producer_checks
        + inventory_checks
        + [
            item
            for rule in per_rule
            for item in rule["checks"]
        ]
        + stage4_checks
        + [
            item
            for obligation in per_obligation
            for item in obligation["checks"]
        ]
    )
    result["all_structural_checks_pass"] = all(
        item["pass"] for item in all_checks
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
