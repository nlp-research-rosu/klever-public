#!/usr/bin/env python3
"""Independent Stage 4 source/obligation/target identity checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


FROZEN = Path("/reference/k-proof")
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def result(name: str, ok: bool, detail: object | None = None) -> bool:
    print(f"{name}: {'PASS' if ok else 'FAIL'}")
    if detail is not None:
        print(f"  {detail}")
    return ok


def main() -> int:
    discovery_hash = hashlib.sha256(DISCOVERY_PATH.read_bytes()).hexdigest()
    validated = lemma_discovery_contract.validate_trust_boundary(
        FROZEN, DISCOVERY_PATH
    )
    expected_domain = klean_export._domain_source_rules(
        validated, discovery_hash
    )
    input_manifest = load(GENERATION / "input-manifest.json")
    generator_manifest = load(GENERATION / "generator-manifest.json")
    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = load(obligation_map_path)
    audit_input = load(Path("/audit-input.json"))["resolution"]
    preflight = load(GENERATION / "preflight.json")

    checks: list[bool] = []
    checks.append(
        result(
            "independent_domain_set_equals_input_manifest",
            input_manifest.get("source_rules") == expected_domain,
            [rule["source_rule_id"] for rule in expected_domain],
        )
    )
    checks.append(
        result(
            "independent_domain_set_equals_obligation_source_rules",
            obligation_map.get("source_rules") == expected_domain,
        )
    )

    obligations = obligation_map["obligations"]
    expected_ids = [rule["source_rule_id"] for rule in expected_domain]
    observed_ids = [item["source_rule_id"] for item in obligations]
    checks.append(
        result(
            "source_rule_obligation_ordered_bijection",
            observed_ids == expected_ids
            and len(observed_ids) == len(set(observed_ids)),
            {"expected": expected_ids, "observed": observed_ids},
        )
    )
    obligation_hashes_ok = True
    provenance_ok = True
    spans_ok = True
    for source, obligation in zip(expected_domain, obligations):
        obligation_hashes_ok &= obligation.get(
            "lean_conjunct_sha256"
        ) == klean_export.sha256_text(obligation["lean_conjunct"])
        provenance_ok &= all(
            obligation.get(key) == source.get(key)
            for key in (
                "source_rule_id",
                "normalized_sha256",
                "inventory_sha256",
                "discovery_manifest_sha256",
            )
        )
        spans_ok &= obligation.get("source_span") == {
            "start_line": source["start_line"],
            "end_line": source["end_line"],
        }
    checks.append(result("lean_conjunct_hashes", obligation_hashes_ok))
    checks.append(result("obligation_provenance", provenance_ok))
    checks.append(result("obligation_source_spans", spans_ok))

    map_hash = hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
    checks.append(
        result(
            "obligation_map_sha256",
            generator_manifest.get("obligation_map_sha256") == map_hash,
            map_hash,
        )
    )
    checks.append(
        result(
            "obligation_counts",
            len(obligations)
            == generator_manifest.get("obligation_count")
            == preflight.get("obligation_count")
            == 1,
            len(obligations),
        )
    )

    expected_definition = klean_export.expected_target_definition(
        obligation_map
    )
    target = klean_export.target_statement(GENERATED)
    checks.append(
        result(
            "fixed_target_is_exact_obligation_conjunction",
            expected_definition is not None
            and target is not None
            and target["definition_sha256"]
            == klean_export.sha256_text(expected_definition),
            target,
        )
    )
    target_copies = [
        generator_manifest.get("target"),
        preflight.get("target"),
        audit_input.get("target"),
        audit_input.get("stage4_preflight", {}).get("target"),
    ]
    checks.append(
        result(
            "target_identical_across_generator_preflight_audit_input",
            target is not None and all(item == target for item in target_copies),
        )
    )

    parameters = obligation_map.get("trust_parameters", [])
    parameter_ids = {
        source_rule_id
        for parameter in parameters
        for source_rule_id in parameter.get("source_rule_ids", [])
    }
    checks.append(
        result(
            "target_parameter_links_cover_domain_ids",
            parameter_ids == set(expected_ids),
            sorted(parameter_ids),
        )
    )
    checks.append(
        result(
            "target_parameter_bindings_match_target",
            target is not None
            and target.get("parameters") == parameters
            and len(parameters) == 7
            and len({p["name"] for p in parameters}) == 7,
        )
    )

    proof_text = Path("/candidate/Proof.lean").read_text()
    theorem_matches = re.findall(
        r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
        proof_text,
    )
    theorem_ok = (
        target is not None
        and len(theorem_matches) == 1
        and " ".join(theorem_matches[0].split())
        == " ".join(target["statement"].split())
    )
    checks.append(result("candidate_final_exact_target", theorem_ok))
    checks.append(
        result(
            "candidate_does_not_shadow_target",
            not re.search(
                r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b",
                proof_text,
            ),
        )
    )

    overall = all(checks)
    print("OVERALL:", "PASS" if overall else "FAIL")
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
