#!/usr/bin/env python3
"""Independent mechanical reconstruction for the 159-eat Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract
from tools import stage6_resolution_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
K_AUDIT = Path("/reference/k-audit")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, actual: object, expected: object) -> None:
    passed = actual == expected
    print(
        json.dumps(
            {
                "check": label,
                "actual": actual,
                "expected": expected,
                "pass": passed,
            },
            sort_keys=True,
        )
    )
    if not passed:
        raise AssertionError(label)


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
hashes = resolution["hashes"]

check("resolved_input_sha256", resolved_digest, audit_document["resolved_input_sha256"])
check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), "CLASSIFICATION_ONLY")
check("resolution.mode", resolution["mode"], os.environ.get("AUDIT_MODE"))
check("semantics_mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")
check("condition", resolution["condition"], "semantics")
check("problem_id", resolution["problem_id"], "159-eat")

producer_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
recorded_preflight = json.loads((GENERATION / "preflight.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
discovery = json.loads(DISCOVERY.read_text())

producer_hashes = {
    name: sha256_file(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
check("producer files versus source manifest", producer_hashes, producer_manifest["files"])
check(
    "klean_export.py versus generator manifest",
    producer_hashes["klean_export.py"],
    generator_manifest["exporter_sha256"],
)
check(
    "klean.py versus generator manifest",
    producer_hashes["klean.py"],
    generator_manifest["klean_py_sha256"],
)
check(
    "generator image source/generator manifests",
    generator_manifest["provenance"]["generator_image_id"],
    producer_manifest["generator_image_id"],
)
check(
    "generator image versus audit-input producer path",
    "sha256:" + Path(resolution["generation_producer_sources"]).name,
    producer_manifest["generator_image_id"],
)
check(
    "producer tree versus audit input",
    pipeline_contract.sha256_tree(PRODUCERS),
    hashes["generation_producer_sources_sha256"],
)

observed_hashes = {
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
for key, actual in observed_hashes.items():
    check("audit input hash " + key, actual, hashes[key])

for relative, expected in resolution["stage1_source_hashes"].items():
    check(
        "Stage 1 source " + relative,
        sha256_file(WORKSPACE / relative),
        expected,
    )

check(
    "selected K audit artifact hash",
    observed_hashes["k_audit_sha256"],
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
check(
    "selected generation artifact hash",
    observed_hashes["klean_generation_sha256"],
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)

inventory = inventory_verification(WORKSPACE)
print("CANONICAL_INVENTORY=" + json.dumps(inventory, sort_keys=True))
check("inventory module", inventory["verification_module"], "EAT-VERIFICATION")
check("local module closure", inventory["verification_modules"], ["EAT-VERIFICATION"])
check("inventory rule count", len(inventory["rules"]), 1)

source_lines = (WORKSPACE / "verification.k").read_text().splitlines()
manual_text = "\n".join(source_lines[10:27])
manual_normalized = " ".join(manual_text.split())
manual_hash = hashlib.sha256(manual_normalized.encode()).hexdigest()
rule = inventory["rules"][0]
check("manual source span start", rule["start_line"], 11)
check("manual source span end", rule["end_line"], 27)
check("manual source text", rule["text"], manual_text)
check("manual normalized hash", rule["normalized_sha256"], manual_hash)
check("manual source_rule_id", rule["source_rule_id"], "rule-" + manual_hash)
check(
    "manual inventory hash",
    inventory["inventory_sha256"],
    canonical_json_sha256(inventory["rules"]),
)

check("discovery schema", discovery["schema_version"], 2)
check("discovery inventory hash", discovery["inventory_sha256"], inventory["inventory_sha256"])
check(
    "ordered discovery identities",
    [entry["source_rule_id"] for entry in discovery["rules"]],
    [entry["source_rule_id"] for entry in inventory["rules"]],
)
check(
    "unique discovery identities",
    len({entry["source_rule_id"] for entry in discovery["rules"]}),
    len(discovery["rules"]),
)
check("discovery classification count", len(discovery["rules"]), len(inventory["rules"]))
check("sole classification", discovery["rules"][0]["classification"], "DEFINITION")
for canonical_rule, classified in zip(inventory["rules"], discovery["rules"], strict=True):
    check(
        "classification identity " + canonical_rule["source_rule_id"],
        classified["source_rule_id"],
        canonical_rule["source_rule_id"],
    )
    if "simplification" in canonical_rule["attributes"]:
        check(
            "simplification classification " + canonical_rule["source_rule_id"],
            classified["classification"] in {"DEFINITION", "DOMAIN_LEMMA"},
            True,
        )

validated = lemma_discovery_contract.validate_trust_boundary(WORKSPACE, DISCOVERY)
print("VALIDATED_CLASSIFICATION=" + json.dumps(validated, sort_keys=True))
check("validated inventory", validated["inventory_sha256"], inventory["inventory_sha256"])
check("validated definitions", [r["source_rule_id"] for r in validated["definitions"]], [rule["source_rule_id"]])
check("validated operational rules", validated["operational_rules"], [])
check("validated proved derived lemmas", validated["proved_derived_lemmas"], [])
check("validated domain lemmas", validated["domain_lemmas"], [])

check("input manifest inventory", input_manifest["inventory_sha256"], inventory["inventory_sha256"])
check("input manifest source rules", input_manifest["source_rules"], [])
check(
    "input manifest definition identities",
    [entry["source_rule_id"] for entry in input_manifest["definitions"]],
    [rule["source_rule_id"]],
)
check("input manifest operational rules", input_manifest["operational_rules"], [])
check("input manifest proved derived lemmas", input_manifest["proved_derived_lemmas"], [])
check("input manifest verification hash", input_manifest["verification_sha256"], sha256_file(WORKSPACE / "verification.k"))
check("generator provenance inventory", generator_manifest["provenance"]["inventory_sha256"], inventory["inventory_sha256"])
check("generator obligation count", generator_manifest["obligation_count"], 0)
check("generator target", generator_manifest["target"], None)
check("obligation map source rules", obligation_map["source_rules"], [])
check("obligation map obligations", obligation_map["obligations"], [])
check("obligation map trust parameters", obligation_map["trust_parameters"], [])
check("obligation map hash", sha256_file(GENERATED / "obligation-map.json"), generator_manifest["obligation_map_sha256"])
check("generated target parser", klean_export.target_statement(GENERATED), None)
check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check("export obligation count", export_result["obligation_count"], 0)
check("recorded preflight status", recorded_preflight["status"], "KLEAN_NO_OBLIGATIONS")
check("recorded preflight target", recorded_preflight["target"], None)
check("recorded preflight obligation count", recorded_preflight["obligation_count"], 0)
check("audit input target", resolution["target"], None)
check("audit input Stage 4 status", resolution["stage4_preflight"]["status"], "KLEAN_NO_OBLIGATIONS")
check("audit input Stage 5 result", resolution["stage5_result"], None)
check("candidate absent", Path("/candidate").exists(), False)

print("RESULT=PASS")
