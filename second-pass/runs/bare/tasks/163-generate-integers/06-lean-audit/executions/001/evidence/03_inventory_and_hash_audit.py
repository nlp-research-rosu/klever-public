#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract
from tools import stage6_resolution_contract
from tools.k_rule_inventory import inventory_verification


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> dict[str, object]:
    return {
        "label": label,
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }


audit_input_path = Path("/audit-input.json")
k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_bundle = Path("/reference/generation-tools")
source_manifest_path = producer_bundle / "source-manifest.json"
toolchain_lock_path = Path("/reference/klean-toolchain.lock.json")

audit_input = json.loads(audit_input_path.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_input
)
recorded_hashes = resolution["hashes"]
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
source_manifest = json.loads(source_manifest_path.read_text())
discovery = json.loads(discovery_path.read_text())

hash_checks: list[dict[str, object]] = []
hash_checks.append(
    check(
        "resolved_input_sha256",
        resolved_digest,
        audit_input["resolved_input_sha256"],
    )
)
hash_checks.append(
    check(
        "AUDIT_MODE",
        os.environ.get("AUDIT_MODE"),
        resolution["mode"],
    )
)
hash_checks.append(
    check(
        "k_workspace_sha256 (pipeline tree)",
        pipeline_contract.sha256_tree(k_workspace),
        recorded_hashes["k_workspace_sha256"],
    )
)
hash_checks.append(
    check(
        "stage1_export_sha256 (export tree)",
        klean_export.tree_digest(k_workspace),
        recorded_hashes["stage1_export_sha256"],
    )
)
hash_checks.append(
    check(
        "discovery_manifest_sha256",
        sha256_file(discovery_path),
        recorded_hashes["discovery_manifest_sha256"],
    )
)
hash_checks.append(
    check(
        "k_audit_sha256 (pipeline tree)",
        pipeline_contract.sha256_tree(k_audit),
        recorded_hashes["k_audit_sha256"],
    )
)
hash_checks.append(
    check(
        "klean_generation_sha256 (pipeline tree)",
        pipeline_contract.sha256_tree(generation),
        recorded_hashes["klean_generation_sha256"],
    )
)
hash_checks.append(
    check(
        "generation_producer_sources_sha256 (pipeline tree)",
        pipeline_contract.sha256_tree(producer_bundle),
        recorded_hashes["generation_producer_sources_sha256"],
    )
)
hash_checks.append(
    check(
        "generated_tree_sha256 (export tree)",
        klean_export.tree_digest(generated),
        recorded_hashes["generated_tree_sha256"],
    )
)

for relative, expected in resolution["stage1_source_hashes"].items():
    hash_checks.append(
        check(
            f"stage1_source_hashes[{relative}]",
            sha256_file(k_workspace / relative),
            expected,
        )
    )

for relative, expected in source_manifest["files"].items():
    hash_checks.append(
        check(
            f"producer source {relative}",
            sha256_file(producer_bundle / relative),
            expected,
        )
    )

hash_checks.extend(
    [
        check(
            "producer klean_export.py against generator-manifest",
            sha256_file(producer_bundle / "klean_export.py"),
            generator_manifest["exporter_sha256"],
        ),
        check(
            "producer klean.py against generator-manifest",
            sha256_file(producer_bundle / "klean.py"),
            generator_manifest["klean_py_sha256"],
        ),
        check(
            "generator image: source manifest vs generator manifest",
            source_manifest["generator_image_id"],
            generator_manifest["provenance"]["generator_image_id"],
        ),
        check(
            "generator image: audit-input producer path vs generator manifest",
            "sha256:"
            + Path(resolution["generation_producer_sources"]).name,
            generator_manifest["provenance"]["generator_image_id"],
        ),
        check(
            "generator toolchain vs trusted lock",
            generator_manifest["toolchain"],
            json.loads(toolchain_lock_path.read_text()),
        ),
        check(
            "generator generated_tree_sha256",
            generator_manifest["generated_tree_sha256"],
            recorded_hashes["generated_tree_sha256"],
        ),
        check(
            "generator Stage 1 provenance",
            generator_manifest["provenance"]["stage1_workspace_sha256"],
            recorded_hashes["stage1_export_sha256"],
        ),
        check(
            "generator Stage 3 provenance",
            generator_manifest["provenance"][
                "stage3_discovery_manifest_sha256"
            ],
            recorded_hashes["discovery_manifest_sha256"],
        ),
        check(
            "input manifest frozen_input_sha256",
            input_manifest["frozen_input_sha256"],
            recorded_hashes["stage1_export_sha256"],
        ),
        check(
            "input manifest stage1_workspace_sha256",
            input_manifest["stage1_workspace_sha256"],
            recorded_hashes["stage1_export_sha256"],
        ),
        check(
            "input manifest Stage 3 digest",
            input_manifest["stage3_discovery_manifest_sha256"],
            recorded_hashes["discovery_manifest_sha256"],
        ),
        check(
            "selected K audit artifact digest",
            resolution["selections"]["k_audit"]["artifact_sha256"],
            recorded_hashes["k_audit_sha256"],
        ),
        check(
            "selected Klean generation artifact digest",
            resolution["selections"]["klean_generation"][
                "artifact_sha256"
            ],
            recorded_hashes["klean_generation_sha256"],
        ),
    ]
)

