#!/usr/bin/env python3
"""Independent structural and target checks for the selected Stage 4 output."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


K_PROOF = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, condition: bool, details: object = None) -> dict:
    return {"name": name, "pass": condition, "details": details}


def main() -> None:
    audit_input = load(Path("/audit-input.json"))["resolution"]
    discovery_hash = sha(DISCOVERY)
    input_manifest = load(GENERATION / "input-manifest.json")
    generator_manifest = load(GENERATION / "generator-manifest.json")
    export_result = load(GENERATION / "export-result.json")
    recorded_preflight = load(GENERATION / "preflight.json")
    trust_inventory = load(GENERATION / "trust-inventory.json")
    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = load(obligation_map_path)
    lock = load(Path("/reference/klean-toolchain.lock.json"))

    inventory = inventory_verification(K_PROOF)
    validated = validate_trust_boundary(K_PROOF, DISCOVERY)
    domain_rules = validated["domain_lemmas"]
    domain_ids = [rule["source_rule_id"] for rule in domain_rules]
    generated_source_rules = obligation_map.get("source_rules")
    generated_obligations = obligation_map.get("obligations")
    generated_obligation_ids = [
        item.get("source_rule_id")
        for item in generated_obligations
        if isinstance(item, dict)
    ] if isinstance(generated_obligations, list) else None

    stage1_tree = klean_export.tree_digest(K_PROOF)
    generated_tree = klean_export.tree_digest(GENERATED)
    observed_target = klean_export.target_statement(GENERATED)
    expected_target = klean_export.expected_target_definition(obligation_map)

    lean_files = sorted(GENERATED.rglob("*.lean"))
    target_occurrences = []
    for path in lean_files:
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            if re.search(r"\btargetStatement\b", line):
                target_occurrences.append({
                    "file": path.relative_to(GENERATED).as_posix(),
                    "line": line_number,
                    "text": line,
                })

    validated_definitions = validated["definitions"]
    checks = [
        check("input inventory hash", input_manifest.get("inventory_sha256") == inventory["inventory_sha256"]),
        check("generator inventory provenance", generator_manifest.get("provenance", {}).get("inventory_sha256") == inventory["inventory_sha256"]),
        check("input verification hash", input_manifest.get("verification_sha256") == inventory["verification_sha256"]),
        check("input Stage 1 tree hash", input_manifest.get("stage1_workspace_sha256") == stage1_tree),
        check("input frozen tree hash", input_manifest.get("frozen_input_sha256") == stage1_tree),
        check("generator Stage 1 provenance", generator_manifest.get("provenance", {}).get("stage1_workspace_sha256") == stage1_tree),
        check("export Stage 1 tree hash", export_result.get("frozen_input_sha256") == stage1_tree),
        check("input discovery hash", input_manifest.get("stage3_discovery_manifest_sha256") == discovery_hash),
        check("generator discovery provenance", generator_manifest.get("provenance", {}).get("stage3_discovery_manifest_sha256") == discovery_hash),
        check("export discovery hash", export_result.get("stage3_discovery_manifest_sha256") == discovery_hash),
        check("definitions exact ordered records", input_manifest.get("definitions") == validated_definitions),
        check("input operational set exact", input_manifest.get("operational_rules") == validated["operational_rules"]),
        check("input proved-derived set exact", input_manifest.get("proved_derived_lemmas") == validated["proved_derived_lemmas"]),
        check("input domain set exact", input_manifest.get("source_rules") == domain_rules),
        check("obligation-map source set exact", generated_source_rules == domain_rules),
        check("domain/source/obligation ordered IDs", domain_ids == generated_obligation_ids, {
            "domain_ids": domain_ids,
            "obligation_ids": generated_obligation_ids,
        }),
        check("obligation IDs unique", generated_obligation_ids is not None and len(generated_obligation_ids) == len(set(generated_obligation_ids))),
        check("trust parameters empty for empty obligations", obligation_map.get("trust_parameters") == []),
        check("generator obligation count", generator_manifest.get("obligation_count") == len(domain_ids)),
        check("export obligation count", export_result.get("obligation_count") == len(domain_ids)),
        check("recorded preflight obligation count", recorded_preflight.get("obligation_count") == len(domain_ids)),
        check("obligation map hash", generator_manifest.get("obligation_map_sha256") == sha(obligation_map_path)),
        check("generated tree hash", generator_manifest.get("generated_tree_sha256") == generated_tree),
        check("export generated tree hash", export_result.get("generated_tree_sha256") == generated_tree),
        check("audit-input generated tree hash", audit_input["hashes"].get("generated_tree_sha256") == generated_tree),
        check("trust inventory hash", export_result.get("trust_inventory_sha256") == sha(GENERATION / "trust-inventory.json")),
        check("toolchain exact lock", generator_manifest.get("toolchain") == lock),
        check("zero-domain status", export_result.get("status") == "KLEAN_NO_OBLIGATIONS" and recorded_preflight.get("status") == "KLEAN_NO_OBLIGATIONS"),
        check("expected target absent", expected_target is None),
        check("observed target absent", observed_target is None),
        check("target text absent", target_occurrences == [], target_occurrences),
        check("generator target null", generator_manifest.get("target") is None),
        check("audit-input target null", audit_input.get("target") is None),
        check("Stage 5 result null", audit_input.get("stage5_result") is None),
        check("Stage 5 candidate absent", not Path("/candidate").exists()),
    ]

    print(json.dumps({
        "all_checks_pass": all(item["pass"] for item in checks),
        "independent_domain_rule_count": len(domain_rules),
        "generated_obligation_count": len(generated_obligations) if isinstance(generated_obligations, list) else None,
        "expected_target_definition": expected_target,
        "observed_target": observed_target,
        "checks": checks,
        "manifest_hashes": {
            "input-manifest.json": sha(GENERATION / "input-manifest.json"),
            "generator-manifest.json": sha(GENERATION / "generator-manifest.json"),
            "export-result.json": sha(GENERATION / "export-result.json"),
            "preflight.json": sha(GENERATION / "preflight.json"),
            "trust-inventory.json": sha(GENERATION / "trust-inventory.json"),
            "obligation-map.json": sha(obligation_map_path),
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
