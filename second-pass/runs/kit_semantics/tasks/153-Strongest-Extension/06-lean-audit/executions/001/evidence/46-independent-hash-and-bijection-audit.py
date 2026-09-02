#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from tools import (
    klean_export,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")
LOCK = Path("/reference/klean-toolchain.lock.json")


def load(path: Path):
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: list[tuple[str, bool, object, object]] = []


def check(label: str, observed, expected) -> None:
    checks.append((label, observed == expected, observed, expected))


audit_document = load(AUDIT_INPUT)
resolution, resolution_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
hashes = resolution["hashes"]
discovery = load(DISCOVERY)
reconstructed = load(
    Path("/audit-output/evidence/03-reconstructed-rule-inventory.json")
)
generator = load(GENERATION / "generator-manifest.json")
input_manifest = load(GENERATION / "input-manifest.json")
obligation_map = load(GENERATED / "obligation-map.json")
source_manifest = load(PRODUCERS / "source-manifest.json")
toolchain_lock = load(LOCK)

check(
    "audit-input canonical resolution digest",
    resolution_digest,
    audit_document["resolved_input_sha256"],
)
check("toolchain lock vs generator manifest", toolchain_lock, generator["toolchain"])

for label, root, key in [
    ("Stage 1 full tree", K_WORKSPACE, "k_workspace_sha256"),
    ("selected Stage 2 audit tree", K_AUDIT, "k_audit_sha256"),
    ("Stage 4 generation tree", GENERATION, "klean_generation_sha256"),
    ("Stage 5 candidate tree", CANDIDATE, "lean_workspace_sha256"),
    ("generation producer tree", PRODUCERS, "generation_producer_sources_sha256"),
]:
    check(label, pipeline_contract.sha256_tree(root), hashes[key])

stage1_export = klean_export.tree_digest(K_WORKSPACE)
generated_tree = klean_export.tree_digest(GENERATED)
discovery_sha = sha(DISCOVERY)
check("Stage 1 deterministic export tree", stage1_export, hashes["stage1_export_sha256"])
check("generated deterministic tree", generated_tree, hashes["generated_tree_sha256"])
check("discovery file", discovery_sha, hashes["discovery_manifest_sha256"])

stage1_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): sha(path)
    for path in sorted(K_WORKSPACE.rglob("*"))
    if path.is_file()
}
check(
    "all Stage 1 regular-file hashes and path set",
    stage1_source_hashes,
    resolution["stage1_source_hashes"],
)

producer_hashes = {
    "klean_export.py": sha(PRODUCERS / "klean_export.py"),
    "klean.py": sha(PRODUCERS / "klean.py"),
}
check("producer hashes vs source manifest", producer_hashes, source_manifest["files"])
check(
    "klean_export.py vs generator manifest",
    producer_hashes["klean_export.py"],
    generator["exporter_sha256"],
)
check(
    "klean.py vs generator manifest",
    producer_hashes["klean.py"],
    generator["klean_py_sha256"],
)
check(
    "producer image source/generator agreement",
    source_manifest["generator_image_id"],
    generator["provenance"]["generator_image_id"],
)
check(
    "producer image audit-input path binding",
    source_manifest["generator_image_id"].removeprefix("sha256:"),
    Path(resolution["generation_producer_sources"]).name,
)

check(
    "generator Stage 1 input binding",
    generator["provenance"]["stage1_workspace_sha256"],
    stage1_export,
)
check(
    "input manifest Stage 1 input binding",
    input_manifest["stage1_workspace_sha256"],
    stage1_export,
)
check(
    "generator discovery binding",
    generator["provenance"]["stage3_discovery_manifest_sha256"],
    discovery_sha,
)
check(
    "input manifest discovery binding",
    input_manifest["stage3_discovery_manifest_sha256"],
    discovery_sha,
)
check(
    "generator generated-tree binding",
    generator["generated_tree_sha256"],
    generated_tree,
)
check(
    "obligation-map file hash",
    sha(GENERATED / "obligation-map.json"),
    generator["obligation_map_sha256"],
)

