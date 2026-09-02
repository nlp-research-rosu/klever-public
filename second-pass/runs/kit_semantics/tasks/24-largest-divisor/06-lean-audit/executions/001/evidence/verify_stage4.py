#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


ROOT = Path("/reference")
K_WORKSPACE = ROOT / "k-proof"
DISCOVERY_PATH = ROOT / "lemma-discovery.json"
GENERATION = ROOT / "klean-generation"
GENERATED = GENERATION / "generated"
PRODUCERS = ROOT / "generation-tools"
AUDIT_INPUT_PATH = Path("/audit-input.json")
REGENERATION = Path("/tmp/audit-work/stage4-regeneration")

failures: list[str] = []


def check(label: str, condition: bool, detail: object = "") -> None:
    print(f"{label}: {'PASS' if condition else 'FAIL'}")
    if detail != "":
        print(f"  {detail}")
    if not condition:
        failures.append(label)


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise TypeError(f"{path} is not a JSON object")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = load(AUDIT_INPUT_PATH)
resolution = audit["resolution"]
discovery = load(DISCOVERY_PATH)
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
stored_preflight = load(GENERATION / "preflight.json")
trust_inventory = load(GENERATION / "trust-inventory.json")
obligation_map = load(GENERATED / "obligation-map.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
toolchain_lock = load(ROOT / "klean-toolchain.lock.json")

verified_resolution, resolved_hash = (
    stage6_resolution_contract.verify_audit_input(audit)
)
check(
    "launcher canonical resolved-input hash",
    resolved_hash == audit["resolved_input_sha256"],
    f"observed={resolved_hash} recorded={audit['resolved_input_sha256']}",
)
check(
    "launcher resolution payload",
    verified_resolution == resolution,
)

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
    "discovery_manifest_sha256": sha256_file(DISCOVERY_PATH),
    "k_audit_sha256": pipeline_contract.sha256_tree(ROOT / "k-audit"),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        PRODUCERS
    ),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
}
for name, observed in observed_hashes.items():
    recorded = resolution["hashes"][name]
    check(
        f"launcher {name}",
        observed == recorded,
        f"observed={observed} recorded={recorded}",
    )

observed_stage1_files = {
    path.relative_to(K_WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        K_WORKSPACE, "mounted Stage 1 workspace"
    )
}
check(
    "launcher complete Stage 1 per-file hash map",
    observed_stage1_files == resolution["stage1_source_hashes"],
    (
        f"observed_files={len(observed_stage1_files)} "
        f"recorded_files={len(resolution['stage1_source_hashes'])}"
    ),
)

inventory = k_rule_inventory.inventory_verification(K_WORKSPACE)
validated = lemma_discovery_contract.validate_trust_boundary(
    K_WORKSPACE, DISCOVERY_PATH
)
inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
check(
    "Stage 3 ordered inventory bijection",
    inventory_ids == discovery_ids
    and len(inventory_ids) == len(set(inventory_ids))
    and len(discovery_ids) == len(set(discovery_ids)),
    f"inventory_ids={inventory_ids} discovery_ids={discovery_ids}",
)
check(
    "Stage 3 inventory hash",
    inventory["inventory_sha256"] == discovery["inventory_sha256"],
    (
        f"observed={inventory['inventory_sha256']} "
        f"recorded={discovery['inventory_sha256']}"
    ),
)
for entry in inventory["rules"]:
    check(
        f"{entry['source_rule_id']} ID/hash identity",
        entry["source_rule_id"] == "rule-" + entry["normalized_sha256"],
        (
            f"span={entry['module']}:{entry['start_line']}-"
            f"{entry['end_line']}"
        ),
    )

# These are the audit's independently reached classifications, not values
# copied from Stage 3.
independent_classification = {
    "rule-0f02393212bfcf7e7c8810a806f9829aa2bbf9b5bd9795c9a7b5db26160d7995": (
        "DEFINITION"
    ),
    "rule-99644c7600e08ea07b0c26314084adf2ab5eb468a6b1eb4aadd857b2f427b14a": (
        "DEFINITION"
    ),
}
check(
    "independent classification covers inventory",
    list(independent_classification) == inventory_ids,
    independent_classification,
)
check(
    "Stage 3 classifications equal independent classifications",
    {
        entry["source_rule_id"]: entry["classification"]
        for entry in discovery["rules"]
    }
    == independent_classification,
)
true_domain_ids = [
    source_rule_id
    for source_rule_id, classification in independent_classification.items()
    if classification == "DOMAIN_LEMMA"
]
check("independent domain-lemma set is empty", true_domain_ids == [])

check(
    "input manifest exact definition records",
    input_manifest["definitions"] == validated["definitions"],
    f"count={len(input_manifest['definitions'])}",
)
check(
    "input manifest operational rules",
    input_manifest["operational_rules"] == validated["operational_rules"] == [],
)
check(
    "input manifest proved-derived lemmas",
    input_manifest["proved_derived_lemmas"]
    == validated["proved_derived_lemmas"]
    == [],
)
check(
    "input manifest domain source rules",
    input_manifest["source_rules"] == validated["domain_lemmas"] == [],
)
check(
    "source-rule/obligation empty bijection",
    true_domain_ids == []
    and obligation_map["source_rules"] == []
    and obligation_map["obligations"] == []
    and obligation_map["trust_parameters"] == [],
)

