#!/usr/bin/env python3
"""Independent read-only hash, inventory, and zero-obligation cross-check."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")

failures: list[str] = []


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed, expected) -> None:
    ok = observed == expected
    print(f"{label}: {'PASS' if ok else 'FAIL'}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if not ok:
        failures.append(label)


audit = load(AUDIT_INPUT)
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(audit)
check("audit envelope digest", resolved_digest, audit["resolved_input_sha256"])
check(
    "mechanical checker lock",
    file_sha256(Path("/opt/humaneval/data/klean-audit-tools.lock.json")),
    audit["audit"]["mechanical_checker_lock_sha256"],
)
check("audit mode", resolution["mode"], "CLASSIFICATION_ONLY")
check("environment mode binding", resolution["mode"], "CLASSIFICATION_ONLY")
check("problem", resolution["problem_id"], "94-skjkasdkd")
check("condition", resolution["condition"], "bare")
check("semantics mode", resolution["semantics_mode"], "GENERATED_SEMANTICS")

recorded_hashes = resolution["hashes"]
check(
    "pipeline Stage 1 tree hash",
    pipeline_contract.sha256_tree(WORKSPACE),
    recorded_hashes["k_workspace_sha256"],
)
check(
    "export Stage 1 tree hash",
    klean_export.tree_digest(WORKSPACE),
    recorded_hashes["stage1_export_sha256"],
)
check(
    "Stage 2 audit tree hash",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    recorded_hashes["k_audit_sha256"],
)
check(
    "Stage 3 manifest file hash",
    file_sha256(DISCOVERY),
    recorded_hashes["discovery_manifest_sha256"],
)
check(
    "Stage 4 generation tree hash",
    pipeline_contract.sha256_tree(GENERATION),
    recorded_hashes["klean_generation_sha256"],
)
check(
    "selected Stage 2 artifact hash",
    recorded_hashes["k_audit_sha256"],
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
check(
    "selected Stage 4 artifact hash",
    recorded_hashes["klean_generation_sha256"],
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)
check(
    "producer bundle tree hash",
    pipeline_contract.sha256_tree(PRODUCERS),
    recorded_hashes["generation_producer_sources_sha256"],
)
check(
    "generated project tree hash",
    klean_export.tree_digest(GENERATED),
    recorded_hashes["generated_tree_sha256"],
)
check("Lean workspace hash", recorded_hashes["lean_workspace_sha256"], None)
check("Lean invocation hash", recorded_hashes["lean_invocation_sha256"], None)

observed_stage1_sources = {
    path.relative_to(WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        WORKSPACE, "mounted Stage 1 workspace"
    )
}
check(
    "complete Stage 1 per-file hash map",
    observed_stage1_sources,
    resolution["stage1_source_hashes"],
)

generator = load(GENERATION / "generator-manifest.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
producer_files = {
    "klean.py": file_sha256(PRODUCERS / "klean.py"),
    "klean_export.py": file_sha256(PRODUCERS / "klean_export.py"),
}
expected_producer_files = {
    "klean.py": generator["klean_py_sha256"],
    "klean_export.py": generator["exporter_sha256"],
}
check("producer files versus generator manifest", producer_files, expected_producer_files)
check("producer files versus source manifest", producer_files, source_manifest["files"])
generator_image = generator["provenance"]["generator_image_id"]
check("source manifest generator image", source_manifest["generator_image_id"], generator_image)
check(
    "audit-input producer path image",
    "sha256:" + Path(resolution["generation_producer_sources"]).name,
    generator_image,
)
check(
    "generator toolchain lock",
    generator["toolchain"],
    load(Path("/reference/klean-toolchain.lock.json")),
)

inventory = inventory_verification(WORKSPACE)
validated = validate_trust_boundary(WORKSPACE, DISCOVERY)
discovery = load(DISCOVERY)
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
classified_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
check("inventory whole hash", inventory["inventory_sha256"], discovery["inventory_sha256"])
check("ordered Stage 3 identity bijection", classified_ids, canonical_ids)
check("Stage 3 identity uniqueness", len(set(classified_ids)), len(classified_ids))
check(
    "source IDs encode normalized hashes",
    [rule["source_rule_id"] for rule in inventory["rules"]],
    ["rule-" + rule["normalized_sha256"] for rule in inventory["rules"]],
)
check("canonical rule count", len(inventory["rules"]), 15)
check("validated definition count", len(validated["definitions"]), 15)
check("validated operational-rule count", len(validated["operational_rules"]), 0)
check("validated derived-lemma count", len(validated["proved_derived_lemmas"]), 0)
check("validated domain-lemma count", len(validated["domain_lemmas"]), 0)

input_manifest = load(GENERATION / "input-manifest.json")
check("Stage 4 inventory hash", input_manifest["inventory_sha256"], inventory["inventory_sha256"])
check("Stage 4 definitions preserve full reconstructed records", input_manifest["definitions"], validated["definitions"])
check("Stage 4 operational rules", input_manifest["operational_rules"], [])
check("Stage 4 proved derived lemmas", input_manifest["proved_derived_lemmas"], [])
check("Stage 4 source/domain rules", input_manifest["source_rules"], [])
check(
    "input manifest frozen-input hash",
    input_manifest["frozen_input_sha256"],
    klean_export.tree_digest(WORKSPACE),
)
check(
    "input manifest Stage 1 hash",
    input_manifest["stage1_workspace_sha256"],
    klean_export.tree_digest(WORKSPACE),
)
check(
    "input manifest Stage 3 hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    file_sha256(DISCOVERY),
)
check(
    "input manifest verification.k hash",
    input_manifest["verification_sha256"],
    file_sha256(WORKSPACE / "verification.k"),
)
check(
    "generator generated-tree hash",
    generator["generated_tree_sha256"],
    klean_export.tree_digest(GENERATED),
)
check(
    "generator provenance inventory hash",
    generator["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "generator provenance Stage 1 hash",
    generator["provenance"]["stage1_workspace_sha256"],
    klean_export.tree_digest(WORKSPACE),
)
check(
    "generator provenance Stage 3 hash",
    generator["provenance"]["stage3_discovery_manifest_sha256"],
    file_sha256(DISCOVERY),
)

obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = load(obligation_map_path)
check("obligation-map source rules", obligation_map["source_rules"], [])
check("obligation-map obligations", obligation_map["obligations"], [])
check("obligation-map trust parameters", obligation_map["trust_parameters"], [])
check(
    "obligation-map file hash",
    file_sha256(obligation_map_path),
    generator["obligation_map_sha256"],
)
check("generator obligation count", generator["obligation_count"], 0)
check("generator target", generator["target"], None)
check("actual generated target", klean_export.target_statement(GENERATED), None)
check("launcher fixed target", resolution["target"], None)
check("launcher Stage 5 result", resolution["stage5_result"], None)
check("candidate absence", Path("/candidate").exists(), False)

export_result = load(GENERATION / "export-result.json")
preflight = load(GENERATION / "preflight.json")
check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check("export obligation count", export_result["obligation_count"], 0)
check(
    "export frozen-input hash",
    export_result["frozen_input_sha256"],
    klean_export.tree_digest(WORKSPACE),
)
check(
    "export generated-tree hash",
    export_result["generated_tree_sha256"],
    klean_export.tree_digest(GENERATED),
)
check(
    "export Stage 3 hash",
    export_result["stage3_discovery_manifest_sha256"],
    file_sha256(DISCOVERY),
)
check(
    "export trust-inventory hash",
    export_result["trust_inventory_sha256"],
    file_sha256(GENERATION / "trust-inventory.json"),
)
check("selected preflight status", preflight["status"], "KLEAN_NO_OBLIGATIONS")
check("selected preflight obligation count", preflight["obligation_count"], 0)
check("selected preflight target", preflight["target"], None)
check("launcher selected status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
check("launcher preflight snapshot", resolution["stage4_preflight"], preflight)

if failures:
    print("OVERALL: FAIL")
    print("FAILED CHECKS:")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("OVERALL: PASS")
