#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
candidate = Path("/candidate")
stage1 = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")

discovery = json.loads(discovery_path.read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

observed_pipeline_hashes = {
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "k_workspace_sha256": pipeline_contract.sha256_tree(stage1),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(candidate),
}
for name, value in observed_pipeline_hashes.items():
    require(value == hashes[name], f"audit-input pipeline hash mismatch: {name}")

stage1_export_hash = klean_export.tree_digest(stage1)
generated_hash = klean_export.tree_digest(generated)
require(
    stage1_export_hash == hashes["stage1_export_sha256"],
    "Stage 1 export-tree hash mismatch",
)
require(
    generated_hash == hashes["generated_tree_sha256"],
    "generated-tree hash mismatch against audit input",
)
require(
    generated_hash == generator_manifest["generated_tree_sha256"],
    "generated-tree hash mismatch against generator manifest",
)
for relative, expected in resolution["stage1_source_hashes"].items():
    require(
        sha256(stage1 / relative) == expected,
        f"frozen Stage 1 source hash mismatch: {relative}",
    )

discovery_hash = sha256(discovery_path)
require(
    discovery_hash == hashes["discovery_manifest_sha256"],
    "discovery hash mismatch",
)
require(
    discovery_hash == input_manifest["stage3_discovery_manifest_sha256"],
    "input-manifest discovery hash mismatch",
)
require(
    discovery_hash
    == generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    "generator-manifest discovery hash mismatch",
)
require(
    sha256(obligation_map_path) == generator_manifest["obligation_map_sha256"],
    "obligation-map byte hash mismatch",
)
require(
    sha256(generation / "trust-inventory.json")
    == export_result["trust_inventory_sha256"],
    "trust-inventory byte hash mismatch",
)

domain_classifications = [
    entry
    for entry in discovery["rules"]
    if entry["classification"] == "DOMAIN_LEMMA"
]
reconstructed_inventory = inventory_verification(stage1)
reconstructed_by_id = {
    entry["source_rule_id"]: entry
    for entry in reconstructed_inventory["rules"]
}
domain_rules = [
    {
        **reconstructed_by_id[entry["source_rule_id"]],
        "classification": entry["classification"],
        "rationale": entry["rationale"],
    }
    for entry in domain_classifications
]
source_rules = obligation_map["source_rules"]
obligations = obligation_map["obligations"]
require(len(domain_rules) == 1, "independent classification expects one domain rule")
require(len(source_rules) == 1, "obligation map must contain one source rule")
require(len(obligations) == 1, "obligation map must contain one obligation")
require(generator_manifest["obligation_count"] == 1, "manifest count mismatch")
require(export_result["obligation_count"] == 1, "export count mismatch")

identity_fields = (
    "source_rule_id",
    "normalized_sha256",
    "module",
    "start_line",
    "end_line",
    "text",
    "classification",
)
for field in identity_fields:
    require(
        source_rules[0][field] == domain_rules[0][field],
        f"domain/source identity mismatch: {field}",
    )
obligation = obligations[0]
source = source_rules[0]
require(
    obligation["source_rule_id"] == source["source_rule_id"],
    "source/obligation rule-id mismatch",
)
require(
    obligation["normalized_sha256"] == source["normalized_sha256"],
    "source/obligation normalized hash mismatch",
)
require(
    obligation["source_span"]
    == {"start_line": source["start_line"], "end_line": source["end_line"]},
    "source/obligation span mismatch",
)
require(
    obligation["inventory_sha256"] == discovery["inventory_sha256"],
    "obligation inventory hash mismatch",
)
require(
    obligation["discovery_manifest_sha256"] == discovery_hash,
    "obligation discovery hash mismatch",
)
require(
    obligation["lean_conjunct_sha256"]
    == sha256_text(obligation["lean_conjunct"]),
    "Lean conjunct hash mismatch",
)
require(
    len({entry["source_rule_id"] for entry in obligations}) == len(obligations),
    "duplicate source obligation",
)

lean_sources = sorted(generated.rglob("*.lean"))
raw_target_count = sum(
    len(re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text()))
    for path in lean_sources
)
matches: list[tuple[Path, str]] = []
for path in lean_sources:
    for match in re.finditer(
        r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
        path.read_text(),
    ):
        matches.append((path, match.group(0).strip()))
