#!/usr/bin/env python3
"""Independent, read-only integrity checks for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification


def load(path: str) -> dict:
    value = json.loads(Path(path).read_text())
    assert isinstance(value, dict), path
    return value


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise AssertionError(f"symlink in {root}: {path}")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = file_sha(path)
    return result


def check(label: str, actual, expected) -> None:
    ok = actual == expected
    print(f"{label}: {'PASS' if ok else 'FAIL'}")
    print(f"  actual:   {actual}")
    print(f"  expected: {expected}")
    if not ok:
        raise AssertionError(label)


audit = load("/audit-input.json")["resolution"]
discovery = load("/reference/lemma-discovery.json")
input_manifest = load("/reference/klean-generation/input-manifest.json")
generator = load("/reference/klean-generation/generator-manifest.json")
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
export_result = load("/reference/klean-generation/export-result.json")
source_manifest = load("/reference/generation-tools/source-manifest.json")
stage4_preflight = load("/reference/klean-generation/preflight.json")

inventory = inventory_verification(Path("/reference/k-proof"))
rules = inventory["rules"]
manifest_rules = discovery["rules"]

print("=== inventory reconstruction and Stage 3 bijection ===")
check("inventory schema", inventory["schema_version"], 2)
check("verification module closure", inventory["verification_modules"], ["VERIFICATION"])
check(
    "verification source sha256",
    inventory["verification_sha256"],
    input_manifest["verification_sha256"],
)
check(
    "inventory sha256",
    inventory["inventory_sha256"],
    discovery["inventory_sha256"],
)
inventory_ids = [rule["source_rule_id"] for rule in rules]
manifest_ids = [rule["source_rule_id"] for rule in manifest_rules]
check("manifest identity order", manifest_ids, inventory_ids)
check("manifest identities unique", len(set(manifest_ids)), len(manifest_ids))
check("inventory identities unique", len(set(inventory_ids)), len(inventory_ids))

verification_lines = Path("/reference/k-proof/verification.k").read_text().splitlines()
for index, rule in enumerate(rules):
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    span = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    check(f"rule[{index}] span", span, rule["text"])
    check(f"rule[{index}] normalized sha256", digest, rule["normalized_sha256"])
    check(f"rule[{index}] source_rule_id", "rule-" + digest, rule["source_rule_id"])

# These expected classes are an independent classification from the frozen K
# source, not copied from the Stage 3 manifest.
independent_classes = {
    "rule-d4676ce65d5aa71d896650582ea7fd95efd3f817b5b09d834d0ee937362738f4": "DEFINITION",
    "rule-847ade70763e1124464b657827fa409b360b4ee6da4959b08c37af4bfcc6ea05": "DEFINITION",
    "rule-8f5f9af1fe8efa4c83c0197e4a31cd8150af4cd53c7d3fc694a6fa2796bc0d5a": "DEFINITION",
    "rule-865c4b24763637b23fa93793d11806aae069dc118aea556597904b6aae56a5ad": "DEFINITION",
    "rule-ce7624945e06d02ae5606649e897ef6ded8e343e6c0ed28075613044c8e40503": "DOMAIN_LEMMA",
    "rule-c7e3f2f45bbfd43ef6b8731a4e0c5ffee7b1efe6805f88d96b74e539a66d2e71": "DEFINITION",
    "rule-e766fccb4416695974e50ef3cf530b303db323532b6a6987b87d7a5a123c4193": "DEFINITION",
    "rule-ad345f4ab95b42abade2e1e581a480d6a8f282ec27387d0fc23704a7aa59979b": "DEFINITION",
}
check("independent classification coverage", list(independent_classes), inventory_ids)
manifest_classes = {
    rule["source_rule_id"]: rule["classification"] for rule in manifest_rules
}
check("independent classifications", manifest_classes, independent_classes)
for rule in rules:
    if "simplification" in rule["attributes"]:
        classification = independent_classes[rule["source_rule_id"]]
        check(
            f"simplification class {rule['source_rule_id']}",
            classification in {"DEFINITION", "DOMAIN_LEMMA"},
            True,
        )

definition_ids = [
    source_rule_id
    for source_rule_id in inventory_ids
    if independent_classes[source_rule_id] == "DEFINITION"
]
domain_ids = [
    source_rule_id
    for source_rule_id in inventory_ids
    if independent_classes[source_rule_id] == "DOMAIN_LEMMA"
]
check(
    "input-manifest definition order",
    [entry["source_rule_id"] for entry in input_manifest["definitions"]],
    definition_ids,
)
check(
    "input-manifest domain-rule order",
    [entry["source_rule_id"] for entry in input_manifest["source_rules"]],
    domain_ids,
)
check("input-manifest operational rules", input_manifest["operational_rules"], [])
check(
    "input-manifest proved derived lemmas",
    input_manifest["proved_derived_lemmas"],
    [],
)

print("=== producer authentication ===")
producer_hashes = {
    "klean.py": file_sha(Path("/reference/generation-tools/klean.py")),
    "klean_export.py": file_sha(
        Path("/reference/generation-tools/klean_export.py")
    ),
}
check("producer file manifest", producer_hashes, source_manifest["files"])
check(
    "exporter hash in generator manifest",
    producer_hashes["klean_export.py"],
    generator["exporter_sha256"],
)
check(
    "klean.py hash in generator manifest",
    producer_hashes["klean.py"],
    generator["klean_py_sha256"],
)
check(
    "generator image ID across manifests",
    generator["provenance"]["generator_image_id"],
    source_manifest["generator_image_id"],
)
recorded_producer_dir = Path(audit["generation_producer_sources"]).name
check(
    "launcher producer path image ID",
    "sha256:" + recorded_producer_dir,
    source_manifest["generator_image_id"],
)

print("=== launcher and manifest hashes ===")
hashes = audit["hashes"]
tree_pairs = [
    (
        "k_workspace_sha256",
        pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    ),
    (
        "stage1_export_sha256",
        klean_export.tree_digest(Path("/reference/k-proof")),
    ),
    (
        "k_audit_sha256",
        pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    ),
    (
        "klean_generation_sha256",
        pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
    ),
    (
        "generation_producer_sources_sha256",
        pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
    ),
    (
        "generated_tree_sha256",
        klean_export.tree_digest(
            Path("/reference/klean-generation/generated")
        ),
    ),
    (
        "lean_workspace_sha256",
        pipeline_contract.sha256_tree(Path("/candidate")),
    ),
]
for label, actual in tree_pairs:
    check(label, actual, hashes[label])
check(
    "discovery_manifest_sha256",
    file_sha(Path("/reference/lemma-discovery.json")),
    hashes["discovery_manifest_sha256"],
)
check(
    "all Stage 1 file hashes and paths",
    regular_files(Path("/reference/k-proof")),
    audit["stage1_source_hashes"],
)

check(
    "generator Stage 1 provenance",
    generator["provenance"]["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "generator Stage 3 provenance",
    generator["provenance"]["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check(
    "generator inventory provenance",
    generator["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "input manifest Stage 1 hash",
    input_manifest["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "input manifest Stage 3 hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)

print("=== Stage 4 source-rule/obligation and target identity ===")
obligation_source_ids = [
    item["source_rule_id"] for item in obligation_map["obligations"]
]
obligation_rule_ids = [
    item["source_rule_id"] for item in obligation_map["source_rules"]
]
check("obligation source rule order", obligation_rule_ids, domain_ids)
check("obligation order", obligation_source_ids, domain_ids)
check(
    "obligation identities unique",
    len(set(obligation_source_ids)),
    len(obligation_source_ids),
)
check(
    "obligation map source-rule identities unique",
    len(set(obligation_rule_ids)),
    len(obligation_rule_ids),
)
check("generator obligation count", generator["obligation_count"], len(domain_ids))
check("export obligation count", export_result["obligation_count"], len(domain_ids))
check("export status", export_result["status"], "OK")

for index, obligation in enumerate(obligation_map["obligations"]):
    source = next(
        rule
        for rule in rules
        if rule["source_rule_id"] == obligation["source_rule_id"]
    )
    check(
        f"obligation[{index}] normalized source hash",
        obligation["normalized_sha256"],
        source["normalized_sha256"],
    )
    check(
        f"obligation[{index}] source span",
        obligation["source_span"],
        {
            "start_line": source["start_line"],
            "end_line": source["end_line"],
        },
    )
    check(
        f"obligation[{index}] conjunct hash",
        hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest(),
        obligation["lean_conjunct_sha256"],
    )

check(
    "obligation map file hash",
    file_sha(
        Path("/reference/klean-generation/generated/obligation-map.json")
    ),
    generator["obligation_map_sha256"],
)
recomputed_target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
check("recomputed target vs generator", recomputed_target, generator["target"])
check("launcher target", audit["target"], generator["target"])
check("recorded Stage 4 target", stage4_preflight["target"], generator["target"])
check("Stage 4 status", stage4_preflight["status"], "PASS")
check("Stage 4 obligation count", stage4_preflight["obligation_count"], 1)

print("ALL INTEGRITY CHECKS PASSED")
