#!/usr/bin/env python3
"""Cross-check every Stage 3/4 identity and zero-obligation invariant."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from tools import (
    k_rule_inventory,
    klean_export,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_input = load(Path("/audit-input.json"))
resolution = audit_input["resolution"]
workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")

source_manifest = load(producer / "source-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
input_manifest = load(generation / "input-manifest.json")
obligation_map = load(generated / "obligation-map.json")
export_result = load(generation / "export-result.json")
trust_inventory = load(generation / "trust-inventory.json")
recorded_preflight = load(generation / "preflight.json")

inventory = k_rule_inventory.inventory_verification(workspace)
validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, discovery_path
)

checks: dict[str, object] = {}

checks["resolved_input_envelope"] = {
    "observed": stage6_resolution_contract.canonical_json_sha256(resolution),
    "recorded": audit_input["resolved_input_sha256"],
    "match": (
        stage6_resolution_contract.canonical_json_sha256(resolution)
        == audit_input["resolved_input_sha256"]
    ),
}
checks["audit_mode_env_matches_json"] = (
    os.environ.get("AUDIT_MODE") == resolution["mode"] == "CLASSIFICATION_ONLY"
)
checks["candidate_absent"] = not Path("/candidate").exists()
checks["producer_files_exact"] = sorted(
    path.name for path in producer.iterdir()
) == ["klean.py", "klean_export.py", "source-manifest.json"]
checks["producer_source_hashes"] = {
    name: {
        "observed": sha(producer / name),
        "source_manifest": source_manifest["files"][name],
        "generator_manifest": generator_manifest[
            "exporter_sha256" if name == "klean_export.py" else "klean_py_sha256"
        ],
        "match": (
            sha(producer / name)
            == source_manifest["files"][name]
            == generator_manifest[
                "exporter_sha256"
                if name == "klean_export.py"
                else "klean_py_sha256"
            ]
        ),
    }
    for name in ("klean_export.py", "klean.py")
}
generator_image = generator_manifest["provenance"]["generator_image_id"]
checks["producer_image_identity"] = {
    "generator_manifest": generator_image,
    "source_manifest": source_manifest["generator_image_id"],
    "audit_input_bundle_basename": Path(
        resolution["generation_producer_sources"]
    ).name,
    "match": (
        generator_image == source_manifest["generator_image_id"]
        and generator_image.removeprefix("sha256:")
        == Path(resolution["generation_producer_sources"]).name
    ),
}

tree_hashes = {
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer
    ),
    "k_workspace_sha256": pipeline_contract.sha256_tree(workspace),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "stage1_export_sha256": klean_export.tree_digest(workspace),
}
checks["tree_hashes"] = {
    key: {
        "observed": value,
        "audit_input": resolution["hashes"][key],
        "match": value == resolution["hashes"][key],
    }
    for key, value in tree_hashes.items()
}

stage1_source_checks: dict[str, object] = {}
for relative, expected in resolution["stage1_source_hashes"].items():
    observed = sha(workspace / relative)
    stage1_source_checks[relative] = {
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }
checks["stage1_source_hashes"] = stage1_source_checks

discovery_hash = sha(discovery_path)
checks["discovery_hash"] = {
    "observed": discovery_hash,
    "audit_input": resolution["hashes"]["discovery_manifest_sha256"],
    "generator_provenance": generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ],
    "input_manifest": input_manifest[
        "stage3_discovery_manifest_sha256"
    ],
    "export_result": export_result[
        "stage3_discovery_manifest_sha256"
    ],
}
checks["discovery_hash"]["match"] = len(
    set(checks["discovery_hash"].values())
) == 1

inventory_hash_values = {
    inventory["inventory_sha256"],
    validated["inventory_sha256"],
    input_manifest["inventory_sha256"],
    generator_manifest["provenance"]["inventory_sha256"],
}
checks["inventory_hash_consistent"] = len(inventory_hash_values) == 1
checks["toolchain_lock_exact"] = (
    generator_manifest["toolchain"]
    == load(Path("/reference/klean-toolchain.lock.json"))
)

category_names = (
    "definitions",
    "operational_rules",
    "proved_derived_lemmas",
    "domain_lemmas",
)
checks["input_manifest_categories"] = {
    "definitions_exact": (
        input_manifest["definitions"] == validated["definitions"]
    ),
    "operational_rules_exact": (
        input_manifest["operational_rules"]
        == validated["operational_rules"]
    ),
    "proved_derived_lemmas_exact": (
        input_manifest["proved_derived_lemmas"]
        == validated["proved_derived_lemmas"]
    ),
    "domain_source_rules_exact": (
        input_manifest["source_rules"] == validated["domain_lemmas"]
    ),
}
category_ids = [
    rule["source_rule_id"]
    for category in category_names
    for rule in validated[category]
]
canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
manifest_ids = [
    rule["source_rule_id"]
    for rule in load(discovery_path)["rules"]
]
checks["category_partition"] = {
    "canonical_count": len(canonical_ids),
    "classified_count": len(category_ids),
    "unique": len(category_ids) == len(set(category_ids)),
    "same_set": set(category_ids) == set(canonical_ids),
    "manifest_order_exact": manifest_ids == canonical_ids,
}

actual_obligation_map_hash = sha(generated / "obligation-map.json")
checks["obligation_map_hash"] = {
    "observed": actual_obligation_map_hash,
    "generator_manifest": generator_manifest["obligation_map_sha256"],
    "match": (
        actual_obligation_map_hash
        == generator_manifest["obligation_map_sha256"]
    ),
}
checks["zero_obligation_bijection"] = {
    "independent_domain_rule_count": len(validated["domain_lemmas"]),
    "input_source_rule_count": len(input_manifest["source_rules"]),
    "map_source_rule_count": len(obligation_map["source_rules"]),
    "obligation_count": len(obligation_map["obligations"]),
    "trust_parameter_count": len(obligation_map["trust_parameters"]),
    "generator_manifest_count": generator_manifest["obligation_count"],
    "export_result_count": export_result["obligation_count"],
    "all_empty": (
        validated["domain_lemmas"] == []
        and input_manifest["source_rules"] == []
        and obligation_map["source_rules"] == []
        and obligation_map["obligations"] == []
        and obligation_map["trust_parameters"] == []
        and generator_manifest["obligation_count"] == 0
        and export_result["obligation_count"] == 0
    ),
}
checks["no_vacuous_conjuncts"] = obligation_map["obligations"] == []

expected_target = klean_export.expected_target_definition(obligation_map)
detected_target = klean_export.target_statement(generated)
lemmas_text = (generated / "Klean84Solve" / "Lemmas.lean").read_text()
checks["fixed_generated_target"] = {
    "expected_definition": expected_target,
    "detected_target": detected_target,
    "generator_manifest": generator_manifest["target"],
    "audit_input": resolution["target"],
    "audit_input_preflight": resolution["stage4_preflight"]["target"],
    "recorded_preflight": recorded_preflight["target"],
    "lemmas_declarations": re.findall(
        r"(?m)^\\s*(?:def|theorem|lemma|axiom|opaque)\\s+([^\\s:(]+)",
        lemmas_text,
    ),
    "all_absent": (
        expected_target is None
        and detected_target is None
        and generator_manifest["target"] is None
        and resolution["target"] is None
        and resolution["stage4_preflight"]["target"] is None
        and recorded_preflight["target"] is None
        and not re.search(
            r"(?m)^\\s*(?:def|theorem|lemma|axiom|opaque)\\s+",
            lemmas_text,
        )
    ),
}

status_values = {
    resolution["selections"]["klean_generation"]["status"],
    resolution["stage4_preflight"]["status"],
    recorded_preflight["status"],
    export_result["status"],
}
checks["status_consistent"] = (
    status_values == {"KLEAN_NO_OBLIGATIONS"}
)
checks["trust_inventory_hash"] = {
    "observed": sha(generation / "trust-inventory.json"),
    "export_result": export_result["trust_inventory_sha256"],
    "match": (
        sha(generation / "trust-inventory.json")
        == export_result["trust_inventory_sha256"]
    ),
}
checks["recorded_preflight_matches_audit_input"] = (
    recorded_preflight == resolution["stage4_preflight"]
)
checks["proof_mode_fields_null"] = (
    resolution["hashes"]["lean_invocation_sha256"] is None
    and resolution["hashes"]["lean_workspace_sha256"] is None
    and resolution["stage5_result"] is None
    and resolution["lean_invocation"] is None
    and resolution["lean_workspace"] is None
)


def all_true(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, dict):
        if "match" in value and isinstance(value["match"], bool):
            return value["match"] and all(
                all_true(item)
                for key, item in value.items()
                if key not in {
                    "observed",
                    "expected",
                    "audit_input",
                    "source_manifest",
                    "generator_manifest",
                    "input_manifest",
                    "export_result",
                    "generator_provenance",
                    "expected_definition",
                    "detected_target",
                    "audit_input_preflight",
                    "recorded_preflight",
                    "lemmas_declarations",
                    "audit_input_bundle_basename",
                }
            )
        return all(all_true(item) for item in value.values())
    if isinstance(value, list):
        return all(all_true(item) for item in value)
    return True


checks["ALL_BOOLEAN_CHECKS_PASS"] = all_true(checks)
print(json.dumps(checks, indent=2, sort_keys=True))
