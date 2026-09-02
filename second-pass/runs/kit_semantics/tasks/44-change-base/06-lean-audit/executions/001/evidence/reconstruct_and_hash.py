#!/usr/bin/env python3
"""Independent mechanical reconstruction and hash checks for this audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import k_rule_inventory
from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract
from tools import stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
K_AUDIT = Path("/reference/k-audit")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> bool:
    matches = observed == expected
    print(f"CHECK {label}: {'MATCH' if matches else 'MISMATCH'}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    return matches


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
print("AUDIT INPUT ENVELOPE: VALID")
check(
    "resolved_input_sha256",
    stage6_resolution_contract.canonical_json_sha256(resolution),
    resolved_digest,
)

generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
producer_hashes = {
    name: sha256_file(PRODUCERS / name)
    for name in ("klean.py", "klean_export.py")
}
print("PRODUCER FILE HASHES")
print(json.dumps(producer_hashes, indent=2, sort_keys=True))
check("producer source-manifest files", producer_hashes, source_manifest["files"])
check(
    "klean.py generator-manifest hash",
    producer_hashes["klean.py"],
    generator_manifest["klean_py_sha256"],
)
check(
    "klean_export.py generator-manifest hash",
    producer_hashes["klean_export.py"],
    generator_manifest["exporter_sha256"],
)
image_id = generator_manifest["provenance"]["generator_image_id"]
check("producer source-manifest image", source_manifest["generator_image_id"], image_id)
check(
    "audit-input producer path image key",
    Path(resolution["generation_producer_sources"]).name,
    image_id.removeprefix("sha256:"),
)
check(
    "producer mounted bundle file set",
    sorted(path.relative_to(PRODUCERS).as_posix() for path in PRODUCERS.iterdir()),
    ["klean.py", "klean_export.py", "source-manifest.json"],
)

inventory = k_rule_inventory.inventory_verification(WORKSPACE)
print("CANONICAL INVENTORY")
print(json.dumps(inventory, indent=2, sort_keys=True))
discovery_document = json.loads(DISCOVERY.read_text())
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery_document["rules"]]
check("discovery inventory_sha256", discovery_document["inventory_sha256"], inventory["inventory_sha256"])
check("discovery ordered source_rule_id bijection", discovery_ids, inventory_ids)
check("discovery unique IDs", len(set(discovery_ids)), len(discovery_ids))
validated = lemma_discovery_contract.validate_trust_boundary(WORKSPACE, DISCOVERY)
print("TRUST-BOUNDARY VALIDATION: PASS")
print(
    "CLASSIFICATION COUNTS "
    + json.dumps(
        {
            "definitions": len(validated["definitions"]),
            "operational_rules": len(validated["operational_rules"]),
            "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
            "domain_lemmas": len(validated["domain_lemmas"]),
        },
        sort_keys=True,
    )
)

recorded_hashes = resolution["hashes"]
computed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(WORKSPACE),
    "stage1_export_sha256": klean_export.tree_digest(WORKSPACE),
    "discovery_manifest_sha256": sha256_file(DISCOVERY),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "generated_tree_sha256": klean_export.tree_digest(GENERATED),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
print("RESOLUTION HASH CHECKS")
for name, observed in computed_hashes.items():
    check(name, observed, recorded_hashes[name])

recorded_sources = resolution["stage1_source_hashes"]
observed_sources = {
    path.relative_to(WORKSPACE).as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        WORKSPACE, "Stage 1 source workspace"
    )
}
source_mismatches = [
    name
    for name in sorted(set(recorded_sources) | set(observed_sources))
    if recorded_sources.get(name) != observed_sources.get(name)
]
print(f"STAGE1 SOURCE HASH COUNT recorded={len(recorded_sources)} observed={len(observed_sources)}")
print(f"STAGE1 SOURCE HASH MISMATCH COUNT {len(source_mismatches)}")
for name in source_mismatches:
    print(
        f"  {name}: observed={observed_sources.get(name)!r} "
        f"expected={recorded_sources.get(name)!r}"
    )

input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
check("input inventory hash", input_manifest["inventory_sha256"], inventory["inventory_sha256"])
check("input verification hash", input_manifest["verification_sha256"], inventory["verification_sha256"])
check("input frozen hash", input_manifest["frozen_input_sha256"], computed_hashes["stage1_export_sha256"])
check("input Stage 1 hash", input_manifest["stage1_workspace_sha256"], computed_hashes["stage1_export_sha256"])
check("input discovery hash", input_manifest["stage3_discovery_manifest_sha256"], computed_hashes["discovery_manifest_sha256"])
check("generator generated hash", generator_manifest["generated_tree_sha256"], computed_hashes["generated_tree_sha256"])
check("generator inventory hash", generator_manifest["provenance"]["inventory_sha256"], inventory["inventory_sha256"])
check("generator Stage 1 hash", generator_manifest["provenance"]["stage1_workspace_sha256"], computed_hashes["stage1_export_sha256"])
check("generator discovery hash", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"], computed_hashes["discovery_manifest_sha256"])
check("obligation-map file hash", sha256_file(GENERATED / "obligation-map.json"), generator_manifest["obligation_map_sha256"])
check("preflight generated hash", preflight["generated_tree_sha256"], computed_hashes["generated_tree_sha256"])
check("preflight Stage 1 hash", preflight["stage1_workspace_sha256"], computed_hashes["stage1_export_sha256"])
check("preflight discovery hash", preflight["stage3_discovery_manifest_sha256"], computed_hashes["discovery_manifest_sha256"])
check("export generated hash", export_result["generated_tree_sha256"], computed_hashes["generated_tree_sha256"])
check("export frozen hash", export_result["frozen_input_sha256"], computed_hashes["stage1_export_sha256"])
check("export discovery hash", export_result["stage3_discovery_manifest_sha256"], computed_hashes["discovery_manifest_sha256"])
check("obligation-map source_rules", obligation_map["source_rules"], input_manifest["source_rules"])
check("obligation count manifest/map", generator_manifest["obligation_count"], len(obligation_map["obligations"]))
check("target generator/audit", generator_manifest["target"], resolution["target"])
check("target expected absent", generator_manifest["target"], None)
print("MECHANICAL RECONSTRUCTION COMPLETE")
