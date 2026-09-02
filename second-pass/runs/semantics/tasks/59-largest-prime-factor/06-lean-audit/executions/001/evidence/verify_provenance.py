#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
hashes = audit["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
generated = Path("/reference/klean-generation/generated")

producer_actual = {
    name: file_sha256(Path("/reference/generation-tools") / name)
    for name in ("klean.py", "klean_export.py")
}
source_actual = {
    path.relative_to("/reference/k-proof").as_posix(): file_sha256(path)
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file() and not path.is_symlink()
}
tree_actual = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}
actual_target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
rule_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
domain_ids = [
    rule["source_rule_id"]
    for rule in discovery["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
mapped_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

result = {
    "producer": {
        "actual": producer_actual,
        "source_manifest": source_manifest["files"],
        "generator_manifest": {
            "klean.py": generator["klean_py_sha256"],
            "klean_export.py": generator["exporter_sha256"],
        },
        "hashes_match": (
            producer_actual == source_manifest["files"]
            and producer_actual["klean.py"] == generator["klean_py_sha256"]
            and producer_actual["klean_export.py"]
            == generator["exporter_sha256"]
        ),
        "source_manifest_image_id": source_manifest["generator_image_id"],
        "generator_manifest_image_id": generator["provenance"][
            "generator_image_id"
        ],
        "audit_input_path_image_id": (
            "sha256:"
            + Path(audit["generation_producer_sources"]).name
        ),
        "image_ids_match": (
            source_manifest["generator_image_id"]
            == generator["provenance"]["generator_image_id"]
            == "sha256:"
            + Path(audit["generation_producer_sources"]).name
        ),
    },
    "source_files": {
        "actual": source_actual,
        "recorded": audit["stage1_source_hashes"],
        "exact_match": source_actual == audit["stage1_source_hashes"],
    },
    "tree_hashes": {
        key: {
            "actual": value,
            "recorded": hashes[key],
            "match": value == hashes[key],
        }
        for key, value in tree_actual.items()
    },
    "discovery_manifest": {
        "actual_sha256": file_sha256(
            Path("/reference/lemma-discovery.json")
        ),
        "recorded_sha256": hashes["discovery_manifest_sha256"],
        "match": file_sha256(Path("/reference/lemma-discovery.json"))
        == hashes["discovery_manifest_sha256"],
    },
    "obligation_bijection": {
        "domain_rule_ids": domain_ids,
        "mapped_rule_ids": mapped_ids,
        "unique_domain_ids": len(domain_ids) == len(set(domain_ids)),
        "unique_mapped_ids": len(mapped_ids) == len(set(mapped_ids)),
        "ordered_exact_match": domain_ids == mapped_ids,
        "all_mapped_ids_in_inventory": all(
            source_rule_id in rule_ids for source_rule_id in mapped_ids
        ),
        "source_rules_exactly_domain_rules": [
            rule["source_rule_id"]
            for rule in obligation_map["source_rules"]
        ]
        == domain_ids,
    },
    "target": {
        "actual": actual_target,
        "generator_manifest": generator["target"],
        "audit_input": audit["target"],
        "actual_equals_generator": actual_target == generator["target"],
        "actual_equals_audit_input": actual_target == audit["target"],
        "expected_definition": expected_definition,
        "expected_definition_sha256": (
            klean_export.sha256_text(expected_definition)
            if expected_definition is not None
            else None
        ),
        "expected_definition_matches_manifest": (
            expected_definition is not None
            and klean_export.sha256_text(expected_definition)
            == generator["target"]["definition_sha256"]
        ),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
