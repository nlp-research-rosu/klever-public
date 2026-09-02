#!/usr/bin/env python3
"""Independent read-only hash, inventory, and Stage 4 structural checks."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            if entry.is_symlink():
                raise RuntimeError(f"symlink in immutable tree: {path}")
            if entry.is_dir(follow_symlinks=False):
                pending.append(path)
            elif entry.is_file(follow_symlinks=False):
                result[path.relative_to(root).as_posix()] = file_hash(path)
            else:
                raise RuntimeError(f"unsupported immutable-tree entry: {path}")
    return dict(sorted(result.items()))


checks: list[dict[str, Any]] = []


def check(name: str, observed: Any, expected: Any) -> None:
    checks.append(
        {
            "name": name,
            "ok": observed == expected,
            "observed": observed,
            "expected": expected,
        }
    )


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution, signed_digest = stage6_resolution_contract.verify_audit_input(
    audit_input
)
check(
    "signed resolution digest",
    signed_digest,
    audit_input["resolved_input_sha256"],
)
check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
check(
    "AUDIT_PROBLEM_ID",
    os.environ.get("AUDIT_PROBLEM_ID"),
    resolution["problem_id"],
)
check(
    "AUDIT_CONDITION",
    os.environ.get("AUDIT_CONDITION"),
    resolution["condition"],
)
check(
    "AUDIT_SEMANTICS_MODE",
    os.environ.get("AUDIT_SEMANTICS_MODE"),
    resolution["semantics_mode"],
)

k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_dir = Path("/reference/generation-tools")
lock_path = Path("/reference/klean-toolchain.lock.json")

recorded_hashes = resolution["hashes"]
check(
    "Stage 1 selected-tree hash",
    pipeline_contract.sha256_tree(k_workspace),
    recorded_hashes["k_workspace_sha256"],
)
check(
    "Stage 1 export hash",
    klean_export.tree_digest(k_workspace),
    recorded_hashes["stage1_export_sha256"],
)
check(
    "Stage 2 selected-tree hash",
    pipeline_contract.sha256_tree(k_audit),
    recorded_hashes["k_audit_sha256"],
)
check(
    "Stage 3 discovery file hash",
    file_hash(discovery_path),
    recorded_hashes["discovery_manifest_sha256"],
)
check(
    "Stage 4 selected-tree hash",
    pipeline_contract.sha256_tree(generation),
    recorded_hashes["klean_generation_sha256"],
)
check(
    "Stage 4 generated-project hash",
    klean_export.tree_digest(generated),
    recorded_hashes["generated_tree_sha256"],
)
check(
    "generation producer-source tree hash",
    pipeline_contract.sha256_tree(producer_dir),
    recorded_hashes["generation_producer_sources_sha256"],
)
check(
    "Stage 1 per-file hash map",
    regular_file_hashes(k_workspace),
    resolution["stage1_source_hashes"],
)

source_manifest = json.loads((producer_dir / "source-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
trust_inventory = json.loads((generation / "trust-inventory.json").read_text())
obligation_map = json.loads(
    (generated / "obligation-map.json").read_text()
)
toolchain_lock = json.loads(lock_path.read_text())

producer_files = {
    "klean.py": file_hash(producer_dir / "klean.py"),
    "klean_export.py": file_hash(producer_dir / "klean_export.py"),
}
check("producer files versus source manifest", producer_files, source_manifest["files"])
check(
    "producer klean.py versus generator manifest",
    producer_files["klean.py"],
    generator_manifest["klean_py_sha256"],
)
check(
    "producer klean_export.py versus generator manifest",
    producer_files["klean_export.py"],
    generator_manifest["exporter_sha256"],
)
check(
    "producer directory exact members",
    sorted(path.name for path in producer_dir.iterdir()),
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
check(
    "generator image: source manifest versus generator manifest",
    source_manifest["generator_image_id"],
    generator_manifest["provenance"]["generator_image_id"],
)
check(
    "generator image: signed producer-source path",
    Path(resolution["generation_producer_sources"]).name,
    source_manifest["generator_image_id"].removeprefix("sha256:"),
)

inventory = k_rule_inventory.inventory_verification(k_workspace)
discovery = json.loads(discovery_path.read_text())
validated = lemma_discovery_contract.validate_trust_boundary(
    k_workspace, discovery_path
)
check(
    "inventory hash versus Stage 3",
    inventory["inventory_sha256"],
    discovery["inventory_sha256"],
)
check(
    "inventory count versus Stage 3 count",
    len(inventory["rules"]),
    len(discovery["rules"]),
)
check(
    "ordered inventory identity versus Stage 3",
    [rule["source_rule_id"] for rule in inventory["rules"]],
    [rule["source_rule_id"] for rule in discovery["rules"]],
)
check(
    "Stage 3 IDs unique",
    len({rule["source_rule_id"] for rule in discovery["rules"]}),
    len(discovery["rules"]),
)

verification_lines = (k_workspace / "verification.k").read_text().splitlines()
recomputed_rules: list[dict[str, Any]] = []
for rule in inventory["rules"]:
    exact_span = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(exact_span.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    recomputed_rules.append(
        {
            "source_rule_id": f"rule-{normalized_sha256}",
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "normalized_sha256": normalized_sha256,
            "attributes": rule["attributes"],
            "text": exact_span,
        }
    )
check("source-span/hash/ID reconstruction", recomputed_rules, inventory["rules"])
check(
    "whole inventory hash reconstruction",
    k_rule_inventory.canonical_json_sha256(recomputed_rules),
    inventory["inventory_sha256"],
)

current_stage1_export_hash = klean_export.tree_digest(k_workspace)
current_discovery_hash = file_hash(discovery_path)
current_generated_hash = klean_export.tree_digest(generated)
current_obligation_map_hash = file_hash(generated / "obligation-map.json")
current_trust_inventory_hash = file_hash(generation / "trust-inventory.json")
current_verification_hash = file_hash(k_workspace / "verification.k")

check(
    "input manifest frozen-input hash",
    input_manifest["frozen_input_sha256"],
    current_stage1_export_hash,
)
check(
    "input manifest Stage 1 hash",
    input_manifest["stage1_workspace_sha256"],
    current_stage1_export_hash,
)
check(
    "input manifest Stage 3 hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    current_discovery_hash,
)
check(
    "input manifest verification hash",
    input_manifest["verification_sha256"],
    current_verification_hash,
)
check(
    "input manifest inventory hash",
    input_manifest["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "input manifest definitions",
    input_manifest["definitions"],
    validated["definitions"],
)
check(
    "input manifest operational rules",
    input_manifest["operational_rules"],
    validated["operational_rules"],
)
check(
    "input manifest proved derived lemmas",
    input_manifest["proved_derived_lemmas"],
    validated["proved_derived_lemmas"],
)

domain_source_rules = klean_export._domain_source_rules(
    validated, current_discovery_hash
)
check(
    "input manifest domain source rules",
    input_manifest["source_rules"],
    domain_source_rules,
)
check(
    "obligation-map domain source rules",
    obligation_map["source_rules"],
    domain_source_rules,
)
check("obligation-map obligations", obligation_map["obligations"], [])
check("obligation-map trust parameters", obligation_map["trust_parameters"], [])
check(
    "expected generated target definition",
    klean_export.expected_target_definition(obligation_map),
    None,
)
check("actual generated target", klean_export.target_statement(generated), None)
check("generator-manifest target", generator_manifest["target"], None)
check("signed audit target", resolution["target"], None)
check("generator obligation count", generator_manifest["obligation_count"], 0)
check("export-result obligation count", export_result["obligation_count"], 0)
check("export-result status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check(
    "selected Stage 4 status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)
check("audit mode for no-obligation generation", resolution["mode"], "CLASSIFICATION_ONLY")
check("Stage 5 result absent", resolution["stage5_result"], None)
check("Stage 5 workspace absent", resolution["lean_workspace"], None)
check("Stage 5 invocation absent", resolution["lean_invocation"], None)
check("mounted candidate absent", Path("/candidate").exists(), False)

check(
    "generator generated-tree hash",
    generator_manifest["generated_tree_sha256"],
    current_generated_hash,
)
check(
    "generator obligation-map hash",
    generator_manifest["obligation_map_sha256"],
    current_obligation_map_hash,
)
check(
    "generator Stage 1 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    current_stage1_export_hash,
)
check(
    "generator Stage 3 provenance",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    current_discovery_hash,
)
check(
    "generator inventory provenance",
    generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
check("generator toolchain lock", generator_manifest["toolchain"], toolchain_lock)

check(
    "export-result frozen-input hash",
    export_result["frozen_input_sha256"],
    current_stage1_export_hash,
)
check(
    "export-result Stage 3 hash",
    export_result["stage3_discovery_manifest_sha256"],
    current_discovery_hash,
)
check(
    "export-result generated-tree hash",
    export_result["generated_tree_sha256"],
    current_generated_hash,
)
check(
    "export-result trust-inventory hash",
    export_result["trust_inventory_sha256"],
    current_trust_inventory_hash,
)
check(
    "launcher Stage 4 preflight snapshot",
    resolution["stage4_preflight"],
    json.loads((generation / "preflight.json").read_text()),
)

summary = {
    "schema_version": 1,
    "all_checks_pass": all(item["ok"] for item in checks),
    "check_count": len(checks),
    "failed_checks": [item["name"] for item in checks if not item["ok"]],
    "inventory": inventory,
    "validated_category_counts": {
        "DEFINITION": len(validated["definitions"]),
        "OPERATIONAL_RULE": len(validated["operational_rules"]),
        "PROVED_DERIVED_LEMMA": len(validated["proved_derived_lemmas"]),
        "DOMAIN_LEMMA": len(validated["domain_lemmas"]),
    },
    "producer_authentication": {
        "files": producer_files,
        "tree_sha256": pipeline_contract.sha256_tree(producer_dir),
        "generator_image_id": source_manifest["generator_image_id"],
    },
    "stage4": {
        "generated_tree_sha256": current_generated_hash,
        "obligation_map_sha256": current_obligation_map_hash,
        "obligation_count": len(obligation_map["obligations"]),
        "target": klean_export.target_statement(generated),
    },
    "checks": checks,
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(0 if summary["all_checks_pass"] else 1)
