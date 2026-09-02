#!/usr/bin/env python3
"""Independent Stage 4 manifest, obligation, and target checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> dict[str, object]:
    return {
        "label": label,
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }


k_workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

audit_input = read_json(Path("/audit-input.json"))
resolution = audit_input["resolution"]
input_manifest = read_json(generation / "input-manifest.json")
generator_manifest = read_json(generation / "generator-manifest.json")
export_result = read_json(generation / "export-result.json")
recorded_preflight = read_json(generation / "preflight.json")
trust_inventory = read_json(generation / "trust-inventory.json")
obligation_map = read_json(generated / "obligation-map.json")
toolchain_lock = read_json(Path("/reference/klean-toolchain.lock.json"))

validated = lemma_discovery_contract.validate_trust_boundary(
    k_workspace, discovery_path
)
discovery_sha256 = sha256_file(discovery_path)
domain_source_rules = klean_export._domain_source_rules(
    validated, discovery_sha256
)
obligations = obligation_map["obligations"]
expected_ids = [
    rule["source_rule_id"] for rule in domain_source_rules
]
observed_ids = [
    obligation["source_rule_id"] for obligation in obligations
]
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)
observed_target = klean_export.target_statement(generated)

checks = [
    check(
        "Stage 3 DOMAIN_LEMMA source rules vs input manifest",
        input_manifest["source_rules"],
        domain_source_rules,
    ),
    check(
        "Stage 3 DOMAIN_LEMMA source rules vs obligation map",
        obligation_map["source_rules"],
        domain_source_rules,
    ),
    check(
        "ordered obligation IDs vs ordered source-rule IDs",
        observed_ids,
        expected_ids,
    ),
    check(
        "obligation IDs are unique",
        len(observed_ids),
        len(set(observed_ids)),
    ),
    check(
        "obligation count vs generator manifest",
        len(obligations),
        generator_manifest["obligation_count"],
    ),
    check(
        "obligation count vs export result",
        len(obligations),
        export_result["obligation_count"],
    ),
    check(
        "obligation count vs recorded preflight",
        len(obligations),
        recorded_preflight["obligation_count"],
    ),
    check(
        "obligation-map byte hash",
        sha256_file(generated / "obligation-map.json"),
        generator_manifest["obligation_map_sha256"],
    ),
    check(
        "expected target definition for mapped obligations",
        expected_target_definition,
        None,
    ),
    check(
        "observed generated target",
        observed_target,
        None,
    ),
    check(
        "observed target vs generator manifest",
        observed_target,
        generator_manifest["target"],
    ),
    check(
        "observed target vs recorded preflight",
        observed_target,
        recorded_preflight["target"],
    ),
    check(
        "observed target vs audit input",
        observed_target,
        resolution["target"],
    ),
    check(
        "generator toolchain vs pinned lock",
        generator_manifest["toolchain"],
        toolchain_lock,
    ),
    check(
        "input frozen hash",
        input_manifest["frozen_input_sha256"],
        klean_export.tree_digest(k_workspace),
    ),
    check(
        "input Stage 1 hash",
        input_manifest["stage1_workspace_sha256"],
        klean_export.tree_digest(k_workspace),
    ),
    check(
        "generator Stage 1 provenance",
        generator_manifest["provenance"]["stage1_workspace_sha256"],
        klean_export.tree_digest(k_workspace),
    ),
    check(
        "export Stage 1 hash",
        export_result["frozen_input_sha256"],
        klean_export.tree_digest(k_workspace),
    ),
    check(
        "recorded preflight Stage 1 hash",
        recorded_preflight["stage1_workspace_sha256"],
        klean_export.tree_digest(k_workspace),
    ),
    check(
        "input Stage 3 provenance",
        input_manifest["stage3_discovery_manifest_sha256"],
        discovery_sha256,
    ),
    check(
        "generator Stage 3 provenance",
        generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ],
        discovery_sha256,
    ),
    check(
        "export Stage 3 provenance",
        export_result["stage3_discovery_manifest_sha256"],
        discovery_sha256,
    ),
    check(
        "recorded preflight Stage 3 provenance",
        recorded_preflight["stage3_discovery_manifest_sha256"],
        discovery_sha256,
    ),
    check(
        "input inventory provenance",
        input_manifest["inventory_sha256"],
        validated["inventory_sha256"],
    ),
    check(
        "generator inventory provenance",
        generator_manifest["provenance"]["inventory_sha256"],
        validated["inventory_sha256"],
    ),
    check(
        "input verification.k hash",
        input_manifest["verification_sha256"],
        sha256_file(k_workspace / "verification.k"),
    ),
    check(
        "generator generated-tree hash",
        generator_manifest["generated_tree_sha256"],
        klean_export.tree_digest(generated),
    ),
    check(
        "export generated-tree hash",
        export_result["generated_tree_sha256"],
        klean_export.tree_digest(generated),
    ),
    check(
        "recorded preflight generated-tree hash",
        recorded_preflight["generated_tree_sha256"],
        klean_export.tree_digest(generated),
    ),
    check(
        "export trust-inventory byte hash",
        export_result["trust_inventory_sha256"],
        sha256_file(generation / "trust-inventory.json"),
    ),
    check(
        "zero trust parameters",
        obligation_map["trust_parameters"],
        [],
    ),
    check(
        "zero Stage 5 result",
        resolution["stage5_result"],
        None,
    ),
    check(
        "zero Lean workspace",
        resolution["lean_workspace"],
        None,
    ),
    check(
        "zero Lean invocation",
        resolution["lean_invocation"],
        None,
    ),
    check(
        "proof candidate absent",
        Path("/candidate").exists(),
        False,
    ),
]

for obligation in obligations:
    checks.extend(
        [
            check(
                f"{obligation['source_rule_id']} conjunct hash",
                hashlib.sha256(
                    obligation["lean_conjunct"].encode()
                ).hexdigest(),
                obligation["lean_conjunct_sha256"],
            ),
            check(
                f"{obligation['source_rule_id']} inventory hash",
                obligation["inventory_sha256"],
                validated["inventory_sha256"],
            ),
            check(
                f"{obligation['source_rule_id']} discovery hash",
                obligation["discovery_manifest_sha256"],
                discovery_sha256,
            ),
        ]
    )

document = {
    "all_checks_match": all(item["match"] for item in checks),
    "checks": checks,
    "classification_counts": {
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(
            validated["proved_derived_lemmas"]
        ),
        "domain_lemmas": len(validated["domain_lemmas"]),
    },
    "domain_source_rule_count": len(domain_source_rules),
    "obligation_count": len(obligations),
    "expected_target_definition": expected_target_definition,
    "observed_target": observed_target,
    "trust_allowlist_count": len(trust_inventory["allowlist"]),
}
print(json.dumps(document, indent=2, sort_keys=True))
