#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import k_rule_inventory
from tools import klean_export
from tools import pipeline_contract


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_digest(value: object) -> str:
    return digest(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
    )


def check(name: str, condition: bool, actual: object = None) -> None:
    print(
        json.dumps(
            {"check": name, "pass": bool(condition), "actual": actual},
            sort_keys=True,
        )
    )
    if not condition:
        raise AssertionError(name)


workspace = Path("/reference/k-proof")
verification_path = workspace / "verification.k"
verification_text = verification_path.read_text()
verification_lines = verification_text.splitlines()
canonical = k_rule_inventory.inventory_verification(workspace)
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())

manual_spans = ((10, 10), (12, 12), (13, 13), (14, 15))
manual_rules = []
for start, end in manual_spans:
    text = "\n".join(verification_lines[start - 1 : end])
    normalized_sha256 = digest(" ".join(text.split()).encode())
    manual_rules.append(
        {
            "source_rule_id": f"rule-{normalized_sha256}",
            "module": "VERIFICATION",
            "start_line": start,
            "end_line": end,
            "normalized_sha256": normalized_sha256,
            "attributes": [],
            "text": text,
        }
    )

check("manual rule documents equal trusted inventory", manual_rules == canonical["rules"])
check(
    "manual whole inventory hash",
    canonical_digest(manual_rules) == canonical["inventory_sha256"],
    canonical_digest(manual_rules),
)

canonical_ids = [entry["source_rule_id"] for entry in canonical["rules"]]
discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
check("discovery identity order is canonical", discovery_ids == canonical_ids, discovery_ids)
check("canonical identities are unique", len(canonical_ids) == len(set(canonical_ids)))
check("discovery identities are unique", len(discovery_ids) == len(set(discovery_ids)))
check("no omitted or extra discovery identities", set(discovery_ids) == set(canonical_ids))
check(
    "discovery inventory hash matches reconstruction",
    discovery["inventory_sha256"] == canonical["inventory_sha256"],
    discovery["inventory_sha256"],
)

independent_classification = {
    canonical_ids[0]: "DEFINITION",
    canonical_ids[1]: "DEFINITION",
    canonical_ids[2]: "DEFINITION",
    canonical_ids[3]: "DEFINITION",
}
discovery_classification = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
discovery_by_id = {
    entry["source_rule_id"]: entry for entry in discovery["rules"]
}
check(
    "independent classifications match Stage 3",
    discovery_classification == independent_classification,
    discovery_classification,
)
check(
    "every simplification is definition or domain lemma",
    all(
        "simplification" not in rule["attributes"]
        or independent_classification[rule["source_rule_id"]]
        in {"DEFINITION", "DOMAIN_LEMMA"}
        for rule in canonical["rules"]
    ),
)
independent_domain_ids = [
    source_rule_id
    for source_rule_id in canonical_ids
    if independent_classification[source_rule_id] == "DOMAIN_LEMMA"
]
check("independent true domain set is empty", independent_domain_ids == [])

audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
recorded_preflight = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)
obligation_map_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
obligation_map = json.loads(obligation_map_path.read_text())
generated = Path("/reference/klean-generation/generated")
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
trust_inventory_path = Path(
    "/reference/klean-generation/trust-inventory.json"
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

stage1_tree_hash = klean_export.tree_digest(workspace)
discovery_hash = digest(Path("/reference/lemma-discovery.json").read_bytes())
generated_tree_hash = klean_export.tree_digest(generated)
verification_hash = digest(verification_path.read_bytes())
expected_definitions = [
    {
        **rule,
        "classification": discovery_by_id[rule["source_rule_id"]][
            "classification"
        ],
        "rationale": discovery_by_id[rule["source_rule_id"]]["rationale"],
    }
    for rule in canonical["rules"]
]

check("Stage 4 input schema", input_manifest["schema_version"] == 3)
check("Stage 4 generator schema", generator_manifest["schema_version"] == 3)
check("Stage 4 export-result schema", export_result["schema_version"] == 3)
check("Stage 4 obligation-map schema", obligation_map["schema_version"] == 3)
check("Stage 4 input definitions exact", input_manifest["definitions"] == expected_definitions)
check("Stage 4 input operational rules empty", input_manifest["operational_rules"] == [])
check(
    "Stage 4 input proved-derived rules empty",
    input_manifest["proved_derived_lemmas"] == [],
)
check(
    "Stage 4 input inventory hash exact",
    input_manifest["inventory_sha256"] == canonical["inventory_sha256"],
    input_manifest["inventory_sha256"],
)
check(
    "Stage 4 input verification hash exact",
    input_manifest["verification_sha256"] == verification_hash,
    verification_hash,
)
check(
    "Stage 4 input frozen hash exact",
    input_manifest["frozen_input_sha256"] == stage1_tree_hash,
    stage1_tree_hash,
)
check(
    "Stage 4 input workspace hash exact",
    input_manifest["stage1_workspace_sha256"] == stage1_tree_hash,
    stage1_tree_hash,
)
check(
    "Stage 4 input discovery hash exact",
    input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash,
    discovery_hash,
)
check("generator toolchain exact", generator_manifest["toolchain"] == toolchain_lock)
check(
    "generator tree hash exact",
    generator_manifest["generated_tree_sha256"] == generated_tree_hash,
    generated_tree_hash,
)
check(
    "generator Stage 1 provenance exact",
    generator_manifest["provenance"]["stage1_workspace_sha256"]
    == stage1_tree_hash,
)
check(
    "generator Stage 3 provenance exact",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == discovery_hash,
)
check(
    "generator inventory provenance exact",
    generator_manifest["provenance"]["inventory_sha256"]
    == canonical["inventory_sha256"],
)
check(
    "export generated tree hash exact",
    export_result["generated_tree_sha256"] == generated_tree_hash,
)
check(
    "export frozen tree hash exact",
    export_result["frozen_input_sha256"] == stage1_tree_hash,
)
check(
    "export discovery hash exact",
    export_result["stage3_discovery_manifest_sha256"] == discovery_hash,
)
check(
    "export trust-inventory hash exact",
    export_result["trust_inventory_sha256"]
    == digest(trust_inventory_path.read_bytes()),
    digest(trust_inventory_path.read_bytes()),
)
check(
    "recorded preflight frozen hash exact",
    recorded_preflight["frozen_input_sha256"] == stage1_tree_hash,
)
check(
    "recorded preflight workspace hash exact",
    recorded_preflight["stage1_workspace_sha256"] == stage1_tree_hash,
)
check(
    "recorded preflight discovery hash exact",
    recorded_preflight["stage3_discovery_manifest_sha256"]
    == discovery_hash,
)
check(
    "recorded preflight generated hash exact",
    recorded_preflight["generated_tree_sha256"] == generated_tree_hash,
)
check(
    "launcher preflight frozen hash exact",
    resolution["stage4_preflight"]["frozen_input_sha256"]
    == stage1_tree_hash,
)
check(
    "launcher preflight workspace hash exact",
    resolution["stage4_preflight"]["stage1_workspace_sha256"]
    == stage1_tree_hash,
)
check(
    "launcher preflight discovery hash exact",
    resolution["stage4_preflight"]["stage3_discovery_manifest_sha256"]
    == discovery_hash,
)
check(
    "launcher preflight generated hash exact",
    resolution["stage4_preflight"]["generated_tree_sha256"]
    == generated_tree_hash,
)

producer_hashes = {
    name: digest((Path("/reference/generation-tools") / name).read_bytes())
    for name in ("klean_export.py", "klean.py")
}
expected_producer_hashes = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
check("producer hashes equal generator manifest", producer_hashes == expected_producer_hashes)
check("producer hashes equal source manifest", producer_hashes == source_manifest["files"])
check(
    "producer image IDs agree",
    source_manifest["generator_image_id"]
    == generator_manifest["provenance"]["generator_image_id"],
    source_manifest["generator_image_id"],
)
check(
    "audit-input producer path binds image ID",
    Path(resolution["generation_producer_sources"]).name
    == source_manifest["generator_image_id"].removeprefix("sha256:"),
    Path(resolution["generation_producer_sources"]).name,
)
check(
    "audit-input producer tree hash exact",
    pipeline_contract.sha256_tree(Path("/reference/generation-tools"))
    == resolution["hashes"]["generation_producer_sources_sha256"],
    pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
)

check("Stage 4 input source_rules empty", input_manifest["source_rules"] == [])
check("obligation map source_rules empty", obligation_map["source_rules"] == [])
check("obligation map obligations empty", obligation_map["obligations"] == [])
check("obligation map trust parameters empty", obligation_map["trust_parameters"] == [])
check("generator obligation count zero", generator_manifest["obligation_count"] == 0)
check(
    "obligation map hash fixed",
    digest(obligation_map_path.read_bytes())
    == generator_manifest["obligation_map_sha256"],
    digest(obligation_map_path.read_bytes()),
)

lean_text = "\n".join(
    path.read_text() for path in sorted(generated.rglob("*.lean"))
)
raw_targets = re.findall(r"(?m)^\s*def\s+targetStatement\b", lean_text)
check("no raw generated target declaration", len(raw_targets) == 0)
check("trusted target parser returns none", klean_export.target_statement(generated) is None)
check("generator manifest target null", generator_manifest["target"] is None)
check("audit input target null", resolution["target"] is None)
check("recorded preflight target null", recorded_preflight["target"] is None)
check("launcher Stage 4 preflight target null", resolution["stage4_preflight"]["target"] is None)

check(
    "selected Stage 4 status KLEAN_NO_OBLIGATIONS",
    resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
)
check("export status KLEAN_NO_OBLIGATIONS", export_result["status"] == "KLEAN_NO_OBLIGATIONS")
check(
    "recorded preflight status KLEAN_NO_OBLIGATIONS",
    recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS",
)
check(
    "launcher preflight status KLEAN_NO_OBLIGATIONS",
    resolution["stage4_preflight"]["status"] == "KLEAN_NO_OBLIGATIONS",
)

check("launcher mode classification only", resolution["mode"] == "CLASSIFICATION_ONLY")
check("launcher Lean invocation absent", resolution["lean_invocation"] is None)
check("launcher Lean workspace absent", resolution["lean_workspace"] is None)
check("launcher Lean invocation hash absent", resolution["hashes"]["lean_invocation_sha256"] is None)
check("launcher Lean workspace hash absent", resolution["hashes"]["lean_workspace_sha256"] is None)
check("launcher Stage 5 result absent", resolution["stage5_result"] is None)
check("candidate mount absent", not Path("/candidate").exists())

check(
    "resolved-input canonical hash",
    canonical_digest(resolution) == audit_input["resolved_input_sha256"],
    canonical_digest(resolution),
)

print("INDEPENDENT_CLASSIFICATION")
for rule in canonical["rules"]:
    print(
        json.dumps(
            {
                "source_rule_id": rule["source_rule_id"],
                "source_span": [rule["start_line"], rule["end_line"]],
                "normalized_sha256": rule["normalized_sha256"],
                "classification": independent_classification[
                    rule["source_rule_id"]
                ],
                "text": rule["text"],
            },
            sort_keys=True,
        )
    )
