#!/usr/bin/env python3
"""Independent integrity checks for the 51-remove-vowels Stage 3/4 audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import k_rule_inventory, klean_export, lemma_discovery_contract
from tools import pipeline_contract


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    observed: dict[str, str] = {}
    for directory, directory_names, file_names in os.walk(root):
        directory_names.sort()
        file_names.sort()
        for name in file_names:
            path = Path(directory) / name
            mode = path.stat(follow_symlinks=False).st_mode
            if not stat.S_ISREG(mode):
                raise RuntimeError(f"non-regular file in source tree: {path}")
            observed[path.relative_to(root).as_posix()] = sha256_file(path)
    return observed


def check(name: str, observed: object, expected: object) -> None:
    ok = observed == expected
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'}")
    print(f"  observed={json.dumps(observed, sort_keys=True)}")
    print(f"  expected={json.dumps(expected, sort_keys=True)}")
    if not ok:
        raise RuntimeError(f"integrity check failed: {name}")


def main() -> None:
    workspace = Path("/reference/k-proof")
    discovery_path = Path("/reference/lemma-discovery.json")
    generation = Path("/reference/klean-generation")
    generated = generation / "generated"
    producer = Path("/reference/generation-tools")
    audit_input = json.loads(Path("/audit-input.json").read_text())
    resolution = audit_input["resolution"]
    hashes = resolution["hashes"]
    discovery = json.loads(discovery_path.read_text())
    generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
    input_manifest = json.loads((generation / "input-manifest.json").read_text())
    obligation_map = json.loads((generated / "obligation-map.json").read_text())
    source_manifest = json.loads((producer / "source-manifest.json").read_text())

    print("=== canonical local verification-module rule inventory ===")
    inventory = k_rule_inventory.inventory_verification(workspace)
    print(json.dumps(inventory, indent=2, sort_keys=True))
    source_lines = (workspace / "verification.k").read_text().splitlines()
    for index, rule in enumerate(inventory["rules"]):
        span_text = "\n".join(source_lines[rule["start_line"] - 1 : rule["end_line"]])
        check(f"rule[{index}] exact source span", span_text, rule["text"])
        independent_normalized = " ".join(span_text.split())
        independent_digest = hashlib.sha256(independent_normalized.encode()).hexdigest()
        check(f"rule[{index}] normalized_sha256", independent_digest, rule["normalized_sha256"])
        check(f"rule[{index}] source_rule_id", "rule-" + independent_digest, rule["source_rule_id"])
    independent_inventory_hash = k_rule_inventory.canonical_json_sha256(inventory["rules"])
    check("whole inventory hash", independent_inventory_hash, inventory["inventory_sha256"])

    print("=== raw Stage 3 bijection and order ===")
    canonical_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    check("Stage 3 ordered identities", manifest_ids, canonical_ids)
    check("Stage 3 no duplicate identities", len(set(manifest_ids)), len(manifest_ids))
    check("Stage 3 inventory hash", discovery["inventory_sha256"], inventory["inventory_sha256"])
    validated = lemma_discovery_contract.validate_trust_boundary(workspace, discovery_path)
    check("validated inventory rules", validated["rules"], inventory["rules"])
    print("CLASSIFICATION_COUNTS", json.dumps({
        "definitions": len(validated["definitions"]),
        "operational_rules": len(validated["operational_rules"]),
        "proved_derived_lemmas": len(validated["proved_derived_lemmas"]),
        "domain_lemmas": len(validated["domain_lemmas"]),
    }, sort_keys=True))

    print("=== producer authentication ===")
    observed_producer_files = {
        "klean_export.py": sha256_file(producer / "klean_export.py"),
        "klean.py": sha256_file(producer / "klean.py"),
    }
    check("producer files vs source manifest", observed_producer_files, source_manifest["files"])
    check("exporter vs generator manifest", observed_producer_files["klean_export.py"], generator_manifest["exporter_sha256"])
    check("klean.py vs generator manifest", observed_producer_files["klean.py"], generator_manifest["klean_py_sha256"])
    check("generator image across manifests", source_manifest["generator_image_id"], generator_manifest["provenance"]["generator_image_id"])
    recorded_bundle_name = Path(resolution["generation_producer_sources"]).name
    check("audit-input producer path binds image", "sha256:" + recorded_bundle_name, source_manifest["generator_image_id"])
    check("producer bundle file set", sorted(path.name for path in producer.iterdir()), ["klean.py", "klean_export.py", "source-manifest.json"])

    print("=== recorded tree and source hashes ===")
    check("producer source tree", pipeline_contract.sha256_tree(producer), hashes["generation_producer_sources_sha256"])
    check("Stage 1 pipeline tree", pipeline_contract.sha256_tree(workspace), hashes["k_workspace_sha256"])
    check("Stage 1 export tree", klean_export.tree_digest(workspace), hashes["stage1_export_sha256"])
    check("Stage 2 selected audit tree", pipeline_contract.sha256_tree(Path("/reference/k-audit")), hashes["k_audit_sha256"])
    check("Stage 3 discovery file", sha256_file(discovery_path), hashes["discovery_manifest_sha256"])
    check("Stage 4 selected generation tree", pipeline_contract.sha256_tree(generation), hashes["klean_generation_sha256"])
    check("generated project export tree", klean_export.tree_digest(generated), hashes["generated_tree_sha256"])
    check("Stage 1 per-file source hashes", regular_file_hashes(workspace), resolution["stage1_source_hashes"])

    print("=== Stage 4 manifest bindings ===")
    check("input frozen tree", input_manifest["frozen_input_sha256"], hashes["stage1_export_sha256"])
    check("input Stage 1 tree", input_manifest["stage1_workspace_sha256"], hashes["stage1_export_sha256"])
    check("input Stage 3 hash", input_manifest["stage3_discovery_manifest_sha256"], hashes["discovery_manifest_sha256"])
    check("input inventory hash", input_manifest["inventory_sha256"], inventory["inventory_sha256"])
    check("input verification file hash", input_manifest["verification_sha256"], sha256_file(workspace / "verification.k"))
    check("generator Stage 1 provenance", generator_manifest["provenance"]["stage1_workspace_sha256"], hashes["stage1_export_sha256"])
    check("generator Stage 3 provenance", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"], hashes["discovery_manifest_sha256"])
    check("generator inventory provenance", generator_manifest["provenance"]["inventory_sha256"], inventory["inventory_sha256"])
    check("generator generated tree", generator_manifest["generated_tree_sha256"], hashes["generated_tree_sha256"])
    check("generator obligation-map hash", generator_manifest["obligation_map_sha256"], sha256_file(generated / "obligation-map.json"))
    check("generator obligation count", generator_manifest["obligation_count"], len(obligation_map["obligations"]))
    check("source-rule list input/map", input_manifest["source_rules"], obligation_map["source_rules"])
    check("zero-obligation target", generator_manifest["target"], None)
    check("Lean workspace hash absent", hashes["lean_workspace_sha256"], None)
    check("Lean invocation hash absent", hashes["lean_invocation_sha256"], None)
    print("ALL_INTEGRITY_CHECKS_PASS")


if __name__ == "__main__":
    main()
