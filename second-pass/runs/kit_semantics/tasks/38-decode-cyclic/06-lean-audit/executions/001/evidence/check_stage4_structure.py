#!/usr/bin/env python3
"""Independent structural and target-identity checks for Stage 4."""

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification


def load(path):
    return json.loads(Path(path).read_text())


stage1 = Path("/reference/k-proof")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
audit = load("/audit-input.json")["resolution"]
discovery = load("/reference/lemma-discovery.json")
inventory = inventory_verification(stage1)
input_manifest = load(generation / "input-manifest.json")
generator_manifest = load(generation / "generator-manifest.json")
obligation_map = load(generated / "obligation-map.json")
export_result = load(generation / "export-result.json")
fresh_preflight = load(
    "/audit-output/evidence/33-klean-check-generation-result.json"
)

expected_definitions = []
for source, classified in zip(inventory["rules"], discovery["rules"]):
    assert source["source_rule_id"] == classified["source_rule_id"]
    expected_definitions.append(
        source
        | {
            "classification": classified["classification"],
            "rationale": classified["rationale"],
        }
    )

checks = {}
checks["all_13_inventory_rules_exported_as_definitions"] = (
    input_manifest.get("definitions") == expected_definitions
)
checks["independently_classified_domain_set_empty"] = all(
    entry["classification"] != "DOMAIN_LEMMA" for entry in expected_definitions
)
checks["no_other_classification_buckets"] = all(
    input_manifest.get(name) == []
    for name in (
        "source_rules",
        "operational_rules",
        "proved_derived_lemmas",
        "lowered_structural_definition_rules",
        "promoted_structural_definitions",
    )
)
checks["source_rule_obligation_bijection_empty"] = obligation_map == {
    "schema_version": 3,
    "source_rules": [],
    "obligations": [],
    "trust_parameters": [],
}
checks["obligation_map_hash"] = generator_manifest.get(
    "obligation_map_sha256"
) == hashlib.sha256((generated / "obligation-map.json").read_bytes()).hexdigest()
checks["manifest_obligation_count_zero"] = (
    generator_manifest.get("obligation_count") == 0
    and export_result.get("obligation_count") == 0
    and fresh_preflight.get("obligation_count") == 0
)
checks["statuses_no_obligations"] = (
    audit["selections"]["klean_generation"]["status"]
    == export_result.get("status")
    == fresh_preflight.get("status")
    == "KLEAN_NO_OBLIGATIONS"
)

expected_target = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(generated)
checks["no_expected_or_observed_target"] = (
    expected_target is None
    and observed_target is None
    and generator_manifest.get("target") is None
    and fresh_preflight.get("target") is None
    and audit.get("target") is None
)
lean_text = "\n".join(
    path.read_text() for path in sorted(generated.rglob("*.lean"))
)
checks["no_final_target_declaration"] = re.search(
    r"(?m)^\s*(?:def|theorem|lemma|opaque|axiom)\s+(?:Proof\.)?final\b",
    lean_text,
) is None
checks["no_vacuous_conjunct_possible"] = obligation_map["obligations"] == []
checks["candidate_absent"] = not Path("/candidate").exists()

expected_summaries = [
    {
        "name": "decodedResult",
        "argument_sorts": ["IntSeq", "IntSeq"],
        "return_sort": "IntSeq",
    },
    {
        "name": "decodedTail",
        "argument_sorts": ["IntSeq"],
        "return_sort": "IntSeq",
    },
    {
        "name": "decodeCodes",
        "argument_sorts": ["IntSeq"],
        "return_sort": "IntSeq",
    },
    {
        "name": "finalLoopChar",
        "argument_sorts": ["IntSeq", "Val"],
        "return_sort": "Val",
    },
]
checks["summary_signature_identity"] = (
    input_manifest.get("summary_functions") == expected_summaries
)

required = input_manifest.get("required_k_files", [])
required_relative = [
    path.removeprefix("/frozen-k/")
    for path in required
    if isinstance(path, str) and path.startswith("/frozen-k/")
]
checks["required_k_files_all_present"] = (
    len(required_relative) == len(required)
    and len(required_relative) == len(set(required_relative))
    and all((stage1 / path).is_file() for path in required_relative)
)

checks["fresh_preflight_matches_launcher_record"] = (
    fresh_preflight == audit["stage4_preflight"]
)
checks["frozen_hash_bindings"] = (
    input_manifest.get("frozen_input_sha256")
    == input_manifest.get("stage1_workspace_sha256")
    == generator_manifest["provenance"]["stage1_workspace_sha256"]
    == export_result["frozen_input_sha256"]
    == fresh_preflight["frozen_input_sha256"]
    == audit["hashes"]["stage1_export_sha256"]
)
checks["discovery_hash_bindings"] = (
    input_manifest.get("stage3_discovery_manifest_sha256")
    == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]
    == export_result["stage3_discovery_manifest_sha256"]
    == fresh_preflight["stage3_discovery_manifest_sha256"]
    == audit["hashes"]["discovery_manifest_sha256"]
)
checks["generated_hash_bindings"] = (
    generator_manifest.get("generated_tree_sha256")
    == export_result["generated_tree_sha256"]
    == fresh_preflight["generated_tree_sha256"]
    == audit["hashes"]["generated_tree_sha256"]
)

for name, value in checks.items():
    print(f"{name}={'PASS' if value else 'FAIL'}")
print(f"definition_count={len(expected_definitions)}")
print(f"domain_lemma_count={len(input_manifest['source_rules'])}")
print(f"obligation_count={len(obligation_map['obligations'])}")
print(f"expected_target={expected_target!r}")
print(f"observed_target={observed_target!r}")
ok = all(checks.values())
print(f"OVERALL={'PASS' if ok else 'FAIL'}")
raise SystemExit(0 if ok else 1)
