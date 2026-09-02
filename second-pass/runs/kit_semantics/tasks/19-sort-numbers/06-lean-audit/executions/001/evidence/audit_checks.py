#!/usr/bin/env python3
"""Independent structural/hash checks for the 19-sort-numbers Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from typing import Any

from tools import k_rule_inventory
from tools import klean_export
from tools import pipeline_contract
from tools import stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


checks: list[dict[str, Any]] = []


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(name: str, observed: Any, expected: Any) -> None:
    checks.append(
        {
            "name": name,
            "pass": observed == expected,
            "observed": observed,
            "expected": expected,
        }
    )


def regular_files(root: Path) -> dict[str, str]:
    observed: dict[str, str] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            mode = entry.stat(follow_symlinks=False).st_mode
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                pending.append(path)
            elif stat.S_ISREG(mode):
                observed[relative] = sha256_file(path)
            else:
                raise RuntimeError(f"unsupported filesystem entry: {path}")
    return dict(sorted(observed.items()))


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
record(
    "audit input canonical resolution digest",
    stage6_resolution_contract.canonical_json_sha256(resolution),
    resolved_digest,
)
record(
    "mounted audit-input copies are byte-identical",
    sha256_file(Path("/audit-output/audit-input.json")),
    sha256_file(AUDIT_INPUT),
)
record("AUDIT_MODE environment", os.environ.get("AUDIT_MODE"), resolution["mode"])
record("problem", resolution["problem_id"], "19-sort-numbers")
record("condition", resolution["condition"], "kit-semantics")
record(
    "semantics mode",
    resolution["semantics_mode"],
    "SUPPLIED_SEMANTICS",
)

# Hash producer files before any Stage 4 structural judgment.
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
producer_names = set(regular_files(PRODUCERS))
record(
    "producer bundle exact file set",
    sorted(producer_names),
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
producer_hashes = {
    name: sha256_file(PRODUCERS / name)
    for name in ("klean.py", "klean_export.py")
}
record(
    "producer hashes vs source manifest",
    producer_hashes,
    source_manifest["files"],
)
record(
    "klean.py hash vs generator manifest",
    producer_hashes["klean.py"],
    generator_manifest["klean_py_sha256"],
)
record(
    "klean_export.py hash vs generator manifest",
    producer_hashes["klean_export.py"],
    generator_manifest["exporter_sha256"],
)
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
record(
    "generator image ID vs source manifest",
    generator_image_id,
    source_manifest["generator_image_id"],
)
record(
    "generator image ID vs audit-input producer path",
    generator_image_id.removeprefix("sha256:"),
    Path(resolution["generation_producer_sources"]).name,
)
record(
    "producer source tree hash",
    pipeline_contract.sha256_tree(PRODUCERS),
    resolution["hashes"]["generation_producer_sources_sha256"],
)

# Reconstruct the canonical local verification-module inventory.
inventory = k_rule_inventory.inventory_verification(WORKSPACE)
verification_lines = (WORKSPACE / "verification.k").read_text().splitlines()
span_checks: list[dict[str, Any]] = []
for rule in inventory["rules"]:
    source_text = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    span_checks.append(
        {
            "source_rule_id": rule["source_rule_id"],
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "source_span_exact": source_text == rule["text"],
            "normalized_sha256_recomputed": normalized_sha256,
            "normalized_sha256_recorded": rule["normalized_sha256"],
            "source_rule_id_recomputed": f"rule-{normalized_sha256}",
            "attributes": rule["attributes"],
            "text": rule["text"],
        }
    )
record(
    "every reconstructed source span is exact",
    all(item["source_span_exact"] for item in span_checks),
    True,
)
record(
    "every normalized source hash is exact",
    all(
        item["normalized_sha256_recomputed"]
        == item["normalized_sha256_recorded"]
        for item in span_checks
    ),
    True,
)
record(
    "every source_rule_id is exact",
    all(
        item["source_rule_id_recomputed"] == item["source_rule_id"]
        for item in span_checks
    ),
    True,
)
record(
    "whole inventory hash independently recomputed",
    k_rule_inventory.canonical_json_sha256(inventory["rules"]),
    inventory["inventory_sha256"],
)

discovery = json.loads(DISCOVERY.read_text())
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
record("discovery inventory hash", discovery["inventory_sha256"], inventory["inventory_sha256"])
record("discovery identity order", discovery_ids, inventory_ids)
record(
    "discovery has no duplicate identities",
    len(discovery_ids),
    len(set(discovery_ids)),
)
record(
    "discovery identity set",
    sorted(discovery_ids),
    sorted(inventory_ids),
)
record(
    "discovery manifest file hash",
    sha256_file(DISCOVERY),
    resolution["hashes"]["discovery_manifest_sha256"],
)

# This is the independent rule-by-rule classification judgment, encoded only
# after inspecting the frozen rules, source solution, spec, and supplied
# operational rules. It is compared by identity and order.
independent_classifications = [
    {
        "source_rule_id": "rule-e16b3241b5675fa807f7287fd8db8e3e71b24e7b7b130da84250149d7e166ca8",
        "classification": "DEFINITION",
    },
    {
        "source_rule_id": "rule-5692cca793a2159c984323ca422a6e908349e27acd9f001a5718828b318b0c67",
        "classification": "DEFINITION",
    },
    {
        "source_rule_id": "rule-9b835db36ee25ad7bebed412bf86771e90764ac448f5b8c18671f2ffdbd65747",
        "classification": "DEFINITION",
    },
    {
        "source_rule_id": "rule-e47e06c71c6d44b8fb7a5471bbd23d7a1afd8a6499d2077f4bfcae6064ac294c",
        "classification": "DEFINITION",
    },
    {
        "source_rule_id": "rule-fde315ba45836b08d40df28f6a9f608e17b9e5b5a70d717c5ecc140209f4ba29",
        "classification": "DEFINITION",
    },
    {
        "source_rule_id": "rule-ea52da411b9ddcd44409f34ea1ec779091c47f11ec46ca66f711f60bd835a10b",
        "classification": "DEFINITION",
    },
]
observed_classifications = [
    {
        "source_rule_id": item["source_rule_id"],
        "classification": item["classification"],
    }
    for item in discovery["rules"]
]
record(
    "independent classifications match protected manifest",
    observed_classifications,
    independent_classifications,
)
record(
    "true DOMAIN_LEMMA set",
    [
        item["source_rule_id"]
        for item in independent_classifications
        if item["classification"] == "DOMAIN_LEMMA"
    ],
    [],
)
record(
    "every explicit simplification is definition or domain lemma",
    all(
        "simplification" not in rule["attributes"]
        or classification["classification"] in {"DEFINITION", "DOMAIN_LEMMA"}
        for rule, classification in zip(
            inventory["rules"], independent_classifications, strict=True
        )
    ),
    True,
)

# Independently hash every launcher-recorded mounted input.
resolution_hashes = resolution["hashes"]
record(
    "Stage 1 full workspace tree hash",
    pipeline_contract.sha256_tree(WORKSPACE),
    resolution_hashes["k_workspace_sha256"],
)
record(
    "Stage 1 generator-export tree hash",
    klean_export.tree_digest(WORKSPACE),
    resolution_hashes["stage1_export_sha256"],
)
observed_stage1_files = regular_files(WORKSPACE)
expected_stage1_files = dict(sorted(resolution["stage1_source_hashes"].items()))
record(
    "Stage 1 per-file source hash map digest",
    k_rule_inventory.canonical_json_sha256(observed_stage1_files),
    k_rule_inventory.canonical_json_sha256(expected_stage1_files),
)
record(
    "Stage 1 per-file source hash map count",
    len(observed_stage1_files),
    len(expected_stage1_files),
)
record(
    "Stage 1 per-file source hash map mismatches",
    sorted(
        name
        for name in set(observed_stage1_files) | set(expected_stage1_files)
        if observed_stage1_files.get(name) != expected_stage1_files.get(name)
    ),
    [],
)
record(
    "selected Stage 2 audit tree hash",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    resolution_hashes["k_audit_sha256"],
)
record(
    "selected Stage 4 generation tree hash",
    pipeline_contract.sha256_tree(GENERATION),
    resolution_hashes["klean_generation_sha256"],
)
record(
    "selected Stage 2 artifact hash",
    resolution["selections"]["k_audit"]["artifact_sha256"],
    resolution_hashes["k_audit_sha256"],
)
record(
    "selected Stage 4 artifact hash",
    resolution["selections"]["klean_generation"]["artifact_sha256"],
    resolution_hashes["klean_generation_sha256"],
)
record(
    "generated project tree hash",
    klean_export.tree_digest(GENERATED),
    resolution_hashes["generated_tree_sha256"],
)
record("Lean workspace hash is absent", resolution_hashes["lean_workspace_sha256"], None)
record("Lean invocation hash is absent", resolution_hashes["lean_invocation_sha256"], None)

# Verify all Stage 4 manifest/hash bindings and the exact empty bijection.
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
trust_inventory = json.loads((GENERATION / "trust-inventory.json").read_text())
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
toolchain_lock = json.loads(TOOLCHAIN_LOCK.read_text())
stage1_export_hash = klean_export.tree_digest(WORKSPACE)
generated_tree_hash = klean_export.tree_digest(GENERATED)
discovery_hash = sha256_file(DISCOVERY)
domain_ids = [
    item["source_rule_id"]
    for item in independent_classifications
    if item["classification"] == "DOMAIN_LEMMA"
]
source_rule_ids = [
    item["source_rule_id"] for item in input_manifest["source_rules"]
]
obligation_ids = [
    item["source_rule_id"] for item in obligation_map["obligations"]
]
record("generator toolchain lock", generator_manifest["toolchain"], toolchain_lock)
record("input verification hash", input_manifest["verification_sha256"], inventory["verification_sha256"])
record("input inventory hash", input_manifest["inventory_sha256"], inventory["inventory_sha256"])
record("input frozen hash", input_manifest["frozen_input_sha256"], stage1_export_hash)
record("input Stage 1 hash", input_manifest["stage1_workspace_sha256"], stage1_export_hash)
record("input discovery hash", input_manifest["stage3_discovery_manifest_sha256"], discovery_hash)
record("generator Stage 1 provenance", generator_manifest["provenance"]["stage1_workspace_sha256"], stage1_export_hash)
record("generator discovery provenance", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"], discovery_hash)
record("generator inventory provenance", generator_manifest["provenance"]["inventory_sha256"], inventory["inventory_sha256"])
record("generator generated-tree hash", generator_manifest["generated_tree_sha256"], generated_tree_hash)
record("generator obligation-map hash", generator_manifest["obligation_map_sha256"], sha256_file(obligation_map_path))
record("generator obligation count", generator_manifest["obligation_count"], len(obligation_map["obligations"]))
record("input source-rule IDs equal independent domain IDs", source_rule_ids, domain_ids)
record(
    "obligation-map source-rule IDs equal independent domain IDs",
    [item["source_rule_id"] for item in obligation_map["source_rules"]],
    domain_ids,
)
record("obligation IDs equal independent domain IDs", obligation_ids, domain_ids)
record("obligation IDs are unique", len(obligation_ids), len(set(obligation_ids)))
record("zero obligations have zero trust parameters", obligation_map["trust_parameters"], [])
record("fixed target declaration absent", klean_export.target_statement(GENERATED), None)
record("generator target absent", generator_manifest["target"], None)
record("launcher target absent", resolution["target"], None)
record("no vacuous generated conjuncts", obligation_map["obligations"], [])
record("export result status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
record("export obligation count", export_result["obligation_count"], 0)
record("export frozen hash", export_result["frozen_input_sha256"], stage1_export_hash)
record("export discovery hash", export_result["stage3_discovery_manifest_sha256"], discovery_hash)
record("export generated-tree hash", export_result["generated_tree_sha256"], generated_tree_hash)
record("export trust-inventory hash", export_result["trust_inventory_sha256"], sha256_file(GENERATION / "trust-inventory.json"))
record("selected Stage 4 status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
record("preflight status", preflight["status"], "KLEAN_NO_OBLIGATIONS")
record("preflight Stage 1 hash", preflight["stage1_workspace_sha256"], stage1_export_hash)
record("preflight discovery hash", preflight["stage3_discovery_manifest_sha256"], discovery_hash)
record("preflight generated-tree hash", preflight["generated_tree_sha256"], generated_tree_hash)
record("preflight target absent", preflight["target"], None)
record("preflight obligation count", preflight["obligation_count"], 0)
record("launcher preflight exact document", resolution["stage4_preflight"], preflight)
record("launcher Stage 5 result absent", resolution["stage5_result"], None)
record("candidate path absent", Path("/candidate").exists(), False)

report = {
    "schema_version": 1,
    "inventory": inventory,
    "span_reconstruction": span_checks,
    "independent_classifications": independent_classifications,
    "producer_hashes": producer_hashes,
    "checks": checks,
    "failed_checks": [item["name"] for item in checks if not item["pass"]],
    "all_checks_pass": all(item["pass"] for item in checks),
}
print(json.dumps(report, indent=2, sort_keys=True))
