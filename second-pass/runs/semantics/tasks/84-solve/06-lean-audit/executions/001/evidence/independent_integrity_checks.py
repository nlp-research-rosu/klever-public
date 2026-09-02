#!/usr/bin/env python3
"""Read-only independent integrity checks for the Stage 3-5 audit inputs."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/reference")

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")
LOCK = Path("/reference/klean-toolchain.lock.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(document: object) -> str:
    encoded = json.dumps(
        document, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def require(label: str, observed: object, expected: object) -> None:
    status = "PASS" if observed == expected else "FAIL"
    print(f"{status} {label}")
    if isinstance(observed, (dict, list)) or isinstance(expected, (dict, list)):
        observed_length = len(observed) if hasattr(observed, "__len__") else "n/a"
        expected_length = len(expected) if hasattr(expected, "__len__") else "n/a"
        print(
            "  observed summary: "
            f"type={type(observed).__name__} length={observed_length} "
            f"canonical_sha256={canonical_sha256(observed)}"
        )
        print(
            "  expected summary: "
            f"type={type(expected).__name__} length={expected_length} "
            f"canonical_sha256={canonical_sha256(expected)}"
        )
    elif isinstance(observed, str) and isinstance(expected, str) and (
        len(observed) > 160 or len(expected) > 160
    ):
        print(
            "  observed summary: "
            f"length={len(observed)} sha256={hashlib.sha256(observed.encode()).hexdigest()}"
        )
        print(
            "  expected summary: "
            f"length={len(expected)} sha256={hashlib.sha256(expected.encode()).hexdigest()}"
        )
    else:
        print(f"  observed: {observed}")
        print(f"  expected: {expected}")
    if status == "FAIL":
        raise SystemExit(1)


def main() -> None:
    envelope = json.loads(AUDIT_INPUT.read_text())
    resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
        envelope
    )
    print("PASS audit-input envelope")
    print(f"  resolved_input_sha256: {resolved_digest}")
    require(
        "launcher mode",
        resolution["mode"],
        "CLASSIFICATION_AND_PROOF",
    )
    require(
        "semantics mode",
        resolution["semantics_mode"],
        "SUPPLIED_SEMANTICS",
    )

    audit_hashes = resolution["hashes"]
    require(
        "Stage 1 pipeline tree",
        pipeline_contract.sha256_tree(WORKSPACE),
        audit_hashes["k_workspace_sha256"],
    )
    require(
        "Stage 1 export tree",
        klean_export.tree_digest(WORKSPACE),
        audit_hashes["stage1_export_sha256"],
    )
    observed_source_hashes = {
        path.relative_to(WORKSPACE).as_posix(): sha256_file(path)
        for path in sorted(WORKSPACE.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }
    require(
        "Stage 1 complete per-file hash map",
        observed_source_hashes,
        resolution["stage1_source_hashes"],
    )
    require(
        "Stage 3 discovery file",
        sha256_file(DISCOVERY),
        audit_hashes["discovery_manifest_sha256"],
    )
    require(
        "Stage 4 pipeline tree",
        pipeline_contract.sha256_tree(GENERATION),
        audit_hashes["klean_generation_sha256"],
    )
    require(
        "generated Lean tree",
        klean_export.tree_digest(GENERATED),
        audit_hashes["generated_tree_sha256"],
    )
    require(
        "Stage 5 candidate tree",
        pipeline_contract.sha256_tree(CANDIDATE),
        audit_hashes["lean_workspace_sha256"],
    )

    generator = json.loads((GENERATION / "generator-manifest.json").read_text())
    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    require(
        "producer bundle pipeline tree",
        pipeline_contract.sha256_tree(PRODUCERS),
        audit_hashes["generation_producer_sources_sha256"],
    )
    require(
        "producer source file set",
        sorted(
            path.relative_to(PRODUCERS).as_posix()
            for path in PRODUCERS.rglob("*")
            if path.is_file() and not path.is_symlink()
        ),
        ["klean.py", "klean_export.py", "source-manifest.json"],
    )
    expected_producer_files = {
        "klean.py": generator["klean_py_sha256"],
        "klean_export.py": generator["exporter_sha256"],
    }
    require(
        "producer source manifest file bindings",
        source_manifest["files"],
        expected_producer_files,
    )
    for name, expected in expected_producer_files.items():
        require(f"producer file {name}", sha256_file(PRODUCERS / name), expected)
    image_id = generator["provenance"]["generator_image_id"]
    require(
        "producer source manifest image",
        source_manifest["generator_image_id"],
        image_id,
    )
    require(
        "launcher producer path image key",
        Path(resolution["generation_producer_sources"]).name,
        image_id.removeprefix("sha256:"),
    )

    inventory = inventory_verification(WORKSPACE)
    discovery = json.loads(DISCOVERY.read_text())
    require(
        "inventory hash",
        inventory["inventory_sha256"],
        discovery["inventory_sha256"],
    )
    canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
    discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    require("ordered Stage 3 rule identities", discovery_ids, canonical_ids)
    require("Stage 3 identity uniqueness", len(set(discovery_ids)), len(discovery_ids))
    for rule in inventory["rules"]:
        require(
            f"{rule['source_rule_id']} ID/hash binding",
            rule["source_rule_id"],
            f"rule-{rule['normalized_sha256']}",
        )
        normalized = " ".join(rule["text"].split())
        require(
            f"{rule['source_rule_id']} normalized source hash",
            hashlib.sha256(normalized.encode()).hexdigest(),
            rule["normalized_sha256"],
        )
        lines = (WORKSPACE / "verification.k").read_text().splitlines()
        source_span = "\n".join(
            lines[rule["start_line"] - 1 : rule["end_line"]]
        )
        require(
            f"{rule['source_rule_id']} source span",
            source_span.strip(),
            rule["text"].strip(),
        )
    require(
        "whole inventory canonical hash",
        canonical_sha256(inventory["rules"]),
        inventory["inventory_sha256"],
    )

    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
    independent_domain_ids = [
        "rule-a85038e1ac209993c7ddd60086463b961c8ffbd45be861486d9c8442d108f370"
    ]
    input_ids = [
        entry["source_rule_id"] for entry in input_manifest["source_rules"]
    ]
    map_source_ids = [
        entry["source_rule_id"] for entry in obligation_map["source_rules"]
    ]
    obligation_ids = [
        entry["source_rule_id"] for entry in obligation_map["obligations"]
    ]
    require("independent domain set to Stage 4 input", input_ids, independent_domain_ids)
    require("Stage 4 source-rule map", map_source_ids, independent_domain_ids)
    require("Stage 4 obligation identities", obligation_ids, independent_domain_ids)
    require(
        "Stage 4 obligation uniqueness",
        len(set(obligation_ids)),
        len(obligation_ids),
    )
    require(
        "Stage 4 obligation count",
        generator["obligation_count"],
        len(independent_domain_ids),
    )
    require(
        "obligation-map file hash",
        sha256_file(GENERATED / "obligation-map.json"),
        generator["obligation_map_sha256"],
    )
    for obligation in obligation_map["obligations"]:
        require(
            "obligation conjunct hash",
            hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest(),
            obligation["lean_conjunct_sha256"],
        )
        require(
            "obligation provenance inventory hash",
            obligation["inventory_sha256"],
            inventory["inventory_sha256"],
        )
        require(
            "obligation provenance discovery hash",
            obligation["discovery_manifest_sha256"],
            sha256_file(DISCOVERY),
        )
    require("target parameter set", obligation_map["trust_parameters"], [])

    target = klean_export.target_statement(GENERATED)
    require("target manifest", target, generator["target"])
    require("launcher target", target, resolution["target"])
    require("launcher preflight target", target, resolution["stage4_preflight"]["target"])
    expected_definition = klean_export.expected_target_definition(obligation_map)
    lemmas = (GENERATED / target["file"]).read_text()
    definitions = re.findall(
        r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
        lemmas,
    )
    require("single generated target definition", len(definitions), 1)
    actual_definition = definitions[0].strip()
    require("fixed target exact conjunction", actual_definition, expected_definition)
    require(
        "fixed target definition hash",
        hashlib.sha256(actual_definition.encode()).hexdigest(),
        target["definition_sha256"],
    )
    require(
        "fixed target statement hash",
        hashlib.sha256(target["statement"].encode()).hexdigest(),
        target["statement_sha256"],
    )
    require("generator toolchain lock", generator["toolchain"], json.loads(LOCK.read_text()))

    print("ALL INDEPENDENT INTEGRITY CHECKS PASSED")


if __name__ == "__main__":
    main()
