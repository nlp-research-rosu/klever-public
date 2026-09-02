#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.klean_export import (
    expected_target_definition,
    sha256_text,
    target_statement,
    tree_digest,
)
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_tree


def read_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(label: str, condition: bool, checks: list[dict]) -> None:
    checks.append({"check": label, "pass": bool(condition)})
    if not condition:
        raise AssertionError(label)


def main() -> None:
    audit = read_json("/audit-input.json")
    resolution = audit["resolution"]
    generator = read_json("/reference/klean-generation/generator-manifest.json")
    source_manifest = read_json("/reference/generation-tools/source-manifest.json")
    input_manifest = read_json("/reference/klean-generation/input-manifest.json")
    obligation_map = read_json(
        "/reference/klean-generation/generated/obligation-map.json"
    )
    recorded_preflight = read_json("/reference/klean-generation/preflight.json")
    rerun_preflight = read_json("/audit-output/evidence/preflight-rerun.json")
    discovery = read_json("/reference/lemma-discovery.json")
    lock = read_json("/reference/klean-toolchain.lock.json")
    inventory = inventory_verification(Path("/reference/k-proof"))
    validated = validate_trust_boundary(
        Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
    )
    actual_target = target_statement(
        Path("/reference/klean-generation/generated")
    )
    checks: list[dict] = []

    require(
        "launcher mode agrees with AUDIT_MODE",
        resolution["mode"] == os.environ["AUDIT_MODE"]
        == "CLASSIFICATION_AND_PROOF",
        checks,
    )
    require(
        "semantics mode is SUPPLIED_SEMANTICS",
        resolution["semantics_mode"] == "SUPPLIED_SEMANTICS",
        checks,
    )

    image_id = generator["provenance"]["generator_image_id"]
    producer_hashes = {
        "klean_export.py": file_sha256(
            "/reference/generation-tools/klean_export.py"
        ),
        "klean.py": file_sha256("/reference/generation-tools/klean.py"),
    }
    require(
        "producer file hashes equal source manifest",
        producer_hashes == source_manifest["files"],
        checks,
    )
    require(
        "producer file hashes equal generator manifest",
        producer_hashes["klean_export.py"] == generator["exporter_sha256"]
        and producer_hashes["klean.py"] == generator["klean_py_sha256"],
        checks,
    )
    require(
        "producer image ID is identical in both manifests",
        source_manifest["generator_image_id"] == image_id,
        checks,
    )
    require(
        "launcher producer path is bound to image ID",
        Path(resolution["generation_producer_sources"]).name
        == image_id.removeprefix("sha256:"),
        checks,
    )
    require(
        "launcher producer tree hash matches mounted bundle",
        sha256_tree(Path("/reference/generation-tools"))
        == resolution["hashes"]["generation_producer_sources_sha256"],
        checks,
    )

    require(
        "verification source hash matches launcher",
        file_sha256("/reference/k-proof/verification.k")
        == resolution["stage1_source_hashes"]["verification.k"],
        checks,
    )
    require(
        "canonical inventory hash matches discovery",
        inventory["inventory_sha256"] == discovery["inventory_sha256"],
        checks,
    )
    canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
    discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    require(
        "discovery identities are a unique exact ordered bijection",
        discovery_ids == canonical_ids
        and len(discovery_ids) == len(set(discovery_ids)),
        checks,
    )
    require(
        "canonical source_rule_id is normalized hash",
        all(
            entry["source_rule_id"]
            == "rule-" + entry["normalized_sha256"]
            for entry in inventory["rules"]
        ),
        checks,
    )
    require(
        "verification-module closure is local and exact",
        inventory["verification_modules"] == ["DIGITS-VERIFICATION"],
        checks,
    )

    classified = {
        entry["source_rule_id"]: entry["classification"]
        for entry in discovery["rules"]
    }
    expected_classes = ["DEFINITION"] * 5 + ["DOMAIN_LEMMA"] * 3
    require(
        "classification sequence is five definitions then three domain lemmas",
        [classified[source_id] for source_id in canonical_ids]
        == expected_classes,
        checks,
    )
    require(
        "all simplification rules are domain lemmas",
        all(
            classified[entry["source_rule_id"]] == "DOMAIN_LEMMA"
            for entry in inventory["rules"]
            if "simplification" in entry["attributes"]
        ),
        checks,
    )
    domain_rules = validated["domain_lemmas"]
    domain_ids = [entry["source_rule_id"] for entry in domain_rules]
    require(
        "generated source rules equal validated domain rules",
        input_manifest["source_rules"] == obligation_map["source_rules"]
        == [
            {
                **entry,
                "inventory_sha256": inventory["inventory_sha256"],
                "discovery_manifest_sha256": file_sha256(
                    "/reference/lemma-discovery.json"
                ),
            }
            for entry in domain_rules
        ],
        checks,
    )

    obligations = obligation_map["obligations"]
    obligation_ids = [entry["source_rule_id"] for entry in obligations]
    require(
        "obligations are a unique exact ordered domain-rule bijection",
        obligation_ids == domain_ids
        and len(obligation_ids) == len(set(obligation_ids)),
        checks,
    )
    for source, obligation in zip(domain_rules, obligations, strict=True):
        require(
            f"{source['source_rule_id']} span and hashes are exact",
            obligation["source_span"]
            == {
                "start_line": source["start_line"],
                "end_line": source["end_line"],
            }
            and obligation["normalized_sha256"]
            == source["normalized_sha256"]
            and obligation["inventory_sha256"]
            == inventory["inventory_sha256"]
            and obligation["discovery_manifest_sha256"]
            == file_sha256("/reference/lemma-discovery.json")
            and obligation["lean_conjunct_sha256"]
            == sha256_text(obligation["lean_conjunct"]),
            checks,
        )
        conjunct = obligation["lean_conjunct"]
        require(
            f"{source['source_rule_id']} conjunct is guarded and nontrivial",
            conjunct.startswith("∀ ")
            and "(h :" in conjunct
            and "= true)" in conjunct
            and ") = (" in conjunct
            and conjunct.strip() not in {"True", "∀ (_ : False), True"},
            checks,
        )

    expected_definition = expected_target_definition(obligation_map)
    require(
        "actual target is exact generated conjunction",
        actual_target == generator["target"]
        and actual_target["definition_sha256"]
        == sha256_text(expected_definition),
        checks,
    )
    require(
        "target is identical across generator, preflight, rerun, and launcher",
        generator["target"]
        == recorded_preflight["target"]
        == rerun_preflight["target"]
        == resolution["target"],
        checks,
    )
    require(
        "rerun preflight exactly reproduces recorded preflight",
        rerun_preflight == recorded_preflight
        == resolution["stage4_preflight"],
        checks,
    )
    require(
        "generator toolchain equals pinned lock",
        generator["toolchain"] == lock,
        checks,
    )
    require(
        "obligation map file hash and count match generator",
        file_sha256(
            "/reference/klean-generation/generated/obligation-map.json"
        )
        == generator["obligation_map_sha256"]
        and len(obligations) == generator["obligation_count"] == 3,
        checks,
    )

    expected_hashes = resolution["hashes"]
    require(
        "Stage 1 pipeline tree hash matches launcher",
        sha256_tree(Path("/reference/k-proof"))
        == expected_hashes["k_workspace_sha256"],
        checks,
    )
    require(
        "Stage 1 export tree hash matches launcher and manifests",
        tree_digest(Path("/reference/k-proof"))
        == expected_hashes["stage1_export_sha256"]
        == generator["provenance"]["stage1_workspace_sha256"]
        == input_manifest["stage1_workspace_sha256"],
        checks,
    )
    require(
        "discovery file hash matches launcher and manifests",
        file_sha256("/reference/lemma-discovery.json")
        == expected_hashes["discovery_manifest_sha256"]
        == generator["provenance"]["stage3_discovery_manifest_sha256"]
        == input_manifest["stage3_discovery_manifest_sha256"],
        checks,
    )
    require(
        "Stage 2 audit pipeline tree hash matches launcher",
        sha256_tree(Path("/reference/k-audit"))
        == expected_hashes["k_audit_sha256"],
        checks,
    )
    require(
        "Stage 4 generation pipeline tree hash matches launcher",
        sha256_tree(Path("/reference/klean-generation"))
        == expected_hashes["klean_generation_sha256"],
        checks,
    )
    require(
        "generated export tree hash matches launcher and generator",
        tree_digest(Path("/reference/klean-generation/generated"))
        == expected_hashes["generated_tree_sha256"]
        == generator["generated_tree_sha256"],
        checks,
    )
    require(
        "candidate pipeline tree hash matches launcher",
        sha256_tree(Path("/candidate"))
        == expected_hashes["lean_workspace_sha256"],
        checks,
    )

    print(
        json.dumps(
            {
                "status": "PASS",
                "check_count": len(checks),
                "inventory_rule_count": len(canonical_ids),
                "domain_rule_count": len(domain_ids),
                "obligation_count": len(obligations),
                "producer_hashes": producer_hashes,
                "image_id": image_id,
                "inventory_sha256": inventory["inventory_sha256"],
                "target": actual_target,
                "checks": checks,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
