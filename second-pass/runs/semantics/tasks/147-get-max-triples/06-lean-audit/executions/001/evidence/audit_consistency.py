#!/usr/bin/env python3
# Reproducible independent consistency checks used by this audit.
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


ROOT = Path("/reference")
AUDIT_INPUT = Path("/audit-input.json")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


checks: dict[str, object] = {}


def check(name: str, condition: bool, detail: object = None) -> None:
    checks[name] = {"pass": bool(condition), "detail": detail}


audit = load(AUDIT_INPUT)
resolution, resolved_hash = stage6_resolution_contract.verify_audit_input(audit)
check("audit_input_signature", True, resolved_hash)
check(
    "launcher_mode",
    os.environ.get("AUDIT_MODE") == resolution["mode"] == "CLASSIFICATION_ONLY",
    {"env": os.environ.get("AUDIT_MODE"), "signed": resolution["mode"]},
)

generation = ROOT / "klean-generation"
generated = generation / "generated"
stage1 = ROOT / "k-proof"
stage3 = ROOT / "lemma-discovery.json"
producer = ROOT / "generation-tools"
generator_manifest = load(generation / "generator-manifest.json")
input_manifest = load(generation / "input-manifest.json")
export_result = load(generation / "export-result.json")
trust_inventory = load(generation / "trust-inventory.json")
obligation_map = load(generated / "obligation-map.json")
source_manifest = load(producer / "source-manifest.json")
toolchain_lock = load(ROOT / "klean-toolchain.lock.json")

actual_producer_hashes = {
    "klean_export.py": sha(producer / "klean_export.py"),
    "klean.py": sha(producer / "klean.py"),
}
manifest_producer_hashes = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
check(
    "producer_file_hashes",
    actual_producer_hashes
    == manifest_producer_hashes
    == source_manifest["files"],
    {
        "actual": actual_producer_hashes,
        "generator_manifest": manifest_producer_hashes,
        "source_manifest": source_manifest["files"],
    },
)
producer_image_from_audit_path = (
    "sha256:" + Path(resolution["generation_producer_sources"]).name
)
check(
    "generator_image_identity",
    generator_manifest["provenance"]["generator_image_id"]
    == source_manifest["generator_image_id"]
    == producer_image_from_audit_path,
    {
        "generator_manifest": generator_manifest["provenance"][
            "generator_image_id"
        ],
        "source_manifest": source_manifest["generator_image_id"],
        "audit_input_path_binding": producer_image_from_audit_path,
    },
)
check(
    "producer_bundle_exact_files",
    sorted(p.relative_to(producer).as_posix() for p in producer.rglob("*") if p.is_file())
    == ["klean.py", "klean_export.py", "source-manifest.json"],
)

pipeline_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(stage1),
    "k_audit_sha256": pipeline_contract.sha256_tree(ROOT / "k-audit"),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(producer),
}
for key, actual in pipeline_hashes.items():
    check(
        f"signed_{key}",
        actual == resolution["hashes"][key],
        {"actual": actual, "signed": resolution["hashes"][key]},
    )

