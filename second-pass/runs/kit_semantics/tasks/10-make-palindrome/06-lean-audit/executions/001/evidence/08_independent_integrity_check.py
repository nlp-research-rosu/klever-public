#!/usr/bin/env python3
"""Independent Stage 3/4 provenance, inventory, and target integrity checks."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
K_AUDIT = Path("/reference/k-audit")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def load_json(path: Path) -> dict:
    assert path.is_file() and not path.is_symlink(), path
    value = json.loads(path.read_bytes())
    assert isinstance(value, dict), path
    return value


def file_sha256(path: Path) -> str:
    assert path.is_file() and not path.is_symlink(), path
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    assert root.is_dir() and not root.is_symlink(), root
    pending = [root]
    entries: list[tuple[str, str, Path]] = []
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise AssertionError(f"unsupported tree entry: {path}")
    return sorted(entries)


def pipeline_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in regular_tree_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def export_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in regular_tree_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def report(label: str, value: object) -> None:
    print(f"PASS {label}: {value}")


def main() -> None:
    audit = load_json(AUDIT_INPUT)
    resolution = audit["resolution"]
    assert audit["schema_version"] == 4
    assert resolution["schema_version"] == 4
    assert canonical_sha256(resolution) == audit["resolved_input_sha256"]
    report("audit-input canonical binding", audit["resolved_input_sha256"])

    assert os.environ.get("AUDIT_MODE") == resolution["mode"]
    assert resolution["mode"] == "CLASSIFICATION_ONLY"
    assert resolution["condition"] == "kit-semantics"
    assert resolution["semantics_mode"] == "SUPPLIED_SEMANTICS"
    assert resolution["problem_id"] == "10-make-palindrome"
    report("launcher mode and problem binding", resolution["mode"])

    hashes = resolution["hashes"]
    observed_pipeline_trees = {
        "k_workspace_sha256": pipeline_tree_sha256(WORKSPACE),
        "k_audit_sha256": pipeline_tree_sha256(K_AUDIT),
        "klean_generation_sha256": pipeline_tree_sha256(GENERATION),
        "generation_producer_sources_sha256": pipeline_tree_sha256(PRODUCERS),
    }
    for key, observed in observed_pipeline_trees.items():
        assert hashes[key] == observed, (key, hashes[key], observed)
        report(key, observed)

    stage1_export = export_tree_sha256(WORKSPACE)
    generated_tree = export_tree_sha256(GENERATED)
    assert hashes["stage1_export_sha256"] == stage1_export
    assert hashes["generated_tree_sha256"] == generated_tree
    assert hashes["discovery_manifest_sha256"] == file_sha256(DISCOVERY)
    assert hashes["lean_workspace_sha256"] is None
    assert hashes["lean_invocation_sha256"] is None
    report("stage1 export tree", stage1_export)
    report("generated project tree", generated_tree)
    report("discovery manifest", hashes["discovery_manifest_sha256"])

    observed_stage1_files = {
        relative: file_sha256(path)
        for relative, kind, path in regular_tree_entries(WORKSPACE)
        if kind == "file"
    }
    assert observed_stage1_files == resolution["stage1_source_hashes"]
    report("all Stage 1 per-file hashes", len(observed_stage1_files))

    assert (
        resolution["selections"]["k_audit"]["artifact_sha256"]
        == hashes["k_audit_sha256"]
    )
    assert (
        resolution["selections"]["klean_generation"]["artifact_sha256"]
        == hashes["klean_generation_sha256"]
    )
    assert resolution["selections"]["klean_generation"]["status"] == (
        "KLEAN_NO_OBLIGATIONS"
    )
    report("selection hash bindings", "both exact")

    source_manifest = load_json(PRODUCERS / "source-manifest.json")
    generator_manifest = load_json(GENERATION / "generator-manifest.json")
    producer_names = {
        relative
        for relative, kind, _path in regular_tree_entries(PRODUCERS)
        if kind == "file"
    }
    assert producer_names == {
        "source-manifest.json",
        "klean_export.py",
        "klean.py",
    }
    producer_hashes = {
        "klean_export.py": file_sha256(PRODUCERS / "klean_export.py"),
        "klean.py": file_sha256(PRODUCERS / "klean.py"),
    }
    assert source_manifest == {
        "schema_version": 1,
        "generator_image_id": generator_manifest["provenance"][
            "generator_image_id"
        ],
        "files": producer_hashes,
    }
    assert generator_manifest["exporter_sha256"] == producer_hashes[
        "klean_export.py"
    ]
    assert generator_manifest["klean_py_sha256"] == producer_hashes["klean.py"]
    audit_image_key = Path(resolution["generation_producer_sources"]).name
    assert source_manifest["generator_image_id"] == f"sha256:{audit_image_key}"
    report("producer source hashes", producer_hashes)
    report("immutable generator image", source_manifest["generator_image_id"])

    inventory = inventory_verification(WORKSPACE)
    discovery = load_json(DISCOVERY)
    assert discovery["schema_version"] == 2
    assert discovery["inventory_sha256"] == inventory["inventory_sha256"]
    assert len(discovery["rules"]) == len(inventory["rules"])
    inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
    discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    assert discovery_ids == inventory_ids
    assert len(set(discovery_ids)) == len(discovery_ids)
    classifications = {
        entry["source_rule_id"]: {
            "classification": entry["classification"],
            "rationale": entry["rationale"],
        }
        for entry in discovery["rules"]
    }
    assert len(classifications) == len(discovery_ids)
    classified = [
        {**rule, **classifications[rule["source_rule_id"]]}
        for rule in inventory["rules"]
    ]
    definitions = [
        rule for rule in classified if rule["classification"] == "DEFINITION"
    ]
    operational = [
        rule
        for rule in classified
        if rule["classification"] == "OPERATIONAL_RULE"
    ]
    derived = [
        rule
        for rule in classified
        if rule["classification"] == "PROVED_DERIVED_LEMMA"
    ]
    domains = [
        rule for rule in classified if rule["classification"] == "DOMAIN_LEMMA"
    ]
    assert len(inventory["rules"]) == 16
    assert len(definitions) == 16
    assert not operational and not derived and not domains
    assert inventory["inventory_sha256"] == canonical_json_sha256(
        inventory["rules"]
    )
    report(
        "canonical rule inventory",
        {
            "rules": len(inventory["rules"]),
            "inventory_sha256": inventory["inventory_sha256"],
            "modules": inventory["verification_modules"],
        },
    )
    report(
        "protected manifest identity order",
        "16 unique IDs, exact source order",
    )

    discovery_sha = file_sha256(DISCOVERY)
    domain_source_rules = [
        {
            **rule,
            "inventory_sha256": inventory["inventory_sha256"],
            "discovery_manifest_sha256": discovery_sha,
        }
        for rule in domains
    ]
    input_manifest = load_json(GENERATION / "input-manifest.json")
    assert input_manifest["definitions"] == definitions
    assert input_manifest["operational_rules"] == operational
    assert input_manifest["proved_derived_lemmas"] == derived
    assert input_manifest["source_rules"] == domain_source_rules
    assert input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
    assert input_manifest["verification_sha256"] == file_sha256(
        WORKSPACE / "verification.k"
    )
    assert input_manifest["stage1_workspace_sha256"] == stage1_export
    assert input_manifest["frozen_input_sha256"] == stage1_export
    assert input_manifest["stage3_discovery_manifest_sha256"] == discovery_sha
    report("input-manifest classified inventory", "exact")

    provenance = generator_manifest["provenance"]
    assert provenance["stage1_workspace_sha256"] == stage1_export
    assert provenance["stage3_discovery_manifest_sha256"] == discovery_sha
    assert provenance["inventory_sha256"] == inventory["inventory_sha256"]
    assert generator_manifest["generated_tree_sha256"] == generated_tree
    assert generator_manifest["toolchain"] == load_json(TOOLCHAIN_LOCK)
    report("generator provenance and toolchain", "exact")

    obligation_map_path = GENERATED / "obligation-map.json"
    obligation_map = load_json(obligation_map_path)
    assert obligation_map["schema_version"] == 3
    assert obligation_map["source_rules"] == domain_source_rules
    obligations = obligation_map["obligations"]
    observed_obligation_ids = [
        obligation["source_rule_id"] for obligation in obligations
    ]
    expected_obligation_ids = [
        source_rule["source_rule_id"] for source_rule in domain_source_rules
    ]
    assert observed_obligation_ids == expected_obligation_ids
    assert len(set(observed_obligation_ids)) == len(observed_obligation_ids)
    assert obligation_map["trust_parameters"] == []
    assert obligations == []
    assert generator_manifest["obligation_count"] == len(obligations)
    assert generator_manifest["obligation_map_sha256"] == file_sha256(
        obligation_map_path
    )
    report(
        "source-rule/obligation bijection",
        "empty domain set maps bijectively to zero obligations",
    )

    target_declarations: list[str] = []
    for relative, kind, path in regular_tree_entries(GENERATED):
        if kind == "file" and path.suffix == ".lean":
            for line_number, line in enumerate(
                path.read_text().splitlines(), start=1
            ):
                if "targetStatement" in line:
                    target_declarations.append(f"{relative}:{line_number}:{line}")
    assert target_declarations == []
    assert generator_manifest["target"] is None
    assert resolution["target"] is None
    assert resolution["stage5_result"] is None
    assert resolution["lean_workspace"] is None
    assert resolution["lean_invocation"] is None
    assert not Path("/candidate").exists()
    report("fixed generated target", "absent, as required for zero obligations")
    report("Stage 5 candidate", "absent")

    export_result = load_json(GENERATION / "export-result.json")
    trust_inventory_path = GENERATION / "trust-inventory.json"
    assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    assert export_result["obligation_count"] == 0
    assert export_result["frozen_input_sha256"] == stage1_export
    assert export_result["stage3_discovery_manifest_sha256"] == discovery_sha
    assert export_result["generated_tree_sha256"] == generated_tree
    assert export_result["trust_inventory_sha256"] == file_sha256(
        trust_inventory_path
    )
    assert load_json(GENERATION / "preflight.json") == resolution[
        "stage4_preflight"
    ]
    assert resolution["stage4_preflight"]["status"] == (
        "KLEAN_NO_OBLIGATIONS"
    )
    assert resolution["stage4_preflight"]["target"] is None
    assert resolution["stage4_preflight"]["obligation_count"] == 0
    report("export result and launcher preflight binding", "exact")

    print("ALL INDEPENDENT INTEGRITY CHECKS PASSED")


if __name__ == "__main__":
    main()
