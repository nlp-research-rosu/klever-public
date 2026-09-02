#!/usr/bin/env python3
"""Independent structural/hash checks for the 110-exchange Stage 6 audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


REFERENCE = Path("/reference")
STAGE1 = REFERENCE / "k-proof"
DISCOVERY = REFERENCE / "lemma-discovery.json"
GENERATION = REFERENCE / "klean-generation"
GENERATED = GENERATION / "generated"
PRODUCERS = REFERENCE / "generation-tools"
CANDIDATE = Path("/candidate")
AUDIT_INPUT = Path("/audit-input.json")


def load(path: Path) -> Any:
    return json.loads(path.read_text())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            path = Path(entry.path)
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                result[path.relative_to(root).as_posix()] = sha256_file(path)
            else:
                raise RuntimeError(f"unsupported Stage 1 entry: {path}")
    return dict(sorted(result.items()))


def check(label: str, observed: Any, expected: Any) -> dict[str, Any]:
    return {
        "label": label,
        "ok": observed == expected,
        "observed": observed,
        "expected": expected,
    }


audit = load(AUDIT_INPUT)
resolution = audit["resolution"]
hashes = resolution["hashes"]
discovery = load(DISCOVERY)
generator = load(GENERATION / "generator-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
export_result = load(GENERATION / "export-result.json")
obligation_map = load(GENERATED / "obligation-map.json")
source_manifest = load(PRODUCERS / "source-manifest.json")

inventory = inventory_verification(STAGE1)
validated = validate_trust_boundary(STAGE1, DISCOVERY)

inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
discovery_classification = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}

classification_counts: dict[str, int] = {}
for entry in discovery["rules"]:
    role = entry["classification"]
    classification_counts[role] = classification_counts.get(role, 0) + 1

domain = validated["domain_lemmas"]
domain_ids = [entry["source_rule_id"] for entry in domain]
mapped_ids = [
    entry["source_rule_id"] for entry in obligation_map["obligations"]
]
mapped_source_ids = [
    entry["source_rule_id"] for entry in obligation_map["source_rules"]
]

target = klean_export.target_statement(GENERATED)
expected_definition = klean_export.expected_target_definition(obligation_map)

producer_image_from_audit_path = "sha256:" + Path(
    resolution["generation_producer_sources"]
).name

checks = [
    check(
        "verification bytes",
        inventory["verification_sha256"],
        input_manifest["verification_sha256"],
    ),
    check(
        "inventory canonical hash",
        inventory["inventory_sha256"],
        discovery["inventory_sha256"],
    ),
    check(
        "inventory hash in input manifest",
        inventory["inventory_sha256"],
        input_manifest["inventory_sha256"],
    ),
    check("discovery rule identity order", discovery_ids, inventory_ids),
    check("discovery identity uniqueness", len(set(discovery_ids)), len(discovery_ids)),
    check("discovery inventory length", len(discovery_ids), len(inventory_ids)),
    check("domain/order to obligation map source rules", mapped_source_ids, domain_ids),
    check("domain/order to obligations", mapped_ids, domain_ids),
    check("obligation identity uniqueness", len(set(mapped_ids)), len(mapped_ids)),
    check("obligation count", len(mapped_ids), generator["obligation_count"]),
    check(
        "obligation map bytes",
        sha256_file(GENERATED / "obligation-map.json"),
        generator["obligation_map_sha256"],
    ),
    check(
        "expected target definition hash",
        klean_export.sha256_text(expected_definition),
        generator["target"]["definition_sha256"],
    ),
    check("parsed target", target, generator["target"]),
    check("audit-input target", generator["target"], resolution["target"]),
    check(
        "producer klean_export.py",
        sha256_file(PRODUCERS / "klean_export.py"),
        generator["exporter_sha256"],
    ),
    check(
        "producer klean.py",
        sha256_file(PRODUCERS / "klean.py"),
        generator["klean_py_sha256"],
    ),
    check(
        "producer source manifest files",
        source_manifest["files"],
        {
            "klean_export.py": generator["exporter_sha256"],
            "klean.py": generator["klean_py_sha256"],
        },
    ),
    check(
        "producer image source/generator",
        source_manifest["generator_image_id"],
        generator["provenance"]["generator_image_id"],
    ),
    check(
        "producer image audit path/generator",
        producer_image_from_audit_path,
        generator["provenance"]["generator_image_id"],
    ),
    check(
        "producer bundle tree",
        pipeline_contract.sha256_tree(PRODUCERS),
        hashes["generation_producer_sources_sha256"],
    ),
    check(
        "producer bundle exact names",
        sorted(path.relative_to(PRODUCERS).as_posix() for path in PRODUCERS.iterdir()),
        ["klean.py", "klean_export.py", "source-manifest.json"],
    ),
    check(
        "Stage 1 pipeline tree",
        pipeline_contract.sha256_tree(STAGE1),
        hashes["k_workspace_sha256"],
    ),
    check(
        "Stage 1 exporter tree",
        klean_export.tree_digest(STAGE1),
        hashes["stage1_export_sha256"],
    ),
    check(
        "Stage 1 per-file hashes",
        source_hashes(STAGE1),
        resolution["stage1_source_hashes"],
    ),
    check(
        "Stage 3 manifest bytes",
        sha256_file(DISCOVERY),
        hashes["discovery_manifest_sha256"],
    ),
    check(
        "Stage 2 selected audit tree",
        pipeline_contract.sha256_tree(REFERENCE / "k-audit"),
        hashes["k_audit_sha256"],
    ),
    check(
        "Stage 4 generation tree",
        pipeline_contract.sha256_tree(GENERATION),
        hashes["klean_generation_sha256"],
    ),
    check(
        "generated project exporter tree",
        klean_export.tree_digest(GENERATED),
        hashes["generated_tree_sha256"],
    ),
    check(
        "generated project manifest tree",
        klean_export.tree_digest(GENERATED),
        generator["generated_tree_sha256"],
    ),
    check(
        "candidate Stage 5 tree",
        pipeline_contract.sha256_tree(CANDIDATE),
        hashes["lean_workspace_sha256"],
    ),
    check(
        "input manifest Stage 1",
        input_manifest["stage1_workspace_sha256"],
        hashes["stage1_export_sha256"],
    ),
    check(
        "input manifest Stage 3",
        input_manifest["stage3_discovery_manifest_sha256"],
        hashes["discovery_manifest_sha256"],
    ),
    check(
        "generator provenance Stage 1",
        generator["provenance"]["stage1_workspace_sha256"],
        hashes["stage1_export_sha256"],
    ),
    check(
        "generator provenance Stage 3",
        generator["provenance"]["stage3_discovery_manifest_sha256"],
        hashes["discovery_manifest_sha256"],
    ),
    check(
        "generator provenance inventory",
        generator["provenance"]["inventory_sha256"],
        inventory["inventory_sha256"],
    ),
    check(
        "export status/count",
        (export_result["status"], export_result["obligation_count"]),
        ("OK", len(domain_ids)),
    ),
]

report = {
    "audit_mode_env": os.environ.get("AUDIT_MODE"),
    "audit_mode_json": resolution["mode"],
    "semantics_mode": resolution["semantics_mode"],
    "inventory_summary": {
        "verification_module": inventory["verification_module"],
        "verification_modules": inventory["verification_modules"],
        "rule_count": len(inventory["rules"]),
        "inventory_sha256": inventory["inventory_sha256"],
        "classification_counts": classification_counts,
        "domain_rule_ids": domain_ids,
    },
    "checks": checks,
    "all_checks_pass": all(entry["ok"] for entry in checks),
}
print(json.dumps(report, indent=2, sort_keys=True))