check(
    "reconstructed whole inventory hash",
    reconstructed["inventory_sha256"],
    discovery["inventory_sha256"],
)
check(
    "discovery/reconstruction ordered identity bijection",
    [rule["source_rule_id"] for rule in discovery["rules"]],
    [rule["source_rule_id"] for rule in reconstructed["rules"]],
)
discovery_by_id = {
    rule["source_rule_id"]: rule for rule in discovery["rules"]
}
rules = [
    {
        **rule,
        "classification": discovery_by_id[rule["source_rule_id"]][
            "classification"
        ],
    }
    for rule in reconstructed["rules"]
]
ids = [rule["source_rule_id"] for rule in rules]
check("discovery source-rule identities unique", len(ids), len(set(ids)))
for rule in rules:
    check(
        f"{rule['source_rule_id']} id/hash binding",
        rule["source_rule_id"],
        "rule-" + rule["normalized_sha256"],
    )

category_key = {
    "DEFINITION": "definitions",
    "DOMAIN_LEMMA": "source_rules",
    "OPERATIONAL_RULE": "operational_rules",
    "PROVED_DERIVED_LEMMA": "proved_derived_lemmas",
}
manifest_records = []
for classification, key in category_key.items():
    for record in input_manifest[key]:
        check(
            f"{record['source_rule_id']} category container",
            record["classification"],
            classification,
        )
        manifest_records.append(record)

manifest_by_id = {record["source_rule_id"]: record for record in manifest_records}
check(
    "input-manifest source-rule set and uniqueness",
    (len(manifest_records), set(manifest_by_id)),
    (len(rules), set(ids)),
)
for rule in rules:
    record = manifest_by_id[rule["source_rule_id"]]
    for field in [
        "module",
        "start_line",
        "end_line",
        "normalized_sha256",
        "text",
    ]:
        check(
            f"{rule['source_rule_id']} input-manifest {field}",
            record[field],
            rule[field],
        )
    check(
        f"{rule['source_rule_id']} input-manifest classification",
        record["classification"],
        rule["classification"],
    )

domain = [rule for rule in rules if rule["classification"] == "DOMAIN_LEMMA"]
obligations = obligation_map["obligations"]
check("generator obligation count", len(obligations), generator["obligation_count"])
check(
    "domain-rule/obligation ordered bijection",
    [item["source_rule_id"] for item in obligations],
    [item["source_rule_id"] for item in domain],
)
check(
    "domain-rule/source_rules ordered bijection",
    [item["source_rule_id"] for item in obligation_map["source_rules"]],
    [item["source_rule_id"] for item in domain],
)
check(
    "obligation identities unique",
    len(obligations),
    len({item["source_rule_id"] for item in obligations}),
)
for rule, obligation in zip(domain, obligations, strict=True):
    check(
        f"{rule['source_rule_id']} obligation normalized hash",
        obligation["normalized_sha256"],
        rule["normalized_sha256"],
    )
    check(
        f"{rule['source_rule_id']} obligation source span",
        obligation["source_span"],
        {"start_line": rule["start_line"], "end_line": rule["end_line"]},
    )
    check(
        f"{rule['source_rule_id']} obligation discovery binding",
        obligation["discovery_manifest_sha256"],
        discovery_sha,
    )
    check(
        f"{rule['source_rule_id']} obligation inventory binding",
        obligation["inventory_sha256"],
        discovery["inventory_sha256"],
    )
    check(
        f"{rule['source_rule_id']} conjunct hash",
        hashlib.sha256(obligation["lean_conjunct"].encode()).hexdigest(),
        obligation["lean_conjunct_sha256"],
    )

target = klean_export.target_statement(GENERATED)
check("recomputed target vs generator manifest", target, generator["target"])
check("recomputed target vs audit target", target, resolution["target"])
check(
    "recomputed target vs launcher preflight target",
    target,
    resolution["stage4_preflight"]["target"],
)
check(
    "trust-parameter bindings vs target parameters",
    obligation_map["trust_parameters"],
    target["parameters"],
)
check(
    "classification counts",
    Counter(rule["classification"] for rule in rules),
    Counter(
        {
            "DEFINITION": 34,
            "DOMAIN_LEMMA": 5,
            "PROVED_DERIVED_LEMMA": 3,
        }
    ),
)

print(f"checks={len(checks)}")
failed = [item for item in checks if not item[1]]
for label, passed, observed, expected in checks:
    print(f"{'PASS' if passed else 'FAIL'} {label}")
    if not passed:
        print(f"  observed={observed!r}")
        print(f"  expected={expected!r}")
print(
    "UNREPRODUCIBLE_BY_MOUNT_DESIGN lean_invocation_sha256="
    + hashes["lean_invocation_sha256"]
    + " (the invocation directory is recorded but not mounted; candidate tree and"
    + " all mounted Stage 5 files were hashed above)"
)
print(f"failed={len(failed)}")
raise SystemExit(1 if failed else 0)
