#!/usr/bin/env python3
"""Independent hash, inventory, and no-obligation integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")

failures: list[str] = []


def check(label: str, observed: object, expected: object) -> None:
    if observed == expected:
        print(f"PASS {label}: {observed!r}")
    else:
        print(f"FAIL {label}: observed={observed!r} expected={expected!r}")
        failures.append(label)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
print(f"PASS signed audit-input envelope: {resolved_digest}")
check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("problem_id", resolution["problem_id"], "139-special-factorial")
check("condition", resolution["condition"], "semantics")
check("semantics_mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")

recorded_hashes = resolution["hashes"]
check(
    "Stage 1 pipeline tree SHA-256",
    pipeline_contract.sha256_tree(K_WORKSPACE),
    recorded_hashes["k_workspace_sha256"],
)
check(
    "Stage 1 export tree SHA-256",
    klean_export.tree_digest(K_WORKSPACE),
    recorded_hashes["stage1_export_sha256"],
)
check(
    "Stage 2 audit pipeline tree SHA-256",
    pipeline_contract.sha256_tree(K_AUDIT),
    recorded_hashes["k_audit_sha256"],
)
check(
    "Stage 3 discovery SHA-256",
    sha256_file(DISCOVERY),
    recorded_hashes["discovery_manifest_sha256"],
)
check(
    "Stage 4 generation pipeline tree SHA-256",
    pipeline_contract.sha256_tree(GENERATION),
    recorded_hashes["klean_generation_sha256"],
)
check(
    "Stage 4 generated project tree SHA-256",
    klean_export.tree_digest(GENERATED),
    recorded_hashes["generated_tree_sha256"],
)
check(
    "producer-source pipeline tree SHA-256",
    pipeline_contract.sha256_tree(PRODUCERS),
    recorded_hashes["generation_producer_sources_sha256"],
)
check("Lean workspace hash", recorded_hashes["lean_workspace_sha256"], None)
check("Lean invocation hash", recorded_hashes["lean_invocation_sha256"], None)

observed_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): sha256_file(path)
    for path in sorted(K_WORKSPACE.rglob("*"))
    if path.is_file() and not path.is_symlink()
}
check(
    "exact Stage 1 source-file hash map",
    observed_source_hashes,
    resolution["stage1_source_hashes"],
)

generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
toolchain_lock = json.loads(TOOLCHAIN_LOCK.read_text())
discovery = json.loads(DISCOVERY.read_text())

producer_names = {
    path.relative_to(PRODUCERS).as_posix()
    for path in PRODUCERS.rglob("*")
    if path.is_file() and not path.is_symlink()
}
check(
    "exact producer-source file set",
    producer_names,
    {"source-manifest.json", "klean_export.py", "klean.py"},
)
expected_producer_files = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
check("producer source manifest file hashes", source_manifest["files"], expected_producer_files)
for name, expected in expected_producer_files.items():
    check(f"producer {name} SHA-256", sha256_file(PRODUCERS / name), expected)
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
check("producer source manifest image ID", source_manifest["generator_image_id"], generator_image_id)
check(
    "audit-input producer path image ID",
    Path(resolution["generation_producer_sources"]).name,
    generator_image_id.removeprefix("sha256:"),
)
check("generator toolchain lock", generator_manifest["toolchain"], toolchain_lock)

inventory = inventory_verification(K_WORKSPACE)
inventory_rules = inventory["rules"]
check("inventory hash in Stage 3", discovery["inventory_sha256"], inventory["inventory_sha256"])
inventory_ids = [entry["source_rule_id"] for entry in inventory_rules]
discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
check("ordered Stage 3 source_rule_id list", discovery_ids, inventory_ids)
check("unique Stage 3 source_rule_ids", len(set(discovery_ids)), len(discovery_ids))
check("Stage 3 rule count", len(discovery_ids), len(inventory_ids))

verification_lines = (K_WORKSPACE / "verification.k").read_text().splitlines()
for index, rule in enumerate(inventory_rules):
    normalized = " ".join(rule["text"].split())
    normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
    source_slice = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    check(f"rule {index} exact source span", rule["text"], source_slice)
    check(f"rule {index} normalized SHA-256", rule["normalized_sha256"], normalized_hash)
    check(f"rule {index} source_rule_id", rule["source_rule_id"], f"rule-{normalized_hash}")
check("whole inventory canonical hash", inventory["inventory_sha256"], canonical_json_sha256(inventory_rules))

classifications = {
    entry["source_rule_id"]: {
        "classification": entry["classification"],
        "rationale": entry["rationale"],
    }
    for entry in discovery["rules"]
}
classified = [{**rule, **classifications[rule["source_rule_id"]]} for rule in inventory_rules]
definitions = [rule for rule in classified if rule["classification"] == "DEFINITION"]
operational = [rule for rule in classified if rule["classification"] == "OPERATIONAL_RULE"]
derived = [rule for rule in classified if rule["classification"] == "PROVED_DERIVED_LEMMA"]
domain = [rule for rule in classified if rule["classification"] == "DOMAIN_LEMMA"]

check("Stage 4 ordered definitions", input_manifest["definitions"], definitions)
check("Stage 4 operational rules", input_manifest["operational_rules"], operational)
check("Stage 4 proved derived lemmas", input_manifest["proved_derived_lemmas"], derived)
check("Stage 4 source/domain rules", input_manifest["source_rules"], domain)
check("obligation-map source/domain rules", obligation_map["source_rules"], domain)
check("obligation-map obligations", obligation_map["obligations"], [])
check("obligation-map trust parameters", obligation_map["trust_parameters"], [])
check("generator obligation count", generator_manifest["obligation_count"], len(domain))
check("export obligation count", export_result["obligation_count"], len(domain))
check("preflight obligation count", preflight["obligation_count"], len(domain))
check("audit-input preflight", resolution["stage4_preflight"], preflight)
check("generator target", generator_manifest["target"], None)
check("preflight target", preflight["target"], None)
check("audit-input target", resolution["target"], None)
check("detected generated target", klean_export.target_statement(GENERATED), None)
check("Stage 4 status", preflight["status"], "KLEAN_NO_OBLIGATIONS")
check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check("selected Stage 4 status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
check("Stage 5 result", resolution["stage5_result"], None)
check("candidate path absent", Path("/candidate").exists(), False)

check(
    "generator obligation-map SHA-256",
    generator_manifest["obligation_map_sha256"],
    sha256_file(GENERATED / "obligation-map.json"),
)
check(
    "generator generated-tree SHA-256",
    generator_manifest["generated_tree_sha256"],
    klean_export.tree_digest(GENERATED),
)
check(
    "Stage 4 Stage 1 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    klean_export.tree_digest(K_WORKSPACE),
)
check(
    "Stage 4 Stage 3 provenance",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    sha256_file(DISCOVERY),
)
check(
    "Stage 4 inventory provenance",
    generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "selected Stage 2 hash",
    resolution["selections"]["k_audit"]["artifact_sha256"],
    pipeline_contract.sha256_tree(K_AUDIT),
)
check(
    "selected Stage 4 hash",
    resolution["selections"]["klean_generation"]["artifact_sha256"],
    pipeline_contract.sha256_tree(GENERATION),
)

if failures:
    print(f"SUMMARY FAIL ({len(failures)} failures): {', '.join(failures)}")
    raise SystemExit(1)
print("SUMMARY PASS: every checked recorded hash and structural binding matches")
