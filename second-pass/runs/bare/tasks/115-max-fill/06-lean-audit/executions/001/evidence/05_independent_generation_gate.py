#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification


def load(path: Path) -> object:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report(name: str, observed: object, expected: object) -> None:
    print(
        json.dumps(
            {
                "check": name,
                "observed": observed,
                "expected": expected,
                "match": observed == expected,
            },
            sort_keys=True,
        )
    )


audit_document = load(Path("/audit-input.json"))
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")
generator = load(generation / "generator-manifest.json")
input_manifest = load(generation / "input-manifest.json")
export_result = load(generation / "export-result.json")
obligation_map = load(generated / "obligation-map.json")
preflight = load(generation / "preflight.json")
source_manifest = load(producer / "source-manifest.json")
discovery = load(discovery_path)
inventory = inventory_verification(workspace)

print("=== signed audit envelope ===")
report(
    "resolved_input_sha256",
    resolved_digest,
    audit_document["resolved_input_sha256"],
)
report("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
report("condition", resolution["condition"], "bare")
report(
    "semantics_mode",
    resolution["semantics_mode"],
    "GENERATED_SEMANTICS",
)

print("=== resolution tree/file hashes ===")
hashes = resolution["hashes"]
report(
    "k_workspace_sha256",
    pipeline_contract.sha256_tree(workspace),
    hashes["k_workspace_sha256"],
)
report(
    "stage1_export_sha256",
    klean_export.tree_digest(workspace),
    hashes["stage1_export_sha256"],
)
report(
    "k_audit_sha256",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    hashes["k_audit_sha256"],
)
report(
    "discovery_manifest_sha256",
    sha(discovery_path),
    hashes["discovery_manifest_sha256"],
)
report(
    "generation_producer_sources_sha256",
    pipeline_contract.sha256_tree(producer),
    hashes["generation_producer_sources_sha256"],
)
report(
    "generated_tree_sha256",
    klean_export.tree_digest(generated),
    hashes["generated_tree_sha256"],
)
report(
    "klean_generation_sha256",
    pipeline_contract.sha256_tree(generation),
    hashes["klean_generation_sha256"],
)
report("lean_workspace_sha256", None, hashes["lean_workspace_sha256"])
report("lean_invocation_sha256", None, hashes["lean_invocation_sha256"])

print("=== selection and producer provenance ===")
report(
    "k-audit selection artifact",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
report(
    "generation selection artifact",
    pipeline_contract.sha256_tree(generation),
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)
report(
    "producer klean_export.py",
    sha(producer / "klean_export.py"),
    generator["exporter_sha256"],
)
report(
    "producer klean.py",
    sha(producer / "klean.py"),
    generator["klean_py_sha256"],
)
report(
    "producer source manifest files",
    source_manifest["files"],
    {
        "klean_export.py": generator["exporter_sha256"],
        "klean.py": generator["klean_py_sha256"],
    },
)
report(
    "generator image source-vs-generator",
    source_manifest["generator_image_id"],
    generator["provenance"]["generator_image_id"],
)
report(
    "generator image audit-path binding",
    "sha256:" + Path(resolution["generation_producer_sources"]).name,
    generator["provenance"]["generator_image_id"],
)

print("=== manifest/hash bindings ===")
stage1_export = klean_export.tree_digest(workspace)
discovery_sha = sha(discovery_path)
generated_sha = klean_export.tree_digest(generated)
report(
    "input frozen_input_sha256",
    stage1_export,
    input_manifest["frozen_input_sha256"],
)
report(
    "input stage1_workspace_sha256",
    stage1_export,
    input_manifest["stage1_workspace_sha256"],
)
report(
    "input discovery sha256",
    discovery_sha,
    input_manifest["stage3_discovery_manifest_sha256"],
)
report(
    "input verification sha256",
    sha(workspace / "verification.k"),
    input_manifest["verification_sha256"],
)
report(
    "input inventory sha256",
    inventory["inventory_sha256"],
    input_manifest["inventory_sha256"],
)
report(
    "generator generated_tree_sha256",
    generated_sha,
    generator["generated_tree_sha256"],
)
report(
    "generator obligation_map_sha256",
    sha(generated / "obligation-map.json"),
    generator["obligation_map_sha256"],
)
report(
    "generator stage1 provenance",
    stage1_export,
    generator["provenance"]["stage1_workspace_sha256"],
)
report(
    "generator discovery provenance",
    discovery_sha,
    generator["provenance"]["stage3_discovery_manifest_sha256"],
)
report(
    "generator inventory provenance",
    inventory["inventory_sha256"],
    generator["provenance"]["inventory_sha256"],
)
report(
    "generator toolchain lock",
    generator["toolchain"],
    load(Path("/reference/klean-toolchain.lock.json")),
)
report(
    "export frozen_input_sha256",
    stage1_export,
    export_result["frozen_input_sha256"],
)
report(
    "export discovery sha256",
    discovery_sha,
    export_result["stage3_discovery_manifest_sha256"],
)
report(
    "export generated tree",
    generated_sha,
    export_result["generated_tree_sha256"],
)
report(
    "export trust inventory",
    sha(generation / "trust-inventory.json"),
    export_result["trust_inventory_sha256"],
)
report("recorded preflight object", preflight, resolution["stage4_preflight"])

print("=== exact domain-rule / obligation / target gate ===")
domain_ids = [
    entry["source_rule_id"]
    for entry in discovery["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
input_source_ids = [
    rule["source_rule_id"] for rule in input_manifest["source_rules"]
]
map_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
report("domain IDs to input source IDs", domain_ids, input_source_ids)
report("domain IDs to map source IDs", domain_ids, map_source_ids)
report("domain IDs to obligation IDs", domain_ids, obligation_ids)
report(
    "unique obligation IDs",
    len(obligation_ids),
    len(set(obligation_ids)),
)
report(
    "obligation count generator",
    len(obligation_ids),
    generator["obligation_count"],
)
report(
    "obligation count export",
    len(obligation_ids),
    export_result["obligation_count"],
)
report("source_rule inventory exact", input_manifest["source_rules"], [])
report("obligation source inventory exact", obligation_map["source_rules"], [])
report("obligation list exact", obligation_map["obligations"], [])
report("trust parameters exact", obligation_map["trust_parameters"], [])

trusted_target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
raw_target_count = 0
target_occurrences: list[str] = []
for source in sorted(generated.rglob("*.lean")):
    for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", source.read_text()):
        raw_target_count += 1
        target_occurrences.append(
            f"{source.relative_to(generated).as_posix()}:{source.read_text()[:match.start()].count(chr(10)) + 1}"
        )
report("trusted target statement", trusted_target, None)
report("expected target definition", expected_definition, None)
report("raw target declaration count", raw_target_count, 0)
report("raw target occurrences", target_occurrences, [])
report("generator target", generator["target"], None)
report("audit-input target", resolution["target"], None)
report("preflight target", preflight["target"], None)
report("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
report(
    "selection status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)
report("Stage 5 result", resolution["stage5_result"], None)
report("candidate absent", Path("/candidate").exists(), False)
