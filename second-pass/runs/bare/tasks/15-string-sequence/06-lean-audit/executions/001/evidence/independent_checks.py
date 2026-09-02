#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import verify_audit_input


K_WORKSPACE = Path("/reference/k-proof")
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
AUDIT_INPUT_PATH = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS {message}")


def main() -> None:
    audit_document = json.loads(AUDIT_INPUT_PATH.read_text())
    resolution, resolution_digest = verify_audit_input(audit_document)
    hashes = resolution["hashes"]
    discovery = json.loads(DISCOVERY_PATH.read_text())
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    prior_preflight = json.loads((GENERATION / "preflight.json").read_text())
    rerun_preflight = json.loads(
        Path("/audit-output/evidence/preflight-rerun.json").read_text()
    )
    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = json.loads(obligation_map_path.read_text())

    print("AUDIT INPUT")
    require(
        resolution_digest == audit_document["resolved_input_sha256"],
        "signed resolution digest is valid",
    )
    require(
        resolution["mode"] == os.environ["AUDIT_MODE"] == "CLASSIFICATION_ONLY",
        "launcher mode, signed mode, and expected classification-only mode agree",
    )

    print("RECORDED TREE AND FILE HASHES")
    observed_hashes = {
        "k_workspace_sha256": sha256_tree(K_WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
        "discovery_manifest_sha256": sha256_file(DISCOVERY_PATH),
        "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
        "klean_generation_sha256": sha256_tree(GENERATION),
        "generation_producer_sources_sha256": sha256_tree(PRODUCERS),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    for name, observed in observed_hashes.items():
        require(hashes[name] == observed, f"{name} matches audit input: {observed}")
    require(
        resolution["selections"]["k_audit"]["artifact_sha256"]
        == observed_hashes["k_audit_sha256"],
        "selected Stage 2 artifact hash matches its recomputed tree",
    )
    require(
        resolution["selections"]["klean_generation"]["artifact_sha256"]
        == observed_hashes["klean_generation_sha256"],
        "selected Stage 4 artifact hash matches its recomputed tree",
    )
    observed_stage1_files = {
        path.relative_to(K_WORKSPACE).as_posix(): sha256_file(path)
        for path in sorted(K_WORKSPACE.rglob("*"))
        if path.is_file()
    }
    require(
        observed_stage1_files == resolution["stage1_source_hashes"],
        "all Stage 1 source-file hashes match audit input",
    )

    print("RULE INVENTORY")
    inventory = inventory_verification(K_WORKSPACE)
    verification_lines = (K_WORKSPACE / "verification.k").read_text().splitlines()
    recomputed_documents = []
    for index, rule in enumerate(inventory["rules"]):
        span_text = "\n".join(
            verification_lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        require(span_text == rule["text"], f"rule {index} source span is exact")
        normalized = " ".join(span_text.split())
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        require(
            digest == rule["normalized_sha256"],
            f"rule {index} normalized source hash is exact",
        )
        require(
            rule["source_rule_id"] == f"rule-{digest}",
            f"rule {index} source_rule_id is hash-derived",
        )
        recomputed_documents.append(rule)
    require(
        canonical_json_sha256(recomputed_documents)
        == inventory["inventory_sha256"],
        "whole inventory hash recomputes",
    )
    canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
    classified_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    require(len(canonical_ids) == len(set(canonical_ids)), "inventory IDs are unique")
    require(
        len(classified_ids) == len(set(classified_ids)),
        "classification IDs are unique",
    )
    require(
        classified_ids == canonical_ids,
        "classification is an ordered bijection with the inventory",
    )
    require(
        discovery["inventory_sha256"] == inventory["inventory_sha256"],
        "classification whole-inventory hash matches reconstruction",
    )
    require(
        all(entry["classification"] == "DEFINITION" for entry in discovery["rules"]),
        "manifest classifies every rule as DEFINITION",
    )
    require(
        all("simplification" not in rule["attributes"] for rule in inventory["rules"]),
        "inventory contains no simplification-attributed rule",
    )
    print(
        "inventory summary",
        json.dumps(
            {
                "module": inventory["verification_module"],
                "closure": inventory["verification_modules"],
                "rule_count": len(inventory["rules"]),
                "inventory_sha256": inventory["inventory_sha256"],
            },
            sort_keys=True,
        ),
    )

    print("PRODUCER PROVENANCE")
    producer_files = {
        path.name
        for path in PRODUCERS.iterdir()
        if path.is_file() and not path.is_symlink()
    }
    require(
        producer_files == {"klean_export.py", "klean.py", "source-manifest.json"},
        "producer bundle contains exactly the expected regular files",
    )
    producer_hashes = {
        "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
        "klean.py": sha256_file(PRODUCERS / "klean.py"),
    }
    require(
        producer_hashes == source_manifest["files"],
        "producer files match source-manifest hashes",
    )
    require(
        producer_hashes["klean_export.py"]
        == generator_manifest["exporter_sha256"],
        "klean_export.py matches generator-manifest hash",
    )
    require(
        producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"],
        "klean.py matches generator-manifest hash",
    )
    image_id = generator_manifest["provenance"]["generator_image_id"]
    require(
        source_manifest["generator_image_id"] == image_id,
        "source manifest and generator manifest bind the same image ID",
    )
    recorded_bundle_key = Path(
        resolution["generation_producer_sources"]
    ).name
    require(
        image_id == f"sha256:{recorded_bundle_key}",
        "audit-input producer path is keyed by the immutable generator image ID",
    )

    print("STAGE 4 MANIFESTS AND OBLIGATIONS")
    require(
        generator_manifest["toolchain"]
        == json.loads(Path("/reference/klean-toolchain.lock.json").read_text()),
        "generator toolchain exactly matches trusted lock",
    )
    require(
        generator_manifest["generated_tree_sha256"]
        == observed_hashes["generated_tree_sha256"],
        "generator manifest binds the generated tree",
    )
    require(
        generator_manifest["obligation_map_sha256"]
        == sha256_file(obligation_map_path),
        "generator manifest binds the obligation map",
    )
    require(
        export_result["trust_inventory_sha256"]
        == sha256_file(GENERATION / "trust-inventory.json"),
        "export result binds the trust inventory",
    )
    require(
        input_manifest["stage3_discovery_manifest_sha256"]
        == observed_hashes["discovery_manifest_sha256"],
        "input manifest binds the protected classification",
    )
    require(
        input_manifest["frozen_input_sha256"]
        == input_manifest["stage1_workspace_sha256"]
        == observed_hashes["stage1_export_sha256"],
        "input manifest binds both Stage 1 tree fields",
    )
    require(
        input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
        "input manifest binds the reconstructed inventory",
    )
    require(
        input_manifest["verification_sha256"]
        == inventory["verification_sha256"],
        "input manifest binds frozen verification.k",
    )
    require(
        generator_manifest["provenance"]["inventory_sha256"]
        == inventory["inventory_sha256"],
        "generator provenance binds the reconstructed inventory",
    )
    require(
        generator_manifest["provenance"]["stage1_workspace_sha256"]
        == observed_hashes["stage1_export_sha256"],
        "generator provenance binds the frozen Stage 1 export tree",
    )
    require(
        generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
        == observed_hashes["discovery_manifest_sha256"],
        "generator provenance binds the protected discovery manifest",
    )
    require(
        export_result["frozen_input_sha256"]
        == observed_hashes["stage1_export_sha256"],
        "export result binds the frozen Stage 1 export tree",
    )
    require(
        export_result["stage3_discovery_manifest_sha256"]
        == observed_hashes["discovery_manifest_sha256"],
        "export result binds the protected discovery manifest",
    )
    require(
        export_result["generated_tree_sha256"]
        == observed_hashes["generated_tree_sha256"],
        "export result binds the generated tree",
    )
    require(
        input_manifest["source_rules"] == [],
        "input manifest records an empty DOMAIN_LEMMA source set",
    )
    require(
        obligation_map
        == {
            "schema_version": 3,
            "source_rules": [],
            "obligations": [],
            "trust_parameters": [],
        },
        "obligation map is the exact empty source/obligation bijection",
    )
    require(
        generator_manifest["obligation_count"]
        == export_result["obligation_count"]
        == rerun_preflight["obligation_count"]
        == 0,
        "all Stage 4 counts agree on zero obligations",
    )
    require(
        generator_manifest["target"]
        is resolution["target"]
        is rerun_preflight["target"]
        is None,
        "generator, audit input, and rerun preflight all record no target",
    )
    require(
        klean_export.expected_target_definition(obligation_map) is None,
        "empty obligation map has no expected target definition",
    )
    require(
        klean_export.target_statement(GENERATED) is None,
        "generated project contains no fixed target declaration",
    )
    require(
        export_result["status"]
        == prior_preflight["status"]
        == rerun_preflight["status"]
        == resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS",
        "all Stage 4 statuses agree on KLEAN_NO_OBLIGATIONS",
    )
    require(
        prior_preflight == rerun_preflight,
        "rerun preflight evidence exactly matches selected preflight",
    )
    require(
        resolution["stage4_preflight"] == rerun_preflight,
        "rerun preflight exactly matches audit-input binding",
    )

    print("STAGE 5 ABSENCE")
    require(not Path("/candidate").exists(), "no Stage 5 candidate is mounted")
    require(
        resolution["lean_workspace"] is None
        and resolution["lean_invocation"] is None
        and resolution["stage5_result"] is None,
        "audit input records no Stage 5 workspace, invocation, or result",
    )
    print("ALL INDEPENDENT STRUCTURAL CHECKS PASSED")


if __name__ == "__main__":
    main()
