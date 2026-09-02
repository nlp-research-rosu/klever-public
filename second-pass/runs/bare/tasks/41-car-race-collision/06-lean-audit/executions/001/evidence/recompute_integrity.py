#!/usr/bin/env python3
"""Independent read-only recomputation of frozen audit identities."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> dict[str, object]:
    return {
        "label": label,
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }


audit_input_path = Path("/audit-input.json")
audit_input = json.loads(audit_input_path.read_text())
resolution = audit_input["resolution"]
hashes = resolution["hashes"]
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

verified_resolution, verified_digest = (
    stage6_resolution_contract.verify_audit_input(audit_input)
)
inventory = k_rule_inventory.inventory_verification(
    Path("/reference/k-proof")
)
validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)

producer_image_id = generator_manifest["provenance"]["generator_image_id"]
producer_path_key = Path(
    resolution["generation_producer_sources"]
).name
producer_expected_files = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}

checks = [
    check(
        "audit input canonical resolved-input hash",
        verified_digest,
        audit_input["resolved_input_sha256"],
    ),
    check(
        "audit input verified resolution",
        verified_resolution,
        resolution,
    ),
    check(
        "producer source manifest exact file map",
        source_manifest["files"],
        producer_expected_files,
    ),
    check(
        "producer image ID: source manifest vs generator manifest",
        source_manifest["generator_image_id"],
        producer_image_id,
    ),
    check(
        "producer image ID: launcher path key vs generator manifest",
        f"sha256:{producer_path_key}",
        producer_image_id,
    ),
    check(
        "producer klean_export.py hash",
        file_sha256(Path("/reference/generation-tools/klean_export.py")),
        generator_manifest["exporter_sha256"],
    ),
    check(
        "producer klean.py hash",
        file_sha256(Path("/reference/generation-tools/klean.py")),
        generator_manifest["klean_py_sha256"],
    ),
    check(
        "producer bundle tree hash",
        pipeline_contract.sha256_tree(
            Path("/reference/generation-tools")
        ),
        hashes["generation_producer_sources_sha256"],
    ),
    check(
        "Stage 1 pipeline tree hash",
        pipeline_contract.sha256_tree(Path("/reference/k-proof")),
        hashes["k_workspace_sha256"],
    ),
    check(
        "Stage 1 deterministic-export tree hash",
        klean_export.tree_digest(Path("/reference/k-proof")),
        hashes["stage1_export_sha256"],
    ),
    check(
        "Stage 2 selected audit tree hash",
        pipeline_contract.sha256_tree(Path("/reference/k-audit")),
        hashes["k_audit_sha256"],
    ),
    check(
        "Stage 3 manifest byte hash",
        file_sha256(Path("/reference/lemma-discovery.json")),
        hashes["discovery_manifest_sha256"],
    ),
    check(
        "Stage 4 generation tree hash",
        pipeline_contract.sha256_tree(
            Path("/reference/klean-generation")
        ),
        hashes["klean_generation_sha256"],
    ),
    check(
        "generated project deterministic tree hash",
        klean_export.tree_digest(
            Path("/reference/klean-generation/generated")
        ),
        hashes["generated_tree_sha256"],
    ),
    check(
        "generated project hash vs generator manifest",
        klean_export.tree_digest(
            Path("/reference/klean-generation/generated")
        ),
        generator_manifest["generated_tree_sha256"],
    ),
    check(
        "canonical inventory hash vs Stage 3",
        inventory["inventory_sha256"],
        json.loads(
            Path("/reference/lemma-discovery.json").read_text()
        )["inventory_sha256"],
    ),
    check(
        "canonical inventory ordered source IDs vs Stage 3",
        [rule["source_rule_id"] for rule in inventory["rules"]],
        [
            rule["source_rule_id"]
            for rule in json.loads(
                Path("/reference/lemma-discovery.json").read_text()
            )["rules"]
        ],
    ),
]

for relative, expected in resolution["stage1_source_hashes"].items():
    checks.append(
        check(
            f"Stage 1 source hash: {relative}",
            file_sha256(Path("/reference/k-proof") / relative),
            expected,
        )
    )

document = {
    "all_checks_match": all(item["match"] for item in checks),
    "checks": checks,
    "inventory": inventory,
    "validated_classification_counts": {
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(
            validated["proved_derived_lemmas"]
        ),
        "domain_lemmas": len(validated["domain_lemmas"]),
    },
}
print(json.dumps(document, indent=2, sort_keys=True))
