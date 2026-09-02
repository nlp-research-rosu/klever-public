#!/usr/bin/env python3
"""Independent zero-obligation and zero-target structural audit."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


K_WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
AUDIT_INPUT = Path("/audit-input.json")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def check(label: str, condition: bool, detail: object) -> bool:
    print(f"{label}: {'PASS' if condition else 'FAIL'}")
    print(f"  {detail}")
    return condition


def main() -> int:
    inventory = inventory_verification(K_WORKSPACE)
    discovery = json.loads(DISCOVERY.read_text())
    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    export_result = json.loads(
        (GENERATION / "export-result.json").read_text()
    )
    preflight = json.loads(
        (GENERATION / "preflight.json").read_text()
    )
    obligation_map = json.loads(
        (GENERATED / "obligation-map.json").read_text()
    )
    audit = json.loads(AUDIT_INPUT.read_text())["resolution"]
    toolchain_lock = json.loads(TOOLCHAIN_LOCK.read_text())

    results: list[bool] = []
    canonical_rules = inventory["rules"]
    classified_rules = discovery["rules"]
    canonical_ids = [rule["source_rule_id"] for rule in canonical_rules]
    classified_ids = [
        rule["source_rule_id"] for rule in classified_rules
    ]
    results.append(
        check(
            "Stage 1/Stage 3 ordered identity bijection",
            canonical_ids == classified_ids
            and len(set(classified_ids)) == len(classified_ids),
            {
                "canonical_ids": canonical_ids,
                "classified_ids": classified_ids,
            },
        )
    )
    results.append(
        check(
            "canonical inventory hash",
            inventory["inventory_sha256"]
            == canonical_json_sha256(canonical_rules)
            == discovery["inventory_sha256"],
            {
                "recomputed": canonical_json_sha256(canonical_rules),
                "inventory": inventory["inventory_sha256"],
                "discovery": discovery["inventory_sha256"],
            },
        )
    )
    results.append(
        check(
            "pinned toolchain identity",
            generator_manifest["toolchain"] == toolchain_lock,
            {
                "generator_manifest": generator_manifest["toolchain"],
                "trusted_lock": toolchain_lock,
            },
        )
    )

    stage4_source_rules = input_manifest["source_rules"]
    mapped_source_rules = obligation_map["source_rules"]
    obligations = obligation_map["obligations"]
    obligation_ids = [
        obligation.get("source_rule_id") for obligation in obligations
    ]
    source_ids = [
        source_rule.get("source_rule_id")
        for source_rule in stage4_source_rules
    ]
    results.append(
        check(
            "Stage 3 DOMAIN_LEMMA/Stage 4 source-rule bijection",
            stage4_source_rules == mapped_source_rules
            and source_ids == obligation_ids
            and len(set(obligation_ids)) == len(obligation_ids),
            {
                "input_source_rules": stage4_source_rules,
                "mapped_source_rules": mapped_source_rules,
                "obligation_ids": obligation_ids,
            },
        )
    )
    vacuous = [
        obligation.get("source_rule_id")
        for obligation in obligations
        if not isinstance(obligation.get("lean_conjunct"), str)
        or not obligation["lean_conjunct"].strip()
        or obligation["lean_conjunct"].strip()
        in {"True", "(True)", "by trivial"}
    ]
    results.append(
        check(
            "non-vacuous generated conjuncts",
            not vacuous,
            {
                "obligation_count": len(obligations),
                "vacuous_ids": vacuous,
                "note": "empty obligation set has no conjunct to weaken",
            },
        )
    )

    target_declarations: list[str] = []
    for path in sorted(GENERATED.rglob("*.lean")):
        text = path.read_text()
        for match in re.finditer(
            r"(?m)^\s*(?:def|theorem|lemma|axiom|opaque)\s+targetStatement\b",
            text,
        ):
            target_declarations.append(
                f"{path.relative_to(GENERATED)}:{text.count(chr(10), 0, match.start()) + 1}"
            )
    targets = {
        "generator_manifest": generator_manifest["target"],
        "recorded_preflight": preflight["target"],
        "audit_input": audit["target"],
    }
    results.append(
        check(
            "fixed generated target is absent",
            target_declarations == []
            and all(target is None for target in targets.values()),
            {
                "declarations": target_declarations,
                "recorded_targets": targets,
            },
        )
    )

    statuses = {
        "selected": audit["selections"]["klean_generation"]["status"],
        "export": export_result["status"],
        "recorded_preflight": preflight["status"],
        "audit_stage4": audit["stage4_preflight"]["status"],
    }
    counts = {
        "generator_manifest": generator_manifest["obligation_count"],
        "export": export_result["obligation_count"],
        "recorded_preflight": preflight["obligation_count"],
        "audit_stage4": audit["stage4_preflight"]["obligation_count"],
    }
    results.append(
        check(
            "zero-obligation status/count consistency",
            all(
                status == "KLEAN_NO_OBLIGATIONS"
                for status in statuses.values()
            )
            and all(count == 0 for count in counts.values())
            and obligations == []
            and stage4_source_rules == [],
            {"statuses": statuses, "counts": counts},
        )
    )
    candidate_exists = Path("/candidate").exists()
    results.append(
        check(
            "classification-only candidate absence",
            audit["mode"] == "CLASSIFICATION_ONLY"
            and audit["stage5_result"] is None
            and audit["lean_workspace"] is None
            and audit["lean_invocation"] is None
            and not candidate_exists,
            {
                "mode": audit["mode"],
                "stage5_result": audit["stage5_result"],
                "lean_workspace": audit["lean_workspace"],
                "lean_invocation": audit["lean_invocation"],
                "candidate_exists": candidate_exists,
            },
        )
    )

    print("OVERALL=" + ("PASS" if all(results) else "FAIL"))
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
