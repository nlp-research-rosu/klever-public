#!/usr/bin/env python3
"""Independent mounted-input, Stage 4 bijection, and target integrity checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.klean_audit_contract import verify_stage6_audit_input


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, condition: bool, details: object = None) -> None:
    record = {"check": name, "pass": bool(condition)}
    if details is not None:
        record["details"] = details
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    if not condition:
        raise SystemExit(1)


audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
resolution, verified_input_hash = verify_stage6_audit_input(audit)
check(
    "audit-input canonical self hash",
    verified_input_hash == audit["resolved_input_sha256"],
    verified_input_hash,
)

hashes = resolution["hashes"]
mounted_artifact_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": sha256(Path("/reference/lemma-discovery.json")),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(Path("/candidate")),
}
for key, observed in mounted_artifact_hashes.items():
    check(f"audit-input mounted hash: {key}", observed == hashes[key], observed)

stage1_observed_files = {
    path.relative_to("/reference/k-proof").as_posix(): sha256(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
stage1_expected_files = resolution["stage1_source_hashes"]
check(
    "all Stage 1 per-file hashes and names",
    stage1_observed_files == stage1_expected_files,
    {
        "observed_count": len(stage1_observed_files),
        "expected_count": len(stage1_expected_files),
        "missing": sorted(set(stage1_expected_files) - set(stage1_observed_files)),
        "extra": sorted(set(stage1_observed_files) - set(stage1_expected_files)),
        "mismatched": sorted(
            name
            for name in set(stage1_observed_files) & set(stage1_expected_files)
            if stage1_observed_files[name] != stage1_expected_files[name]
        ),
    },
)

generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
source_manifest = json.loads((producer / "source-manifest.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())

producer_hashes = {
    "klean_export.py": sha256(producer / "klean_export.py"),
    "klean.py": sha256(producer / "klean.py"),
}
check("producer hashes match source manifest", producer_hashes == source_manifest["files"], producer_hashes)
check(
    "producer hashes match generator manifest",
    producer_hashes
    == {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    },
)
image_id = generator_manifest["provenance"]["generator_image_id"]
recorded_bundle_id = Path(resolution["generation_producer_sources"]).name
check(
    "immutable generator image identity",
    image_id == source_manifest["generator_image_id"]
    and image_id == f"sha256:{recorded_bundle_id}",
    {
        "generator_manifest": image_id,
        "source_manifest": source_manifest["generator_image_id"],
        "audit_input_bundle": recorded_bundle_id,
    },
)

check(
    "Stage 4 input hashes",
    input_manifest["stage1_workspace_sha256"] == hashes["stage1_export_sha256"]
    and input_manifest["frozen_input_sha256"] == hashes["stage1_export_sha256"]
    and input_manifest["stage3_discovery_manifest_sha256"]
    == hashes["discovery_manifest_sha256"]
    and generator_manifest["provenance"]["stage1_workspace_sha256"]
    == hashes["stage1_export_sha256"]
    and generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == hashes["discovery_manifest_sha256"]
    and export_result["frozen_input_sha256"] == hashes["stage1_export_sha256"]
    and export_result["stage3_discovery_manifest_sha256"]
    == hashes["discovery_manifest_sha256"],
)
check(
    "generated tree hash in all records",
    generator_manifest["generated_tree_sha256"] == hashes["generated_tree_sha256"]
    and export_result["generated_tree_sha256"] == hashes["generated_tree_sha256"]
    and resolution["stage4_preflight"]["generated_tree_sha256"]
    == hashes["generated_tree_sha256"],
)
check(
    "obligation map byte hash",
    generator_manifest["obligation_map_sha256"]
    == sha256(generated / "obligation-map.json"),
    sha256(generated / "obligation-map.json"),
)
check(
    "trust inventory byte hash",
    export_result["trust_inventory_sha256"]
    == sha256(generation / "trust-inventory.json"),
    sha256(generation / "trust-inventory.json"),
)

inventory = inventory_verification(Path("/reference/k-proof"))
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
classification = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}
domain_rules = [
    entry
    for entry in inventory["rules"]
    if classification[entry["source_rule_id"]]["classification"] == "DOMAIN_LEMMA"
]
domain_ids = [entry["source_rule_id"] for entry in domain_rules]
obligation_ids = [entry["source_rule_id"] for entry in obligation_map["obligations"]]
mapped_source_ids = [entry["source_rule_id"] for entry in obligation_map["source_rules"]]
check(
    "exact domain-rule/source-rule/obligation bijection and order",
    domain_ids == mapped_source_ids == obligation_ids
    and len(domain_ids) == len(set(domain_ids)),
    {"domain_ids": domain_ids, "mapped_source_ids": mapped_source_ids, "obligation_ids": obligation_ids},
)
for source, mapped, obligation in zip(
    domain_rules, obligation_map["source_rules"], obligation_map["obligations"], strict=True
):
    discovery_entry = classification[source["source_rule_id"]]
    expected_mapped = dict(source)
    expected_mapped.update(
        {
            "classification": discovery_entry["classification"],
            "rationale": discovery_entry["rationale"],
            "inventory_sha256": inventory["inventory_sha256"],
            "discovery_manifest_sha256": hashes["discovery_manifest_sha256"],
        }
    )
    check(f"full mapped source identity: {source['source_rule_id']}", mapped == expected_mapped)
    check(
        f"obligation provenance/hash: {source['source_rule_id']}",
        obligation["normalized_sha256"] == source["normalized_sha256"]
        and obligation["source_span"]
        == {"start_line": source["start_line"], "end_line": source["end_line"]}
        and obligation["inventory_sha256"] == inventory["inventory_sha256"]
        and obligation["discovery_manifest_sha256"] == hashes["discovery_manifest_sha256"]
        and obligation["lean_conjunct_sha256"]
        == klean_export.sha256_text(obligation["lean_conjunct"]),
    )

expected_definition = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(generated)
check("three nonempty, non-True obligations", len(domain_ids) == 3 and all(
    entry["lean_conjunct"].strip() not in {"True", "(True)"}
    for entry in obligation_map["obligations"]
))
check(
    "fixed target definition is exact obligation conjunction",
    expected_definition is not None
    and observed_target["definition_sha256"]
    == klean_export.sha256_text(expected_definition),
    {"expected_definition": expected_definition, "observed_target": observed_target},
)
check("target matches generator manifest", observed_target == generator_manifest["target"])
check("target matches audit input", observed_target == resolution["target"])
check("target matches recorded Stage 4 preflight", observed_target == resolution["stage4_preflight"]["target"])
check(
    "target statement text hash",
    observed_target["statement_sha256"]
    == klean_export.sha256_text(observed_target["statement"]),
)

print("RESULT: ALL_MOUNTED_HASH_BIJECTION_TARGET_CHECKS_PASS")
