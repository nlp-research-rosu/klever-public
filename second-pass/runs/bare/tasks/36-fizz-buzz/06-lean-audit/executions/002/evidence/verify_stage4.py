#!/usr/bin/env python3
"""Independent hash, bijection, and fixed-target checks for Stage 4."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
FROZEN = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
CANDIDATE = Path("/candidate")
K_AUDIT = Path("/reference/k-audit")
TOOLS = Path("/reference/tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict)
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = load(AUDIT_INPUT)
resolution = audit_document["resolution"]
recorded_hashes = resolution["hashes"]
discovery = load(DISCOVERY)
input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
export_result = load(GENERATION / "export-result.json")
preflight = load(GENERATION / "preflight.json")
trust_inventory = load(GENERATION / "trust-inventory.json")
obligation_map = load(GENERATED / "obligation-map.json")
inventory = inventory_verification(FROZEN)

checks: list[dict] = []


def check(name: str, condition: bool, detail: object) -> None:
    checks.append({"name": name, "pass": bool(condition), "detail": detail})


verified_resolution, resolved_digest = (
    stage6_resolution_contract.verify_audit_input(audit_document)
)
check(
    "audit-input canonical binding",
    verified_resolution == resolution
    and resolved_digest == audit_document["resolved_input_sha256"],
    {
        "recomputed": resolved_digest,
        "recorded": audit_document["resolved_input_sha256"],
    },
)

tree_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(FROZEN),
    "stage1_export_sha256": klean_export.tree_digest(FROZEN),
    "discovery_manifest_sha256": sha256_file(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(CANDIDATE),
}
for name, actual in tree_hashes.items():
    check(
        f"audit-input hash {name}",
        recorded_hashes.get(name) == actual,
        {"actual": actual, "recorded": recorded_hashes.get(name)},
    )

source_hashes = {
    path.relative_to(FROZEN).as_posix(): sha256_file(path)
    for path in sorted(FROZEN.rglob("*"))
    if path.is_file() and not path.is_symlink()
}
check(
    "all Stage 1 source hashes",
    source_hashes == resolution["stage1_source_hashes"],
    {
        "actual": source_hashes,
        "recorded": resolution["stage1_source_hashes"],
    },
)

check(
    "Stage 1 export bindings in Stage 4",
    input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == tree_hashes["stage1_export_sha256"]
    == generator_manifest["provenance"]["stage1_workspace_sha256"]
    == export_result["frozen_input_sha256"]
    == preflight["frozen_input_sha256"]
    == preflight["stage1_workspace_sha256"],
    {
        "tree_digest": tree_hashes["stage1_export_sha256"],
        "input_manifest": input_manifest["stage1_workspace_sha256"],
        "generator_manifest": generator_manifest["provenance"][
            "stage1_workspace_sha256"
        ],
        "export_result": export_result["frozen_input_sha256"],
        "preflight": preflight["stage1_workspace_sha256"],
    },
)
check(
    "Stage 3 manifest bindings in Stage 4",
    input_manifest["stage3_discovery_manifest_sha256"]
    == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == export_result["stage3_discovery_manifest_sha256"]
    == preflight["stage3_discovery_manifest_sha256"]
    == tree_hashes["discovery_manifest_sha256"],
    {
        "actual": tree_hashes["discovery_manifest_sha256"],
        "input_manifest": input_manifest["stage3_discovery_manifest_sha256"],
        "generator_manifest": generator_manifest["provenance"][
            "stage3_discovery_manifest_sha256"
        ],
    },
)
check(
    "generated tree bindings",
    generator_manifest["generated_tree_sha256"]
    == export_result["generated_tree_sha256"]
    == preflight["generated_tree_sha256"]
    == tree_hashes["generated_tree_sha256"],
    {
        "actual": tree_hashes["generated_tree_sha256"],
        "generator_manifest": generator_manifest["generated_tree_sha256"],
        "export_result": export_result["generated_tree_sha256"],
        "preflight": preflight["generated_tree_sha256"],
    },
)
check(
    "trust inventory hash binding",
    sha256_file(GENERATION / "trust-inventory.json")
    == export_result["trust_inventory_sha256"],
    {
        "actual": sha256_file(GENERATION / "trust-inventory.json"),
        "recorded": export_result["trust_inventory_sha256"],
    },
)
check(
    "generator executable hashes",
    sha256_file(TOOLS / "klean_export.py")
    == generator_manifest["exporter_sha256"]
    and sha256_file(TOOLS / "klean.py")
    == generator_manifest["klean_py_sha256"],
    {
        "exporter_actual": sha256_file(TOOLS / "klean_export.py"),
        "exporter_recorded": generator_manifest["exporter_sha256"],
        "klean_actual": sha256_file(TOOLS / "klean.py"),
        "klean_recorded": generator_manifest["klean_py_sha256"],
    },
)
check(
    "pinned toolchain object",
    load(TOOLCHAIN_LOCK) == generator_manifest["toolchain"],
    {
        "lock": load(TOOLCHAIN_LOCK),
        "generator": generator_manifest["toolchain"],
    },
)
check(
    "obligation-map file hash",
    sha256_file(GENERATED / "obligation-map.json")
    == generator_manifest["obligation_map_sha256"],
    {
        "actual": sha256_file(GENERATED / "obligation-map.json"),
        "recorded": generator_manifest["obligation_map_sha256"],
    },
)

domain_rules = [
    {
        **rule,
        "classification": protected["classification"],
        "rationale": protected["rationale"],
        "inventory_sha256": inventory["inventory_sha256"],
        "discovery_manifest_sha256": sha256_file(DISCOVERY),
    }
    for rule, protected in zip(inventory["rules"], discovery["rules"], strict=True)
    if protected["classification"] == "DOMAIN_LEMMA"
]
definition_rules = [
    {
        **rule,
        "classification": protected["classification"],
        "rationale": protected["rationale"],
    }
    for rule, protected in zip(inventory["rules"], discovery["rules"], strict=True)
    if protected["classification"] == "DEFINITION"
]
check(
    "input-manifest definition set",
    input_manifest["definitions"] == definition_rules,
    {
        "reconstructed_count": len(definition_rules),
        "manifest_count": len(input_manifest["definitions"]),
    },
)
check(
    "source domain rules exact and ordered",
    input_manifest["source_rules"]
    == obligation_map["source_rules"]
    == domain_rules,
    {
        "reconstructed": domain_rules,
        "input_manifest": input_manifest["source_rules"],
        "obligation_map": obligation_map["source_rules"],
    },
)
check(
    "non-domain class partitions",
    input_manifest["operational_rules"] == []
    and input_manifest["proved_derived_lemmas"] == [],
    {
        "operational_rules": input_manifest["operational_rules"],
        "proved_derived_lemmas": input_manifest["proved_derived_lemmas"],
    },
)

obligations = obligation_map["obligations"]
expected_ids = [rule["source_rule_id"] for rule in domain_rules]
observed_ids = [obligation["source_rule_id"] for obligation in obligations]
check(
    "one-to-one ordered source-rule/obligation mapping",
    observed_ids == expected_ids
    and len(observed_ids) == len(set(observed_ids))
    and len(obligations) == len(domain_rules) == 1,
    {
        "expected_ids": expected_ids,
        "observed_ids": observed_ids,
        "obligation_count": len(obligations),
    },
)
for index, (source, obligation) in enumerate(
    zip(domain_rules, obligations, strict=True)
):
    check(
        f"obligation {index} provenance and conjunct hash",
        obligation["normalized_sha256"] == source["normalized_sha256"]
        and obligation["inventory_sha256"] == source["inventory_sha256"]
        and obligation["discovery_manifest_sha256"]
        == source["discovery_manifest_sha256"]
        and obligation["source_span"]
        == {
            "start_line": source["start_line"],
            "end_line": source["end_line"],
        }
        and hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest()
        == obligation["lean_conjunct_sha256"],
        {"source": source, "obligation": obligation},
    )

expected_conjunct = (
    "∀ (A : SortInt) (B : SortInt) (C : SortInt), "
    "«_+Int_» («_+Int_» A B) C = «_+Int_» A («_+Int_» B C)"
)
check(
    "exact nonvacuous associativity obligation",
    len(obligations) == 1
    and obligations[0]["lean_conjunct"] == expected_conjunct,
    {
        "expected": expected_conjunct,
        "actual": obligations[0]["lean_conjunct"] if obligations else None,
    },
)

expected_definition = klean_export.expected_target_definition(obligation_map)
target = klean_export.target_statement(GENERATED)
target_sources = []
for path in sorted(GENERATED.rglob("*.lean")):
    count = path.read_text().count("def targetStatement")
    if count:
        target_sources.append(
            {"path": path.relative_to(GENERATED).as_posix(), "count": count}
        )
check(
    "single fixed generated target",
    target_sources
    == [{"path": "Klean36FizzBuzz/Lemmas.lean", "count": 1}]
    and target is not None
    and target["definition_sha256"]
    == klean_export.sha256_text(expected_definition),
    {
        "target_sources": target_sources,
        "expected_definition": expected_definition,
        "parsed_target": target,
    },
)
check(
    "target identity across all manifests and audit input",
    target
    == generator_manifest["target"]
    == preflight["target"]
    == resolution["target"]
    == resolution["stage4_preflight"]["target"],
    {
        "parsed": target,
        "generator": generator_manifest["target"],
        "preflight": preflight["target"],
        "audit_input": resolution["target"],
    },
)
check(
    "target and obligation counts/statuses",
    generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == preflight["obligation_count"]
    == resolution["stage4_preflight"]["obligation_count"]
    == len(obligations)
    == 1
    and export_result["status"] == "OK"
    and preflight["status"] == "PASS",
    {
        "generator_count": generator_manifest["obligation_count"],
        "export_result": export_result,
        "preflight_status": preflight["status"],
    },
)

print(
    json.dumps(
        {
            "checks": checks,
            "all_checks_pass": all(item["pass"] for item in checks),
            "unverifiable_recorded_hashes": {
                "lean_invocation_sha256": {
                    "recorded": recorded_hashes.get("lean_invocation_sha256"),
                    "reason": "The Stage 5 invocation tree is not among the mounted inputs.",
                }
            },
            "trust_inventory_summary": {
                "allowlist_count": len(trust_inventory["allowlist"]),
                "designated_sorries": trust_inventory["designated_sorries"],
                "other_sorries": trust_inventory["other_sorries"],
            },
        },
        indent=2,
        ensure_ascii=False,
    )
)