check(
    "input manifest Stage 1 hash",
    input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == observed_hashes["stage1_export_sha256"],
)
check(
    "input manifest Stage 3 hash",
    input_manifest["stage3_discovery_manifest_sha256"]
    == observed_hashes["discovery_manifest_sha256"],
)
check(
    "input manifest verification hash",
    input_manifest["verification_sha256"]
    == sha256_file(K_WORKSPACE / "verification.k"),
)
check(
    "input/generator inventory hash",
    input_manifest["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"]
    == inventory["inventory_sha256"],
)
check(
    "generator toolchain lock",
    generator_manifest["toolchain"] == toolchain_lock,
)
check(
    "generator producer hashes",
    generator_manifest["exporter_sha256"]
    == source_manifest["files"]["klean_export.py"]
    == sha256_file(PRODUCERS / "klean_export.py")
    and generator_manifest["klean_py_sha256"]
    == source_manifest["files"]["klean.py"]
    == sha256_file(PRODUCERS / "klean.py"),
)
audit_image_key = Path(resolution["generation_producer_sources"]).name
check(
    "generator immutable image ID",
    source_manifest["generator_image_id"]
    == generator_manifest["provenance"]["generator_image_id"]
    == "sha256:" + audit_image_key,
)
check(
    "generator Stage 1/Stage 3 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"]
    == observed_hashes["stage1_export_sha256"]
    and generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ]
    == observed_hashes["discovery_manifest_sha256"],
)
check(
    "generator generated-tree hash",
    generator_manifest["generated_tree_sha256"]
    == observed_hashes["generated_tree_sha256"],
)
check(
    "generator obligation-map hash",
    generator_manifest["obligation_map_sha256"]
    == sha256_file(GENERATED / "obligation-map.json"),
)
check(
    "generator obligation count and target",
    generator_manifest["obligation_count"] == 0
    and generator_manifest["target"] is None,
)

observed_target = klean_export.target_statement(GENERATED)
check(
    "fixed generated target is absent",
    observed_target is None
    and generator_manifest["target"] is None
    and stored_preflight["target"] is None
    and resolution["target"] is None,
)
check(
    "export-result binding",
    export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    and export_result["obligation_count"] == 0
    and export_result["frozen_input_sha256"]
    == observed_hashes["stage1_export_sha256"]
    and export_result["stage3_discovery_manifest_sha256"]
    == observed_hashes["discovery_manifest_sha256"]
    and export_result["generated_tree_sha256"]
    == observed_hashes["generated_tree_sha256"]
    and export_result["trust_inventory_sha256"]
    == sha256_file(GENERATION / "trust-inventory.json"),
)
check(
    "selection and launcher no-obligation status",
    resolution["mode"] == "CLASSIFICATION_ONLY"
    and resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS"
    and resolution["stage4_preflight"]["status"]
    == "KLEAN_NO_OBLIGATIONS"
    and resolution["stage4_preflight"]["obligation_count"] == 0,
)
check(
    "no Stage 5 candidate or result",
    not Path("/candidate").exists()
    and resolution["stage5_result"] is None
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None,
)

rerun_log = (
    Path("/audit-output/evidence/22-rerun-check-generation-success.log")
    .read_text()
)
rerun_payload = rerun_log.split("BEGIN OUTPUT\n", 1)[1].split(
    "\nEND OUTPUT", 1
)[0]
rerun_preflight = json.loads(rerun_payload)
check(
    "rerun preflight equals stored preflight",
    rerun_preflight == stored_preflight,
)
check(
    "rerun preflight equals launcher preflight",
    rerun_preflight == resolution["stage4_preflight"],
)

check(
    "exact regenerated generated project",
    klean_export.tree_digest(REGENERATION / "generated")
    == klean_export.tree_digest(GENERATED),
)
for name in (
    "generator-manifest.json",
    "trust-inventory.json",
    "export-result.json",
):
    check(
        f"exact regenerated {name}",
        (REGENERATION / name).read_bytes()
        == (GENERATION / name).read_bytes(),
    )

selected_input = load(GENERATION / "input-manifest.json")
regenerated_input = load(REGENERATION / "input-manifest.json")
selected_required = selected_input.pop("required_k_files")
regenerated_required = regenerated_input.pop("required_k_files")
check(
    "regenerated input manifest semantic fields",
    selected_input == regenerated_input,
)
selected_suffixes = [
    path.removeprefix("/frozen-k/") for path in selected_required
]
regenerated_suffixes = [
    path.removeprefix("/reference/k-proof/")
    for path in regenerated_required
]
check(
    "regenerated required-file closure",
    selected_suffixes == regenerated_suffixes,
    (
        "Only the expected generation-time versus audit-time absolute "
        "workspace prefix differs."
    ),
)

allowlist_names = [entry["name"] for entry in trust_inventory["allowlist"]]
check(
    "Stage 4 trust allowlist is unique",
    len(allowlist_names) == len(set(allowlist_names)) == 43,
)
check(
    "Stage 4 has no proof holes",
    trust_inventory["designated_sorries"] == 0
    and trust_inventory["other_sorries"] == 0,
)

print(f"TOTAL FAILURES: {len(failures)}")
for failure in failures:
    print(f"FAILURE: {failure}")
raise SystemExit(1 if failures else 0)
