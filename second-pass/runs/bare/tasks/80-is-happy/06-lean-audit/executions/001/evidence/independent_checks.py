#!/usr/bin/env python3
"""Independent structural/hash checks for this Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import (
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
AUDIT_INPUT = Path("/audit-input.json")


def load(path: Path) -> dict:
    document = json.loads(path.read_text())
    assert isinstance(document, dict)
    return document


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(label: str, observed, expected) -> None:
    if observed != expected:
        raise AssertionError(f"{label}: observed={observed!r} expected={expected!r}")
    print(f"PASS {label}: {observed!r}")


def main() -> None:
    envelope = load(AUDIT_INPUT)
    resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(envelope)
    checked("signed resolution digest", resolved_digest, envelope["resolved_input_sha256"])
    checked("launcher/environment mode", os.environ.get("AUDIT_MODE"), resolution["mode"])
    checked("problem", resolution["problem_id"], "80-is-happy")
    checked("condition", resolution["condition"], "bare")
    checked("semantics mode", resolution["semantics_mode"], "GENERATED_SEMANTICS")

    hashes = resolution["hashes"]
    observed_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
        "stage1_export_sha256": klean_export.tree_digest(K_PROOF),
        "discovery_manifest_sha256": sha256_file(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    checked("all signed artifact hashes", observed_hashes, hashes)
    observed_source_hashes = {
        path.relative_to(K_PROOF).as_posix(): sha256_file(path)
        for path in sorted(K_PROOF.iterdir())
        if path.is_file() and not path.is_symlink()
    }
    checked("all frozen Stage 1 source hashes", observed_source_hashes, resolution["stage1_source_hashes"])

    source_manifest = load(PRODUCERS / "source-manifest.json")
    generator_manifest = load(GENERATION / "generator-manifest.json")
    input_manifest = load(GENERATION / "input-manifest.json")
    export_result = load(GENERATION / "export-result.json")
    recorded_preflight = load(GENERATION / "preflight.json")
    trust_inventory = load(GENERATION / "trust-inventory.json")
    obligation_map = load(GENERATED / "obligation-map.json")
    toolchain_lock = load(Path("/reference/klean-toolchain.lock.json"))

    producer_hashes = {
        "klean.py": sha256_file(PRODUCERS / "klean.py"),
        "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
    }
    checked("producer source manifest hashes", producer_hashes, source_manifest["files"])
    checked("producer klean.py hash", producer_hashes["klean.py"], generator_manifest["klean_py_sha256"])
    checked(
        "producer klean_export.py hash",
        producer_hashes["klean_export.py"],
        generator_manifest["exporter_sha256"],
    )
    image_id = generator_manifest["provenance"]["generator_image_id"]
    checked("producer source manifest image ID", source_manifest["generator_image_id"], image_id)
    checked(
        "audit-input producer path image ID",
        f"sha256:{Path(resolution['generation_producer_sources']).name}",
        image_id,
    )
    checked("generator toolchain lock", generator_manifest["toolchain"], toolchain_lock)

    inventory = inventory_verification(K_PROOF)
    validated = lemma_discovery_contract.validate_trust_boundary(K_PROOF, DISCOVERY)
    discovery = load(DISCOVERY)
    checked("verification module", inventory["verification_module"], "VERIFICATION")
    checked("local verification-module closure", inventory["verification_modules"], ["VERIFICATION"])
    checked("inventory rule count", len(inventory["rules"]), 10)
    checked("inventory hash", canonical_json_sha256(inventory["rules"]), inventory["inventory_sha256"])
    checked("manifest inventory hash", discovery["inventory_sha256"], inventory["inventory_sha256"])

    source_lines = (K_PROOF / "verification.k").read_text().splitlines()
    canonical_ids = []
    for index, rule in enumerate(inventory["rules"]):
        normalized = " ".join(rule["text"].split())
        normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
        source_text = "\n".join(source_lines[rule["start_line"] - 1:rule["end_line"]])
        checked(f"rule {index} normalized hash", normalized_hash, rule["normalized_sha256"])
        checked(f"rule {index} source_rule_id", rule["source_rule_id"], f"rule-{normalized_hash}")
        checked(f"rule {index} exact source span", source_text, rule["text"])
        canonical_ids.append(rule["source_rule_id"])

    manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    checked("ordered source-rule identities", manifest_ids, canonical_ids)
    checked("unique manifest identities", len(set(manifest_ids)), len(manifest_ids))
    checked("validated inventory rules", validated["rules"], inventory["rules"])
    checked("definition count", len(validated["definitions"]), 10)
    checked("operational-rule count", len(validated["operational_rules"]), 0)
    checked("proved-derived-lemma count", len(validated["proved_derived_lemmas"]), 0)
    checked("domain-lemma count", len(validated["domain_lemmas"]), 0)
    checked(
        "independent classification labels",
        [entry["classification"] for entry in discovery["rules"]],
        ["DEFINITION"] * 10,
    )
    checked("input manifest definitions", input_manifest["definitions"], validated["definitions"])
    checked("input manifest operational rules", input_manifest["operational_rules"], [])
    checked("input manifest proved derived lemmas", input_manifest["proved_derived_lemmas"], [])
    checked("input manifest source rules", input_manifest["source_rules"], [])

    checked("empty source-rule side of bijection", obligation_map["source_rules"], [])
    checked("empty obligation side of bijection", obligation_map["obligations"], [])
    checked("empty target parameter set", obligation_map["trust_parameters"], [])
    checked("no expected target definition", klean_export.expected_target_definition(obligation_map), None)
    checked("no generated target statement", klean_export.target_statement(GENERATED), None)
    checked("generator target", generator_manifest["target"], None)
    checked("audit-input target", resolution["target"], None)
    checked("generator obligation count", generator_manifest["obligation_count"], 0)
    checked("export obligation count", export_result["obligation_count"], 0)
    checked("recorded preflight obligation count", recorded_preflight["obligation_count"], 0)
    checked("generator obligation map hash", sha256_file(GENERATED / "obligation-map.json"), generator_manifest["obligation_map_sha256"])
    checked("export trust inventory hash", sha256_file(GENERATION / "trust-inventory.json"), export_result["trust_inventory_sha256"])
    checked("input frozen hash", input_manifest["frozen_input_sha256"], hashes["stage1_export_sha256"])
    checked("input Stage 1 hash", input_manifest["stage1_workspace_sha256"], hashes["stage1_export_sha256"])
    checked("input Stage 3 hash", input_manifest["stage3_discovery_manifest_sha256"], hashes["discovery_manifest_sha256"])
    checked("input verification.k hash", input_manifest["verification_sha256"], resolution["stage1_source_hashes"]["verification.k"])
    checked("generator Stage 1 provenance", generator_manifest["provenance"]["stage1_workspace_sha256"], hashes["stage1_export_sha256"])
    checked("generator Stage 3 provenance", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"], hashes["discovery_manifest_sha256"])
    checked("generator inventory provenance", generator_manifest["provenance"]["inventory_sha256"], inventory["inventory_sha256"])
    checked("generator generated-tree hash", generator_manifest["generated_tree_sha256"], hashes["generated_tree_sha256"])
    checked("export generated-tree hash", export_result["generated_tree_sha256"], hashes["generated_tree_sha256"])
    checked("export frozen-input hash", export_result["frozen_input_sha256"], hashes["stage1_export_sha256"])
    checked("export Stage 3 hash", export_result["stage3_discovery_manifest_sha256"], hashes["discovery_manifest_sha256"])
    checked("recorded preflight generated-tree hash", recorded_preflight["generated_tree_sha256"], hashes["generated_tree_sha256"])
    checked("recorded preflight frozen-input hash", recorded_preflight["frozen_input_sha256"], hashes["stage1_export_sha256"])
    checked("recorded preflight Stage 1 hash", recorded_preflight["stage1_workspace_sha256"], hashes["stage1_export_sha256"])
    checked("recorded preflight Stage 3 hash", recorded_preflight["stage3_discovery_manifest_sha256"], hashes["discovery_manifest_sha256"])
    checked("audit-input embedded Stage 4 preflight", resolution["stage4_preflight"], recorded_preflight)
    checked("selected K audit artifact hash", resolution["selections"]["k_audit"]["artifact_sha256"], hashes["k_audit_sha256"])
    checked("selected Klean generation artifact hash", resolution["selections"]["klean_generation"]["artifact_sha256"], hashes["klean_generation_sha256"])
    checked("recorded Stage 4 status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
    checked("input manifest source-rule/obligation eligibility", len(input_manifest["source_rules"]), 0)
    checked("no Stage 5 result", resolution["stage5_result"], None)
    checked("no Lean workspace", resolution["lean_workspace"], None)
    checked("no Lean invocation", resolution["lean_invocation"], None)
    checked("candidate path absent", Path("/candidate").exists(), False)

    for diagnostic in recorded_preflight["diagnostics"]:
        tail_hash = hashlib.sha256(diagnostic["output_tail"].encode()).hexdigest()
        checked(
            f"recorded complete diagnostic output hash {' '.join(diagnostic['command'])}",
            tail_hash,
            diagnostic["output_sha256"],
        )

    checked("trust inventory designated sorries", trust_inventory["designated_sorries"], 0)
    checked("trust inventory other sorries", trust_inventory["other_sorries"], 0)
    print("ALL INDEPENDENT STRUCTURAL/HASH CHECKS PASSED")


if __name__ == "__main__":
    main()
