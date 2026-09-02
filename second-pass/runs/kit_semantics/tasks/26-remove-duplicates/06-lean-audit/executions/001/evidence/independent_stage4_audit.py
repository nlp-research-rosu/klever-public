#!/usr/bin/env python3
"""Independent Stage 3/4 structural and zero-obligation audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
OBLIGATION_MAP = GENERATED / "obligation-map.json"


def load(path: Path) -> dict:
    return json.loads(path.read_bytes())


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = load(Path("/audit-input.json"))["resolution"]
discovery = load(DISCOVERY)
inventory = inventory_verification(WORKSPACE)
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
recorded_preflight = load(GENERATION / "preflight.json")
rerun_preflight = load(
    Path("/audit-output/evidence/14_preflight_returned_evidence.json")
)
obligation_map = load(OBLIGATION_MAP)

# The independent semantic classification is recorded here explicitly.
independent_classes = {
    "rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08":
        "DEFINITION",
    "rule-bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0":
        "DEFINITION",
    "rule-6c55d502b263cd9488fb4d13c18990fa8865f154bf5db922ef461ae84c961308":
        "DEFINITION",
    "rule-7614bf9bc54b61933d1cbd1d534bb404043cb2a80c42f36e07b6cf7486cf642d":
        "DEFINITION",
}
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
domain_ids = [
    source_rule_id
    for source_rule_id in canonical_ids
    if independent_classes[source_rule_id] == "DOMAIN_LEMMA"
]

expected_input_definitions = []
discovery_by_id = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}
for rule in inventory["rules"]:
    entry = discovery_by_id[rule["source_rule_id"]]
    expected_input_definitions.append(
        {
            **rule,
            "classification": entry["classification"],
            "rationale": entry["rationale"],
        }
    )

target_occurrences = []
for source in sorted(GENERATED.rglob("*.lean")):
    for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", source.read_text()):
        target_occurrences.append(
            {
                "file": source.relative_to(GENERATED).as_posix(),
                "offset": match.start(),
            }
        )

checks = {
    "canonical_and_discovery_order_equal": canonical_ids == discovery_ids,
    "canonical_and_discovery_bijection": (
        len(canonical_ids)
        == len(discovery_ids)
        == len(set(discovery_ids))
        and set(canonical_ids) == set(discovery_ids)
    ),
    "independent_classification_covers_inventory": (
        list(independent_classes) == canonical_ids
    ),
    "discovery_matches_independent_classification": all(
        discovery_by_id[source_rule_id]["classification"]
        == independent_classes[source_rule_id]
        for source_rule_id in canonical_ids
    ),
    "true_domain_set_empty": domain_ids == [],
    "input_definitions_exact": (
        input_manifest["definitions"] == expected_input_definitions
    ),
    "input_nondefinition_classes_empty": (
        input_manifest["operational_rules"] == []
        and input_manifest["proved_derived_lemmas"] == []
    ),
    "input_source_rules_exact_domain_set": (
        [
            rule["source_rule_id"]
            for rule in input_manifest["source_rules"]
        ]
        == domain_ids
    ),
    "obligation_map_exact_empty_shape": (
        obligation_map
        == {
            "schema_version": 3,
            "source_rules": [],
            "obligations": [],
            "trust_parameters": [],
        }
    ),
    "obligation_source_ids_bijective": (
        [
            obligation["source_rule_id"]
            for obligation in obligation_map["obligations"]
        ]
        == domain_ids
    ),
    "no_duplicate_obligations": (
        len(
            {
                obligation["source_rule_id"]
                for obligation in obligation_map["obligations"]
            }
        )
        == len(obligation_map["obligations"])
    ),
    "no_vacuous_generated_conjuncts": all(
        obligation.get("lean_conjunct", "").strip()
        not in {"", "True", "(True)", "by trivial"}
        for obligation in obligation_map["obligations"]
    ),
    "obligation_map_hash": (
        file_hash(OBLIGATION_MAP)
        == generator_manifest["obligation_map_sha256"]
    ),
    "generator_obligation_count": (
        generator_manifest["obligation_count"]
        == len(obligation_map["obligations"])
        == 0
    ),
    "generated_target_declaration_absent": target_occurrences == [],
    "all_recorded_targets_null": (
        generator_manifest["target"] is None
        and recorded_preflight["target"] is None
        and rerun_preflight["target"] is None
        and audit_input["target"] is None
    ),
    "all_recorded_statuses_no_obligations": (
        export_result["status"] == "KLEAN_NO_OBLIGATIONS"
        and recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and rerun_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
        and audit_input["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS"
    ),
    "export_obligation_count": export_result["obligation_count"] == 0,
    "preflight_rerun_exactly_reproduced": (
        rerun_preflight == recorded_preflight
    ),
    "discovery_hash_bound_everywhere": (
        file_hash(DISCOVERY)
        == input_manifest["stage3_discovery_manifest_sha256"]
        == generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ]
        == export_result["stage3_discovery_manifest_sha256"]
        == recorded_preflight["stage3_discovery_manifest_sha256"]
        == rerun_preflight["stage3_discovery_manifest_sha256"]
        == audit_input["hashes"]["discovery_manifest_sha256"]
    ),
    "inventory_hash_bound_everywhere": (
        inventory["inventory_sha256"]
        == discovery["inventory_sha256"]
        == input_manifest["inventory_sha256"]
        == generator_manifest["provenance"]["inventory_sha256"]
    ),
    "verification_hash_bound": (
        inventory["verification_sha256"]
        == input_manifest["verification_sha256"]
    ),
    "stage1_export_hash_bound_everywhere": (
        input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == generator_manifest["provenance"]["stage1_workspace_sha256"]
        == export_result["frozen_input_sha256"]
        == recorded_preflight["frozen_input_sha256"]
        == recorded_preflight["stage1_workspace_sha256"]
        == rerun_preflight["frozen_input_sha256"]
        == rerun_preflight["stage1_workspace_sha256"]
        == audit_input["hashes"]["stage1_export_sha256"]
    ),
    "generated_tree_hash_bound_everywhere": (
        generator_manifest["generated_tree_sha256"]
        == export_result["generated_tree_sha256"]
        == recorded_preflight["generated_tree_sha256"]
        == rerun_preflight["generated_tree_sha256"]
        == audit_input["hashes"]["generated_tree_sha256"]
    ),
    "trust_inventory_hash_bound": (
        file_hash(GENERATION / "trust-inventory.json")
        == export_result["trust_inventory_sha256"]
    ),
    "toolchain_lock_exact": (
        generator_manifest["toolchain"]
        == load(Path("/reference/klean-toolchain.lock.json"))
    ),
    "classification_only_no_stage5": (
        audit_input["mode"] == "CLASSIFICATION_ONLY"
        and audit_input["lean_workspace"] is None
        and audit_input["lean_invocation"] is None
        and not Path("/candidate").exists()
    ),
}

print(
    json.dumps(
        {
            "checks": checks,
            "canonical_ids": canonical_ids,
            "independent_classes": independent_classes,
            "domain_ids": domain_ids,
            "target_occurrences": target_occurrences,
        },
        indent=2,
        sort_keys=True,
    )
)
if not all(checks.values()):
    raise SystemExit(1)
