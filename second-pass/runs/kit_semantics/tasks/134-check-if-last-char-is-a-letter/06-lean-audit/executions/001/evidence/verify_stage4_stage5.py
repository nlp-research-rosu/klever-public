#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path


def load_producer():
    path = Path("/reference/generation-tools/klean_export.py")
    spec = importlib.util.spec_from_file_location(
        "generation_time_klean_export", path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


producer = load_producer()
generation = Path("/reference/klean-generation")
generated = generation / "generated"
fresh = Path("/tmp/audit-work/stage5-review")
fresh_base = fresh / "Base"
audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
trust_inventory_path = generation / "trust-inventory.json"
trust_inventory = json.loads(trust_inventory_path.read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

independently_reclassified_domain_ids = [
    "rule-e0a5c8a793196820ea84731c2d229d364f6fe3e8c376c15bf12d3d2cfb1f31a4",
    "rule-61ffc6cd69c6bad2d2ff37db34f5511581d591c5239127275c27ebf328e89030",
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
source_rule_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]

actual_target = producer.target_statement(generated)
fresh_target = producer.target_statement(fresh_base)
expected_definition = producer.expected_target_definition(obligation_map)
actual_lemma_text = (
    generated
    / "Klean134CheckIfLastCharIsALetter"
    / "Lemmas.lean"
).read_text()
definition_match = re.search(
    r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
    actual_lemma_text,
)
actual_definition = (
    definition_match.group(0).strip()
    if definition_match is not None
    else None
)

candidate_sources = [
    path
    for path in fresh.rglob("*.lean")
    if fresh_base not in path.parents
]
candidate_text = "\n".join(path.read_text() for path in candidate_sources)
forbidden_matches = {
    token: [
        f"{path.relative_to(fresh)}:{line_number}"
        for path in candidate_sources
        for line_number, line in enumerate(path.read_text().splitlines(), 1)
        if re.search(rf"\b{token}\b", line)
    ]
    for token in ("sorry", "admit", "unsafe", "axiom", "opaque")
}

candidate_target_definitions = [
    f"{path.relative_to(fresh)}:{line_number}"
    for path in candidate_sources
    for line_number, line in enumerate(path.read_text().splitlines(), 1)
    if re.search(r"^\s*def\s+targetStatement\b", line)
]

conjunct_hashes = [
    {
        "source_rule_id": obligation["source_rule_id"],
        "recorded": obligation["lean_conjunct_sha256"],
        "recomputed": producer.sha256_text(obligation["lean_conjunct"]),
        "matches": obligation["lean_conjunct_sha256"]
        == producer.sha256_text(obligation["lean_conjunct"]),
        "source_span": obligation["source_span"],
        "lean_conjunct": obligation["lean_conjunct"],
    }
    for obligation in obligation_map["obligations"]
]

binding_hashes = []
for parameter in obligation_map["trust_parameters"]:
    binding = {
        key: parameter[key]
        for key in ("kore_symbol", "name", "type", "source_rule_ids")
    }
    recomputed = producer.sha256_text(
        json.dumps(binding, sort_keys=True, separators=(",", ":"))
    )
    binding_hashes.append(
        {
            "name": parameter["name"],
            "recorded": parameter["binding_sha256"],
            "recomputed": recomputed,
            "matches": recomputed == parameter["binding_sha256"],
        }
    )

result = {
    "independently_reclassified_domain_ids": (
        independently_reclassified_domain_ids
    ),
    "obligation_ids": obligation_ids,
    "source_rule_ids": source_rule_ids,
    "exact_domain_source_obligation_bijection_and_order": (
        independently_reclassified_domain_ids
        == source_rule_ids
        == obligation_ids
        and len(obligation_ids) == len(set(obligation_ids))
    ),
    "conjunct_hashes": conjunct_hashes,
    "binding_hashes": binding_hashes,
    "obligation_map_sha256": {
        "recomputed": sha256_file(obligation_map_path),
        "generator_manifest": generator_manifest[
            "obligation_map_sha256"
        ],
        "matches": sha256_file(obligation_map_path)
        == generator_manifest["obligation_map_sha256"],
    },
    "trust_inventory_sha256": {
        "recomputed": sha256_file(trust_inventory_path),
        "export_result": export_result["trust_inventory_sha256"],
        "matches": sha256_file(trust_inventory_path)
        == export_result["trust_inventory_sha256"],
    },
    "target_from_generation_time_producer": actual_target,
    "target_in_fresh_base": fresh_target,
    "target_manifest": generator_manifest["target"],
    "target_audit_input": resolution["target"],
    "target_identity_matches_everywhere": (
        actual_target
        == fresh_target
        == generator_manifest["target"]
        == resolution["target"]
    ),
    "expected_target_definition": expected_definition,
    "actual_target_definition": actual_definition,
    "actual_definition_is_exact_conjunction": (
        actual_definition == expected_definition
    ),
    "fresh_base_tree_sha256": producer.tree_digest(fresh_base),
    "reference_generated_tree_sha256": producer.tree_digest(generated),
    "fresh_base_unchanged": (
        producer.tree_digest(fresh_base)
        == producer.tree_digest(generated)
        == generator_manifest["generated_tree_sha256"]
    ),
    "candidate_sources": [
        str(path.relative_to(fresh)) for path in candidate_sources
    ],
    "candidate_forbidden_token_matches": forbidden_matches,
    "candidate_has_no_forbidden_tokens": all(
        not matches for matches in forbidden_matches.values()
    ),
    "candidate_target_definitions": candidate_target_definitions,
    "candidate_does_not_shadow_target": not candidate_target_definitions,
    "candidate_final_statement_occurrences": len(
        re.findall(
            re.escape(generator_manifest["target"]["statement"]),
            candidate_text,
        )
    ),
    "trust_allowlist_count": len(trust_inventory["allowlist"]),
}

print(json.dumps(result, indent=2, sort_keys=True))
