#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, lemma_discovery_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.pipeline_contract import sha256_file, sha256_tree
from tools.stage6_resolution_contract import verify_audit_input


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict), path
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def same(label: str, observed, expected, results: dict) -> None:
    match = observed == expected
    results[label] = {
        "match": match,
        "observed": observed,
        "expected": expected,
    }
    assert match, label


def main() -> None:
    audit = load(AUDIT_INPUT)
    resolution, resolved_digest = verify_audit_input(audit)
    discovery = load(DISCOVERY)
    input_manifest = load(GENERATION / "input-manifest.json")
    generator_manifest = load(GENERATION / "generator-manifest.json")
    export_result = load(GENERATION / "export-result.json")
    preflight = load(GENERATION / "preflight.json")
    obligation_map = load(GENERATED / "obligation-map.json")
    source_manifest = load(PRODUCERS / "source-manifest.json")
    lock = load(Path("/reference/klean-toolchain.lock.json"))
    results: dict = {}

    same(
        "launcher mode",
        os.environ.get("AUDIT_MODE"),
        resolution["mode"],
        results,
    )
    same(
        "resolved input canonical digest",
        resolved_digest,
        audit["resolved_input_sha256"],
        results,
    )
    same(
        "Stage 1 pipeline tree hash",
        sha256_tree(K_WORKSPACE),
        resolution["hashes"]["k_workspace_sha256"],
        results,
    )
    same(
        "Stage 1 export tree hash",
        klean_export.tree_digest(K_WORKSPACE),
        resolution["hashes"]["stage1_export_sha256"],
        results,
    )
    same(
        "selected Stage 2 tree hash",
        sha256_tree(Path("/reference/k-audit")),
        resolution["hashes"]["k_audit_sha256"],
        results,
    )
    same(
        "Stage 3 file hash",
        digest(DISCOVERY),
        resolution["hashes"]["discovery_manifest_sha256"],
        results,
    )
    same(
        "Stage 4 generation pipeline tree hash",
        sha256_tree(GENERATION),
        resolution["hashes"]["klean_generation_sha256"],
        results,
    )
    same(
        "generated project export tree hash",
        klean_export.tree_digest(GENERATED),
        resolution["hashes"]["generated_tree_sha256"],
        results,
    )
    same(
        "producer bundle pipeline tree hash",
        sha256_tree(PRODUCERS),
        resolution["hashes"]["generation_producer_sources_sha256"],
        results,
    )
    for relative, expected in resolution["stage1_source_hashes"].items():
        same(
            f"Stage 1 source hash {relative}",
            sha256_file(K_WORKSPACE / relative),
            expected,
            results,
        )

    inventory = inventory_verification(K_WORKSPACE)
    verification_lines = (K_WORKSPACE / "verification.k").read_text().splitlines()
    start = verification_lines.index("  rule primeHexCount(S) =>")
    end = verification_lines.index("endmodule", start)
    manually_extracted = "\n".join(verification_lines[start:end]).rstrip()
    manually_normalized = " ".join(manually_extracted.split())
    manual_rule_hash = hashlib.sha256(manually_normalized.encode()).hexdigest()
    manual_rule = {
        "source_rule_id": f"rule-{manual_rule_hash}",
        "module": "VERIFICATION",
        "start_line": start + 1,
        "end_line": end,
        "normalized_sha256": manual_rule_hash,
        "attributes": [],
        "text": manually_extracted,
    }
    same(
        "manual source span and normalized rule reconstruction",
        [manual_rule],
        inventory["rules"],
        results,
    )
    same(
        "manual whole-inventory hash",
        canonical_json_sha256([manual_rule]),
        inventory["inventory_sha256"],
        results,
    )
    same(
        "Stage 3 inventory hash",
        discovery["inventory_sha256"],
        inventory["inventory_sha256"],
        results,
    )
    inventory_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
    classified_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    same(
        "ordered Stage 3 identity bijection",
        classified_ids,
        inventory_ids,
        results,
    )
    same(
        "Stage 3 identities unique",
        len(set(classified_ids)),
        len(classified_ids),
        results,
    )
    same(
        "independent classification",
        [entry["classification"] for entry in discovery["rules"]],
        ["DEFINITION"],
        results,
    )

    validated = lemma_discovery_contract.validate_trust_boundary(
        K_WORKSPACE, DISCOVERY
    )
    same(
        "validated domain set",
        [entry["source_rule_id"] for entry in validated["domain_lemmas"]],
        [],
        results,
    )
    same(
        "input-manifest inventory hash",
        input_manifest["inventory_sha256"],
        inventory["inventory_sha256"],
        results,
    )
    same(
        "input-manifest verification hash",
        input_manifest["verification_sha256"],
        inventory["verification_sha256"],
        results,
    )
    for label, document in (
        ("input manifest", input_manifest),
        ("generator provenance", generator_manifest["provenance"]),
        ("export result", export_result),
        ("recorded preflight", preflight),
    ):
        same(
            f"{label} Stage 1 export hash",
            document.get(
                "frozen_input_sha256",
                document.get(
                    "stage1_workspace_sha256",
                    generator_manifest["provenance"].get(
                        "stage1_workspace_sha256"
                    ),
                ),
            ),
            resolution["hashes"]["stage1_export_sha256"],
            results,
        )
        same(
            f"{label} Stage 3 hash",
            document.get("stage3_discovery_manifest_sha256"),
            resolution["hashes"]["discovery_manifest_sha256"],
            results,
        )

    source_rules = input_manifest["source_rules"]
    same("Stage 4 source-rule set", source_rules, [], results)
    same(
        "obligation-map source-rule bijection",
        obligation_map["source_rules"],
        source_rules,
        results,
    )
    same("obligation-map obligations", obligation_map["obligations"], [], results)
    same(
        "obligation-map trust parameters",
        obligation_map["trust_parameters"],
        [],
        results,
    )
    same(
        "obligation-map hash",
        digest(GENERATED / "obligation-map.json"),
        generator_manifest["obligation_map_sha256"],
        results,
    )
    same(
        "generated project hash in generator manifest",
        klean_export.tree_digest(GENERATED),
        generator_manifest["generated_tree_sha256"],
        results,
    )
    same(
        "generated project hash in export result",
        klean_export.tree_digest(GENERATED),
        export_result["generated_tree_sha256"],
        results,
    )
    same(
        "trust-inventory hash",
        digest(GENERATION / "trust-inventory.json"),
        export_result["trust_inventory_sha256"],
        results,
    )
    same(
        "pinned toolchain",
        generator_manifest["toolchain"],
        lock,
        results,
    )

    observed_target = klean_export.target_statement(GENERATED)
    same("generated target absent", observed_target, None, results)
    same("generator-manifest target absent", generator_manifest["target"], None, results)
    same("launcher target absent", resolution["target"], None, results)
    same("recorded preflight target absent", preflight["target"], None, results)
    same("generator obligation count", generator_manifest["obligation_count"], 0, results)
    same("export obligation count", export_result["obligation_count"], 0, results)
    same("preflight obligation count", preflight["obligation_count"], 0, results)
    same("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS", results)
    same("preflight status", preflight["status"], "KLEAN_NO_OBLIGATIONS", results)
    same(
        "launcher selection status",
        resolution["selections"]["klean_generation"]["status"],
        "KLEAN_NO_OBLIGATIONS",
        results,
    )
    same("Stage 5 result absent", resolution["stage5_result"], None, results)
    same("Stage 5 candidate absent", Path("/candidate").exists(), False, results)

    expected_files = source_manifest["files"]
    same(
        "producer exporter hash",
        digest(PRODUCERS / "klean_export.py"),
        expected_files["klean_export.py"],
        results,
    )
    same(
        "producer klean.py hash",
        digest(PRODUCERS / "klean.py"),
        expected_files["klean.py"],
        results,
    )
    same(
        "generator exporter hash",
        generator_manifest["exporter_sha256"],
        expected_files["klean_export.py"],
        results,
    )
    same(
        "generator klean.py hash",
        generator_manifest["klean_py_sha256"],
        expected_files["klean.py"],
        results,
    )
    image_id = source_manifest["generator_image_id"]
    same(
        "generator image provenance",
        generator_manifest["provenance"]["generator_image_id"],
        image_id,
        results,
    )
    same(
        "launcher producer bundle image key",
        Path(resolution["generation_producer_sources"]).name,
        image_id.removeprefix("sha256:"),
        results,
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "check_count": len(results),
                "results": results,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
