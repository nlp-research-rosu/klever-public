#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract
from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def check(label: str, condition: bool, detail: object = "") -> None:
    if not condition:
        raise AssertionError(f"{label}: {detail}")
    print(f"PASS {label}: {detail}")


audit_document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
hashes = resolution["hashes"]
check(
    "audit-input canonical digest",
    resolved_digest == audit_document["resolved_input_sha256"],
    resolved_digest,
)

pipeline_trees = {
    "k_workspace_sha256": Path("/reference/k-proof"),
    "k_audit_sha256": Path("/reference/k-audit"),
    "klean_generation_sha256": Path("/reference/klean-generation"),
    "lean_workspace_sha256": Path("/candidate"),
}
for field, path in pipeline_trees.items():
    observed = pipeline_contract.sha256_tree(path)
    check(field, observed == hashes[field], observed)

stage1_export = klean_export.tree_digest(Path("/reference/k-proof"))
check(
    "stage1_export_sha256",
    stage1_export == hashes["stage1_export_sha256"],
    stage1_export,
)
generated_tree = klean_export.tree_digest(
    Path("/reference/klean-generation/generated")
)
check(
    "generated_tree_sha256",
    generated_tree == hashes["generated_tree_sha256"],
    generated_tree,
)
discovery_hash = sha256_file(Path("/reference/lemma-discovery.json"))
check(
    "discovery_manifest_sha256",
    discovery_hash == hashes["discovery_manifest_sha256"],
    discovery_hash,
)

stage1_files = {
    path.relative_to("/reference/k-proof").as_posix(): sha256_file(path)
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file() and not path.is_symlink()
}
check(
    "stage1 source file set and hashes",
    stage1_files == resolution["stage1_source_hashes"],
    json.dumps(stage1_files, sort_keys=True),
)

inventory = inventory_verification(Path("/reference/k-proof"))
verification_text = Path("/reference/k-proof/verification.k").read_text()
verification_lines = verification_text.splitlines()
for index, rule in enumerate(inventory["rules"]):
    source_slice = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized = " ".join(rule["text"].split())
    normalized_hash = sha256_bytes(normalized.encode())
    check(
        f"inventory rule {index} exact source span",
        source_slice == rule["text"],
        f'{rule["start_line"]}-{rule["end_line"]}',
    )
    check(
        f"inventory rule {index} normalized hash",
        normalized_hash == rule["normalized_sha256"],
        normalized_hash,
    )
    check(
        f"inventory rule {index} source_rule_id",
        rule["source_rule_id"] == f"rule-{normalized_hash}",
        rule["source_rule_id"],
    )
check(
    "whole inventory canonical hash",
    canonical_json_sha256(inventory["rules"]) == inventory["inventory_sha256"],
    inventory["inventory_sha256"],
)

discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
check(
    "Stage 3 ordered identity bijection",
    discovery_ids == inventory_ids
    and len(discovery_ids) == len(set(discovery_ids)),
    discovery_ids,
)
check(
    "Stage 3 inventory hash",
    discovery["inventory_sha256"] == inventory["inventory_sha256"],
    discovery["inventory_sha256"],
)
check(
    "Stage 3 classifications",
    [entry["classification"] for entry in discovery["rules"]]
    == ["DOMAIN_LEMMA", "DOMAIN_LEMMA", "DOMAIN_LEMMA"],
    [entry["classification"] for entry in discovery["rules"]],
)

