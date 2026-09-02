#!/usr/bin/env python3
"""Bind the independent Stage 3 classification to Stage 4's fixed output."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export


ROOT = Path("/reference/klean-generation")
GENERATED = ROOT / "generated"


def load(path: Path):
    return json.loads(path.read_text())


def ids(records):
    return [record["source_rule_id"] for record in records]


def main() -> int:
    independent = load(
        Path("/audit-output/evidence/independent-classification.json")
    )
    discovery = load(Path("/reference/lemma-discovery.json"))
    input_manifest = load(ROOT / "input-manifest.json")
    generator_manifest = load(ROOT / "generator-manifest.json")
    export_result = load(ROOT / "export-result.json")
    obligation_map = load(GENERATED / "obligation-map.json")
    audit_resolution = load(Path("/audit-input.json"))["resolution"]

    independent_rules = independent["rules"]
    independent_ids = ids(independent_rules)
    discovery_ids = ids(discovery["rules"])
    independent_roles = [record["classification"] for record in independent_rules]
    discovery_roles = [record["classification"] for record in discovery["rules"]]
    by_role = {
        role: [
            record["source_rule_id"]
            for record in independent_rules
            if record["classification"] == role
        ]
        for role in (
            "DEFINITION",
            "OPERATIONAL_RULE",
            "PROVED_DERIVED_LEMMA",
            "DOMAIN_LEMMA",
        )
    }

    manifest_partitions = {
        "DEFINITION": ids(input_manifest["definitions"]),
        "OPERATIONAL_RULE": ids(input_manifest["operational_rules"]),
        "PROVED_DERIVED_LEMMA": ids(
            input_manifest["proved_derived_lemmas"]
        ),
        "DOMAIN_LEMMA": ids(input_manifest["source_rules"]),
    }
    map_source_ids = ids(obligation_map["source_rules"])
    obligation_ids = ids(obligation_map["obligations"])
    target_observed = klean_export.target_statement(GENERATED)

    actual_lean_declarations = []
    for path in sorted(GENERATED.rglob("*.lean")):
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            stripped = line.strip()
            if stripped.startswith(("theorem ", "lemma ")):
                actual_lean_declarations.append(
                    {
                        "source": path.relative_to(GENERATED).as_posix(),
                        "line": line_number,
                        "text": stripped,
                    }
                )

    map_hash = hashlib.sha256(
        (GENERATED / "obligation-map.json").read_bytes()
    ).hexdigest()
    no_vacuous_conjuncts = all(
        isinstance(obligation.get("lean_conjunct"), str)
        and obligation["lean_conjunct"].strip()
        and not re.fullmatch(r"(?:True|\(?\s*True\s*\)?)", obligation["lean_conjunct"].strip())
        for obligation in obligation_map["obligations"]
    )

    checks = {
        "independent_vs_protected_ordered_ids": independent_ids == discovery_ids,
        "independent_vs_protected_ordered_classifications": (
            independent_roles == discovery_roles
        ),
        "input_manifest_partitions_match_independent": all(
            manifest_partitions[role] == by_role[role]
            for role in by_role
        ),
        "true_domain_ids": by_role["DOMAIN_LEMMA"],
        "input_manifest_source_rule_ids": manifest_partitions["DOMAIN_LEMMA"],
        "obligation_map_source_rule_ids": map_source_ids,
        "obligation_ids": obligation_ids,
        "source_obligation_ordered_bijection": (
            by_role["DOMAIN_LEMMA"] == map_source_ids == obligation_ids
            and len(obligation_ids) == len(set(obligation_ids))
        ),
        "no_vacuous_conjuncts": no_vacuous_conjuncts,
        "generator_obligation_count": generator_manifest["obligation_count"],
        "export_obligation_count": export_result["obligation_count"],
        "map_obligation_count": len(obligation_ids),
        "obligation_counts_match": (
            generator_manifest["obligation_count"]
            == export_result["obligation_count"]
            == len(obligation_ids)
            == 0
        ),
        "obligation_map_sha256_actual": map_hash,
        "obligation_map_sha256_manifest": generator_manifest[
            "obligation_map_sha256"
        ],
        "obligation_map_hash_matches": map_hash
        == generator_manifest["obligation_map_sha256"],
        "target_observed": target_observed,
        "target_generator_manifest": generator_manifest["target"],
        "target_audit_input": audit_resolution["target"],
        "target_preflight_audit_input": audit_resolution["stage4_preflight"][
            "target"
        ],
        "all_target_records_null": (
            target_observed is None
            and generator_manifest["target"] is None
            and audit_resolution["target"] is None
            and audit_resolution["stage4_preflight"]["target"] is None
        ),
        "lean_theorem_or_lemma_declarations": actual_lean_declarations,
        "no_generated_theorem_or_lemma": not actual_lean_declarations,
        "export_status": export_result["status"],
        "selection_status": audit_resolution["selections"]["klean_generation"][
            "status"
        ],
        "status_is_no_obligations": (
            export_result["status"] == "KLEAN_NO_OBLIGATIONS"
            and audit_resolution["selections"]["klean_generation"]["status"]
            == "KLEAN_NO_OBLIGATIONS"
        ),
        "candidate_present": Path("/candidate").exists(),
        "stage5_result": audit_resolution["stage5_result"],
        "no_stage5_artifact": (
            not Path("/candidate").exists()
            and audit_resolution["stage5_result"] is None
            and audit_resolution["lean_workspace"] is None
            and audit_resolution["lean_invocation"] is None
        ),
    }
    required = (
        checks["independent_vs_protected_ordered_ids"],
        checks["independent_vs_protected_ordered_classifications"],
        checks["input_manifest_partitions_match_independent"],
        not checks["true_domain_ids"],
        checks["source_obligation_ordered_bijection"],
        checks["no_vacuous_conjuncts"],
        checks["obligation_counts_match"],
        checks["obligation_map_hash_matches"],
        checks["all_target_records_null"],
        checks["no_generated_theorem_or_lemma"],
        checks["status_is_no_obligations"],
        checks["no_stage5_artifact"],
    )
    checks["all_stage4_checks_pass"] = all(required)
    print(json.dumps(checks, indent=2, sort_keys=True))
    return 0 if checks["all_stage4_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