inventory = inventory_verification(k_workspace)
validated = lemma_discovery_contract.validate_trust_boundary(
    k_workspace, discovery_path
)
verification_lines = (
    (k_workspace / "verification.k").read_text().splitlines()
)

reconstructed_rules: list[dict[str, object]] = []
for position, rule in enumerate(inventory["rules"]):
    source_slice = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(source_slice.split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_rule_id = "rule-" + normalized_sha256
    reconstructed_rules.append(
        {
            "position": position,
            "module": rule["module"],
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
            "source_slice": source_slice,
            "inventory_text": rule["text"],
            "text_match": source_slice == rule["text"],
            "normalized_sha256": normalized_sha256,
            "recorded_normalized_sha256": rule["normalized_sha256"],
            "normalized_hash_match": (
                normalized_sha256 == rule["normalized_sha256"]
            ),
            "source_rule_id": source_rule_id,
            "recorded_source_rule_id": rule["source_rule_id"],
            "source_rule_id_match": source_rule_id
            == rule["source_rule_id"],
            "attributes": rule["attributes"],
        }
    )

independent_inventory_sha256 = hashlib.sha256(
    json.dumps(
        inventory["rules"],
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
).hexdigest()
inventory_checks = {
    "verification_file": inventory["verification_file"],
    "verification_sha256": inventory["verification_sha256"],
    "verification_module": inventory["verification_module"],
    "verification_modules": inventory["verification_modules"],
    "rule_count": len(inventory["rules"]),
    "unique_inventory_ids": len(
        {rule["source_rule_id"] for rule in inventory["rules"]}
    )
    == len(inventory["rules"]),
    "unique_manifest_ids": len(
        {rule["source_rule_id"] for rule in discovery["rules"]}
    )
    == len(discovery["rules"]),
    "inventory_ids": [
        rule["source_rule_id"] for rule in inventory["rules"]
    ],
    "manifest_ids": [
        rule["source_rule_id"] for rule in discovery["rules"]
    ],
    "exact_order_match": [
        rule["source_rule_id"] for rule in inventory["rules"]
    ]
    == [rule["source_rule_id"] for rule in discovery["rules"]],
    "exact_id_set_match": {
        rule["source_rule_id"] for rule in inventory["rules"]
    }
    == {rule["source_rule_id"] for rule in discovery["rules"]},
    "independent_inventory_sha256": independent_inventory_sha256,
    "trusted_inventory_sha256": inventory["inventory_sha256"],
    "manifest_inventory_sha256": discovery["inventory_sha256"],
    "inventory_hash_match": independent_inventory_sha256
    == inventory["inventory_sha256"]
    == discovery["inventory_sha256"],
    "contract_definition_count": len(validated["definitions"]),
    "contract_operational_rule_count": len(
        validated["operational_rules"]
    ),
    "contract_proved_derived_lemma_count": len(
        validated["proved_derived_lemmas"]
    ),
    "contract_domain_lemma_count": len(validated["domain_lemmas"]),
}

candidate = Path("/candidate")
candidate_state = {
    "exists": candidate.exists(),
    "is_dir": candidate.is_dir(),
}

result = {
    "hash_checks": hash_checks,
    "all_hash_checks_match": all(item["match"] for item in hash_checks),
    "inventory_checks": inventory_checks,
    "reconstructed_rules": reconstructed_rules,
    "manifest_classifications_in_order": discovery["rules"],
    "candidate_state": candidate_state,
}
print(json.dumps(result, indent=2, sort_keys=True))

if not result["all_hash_checks_match"]:
    raise SystemExit("one or more recorded hash checks failed")
if not all(
    (
        inventory_checks["unique_inventory_ids"],
        inventory_checks["unique_manifest_ids"],
        inventory_checks["exact_order_match"],
        inventory_checks["exact_id_set_match"],
        inventory_checks["inventory_hash_match"],
    )
):
    raise SystemExit("inventory bijection/order/hash audit failed")
if not all(
    rule["text_match"]
    and rule["normalized_hash_match"]
    and rule["source_rule_id_match"]
    for rule in reconstructed_rules
):
    raise SystemExit("rule reconstruction failed")
if resolution["mode"] == "CLASSIFICATION_ONLY" and candidate.exists():
    raise SystemExit("candidate exists in CLASSIFICATION_ONLY mode")
