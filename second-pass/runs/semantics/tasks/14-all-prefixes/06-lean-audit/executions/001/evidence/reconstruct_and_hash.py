#!/usr/bin/env python3
"""Read-only reconstruction and hash reconciliation for the independent audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_audit_contract,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, observed: object, expected: object) -> dict[str, object]:
    return {
        "name": name,
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = klean_audit_contract.verify_stage6_audit_input(
    audit_document
)
recorded_hashes = resolution["hashes"]

inventory = k_rule_inventory.inventory_verification(K_WORKSPACE)
validated = lemma_discovery_contract.validate_trust_boundary(
    K_WORKSPACE, DISCOVERY
)
discovery_document = json.loads(DISCOVERY.read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())

source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        K_WORKSPACE, "Stage 1 workspace"
    )
}

rule_reconstruction: list[dict[str, object]] = []
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    physical_lines = (
        (K_WORKSPACE / "verification.k")
        .read_text()
        .splitlines()[rule["start_line"] - 1 : rule["end_line"]]
    )
    rule_reconstruction.append(
        {
            **rule,
            "recomputed_normalized_sha256": normalized_sha256,
            "normalized_hash_match": normalized_sha256
            == rule["normalized_sha256"],
            "source_rule_id_match": rule["source_rule_id"]
            == f"rule-{normalized_sha256}",
            "physical_source_span": physical_lines,
            "span_text_match": "\n".join(physical_lines).strip()
            == rule["text"].strip(),
        }
    )

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [
    rule["source_rule_id"] for rule in discovery_document["rules"]
]
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
producer_files = {
    "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
    "klean.py": sha256_file(PRODUCERS / "klean.py"),
}
producer_bundle_tree = pipeline_contract.sha256_tree(PRODUCERS)

checks = [
    check(
        "audit input signed-resolution digest",
        resolved_digest,
        audit_document["resolved_input_sha256"],
    ),
    check(
        "Stage 1 pipeline tree hash",
        pipeline_contract.sha256_tree(K_WORKSPACE),
        recorded_hashes["k_workspace_sha256"],
    ),
    check(
        "Stage 1 deterministic-export tree hash",
        klean_export.tree_digest(K_WORKSPACE),
        recorded_hashes["stage1_export_sha256"],
    ),
    check(
        "Stage 1 deterministic-export tree hash equals input-manifest frozen hash",
        klean_export.tree_digest(K_WORKSPACE),
        input_manifest["frozen_input_sha256"],
    ),
    check(
        "Stage 1 source file hash map",
        source_hashes,
        resolution["stage1_source_hashes"],
    ),
    check(
        "selected Stage 2 audit tree hash",
        pipeline_contract.sha256_tree(K_AUDIT),
        recorded_hashes["k_audit_sha256"],
    ),
    check(
        "Stage 3 manifest file hash",
        sha256_file(DISCOVERY),
        recorded_hashes["discovery_manifest_sha256"],
    ),
    check(
        "Stage 4 generation pipeline tree hash",
        pipeline_contract.sha256_tree(GENERATION),
        recorded_hashes["klean_generation_sha256"],
    ),
    check(
        "Stage 4 generated-project deterministic tree hash",
        klean_export.tree_digest(GENERATED),
        recorded_hashes["generated_tree_sha256"],
    ),
    check(
        "Stage 4 generated-project hash in generator manifest",
        klean_export.tree_digest(GENERATED),
        generator_manifest["generated_tree_sha256"],
    ),
    check(
        "producer-source bundle tree hash",
        producer_bundle_tree,
        recorded_hashes["generation_producer_sources_sha256"],
    ),
    check(
        "producer-source files against source manifest",
        producer_files,
        source_manifest["files"],
    ),
    check(
        "klean_export.py against generator manifest",
        producer_files["klean_export.py"],
        generator_manifest["exporter_sha256"],
    ),
    check(
        "klean.py against generator manifest",
        producer_files["klean.py"],
        generator_manifest["klean_py_sha256"],
    ),
    check(
        "generator image ID against source manifest",
        generator_image_id,
        source_manifest["generator_image_id"],
    ),
    check(
        "generator image ID against audit-input producer path",
        generator_image_id.removeprefix("sha256:"),
        Path(resolution["generation_producer_sources"]).name,
    ),
    check(
        "verification.k file hash against audit input",
        sha256_file(K_WORKSPACE / "verification.k"),
        resolution["stage1_source_hashes"]["verification.k"],
    ),
    check(
        "verification.k file hash against input manifest",
        sha256_file(K_WORKSPACE / "verification.k"),
        input_manifest["verification_sha256"],
    ),
    check(
        "canonical inventory hash against discovery manifest",
        inventory["inventory_sha256"],
        discovery_document["inventory_sha256"],
    ),
    check(
        "canonical inventory hash against generator provenance",
        inventory["inventory_sha256"],
        generator_manifest["provenance"]["inventory_sha256"],
    ),
    check(
        "ordered Stage 3 source-rule identities",
        manifest_ids,
        inventory_ids,
    ),
    check(
        "Stage 3 source-rule identities are unique",
        len(set(manifest_ids)),
        len(manifest_ids),
    ),
    check(
        "validated classification inventory covers every rule",
        sum(
            len(validated[key])
            for key in (
                "definitions",
                "operational_rules",
                "proved_derived_lemmas",
                "domain_lemmas",
            )
        ),
        len(inventory["rules"]),
    ),
    check(
        "Stage 4 source-rule set",
        input_manifest["source_rules"],
        [],
    ),
    check(
        "Stage 4 obligation-map source-rule set",
        obligation_map["source_rules"],
        [],
    ),
    check("Stage 4 obligations", obligation_map["obligations"], []),
    check("Stage 4 target parameters", obligation_map["trust_parameters"], []),
    check(
        "Stage 4 generated target",
        klean_export.target_statement(GENERATED),
        None,
    ),
    check("Stage 4 manifest target", generator_manifest["target"], None),
    check("audit-input target", resolution["target"], None),
    check(
        "audit-input mode",
        resolution["mode"],
        "CLASSIFICATION_ONLY",
    ),
    check(
        "audit-input selected generation status",
        resolution["selections"]["klean_generation"]["status"],
        "KLEAN_NO_OBLIGATIONS",
    ),
]

document = {
    "resolved_input": {
        "mode": resolution["mode"],
        "condition": resolution["condition"],
        "semantics_mode": resolution["semantics_mode"],
        "problem_id": resolution["problem_id"],
        "resolved_input_sha256": resolved_digest,
    },
    "inventory": inventory,
    "rule_reconstruction": rule_reconstruction,
    "classification_counts": {
        key: len(validated[key])
        for key in (
            "definitions",
            "operational_rules",
            "proved_derived_lemmas",
            "domain_lemmas",
        )
    },
    "checks": checks,
    "all_checks_match": all(item["match"] for item in checks),
}
print(json.dumps(document, indent=2, sort_keys=True))