require(raw_target_count == 1 and len(matches) == 1, "target is not unique")
target_path, target_definition = matches[0]

parameters = obligation_map["trust_parameters"]
expected_lines = ["def targetStatement"]
for parameter in parameters:
    expected_lines.append(f"    ({parameter['name']} : {parameter['type']})")
expected_lines.extend(
    (
        "    : Prop :=",
        "    " + "\n    ∧ ".join(
            f"({entry['lean_conjunct']})" for entry in obligations
        ),
    )
)
expected_definition = "\n".join(expected_lines)
require(
    target_definition == expected_definition,
    "generated target is not the exact deterministic obligation rendering",
)
declaration = f"{target_path.parent.name}.Lemmas.targetStatement"
statement = " ".join(
    [declaration, *(parameter["name"] for parameter in parameters)]
)
manual_target = {
    "declaration": declaration,
    "file": target_path.relative_to(generated).as_posix(),
    "statement": statement,
    "statement_sha256": sha256_text(statement),
    "definition_sha256": sha256_text(target_definition),
    "parameters": parameters,
}
require(
    manual_target == generator_manifest["target"],
    "manual target reconstruction differs from generator manifest",
)
require(manual_target == resolution["target"], "target differs from audit input")
require(
    manual_target == resolution["stage4_preflight"]["target"],
    "target differs from launcher-recorded preflight",
)

domain_ids = {entry["source_rule_id"] for entry in domain_rules}
for parameter in parameters:
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "source_rule_ids": parameter["source_rule_ids"],
        "type": parameter["type"],
    }
    require(
        parameter["binding_sha256"]
        == sha256_text(json.dumps(binding, sort_keys=True, separators=(",", ":"))),
        f"parameter binding hash mismatch: {parameter['name']}",
    )
    require(
        set(parameter["source_rule_ids"]) == domain_ids,
        f"parameter is not bound exactly to the domain rule: {parameter['name']}",
    )

candidate_sources = sorted(candidate.rglob("*.lean"))
candidate_text = "\n".join(path.read_text() for path in candidate_sources)
for token in ("sorry", "admit", "unsafe", "axiom", "opaque"):
    require(
        re.search(rf"\b{token}\b", candidate_text) is None,
        f"candidate contains forbidden token: {token}",
    )
require(
    re.search(r"(?m)^\s*def\s+targetStatement\b", candidate_text) is None,
    "candidate shadows the generated target",
)
proof_text = (candidate / "Proof.lean").read_text()
for parameter in parameters:
    declarations = re.findall(
        rf"(?m)^\s*(?:noncomputable\s+)?def\s+{re.escape(parameter['name'])}\s*(?::|\()",
        proof_text,
    )
    require(
        len(declarations) == 1,
        f"candidate does not define target parameter exactly once: {parameter['name']}",
    )
final_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b", proof_text
)
require(len(final_matches) == 1, "candidate must define theorem final exactly once")
require(
    " ".join(final_matches[0].split()) == " ".join(statement.split()),
    "Proof.final statement differs from fixed generated target",
)

print("INTEGRITY_CHECK: PASS")
print("pipeline_hashes", json.dumps(observed_pipeline_hashes, sort_keys=True))
print("stage1_export_sha256", stage1_export_hash)
print("generated_tree_sha256", generated_hash)
print("discovery_sha256", discovery_hash)
print("inventory_sha256", discovery["inventory_sha256"])
print("domain_rule_id", source["source_rule_id"])
print("lean_conjunct_sha256", obligation["lean_conjunct_sha256"])
print("target_definition_sha256", manual_target["definition_sha256"])
print("target_statement_sha256", manual_target["statement_sha256"])
print("candidate_forbidden_tokens", "none")
print("candidate_shadow_target", "no")
print("proof_final_identity", "exact")