generation = Path("/reference/klean-generation")
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
obligation_map = json.loads(
    (generation / "generated/obligation-map.json").read_text()
)
trust_inventory = json.loads((generation / "trust-inventory.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)

verification_hash = sha256_file(Path("/reference/k-proof/verification.k"))
check(
    "input verification hash",
    input_manifest["verification_sha256"]
    == inventory["verification_sha256"]
    == verification_hash,
    verification_hash,
)
check(
    "input frozen Stage 1 hashes",
    input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == stage1_export,
    stage1_export,
)
check(
    "input Stage 3 hash",
    input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash,
    discovery_hash,
)
check(
    "input inventory hash",
    input_manifest["inventory_sha256"] == inventory["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "generator provenance hashes",
    generator_manifest["provenance"]["stage1_workspace_sha256"]
    == stage1_export
    and generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ]
    == discovery_hash
    and generator_manifest["provenance"]["inventory_sha256"]
    == inventory["inventory_sha256"],
    generator_manifest["provenance"],
)
check(
    "generator pinned toolchain",
    generator_manifest["toolchain"] == toolchain_lock,
    generator_manifest["toolchain"]["lean_toolchain"],
)

source_rules = obligation_map["source_rules"]
source_ids = [rule["source_rule_id"] for rule in source_rules]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligation_map["obligations"]
]
check(
    "Stage 4 source-rule/obligation ordered bijection",
    source_ids == inventory_ids
    and obligation_ids == inventory_ids
    and len(obligation_ids) == len(set(obligation_ids)),
    obligation_ids,
)
check(
    "Stage 4 input source rules",
    input_manifest["source_rules"] == source_rules,
    len(source_rules),
)
for index, (rule, obligation) in enumerate(
    zip(source_rules, obligation_map["obligations"], strict=True)
):
    check(
        f"obligation {index} source span",
        obligation["source_span"]
        == {
            "start_line": rule["start_line"],
            "end_line": rule["end_line"],
        },
        obligation["source_span"],
    )
    for field in (
        "source_rule_id",
        "normalized_sha256",
        "inventory_sha256",
        "discovery_manifest_sha256",
    ):
        check(
            f"obligation {index} {field}",
            obligation[field] == rule[field],
            obligation[field],
        )
    conjunct_hash = sha256_bytes(obligation["lean_conjunct"].encode())
    check(
        f"obligation {index} conjunct hash",
        conjunct_hash == obligation["lean_conjunct_sha256"],
        conjunct_hash,
    )

obligation_map_hash = sha256_file(generation / "generated/obligation-map.json")
check(
    "obligation-map hash",
    obligation_map_hash == generator_manifest["obligation_map_sha256"],
    obligation_map_hash,
)
check(
    "generator obligation count",
    generator_manifest["obligation_count"]
    == len(obligation_map["obligations"])
    == 3,
    generator_manifest["obligation_count"],
)
check(
    "generator generated-tree hash",
    generator_manifest["generated_tree_sha256"] == generated_tree,
    generated_tree,
)
trust_inventory_hash = sha256_file(generation / "trust-inventory.json")
check(
    "export result frozen-input hash",
    export_result["frozen_input_sha256"] == stage1_export,
    export_result["frozen_input_sha256"],
)
check(
    "export result Stage 3 hash",
    export_result["stage3_discovery_manifest_sha256"] == discovery_hash,
    export_result["stage3_discovery_manifest_sha256"],
)
check(
    "export result generated-tree hash",
    export_result["generated_tree_sha256"] == generated_tree,
    export_result["generated_tree_sha256"],
)
check(
    "export result trust-inventory hash",
    export_result["trust_inventory_sha256"] == trust_inventory_hash,
    trust_inventory_hash,
)
check(
    "export result obligation count/status",
    export_result["obligation_count"] == 3
    and export_result["status"] == "OK",
    (export_result["status"], export_result["obligation_count"]),
)

for index, parameter in enumerate(obligation_map["trust_parameters"]):
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "type": parameter["type"],
        "source_rule_ids": parameter["source_rule_ids"],
    }
    binding_hash = sha256_bytes(
        json.dumps(binding, sort_keys=True, separators=(",", ":")).encode()
    )
    check(
        f"target parameter {index} binding hash",
        binding_hash == parameter["binding_sha256"],
        binding_hash,
    )

lemmas_path = generation / "generated/Klean38DecodeCyclic/Lemmas.lean"
lemmas_text = lemmas_path.read_text()
definitions = re.findall(
    r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
    lemmas_text,
)
check("single generated target", len(definitions) == 1, len(definitions))
target_definition = definitions[0].strip()
expected_definition = klean_export.expected_target_definition(obligation_map)
check(
    "generated target exact deterministic definition",
    target_definition == expected_definition,
    sha256_bytes(target_definition.encode()),
)
target = klean_export.target_statement(generation / "generated")
check(
    "generator target object",
    target == generator_manifest["target"],
    target["statement_sha256"],
)
check(
    "audit-input target object",
    target == resolution["target"]
    and target == resolution["stage4_preflight"]["target"],
    target["definition_sha256"],
)

proof_text = Path("/candidate/Proof.lean").read_text()
proof_type = re.search(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b", proof_text
)
check("candidate has exactly typed Proof.final", proof_type is not None)
check(
    "Proof.final exact fixed statement",
    " ".join(proof_type.group(1).split()) == target["statement"],
    " ".join(proof_type.group(1).split()),
)
check(
    "candidate does not define or shadow targetStatement",
    re.search(r"(?m)^\s*def\s+targetStatement\b", proof_text) is None,
)
for token in ("sorry", "admit", "unsafe", "axiom", "opaque"):
    check(
        f"candidate forbidden token {token}",
        re.search(rf"\b{token}\b", proof_text) is None,
    )

parameter_names = [parameter["name"] for parameter in target["parameters"]]
for name in parameter_names:
    escaped = re.escape(name)
    count = len(
        re.findall(
            rf"(?m)^\s*(?:noncomputable\s+)?def\s+{escaped}(?=\s|\()",
            proof_text,
        )
    )
    check(f"candidate exact def {name}", count == 1, count)

check(
    "trust inventory proof holes",
    trust_inventory["designated_sorries"] == 0
    and trust_inventory["other_sorries"] == 0,
    (
        trust_inventory["designated_sorries"],
        trust_inventory["other_sorries"],
    ),
)
print(
    "INFO lean_invocation_sha256 cannot be re-hashed: "
    "the Stage 5 invocation directory is recorded but is not mounted; "
    f"recorded={hashes['lean_invocation_sha256']}"
)
print("ALL INDEPENDENT STRUCTURAL CHECKS PASSED")
