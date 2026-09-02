#!/usr/bin/env python3
"""Independent structural checks for the 146-specialFilter audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
PRODUCERS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report(label: str, observed: object, expected: object) -> bool:
    ok = observed == expected
    print(f"{label}: {'PASS' if ok else 'FAIL'}")
    if ok:
        if isinstance(observed, dict):
            print(f"  exact dict match ({len(observed)} entries)")
        elif isinstance(observed, list):
            print(f"  exact list match ({len(observed)} entries)")
        else:
            print(f"  value={observed!r}")
    else:
        print(f"  observed={observed!r}")
        print(f"  expected={expected!r}")
    return ok


def main() -> int:
    failures = 0
    audit_document = json.loads(AUDIT_INPUT.read_text())
    resolution, resolved_hash = stage6_resolution_contract.verify_audit_input(
        audit_document
    )
    failures += not report(
        "audit input canonical resolved_input_sha256",
        resolved_hash,
        audit_document["resolved_input_sha256"],
    )

    inventory = inventory_verification(WORKSPACE)
    discovery = json.loads(DISCOVERY.read_text())
    canonical_rules = inventory["rules"]
    classified_rules = discovery["rules"]
    canonical_ids = [rule["source_rule_id"] for rule in canonical_rules]
    classified_ids = [rule["source_rule_id"] for rule in classified_rules]

    failures += not report(
        "Stage 3 inventory_sha256",
        discovery["inventory_sha256"],
        inventory["inventory_sha256"],
    )
    failures += not report(
        "Stage 3 ordered source_rule_id list",
        classified_ids,
        canonical_ids,
    )
    failures += not report(
        "Stage 3 unique source_rule_id count",
        len(set(classified_ids)),
        len(classified_ids),
    )
    failures += not report(
        "Stage 3 rule count",
        len(classified_rules),
        len(canonical_rules),
    )

    source_lines = (WORKSPACE / "verification.k").read_text().splitlines()
    print("RECONSTRUCTED RULE INVENTORY")
    for index, rule in enumerate(canonical_rules):
        span = "\n".join(
            source_lines[rule["start_line"] - 1 : rule["end_line"]]
        ).rstrip(" \t\r\n")
        normalized = " ".join(span.split())
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        span_ok = span == rule["text"]
        digest_ok = digest == rule["normalized_sha256"]
        identity_ok = rule["source_rule_id"] == f"rule-{digest}"
        if not (span_ok and digest_ok and identity_ok):
            failures += 1
        classification = classified_rules[index]["classification"]
        print(
            f"{index:02d} {rule['module']}:{rule['start_line']}-"
            f"{rule['end_line']} {rule['source_rule_id']} "
            f"class={classification} attrs={rule['attributes']!r} "
            f"span={'PASS' if span_ok else 'FAIL'} "
            f"hash={'PASS' if digest_ok else 'FAIL'} "
            f"identity={'PASS' if identity_ok else 'FAIL'}"
        )
        is_simplification = any(
            attribute == "simplification"
            or attribute.startswith("simplification(")
            for attribute in rule["attributes"]
        )
        if is_simplification and classification not in {
            "DEFINITION",
            "DOMAIN_LEMMA",
        }:
            print("  FAIL: simplification has forbidden classification")
            failures += 1

    hashes = resolution["hashes"]
    recorded_tree_checks = [
        (
            "Stage 1 pipeline tree SHA-256",
            pipeline_contract.sha256_tree(WORKSPACE),
            hashes["k_workspace_sha256"],
        ),
        (
            "Stage 1 export tree SHA-256",
            klean_export.tree_digest(WORKSPACE),
            hashes["stage1_export_sha256"],
        ),
        (
            "Stage 2 selected audit tree SHA-256",
            pipeline_contract.sha256_tree(Path("/reference/k-audit")),
            hashes["k_audit_sha256"],
        ),
        (
            "Stage 3 manifest file SHA-256",
            sha256_file(DISCOVERY),
            hashes["discovery_manifest_sha256"],
        ),
        (
            "Stage 4 selected generation tree SHA-256",
            pipeline_contract.sha256_tree(GENERATION),
            hashes["klean_generation_sha256"],
        ),
        (
            "Stage 4 generated target tree SHA-256",
            klean_export.tree_digest(GENERATION / "generated"),
            hashes["generated_tree_sha256"],
        ),
        (
            "Stage 4 producer source bundle tree SHA-256",
            pipeline_contract.sha256_tree(PRODUCERS),
            hashes["generation_producer_sources_sha256"],
        ),
        (
            "Stage 5 candidate tree SHA-256",
            pipeline_contract.sha256_tree(CANDIDATE),
            hashes["lean_workspace_sha256"],
        ),
    ]
    for label, observed, expected in recorded_tree_checks:
        failures += not report(label, observed, expected)

    observed_stage1_files = {
        path.relative_to(WORKSPACE).as_posix(): sha256_file(path)
        for path in pipeline_contract._walk_regular_files(
            WORKSPACE, "Stage 1 source workspace"
        )
    }
    failures += not report(
        "all Stage 1 recorded per-file hashes",
        observed_stage1_files,
        resolution["stage1_source_hashes"],
    )

    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    source_manifest = json.loads(
        (PRODUCERS / "source-manifest.json").read_text()
    )
    producer_hashes = {
        "klean.py": sha256_file(PRODUCERS / "klean.py"),
        "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
    }
    failures += not report(
        "producer file hashes vs source-manifest",
        producer_hashes,
        source_manifest["files"],
    )
    failures += not report(
        "klean_export.py hash vs generator-manifest",
        producer_hashes["klean_export.py"],
        generator_manifest["exporter_sha256"],
    )
    failures += not report(
        "klean.py hash vs generator-manifest",
        producer_hashes["klean.py"],
        generator_manifest["klean_py_sha256"],
    )
    image_id = generator_manifest["provenance"]["generator_image_id"]
    failures += not report(
        "generator image ID vs source-manifest",
        image_id,
        source_manifest["generator_image_id"],
    )
    audit_image_key = Path(resolution["generation_producer_sources"]).name
    failures += not report(
        "generator image ID vs audit-input producer path",
        image_id.removeprefix("sha256:"),
        audit_image_key,
    )
    failures += not report(
        "producer bundle exact file set",
        sorted(path.name for path in PRODUCERS.iterdir()),
        ["klean.py", "klean_export.py", "source-manifest.json"],
    )

    target_documents = {
        "generator-manifest": generator_manifest.get("target"),
        "preflight": json.loads((GENERATION / "preflight.json").read_text()).get(
            "target"
        ),
        "audit-input": resolution.get("target"),
        "audit-input.stage4_preflight": resolution["stage4_preflight"].get(
            "target"
        ),
    }
    first_target = target_documents["generator-manifest"]
    for label, target in target_documents.items():
        failures += not report(
            f"fixed target identity in {label}", target, first_target
        )

    print(f"TOTAL FAILURES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
