#!/usr/bin/env python3
"""Read-only independent hash, obligation, and target cross-check."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.pipeline_contract import sha256_tree
from tools.k_rule_inventory import inventory_verification


def load(path: str) -> dict:
    return json.loads(Path(path).read_text())


def sha(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def report(label: str, actual: object, expected: object) -> None:
    print(f"{label}:")
    print(f"  actual   = {actual}")
    print(f"  expected = {expected}")
    print(f"  match    = {actual == expected}")


producer_path = "/reference/generation-tools/klean_export.py"
spec = importlib.util.spec_from_file_location(
    "generation_time_klean_export", producer_path
)
assert spec is not None and spec.loader is not None
producer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = producer
spec.loader.exec_module(producer)

audit = load("/audit-input.json")
resolution = audit["resolution"]
audit_hashes = resolution["hashes"]
manifest = load("/reference/klean-generation/generator-manifest.json")
source_manifest = load("/reference/generation-tools/source-manifest.json")
discovery = load("/reference/lemma-discovery.json")
mapping = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
preflight = load("/reference/klean-generation/preflight.json")

print("PRODUCER IDENTITY")
report(
    "klean_export.py sha256",
    sha("/reference/generation-tools/klean_export.py"),
    manifest["exporter_sha256"],
)
report(
    "klean.py sha256",
    sha("/reference/generation-tools/klean.py"),
    manifest["klean_py_sha256"],
)
report(
    "klean_export.py versus source manifest",
    sha("/reference/generation-tools/klean_export.py"),
    source_manifest["files"]["klean_export.py"],
)
report(
    "klean.py versus source manifest",
    sha("/reference/generation-tools/klean.py"),
    source_manifest["files"]["klean.py"],
)
image_ids = {
    manifest["provenance"]["generator_image_id"],
    source_manifest["generator_image_id"],
}
print(f"generator image ids = {sorted(image_ids)}")
print(
    "audit producer selector contains image id = "
    + str(
        next(iter(image_ids)).removeprefix("sha256:")
        in resolution["generation_producer_sources"]
    )
)

print("\nLAUNCHER TREE HASHES")
for label, path, key in (
    ("Stage 1 workspace", "/reference/k-proof", "k_workspace_sha256"),
    ("Stage 2 audit", "/reference/k-audit", "k_audit_sha256"),
    (
        "generation producer sources",
        "/reference/generation-tools",
        "generation_producer_sources_sha256",
    ),
    (
        "Stage 4 generation",
        "/reference/klean-generation",
        "klean_generation_sha256",
    ),
    ("Stage 5 candidate", "/candidate", "lean_workspace_sha256"),
):
    report(label, sha256_tree(Path(path)), audit_hashes[key])

print("\nGENERATION-SPECIFIC HASHES")
report(
    "Stage 1 exporter tree",
    producer.tree_digest(Path("/reference/k-proof")),
    manifest["provenance"]["stage1_workspace_sha256"],
)
report(
    "discovery manifest bytes",
    sha("/reference/lemma-discovery.json"),
    manifest["provenance"]["stage3_discovery_manifest_sha256"],
)
report(
    "discovery manifest versus audit input",
    sha("/reference/lemma-discovery.json"),
    audit_hashes["discovery_manifest_sha256"],
)
report(
    "obligation-map bytes",
    sha("/reference/klean-generation/generated/obligation-map.json"),
    manifest["obligation_map_sha256"],
)
report(
    "generated exporter tree",
    producer.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    manifest["generated_tree_sha256"],
)
report(
    "generated tree versus audit input",
    producer.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    audit_hashes["generated_tree_sha256"],
)

print("\nSOURCE-RULE / OBLIGATION BIJECTION")
reconstructed = inventory_verification(Path("/reference/k-proof"))
report(
    "reconstructed inventory hash versus discovery",
    reconstructed["inventory_sha256"],
    discovery["inventory_sha256"],
)
report(
    "reconstructed inventory hash versus generator manifest",
    reconstructed["inventory_sha256"],
    manifest["provenance"]["inventory_sha256"],
)
classifications = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
domain_rules = [
    entry for entry in reconstructed["rules"]
    if classifications[entry["source_rule_id"]] == "DOMAIN_LEMMA"
]
source_rules = mapping["source_rules"]
obligations = mapping["obligations"]
domain_ids = [entry["source_rule_id"] for entry in domain_rules]
source_ids = [entry["source_rule_id"] for entry in source_rules]
obligation_ids = [entry["source_rule_id"] for entry in obligations]
print(f"domain ids     = {domain_ids}")
print(f"source ids     = {source_ids}")
print(f"obligation ids = {obligation_ids}")
print(
    "ordered bijection = "
    + str(
        domain_ids == source_ids == obligation_ids
        and len(set(obligation_ids)) == len(obligation_ids)
    )
)
for index, (domain, source, obligation) in enumerate(
    zip(domain_rules, source_rules, obligations, strict=True)
):
    compared = {
        "source_rule_id": (
            domain["source_rule_id"],
            source["source_rule_id"],
            obligation["source_rule_id"],
        ),
        "normalized_sha256": (
            domain["normalized_sha256"],
            source["normalized_sha256"],
            obligation["normalized_sha256"],
        ),
        "source_span": (
            {
                "start_line": domain["start_line"],
                "end_line": domain["end_line"],
            },
            {
                "start_line": source["start_line"],
                "end_line": source["end_line"],
            },
            obligation["source_span"],
        ),
        "inventory_sha256": (
            discovery["inventory_sha256"],
            source["inventory_sha256"],
            obligation["inventory_sha256"],
        ),
        "discovery_manifest_sha256": (
            sha("/reference/lemma-discovery.json"),
            source["discovery_manifest_sha256"],
            obligation["discovery_manifest_sha256"],
        ),
    }
    print(f"entry {index}:")
    for key, values in compared.items():
        print(f"  {key}: equal={values[0] == values[1] == values[2]}")
    report(
        "  Lean conjunct sha256",
        hashlib.sha256(
            obligation["lean_conjunct"].encode()
        ).hexdigest(),
        obligation["lean_conjunct_sha256"],
    )

print("\nTARGET IDENTITY")
actual_target = producer.target_statement(
    Path("/reference/klean-generation/generated")
)
expected_definition = producer.expected_target_definition(mapping)
assert expected_definition is not None
print(json.dumps(actual_target, indent=2, sort_keys=True))
print(f"target equals generator manifest = {actual_target == manifest['target']}")
print(f"target equals preflight          = {actual_target == preflight['target']}")
print(
    "target equals audit input        = "
    + str(actual_target == resolution["target"])
)
report(
    "expected target definition hash",
    producer.sha256_text(expected_definition),
    manifest["target"]["definition_sha256"],
)
report(
    "target statement hash",
    hashlib.sha256(
        manifest["target"]["statement"].encode()
    ).hexdigest(),
    manifest["target"]["statement_sha256"],
)
print(
    "obligation count agrees = "
    + str(
        len(domain_rules)
        == len(source_rules)
        == len(obligations)
        == manifest["obligation_count"]
        == preflight["obligation_count"]
    )
)

print("\nTARGET PARAMETER BINDINGS")
for parameter in manifest["target"]["parameters"]:
    bare = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "type": parameter["type"],
        "source_rule_ids": parameter["source_rule_ids"],
    }
    binding_hash = hashlib.sha256(
        json.dumps(
            bare, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    report(
        parameter["name"],
        binding_hash,
        parameter["binding_sha256"],
    )

print("\nFROZEN STAGE 1 SOURCE HASHES")
source_mismatches: list[str] = []
for relative, expected in sorted(
    resolution["stage1_source_hashes"].items()
):
    actual = sha(f"/reference/k-proof/{relative}")
    matched = actual == expected
    print(f"{relative}: match={matched} sha256={actual}")
    if not matched:
        source_mismatches.append(relative)
print(
    f"source_hash_count={len(resolution['stage1_source_hashes'])} "
    f"mismatch_count={len(source_mismatches)}"
)
