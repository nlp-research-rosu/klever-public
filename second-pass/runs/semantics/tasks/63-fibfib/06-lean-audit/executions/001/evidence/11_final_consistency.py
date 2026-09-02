#!/usr/bin/env python3
"""Fail closed if the final review disagrees with recorded audit evidence."""

from __future__ import annotations

import json
from pathlib import Path


root = Path("/audit-output")
integrity = json.loads((root / "evidence/02_integrity_inventory.json").read_text())
preflight = json.loads((root / "evidence/04_preflight.json").read_text())
stage4 = json.loads((root / "evidence/05_stage4_bijection.json").read_text())
stage5 = json.loads((root / "evidence/09_stage5_identity.json").read_text())
mechanical = json.loads(
    (root / "evidence/10_mechanical_final_gate.json").read_text()
)
build_log = (root / "evidence/06_fresh_stage5_build.log").read_text()
review = (root / "REVIEW.md").read_text()

checks = {
    "producer_provenance": integrity["producer_provenance"][
        "all_file_hashes_match"
    ]
    and integrity["producer_provenance"]["image_ids_match"]
    and integrity["producer_provenance"]["bundle_tree_hash_matches"],
    "mounted_hashes": integrity["mounted_hashes"][
        "all_recorded_top_level_hashes_match"
    ]
    and integrity["mounted_hashes"]["stage1_source_hashes_exact"],
    "inventory_ordered_bijection": integrity["discovery_comparison"][
        "exact_ordered_identity_bijection"
    ],
    "inventory_spans_and_hashes": all(
        item["span_matches_inventory_text"]
        and item["hash_matches_inventory"]
        and item["id_matches_inventory"]
        for item in integrity["independent_span_hash_recomputation"]
    ),
    "fresh_preflight": preflight["status"] == "PASS"
    and preflight["obligation_count"] == 1,
    "stage4_bijection": stage4["source_obligation_ordered_bijection"]
    and stage4["exact_operational_translation"]
    and stage4["target_exactly_expected_conjunction"],
    "stage4_target_identity": stage4["target_matches_generator_manifest"]
    and stage4["target_matches_audit_input"]
    and stage4["target_matches_recorded_preflight"],
    "fresh_clean_build": "lake_clean_exit=0" in build_log
    and "lake_build_exit=0" in build_log,
    "candidate_policy": stage5["no_forbidden_candidate_tokens"]
    and stage5["target_shadow_declaration_count"] == 0
    and stage5["parameter_definitions_exact"],
    "proof_identity": stage5["final_statement_exact"]
    and stage5["target_source_unchanged"],
    "axiom_accounting": stage5["used_axioms"] == ["propext"]
    and stage5["used_generated_allowlist_axioms"] == []
    and stage5["sorryAx_absent"]
    and stage5["all_used_axioms_accounted"],
    "trusted_final_gate": mechanical["status"] == "PASS"
    and mechanical["used_axioms"] == ["propext"],
    "exact_final_pair": review.endswith(
        "VERDICT: PASS\nLEGITIMACY: LEGIT\n"
    )
    and review.count("VERDICT:") == 1
    and review.count("LEGITIMACY:") == 1,
}

if not all(checks.values()):
    raise SystemExit(
        "final consistency failure: "
        + ", ".join(name for name, passed in checks.items() if not passed)
    )
print(json.dumps({"status": "PASS", "checks": checks}, indent=2, sort_keys=True))
