#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


ROOT = Path("/reference")
WORKSPACE = ROOT / "k-proof"
DISCOVERY_PATH = ROOT / "lemma-discovery.json"
GENERATION = ROOT / "klean-generation"
PRODUCERS = ROOT / "generation-tools"
AUDIT_INPUT_PATH = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


audit_input = json.loads(AUDIT_INPUT_PATH.read_text())
resolution = audit_input["resolution"]
discovery = json.loads(DISCOVERY_PATH.read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads(
    (GENERATION / "generator-manifest.json").read_text()
)

producer_hashes = {
    name: sha256_file(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
recorded_producer_hashes = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
require(
    producer_hashes == recorded_producer_hashes,
    "producer hashes differ from generator-manifest.json",
)
require(
    source_manifest["files"] == producer_hashes,
    "producer hashes differ from source-manifest.json",
)
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
require(
    source_manifest["generator_image_id"] == generator_image_id,
    "generator image differs between source and generator manifests",
)
require(
    Path(resolution["generation_producer_sources"]).name
    == generator_image_id.removeprefix("sha256:"),
    "audit-input producer path does not bind the recorded generator image",
)
producer_tree_sha256 = pipeline_contract.sha256_tree(PRODUCERS)
require(
    producer_tree_sha256
    == resolution["hashes"]["generation_producer_sources_sha256"],
    "producer bundle tree hash differs from audit-input.json",
)

inventory = inventory_verification(WORKSPACE)
validated = lemma_discovery_contract.validate_trust_boundary(
    WORKSPACE, DISCOVERY_PATH
)
inventory_rules = inventory["rules"]
discovery_rules = discovery["rules"]
inventory_ids = [entry["source_rule_id"] for entry in inventory_rules]
discovery_ids = [entry["source_rule_id"] for entry in discovery_rules]
require(
    inventory_ids == discovery_ids,
    "discovery identities are omitted, added, or reordered",
)
require(
    len(inventory_ids) == len(set(inventory_ids)),
    "canonical inventory contains duplicate identities",
)
require(
    len(discovery_ids) == len(set(discovery_ids)),
    "discovery manifest contains duplicate identities",
)
require(
    inventory["inventory_sha256"] == discovery["inventory_sha256"],
    "whole inventory hash differs from discovery manifest",
)
require(
    canonical_json_sha256(inventory_rules) == inventory["inventory_sha256"],
    "whole inventory hash does not recompute",
)

verification_text = (WORKSPACE / "verification.k").read_text()
verification_lines = verification_text.splitlines()
rule_reconstruction = []
for rule in inventory_rules:
    normalized = " ".join(rule["text"].split())
    normalized_sha256 = hashlib.sha256(normalized.encode()).hexdigest()
    source_rule_id = f"rule-{normalized_sha256}"
    start = rule["start_line"]
    end = rule["end_line"]
    source_span_text = "\n".join(verification_lines[start - 1 : end])
    require(
        source_span_text == rule["text"],
        f"source span text differs for {rule['source_rule_id']}",
    )
    require(
        normalized_sha256 == rule["normalized_sha256"],
        f"normalized hash differs for {rule['source_rule_id']}",
    )
    require(
        source_rule_id == rule["source_rule_id"],
        f"source_rule_id differs for {rule['source_rule_id']}",
    )
    rule_reconstruction.append(
        {
            "module": rule["module"],
            "start_line": start,
            "end_line": end,
            "source_span_text": source_span_text,
            "normalized_text": normalized,
            "normalized_sha256": normalized_sha256,
            "source_rule_id": source_rule_id,
            "attributes": rule["attributes"],
        }
    )

stage1_source_hashes = {
    path.relative_to(WORKSPACE).as_posix(): sha256_file(path)
    for path in sorted(WORKSPACE.rglob("*"))
    if path.is_file() and not path.is_symlink()
}
require(
    stage1_source_hashes == resolution["stage1_source_hashes"],
    "Stage 1 per-file hashes differ from audit-input.json",
)
pipeline_stage1_tree_sha256 = pipeline_contract.sha256_tree(WORKSPACE)
export_stage1_tree_sha256 = klean_export.tree_digest(WORKSPACE)
require(
    pipeline_stage1_tree_sha256 == resolution["hashes"]["k_workspace_sha256"],
    "Stage 1 pipeline tree hash differs from audit-input.json",
)
require(
    export_stage1_tree_sha256 == resolution["hashes"]["stage1_export_sha256"],
    "Stage 1 export tree hash differs from audit-input.json",
)
require(
    sha256_file(DISCOVERY_PATH)
    == resolution["hashes"]["discovery_manifest_sha256"],
    "Stage 3 manifest hash differs from audit-input.json",
)
require(
    pipeline_contract.sha256_tree(GENERATION)
    == resolution["hashes"]["klean_generation_sha256"],
    "Stage 4 generation tree hash differs from audit-input.json",
)
require(
    klean_export.tree_digest(GENERATION / "generated")
    == resolution["hashes"]["generated_tree_sha256"],
    "generated project tree hash differs from audit-input.json",
)

report = {
    "status": "PASS",
    "producer_provenance": {
        "producer_hashes": producer_hashes,
        "producer_tree_sha256": producer_tree_sha256,
        "generator_image_id": generator_image_id,
        "source_manifest_matches": True,
        "generator_manifest_matches": True,
        "audit_input_matches": True,
    },
    "inventory": inventory,
    "rule_reconstruction": rule_reconstruction,
    "discovery_ordered_bijection": {
        "inventory_ids": inventory_ids,
        "discovery_ids": discovery_ids,
        "unique": True,
        "whole_inventory_hash_matches": True,
        "validated_categories": {
            "definitions": [
                entry["source_rule_id"] for entry in validated["definitions"]
            ],
            "operational_rules": [
                entry["source_rule_id"]
                for entry in validated["operational_rules"]
            ],
            "proved_derived_lemmas": [
                entry["source_rule_id"]
                for entry in validated["proved_derived_lemmas"]
            ],
            "domain_lemmas": [
                entry["source_rule_id"]
                for entry in validated["domain_lemmas"]
            ],
        },
    },
    "frozen_hashes": {
        "stage1_source_hashes": stage1_source_hashes,
        "pipeline_stage1_tree_sha256": pipeline_stage1_tree_sha256,
        "export_stage1_tree_sha256": export_stage1_tree_sha256,
        "discovery_manifest_sha256": sha256_file(DISCOVERY_PATH),
        "generation_tree_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generated_tree_sha256": klean_export.tree_digest(
            GENERATION / "generated"
        ),
    },
}
print(json.dumps(report, indent=2, sort_keys=True))
