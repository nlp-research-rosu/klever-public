#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, discovery_path
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
stored_preflight = json.loads((generation / "preflight.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

preflight_log = Path(
    "/audit-output/evidence/05_stage4_preflight.log"
).read_text()
marker = "RETURNED_EVIDENCE\n"
if marker not in preflight_log:
    raise RuntimeError("successful preflight returned evidence is missing")
rerun_document = json.loads(preflight_log.split(marker, 1)[1])
rerun_preflight = rerun_document["check_generation"]

lean_sources = sorted(generated.rglob("*.lean"))
target_mentions = []
for source in lean_sources:
    for line_number, line in enumerate(source.read_text().splitlines(), 1):
        if re.search(r"\btargetStatement\b", line):
            target_mentions.append(
                {
                    "source": source.relative_to(generated).as_posix(),
                    "line": line_number,
                    "text": line,
                }
            )

expected_domain_ids = [
    rule["source_rule_id"] for rule in validated["domain_lemmas"]
]
source_rule_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
mapped_source_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

result = {
    "classification_partition_vs_input_manifest": {
        "definitions_equal": input_manifest["definitions"]
        == validated["definitions"],
        "operational_rules_equal": input_manifest["operational_rules"]
        == validated["operational_rules"],
        "proved_derived_lemmas_equal": input_manifest["proved_derived_lemmas"]
        == validated["proved_derived_lemmas"],
        "domain_source_ids_expected": expected_domain_ids,
        "domain_source_ids_input_manifest": source_rule_ids,
    },
    "obligation_bijection": {
        "expected_domain_ids": expected_domain_ids,
        "input_manifest_source_rule_ids": source_rule_ids,
        "obligation_map_source_rule_ids": mapped_source_rule_ids,
        "obligation_ids": obligation_ids,
        "unique_obligation_ids": len(set(obligation_ids)),
        "source_and_obligation_ordered_bijection": (
            expected_domain_ids
            == source_rule_ids
            == mapped_source_rule_ids
            == obligation_ids
            and len(obligation_ids) == len(set(obligation_ids))
        ),
        "trust_parameters": obligation_map["trust_parameters"],
        "no_vacuous_conjuncts": len(obligation_map["obligations"]) == 0,
    },
    "fixed_target": {
        "trusted_target_parser_result": klean_export.target_statement(generated),
        "generator_manifest_target": generator_manifest["target"],
        "audit_input_target": resolution["target"],
        "audit_input_preflight_target": resolution["stage4_preflight"][
            "target"
        ],
        "target_text_mentions": target_mentions,
        "target_absent_everywhere": (
            klean_export.target_statement(generated) is None
            and generator_manifest["target"] is None
            and resolution["target"] is None
            and resolution["stage4_preflight"]["target"] is None
            and not target_mentions
        ),
    },
    "status_consistency": {
        "selected_status": resolution["selections"]["klean_generation"][
            "status"
        ],
        "export_status": export_result["status"],
        "stored_preflight_status": stored_preflight["status"],
        "rerun_preflight_status": rerun_preflight["status"],
        "generator_obligation_count": generator_manifest["obligation_count"],
        "export_obligation_count": export_result["obligation_count"],
        "stored_preflight_obligation_count": stored_preflight[
            "obligation_count"
        ],
        "rerun_preflight_obligation_count": rerun_preflight[
            "obligation_count"
        ],
        "obligation_map_count": len(obligation_map["obligations"]),
        "all_no_obligations": (
            resolution["selections"]["klean_generation"]["status"]
            == "KLEAN_NO_OBLIGATIONS"
            and export_result["status"] == "KLEAN_NO_OBLIGATIONS"
            and stored_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
            and rerun_preflight["status"] == "KLEAN_NO_OBLIGATIONS"
            and generator_manifest["obligation_count"] == 0
            and export_result["obligation_count"] == 0
            and stored_preflight["obligation_count"] == 0
            and rerun_preflight["obligation_count"] == 0
            and not obligation_map["obligations"]
        ),
        "rerun_equals_stored_preflight": rerun_preflight == stored_preflight,
        "stored_preflight_equals_audit_input": stored_preflight
        == resolution["stage4_preflight"],
    },
    "hash_bindings": {
        "obligation_map_actual": sha256(obligation_map_path),
        "obligation_map_manifest": generator_manifest[
            "obligation_map_sha256"
        ],
        "generated_tree_actual": klean_export.tree_digest(generated),
        "generated_tree_manifest": generator_manifest[
            "generated_tree_sha256"
        ],
        "generated_tree_audit_input": resolution["hashes"][
            "generated_tree_sha256"
        ],
        "trust_inventory_actual": sha256(generation / "trust-inventory.json"),
        "trust_inventory_export_result": export_result[
            "trust_inventory_sha256"
        ],
    },
    "stage5_absence": {
        "audit_mode": resolution["mode"],
        "lean_workspace": resolution["lean_workspace"],
        "lean_invocation": resolution["lean_invocation"],
        "stage5_result": resolution["stage5_result"],
        "candidate_exists": Path("/candidate").exists(),
        "generated_proof_file_exists": (generated / "Proof.lean").exists(),
        "properly_absent": (
            resolution["mode"] == "CLASSIFICATION_ONLY"
            and resolution["lean_workspace"] is None
            and resolution["lean_invocation"] is None
            and resolution["stage5_result"] is None
            and not Path("/candidate").exists()
            and not (generated / "Proof.lean").exists()
        ),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