stage1_export_hash = klean_export.tree_digest(stage1)
generated_hash = klean_export.tree_digest(generated)
check(
    "signed_stage1_export_sha256",
    stage1_export_hash == resolution["hashes"]["stage1_export_sha256"],
    {"actual": stage1_export_hash, "signed": resolution["hashes"]["stage1_export_sha256"]},
)
check(
    "signed_generated_tree_sha256",
    generated_hash
    == resolution["hashes"]["generated_tree_sha256"]
    == generator_manifest["generated_tree_sha256"]
    == export_result["generated_tree_sha256"],
    {
        "actual": generated_hash,
        "signed": resolution["hashes"]["generated_tree_sha256"],
        "generator_manifest": generator_manifest["generated_tree_sha256"],
        "export_result": export_result["generated_tree_sha256"],
    },
)
stage3_hash = sha(stage3)
check(
    "signed_stage3_sha256",
    stage3_hash
    == resolution["hashes"]["discovery_manifest_sha256"]
    == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == input_manifest["stage3_discovery_manifest_sha256"]
    == export_result["stage3_discovery_manifest_sha256"],
    stage3_hash,
)
check(
    "stage1_provenance_hashes",
    stage1_export_hash
    == generator_manifest["provenance"]["stage1_workspace_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == input_manifest["frozen_input_sha256"]
    == export_result["frozen_input_sha256"],
    stage1_export_hash,
)
check(
    "obligation_map_hash",
    sha(generated / "obligation-map.json")
    == generator_manifest["obligation_map_sha256"],
    {
        "actual": sha(generated / "obligation-map.json"),
        "manifest": generator_manifest["obligation_map_sha256"],
    },
)
check(
    "trust_inventory_hash",
    sha(generation / "trust-inventory.json")
    == export_result["trust_inventory_sha256"],
    {
        "actual": sha(generation / "trust-inventory.json"),
        "export_result": export_result["trust_inventory_sha256"],
    },
)
check(
    "toolchain_lock",
    generator_manifest["toolchain"] == toolchain_lock,
)
check(
    "prior_preflight_signed_copy",
    resolution["stage4_preflight"] == load(generation / "preflight.json"),
)
prior_diagnostics = resolution["stage4_preflight"]["diagnostics"]
check(
    "prior_preflight_output_hashes",
    all(
        hashlib.sha256(item["output_tail"].encode()).hexdigest()
        == item["output_sha256"]
        for item in prior_diagnostics
    ),
    [
        {
            "command": item["command"],
            "tail_hash": hashlib.sha256(item["output_tail"].encode()).hexdigest(),
            "recorded_hash": item["output_sha256"],
        }
        for item in prior_diagnostics
    ],
)

actual_stage1_source_hashes = {
    p.relative_to(stage1).as_posix(): sha(p)
    for p in stage1.rglob("*")
    if p.is_file() and not p.is_symlink()
}
check(
    "stage1_source_file_bijection_and_hashes",
    actual_stage1_source_hashes == resolution["stage1_source_hashes"],
    {
        "actual_count": len(actual_stage1_source_hashes),
        "signed_count": len(resolution["stage1_source_hashes"]),
        "mismatches": sorted(
            key
            for key in set(actual_stage1_source_hashes)
            | set(resolution["stage1_source_hashes"])
            if actual_stage1_source_hashes.get(key)
            != resolution["stage1_source_hashes"].get(key)
        ),
    },
)

inventory = inventory_verification(stage1)
validated = validate_trust_boundary(stage1, stage3)
source_lines = (stage1 / "verification.k").read_text().splitlines()
span_checks = []
for rule in inventory["rules"]:
    sliced = "\n".join(source_lines[rule["start_line"] - 1 : rule["end_line"]])
    normalized_hash = hashlib.sha256(" ".join(sliced.split()).encode()).hexdigest()
    span_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "span": [rule["start_line"], rule["end_line"]],
            "text_exact": sliced == rule["text"],
            "normalized_sha256": normalized_hash,
            "hash_exact": normalized_hash == rule["normalized_sha256"],
            "id_exact": rule["source_rule_id"] == "rule-" + normalized_hash,
        }
    )
check(
    "inventory_spans_hashes_ids",
    all(x["text_exact"] and x["hash_exact"] and x["id_exact"] for x in span_checks),
    span_checks,
)
check(
    "whole_inventory_hash",
    canonical_json_sha256(inventory["rules"])
    == inventory["inventory_sha256"]
    == load(stage3)["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"]
    == input_manifest["inventory_sha256"],
    inventory["inventory_sha256"],
)

stage3_document = load(stage3)
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
stage3_ids = [rule["source_rule_id"] for rule in stage3_document["rules"]]
check(
    "stage3_inventory_bijection_order",
    inventory_ids == stage3_ids
    and len(stage3_ids) == len(set(stage3_ids))
    and len(inventory_ids) == len(set(inventory_ids)),
    {"inventory": inventory_ids, "stage3": stage3_ids},
)
check(
    "stage3_validated_role_partition",
    len(validated["definitions"]) == 4
    and not validated["operational_rules"]
    and not validated["proved_derived_lemmas"]
    and not validated["domain_lemmas"],
    {
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
        "domain_lemmas": len(validated["domain_lemmas"]),
    },
)
check(
    "stage4_input_role_partition",
    input_manifest["definitions"] == validated["definitions"]
    and input_manifest["operational_rules"] == validated["operational_rules"]
    and input_manifest["proved_derived_lemmas"]
    == validated["proved_derived_lemmas"]
    and input_manifest["source_rules"] == validated["domain_lemmas"],
)

domain_ids = [rule["source_rule_id"] for rule in validated["domain_lemmas"]]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]
check(
    "domain_obligation_bijection",
    obligation_map["source_rules"] == []
    and domain_ids == obligation_ids == []
    and len(obligation_ids) == len(set(obligation_ids)),
    {"domain_ids": domain_ids, "obligation_ids": obligation_ids},
)
target = klean_export.target_statement(generated)
check(
    "no_obligation_status_and_target",
    generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == resolution["stage4_preflight"]["obligation_count"]
    == 0
    and export_result["status"]
    == resolution["stage4_preflight"]["status"]
    == resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS"
    and target is None
    and generator_manifest["target"] is None
    and resolution["target"] is None,
    {"observed_target": target},
)
check(
    "classification_only_has_no_stage5",
    resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["stage5_result"] is None
    and not Path("/candidate").exists(),
)
check(
    "trust_inventory_hole_counts",
    trust_inventory["designated_sorries"] == 0
    and trust_inventory["other_sorries"] == 0,
)

failed = [name for name, value in checks.items() if not value["pass"]]
print(json.dumps({"checks": checks, "failed": failed, "overall": not failed}, indent=2, sort_keys=True))
raise SystemExit(1 if failed else 0)
