#!/usr/bin/env python3
"""Independent hash, manifest, bijection, and target-identity checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import target_statement, tree_digest
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import verify_audit_input


AUDIT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK = Path("/reference/klean-toolchain.lock.json")
PREFLIGHT_RERUN = Path("/audit-output/evidence/preflight-result.json")


def load(path: Path):
    return json.loads(path.read_text())


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, condition: bool) -> None:
    print(f"{label}={condition}")
    if not condition:
        raise AssertionError(label)


def main() -> None:
    envelope = load(AUDIT)
    resolution, resolved_digest = verify_audit_input(envelope)
    check("audit_input.canonical_digest", resolved_digest == envelope["resolved_input_sha256"])
    check("audit_input.mode", resolution["mode"] == "CLASSIFICATION_ONLY")
    check("audit_input.problem", resolution["problem_id"] == "36-fizz-buzz")
    check("audit_input.condition", resolution["condition"] == "kit-semantics")
    check("audit_input.semantics", resolution["semantics_mode"] == "SUPPLIED_SEMANTICS")

    observed_hashes = {
        "k_workspace_sha256": sha256_tree(K_PROOF),
        "stage1_export_sha256": tree_digest(K_PROOF),
        "discovery_manifest_sha256": digest(DISCOVERY),
        "k_audit_sha256": sha256_tree(K_AUDIT),
        "klean_generation_sha256": sha256_tree(GENERATION),
        "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
        "generated_tree_sha256": tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    for key, observed in observed_hashes.items():
        check(f"audit_hash.{key}", resolution["hashes"][key] == observed)

    actual_sources = {
        path.relative_to(K_PROOF).as_posix(): digest(path)
        for path in K_PROOF.rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    check("audit_hash.stage1_source_hashes", actual_sources == resolution["stage1_source_hashes"])
    print(f"audit_hash.stage1_source_count={len(actual_sources)}")

    inventory = inventory_verification(K_PROOF)
    discovery = load(DISCOVERY)
    validated = validate_trust_boundary(K_PROOF, DISCOVERY)
    check("inventory.hash", inventory["inventory_sha256"] == discovery["inventory_sha256"])
    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    classified_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
    check("inventory.identity_order", canonical_ids == classified_ids)
    check("inventory.unique_ids", len(classified_ids) == len(set(classified_ids)))
    check("inventory.rule_count", len(canonical_ids) == 6)

    generator = load(GENERATION / "generator-manifest.json")
    inputs = load(GENERATION / "input-manifest.json")
    obligations = load(GENERATED / "obligation-map.json")
    export = load(GENERATION / "export-result.json")
    trust = load(GENERATION / "trust-inventory.json")
    lock = load(LOCK)
    source_manifest = load(PRODUCERS / "source-manifest.json")
    on_disk_preflight = load(GENERATION / "preflight.json")
    rerun_preflight = load(PREFLIGHT_RERUN)

    expected_image = generator["provenance"]["generator_image_id"]
    audit_path_image = "sha256:" + Path(resolution["generation_producer_sources"]).name
    check("producer.bundle_members", sorted(p.name for p in PRODUCERS.iterdir()) == ["klean.py", "klean_export.py", "source-manifest.json"])
    check("producer.image_identity", expected_image == source_manifest["generator_image_id"] == audit_path_image)
    producer_fields = {"klean_export.py": "exporter_sha256", "klean.py": "klean_py_sha256"}
    for name, field in producer_fields.items():
        observed = digest(PRODUCERS / name)
        check(f"producer.hash.{name}", observed == generator[field] == source_manifest["files"][name])

    check("manifest.toolchain", generator["toolchain"] == lock)
    check("manifest.generated_tree", generator["generated_tree_sha256"] == observed_hashes["generated_tree_sha256"])
    check("manifest.obligation_map_hash", generator["obligation_map_sha256"] == digest(GENERATED / "obligation-map.json"))
    check("manifest.stage1_provenance", generator["provenance"]["stage1_workspace_sha256"] == inputs["stage1_workspace_sha256"] == observed_hashes["stage1_export_sha256"])
    check("manifest.discovery_provenance", generator["provenance"]["stage3_discovery_manifest_sha256"] == inputs["stage3_discovery_manifest_sha256"] == observed_hashes["discovery_manifest_sha256"])
    check("manifest.inventory_provenance", generator["provenance"]["inventory_sha256"] == inputs["inventory_sha256"] == inventory["inventory_sha256"])
    check("manifest.verification_hash", inputs["verification_sha256"] == digest(K_PROOF / "verification.k") == inventory["verification_sha256"])
    check("manifest.definitions", inputs["definitions"] == validated["definitions"])
    check("manifest.operational_rules", inputs["operational_rules"] == validated["operational_rules"] == [])
    check("manifest.proved_derived_lemmas", inputs["proved_derived_lemmas"] == validated["proved_derived_lemmas"] == [])

    # Independent Stage 3 judgment is recorded separately; its domain ID set is empty.
    independent_domain_ids: list[str] = []
    mapped_source_ids = [entry["source_rule_id"] for entry in obligations["source_rules"]]
    obligation_ids = [entry["source_rule_id"] for entry in obligations["obligations"]]
    check("bijection.independent_domain_to_source", independent_domain_ids == mapped_source_ids)
    check("bijection.source_to_obligation", mapped_source_ids == obligation_ids)
    check("bijection.unique", len(obligation_ids) == len(set(obligation_ids)))
    check("bijection.no_trust_parameters", obligations["trust_parameters"] == [])
    check("bijection.generator_count", generator["obligation_count"] == len(obligation_ids) == 0)
    check("bijection.export_count", export["obligation_count"] == len(obligation_ids))

    observed_target = target_statement(GENERATED)
    check("target.generator_none", generator["target"] is None)
    check("target.audit_none", resolution["target"] is None)
    check("target.generated_none", observed_target is None)
    check("target.no_candidate", not Path("/candidate").exists())
    check("target.no_stage5", resolution["stage5_result"] is None and resolution["lean_workspace"] is None and resolution["lean_invocation"] is None)

    check("export.status", export["status"] == "KLEAN_NO_OBLIGATIONS")
    check("export.generated_tree", export["generated_tree_sha256"] == observed_hashes["generated_tree_sha256"])
    check("export.stage1", export["frozen_input_sha256"] == observed_hashes["stage1_export_sha256"])
    check("export.discovery", export["stage3_discovery_manifest_sha256"] == observed_hashes["discovery_manifest_sha256"])
    check("export.trust_hash", export["trust_inventory_sha256"] == digest(GENERATION / "trust-inventory.json"))
    check("trust.count", len(trust["allowlist"]) == len(trust["axioms"]) == 43)
    check("trust.no_sorries", trust["designated_sorries"] == trust["other_sorries"] == 0)

    check("preflight.rerun_equals_recorded", rerun_preflight == on_disk_preflight == resolution["stage4_preflight"])
    check("preflight.status", rerun_preflight["status"] == "KLEAN_NO_OBLIGATIONS")
    check("preflight.target", rerun_preflight["target"] is None)
    check("preflight.build", [item["exit_code"] for item in rerun_preflight["diagnostics"]] == [0, 0])
    print("RESULT=PASS")


if __name__ == "__main__":
    main()
