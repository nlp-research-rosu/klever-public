#!/usr/bin/env python3
"""Independent Stage 3/4 structural and hash checks for this audit."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools.k_rule_inventory import inventory_verification
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.stage6_resolution_contract import canonical_json_sha256


REFERENCE = Path("/reference")
K_PROOF = REFERENCE / "k-proof"
K_AUDIT = REFERENCE / "k-audit"
DISCOVERY = REFERENCE / "lemma-discovery.json"
GENERATION = REFERENCE / "klean-generation"
GENERATED = GENERATION / "generated"
PRODUCERS = REFERENCE / "generation-tools"
AUDIT_INPUT = Path("/audit-input.json")


def read_json(path: Path) -> dict:
    value = json.loads(path.read_bytes())
    if not isinstance(value, dict):
        raise AssertionError(f"not a JSON object: {path}")
    return value


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_entries(root: Path) -> list[tuple[str, str, Path]]:
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"not a real directory: {root}")
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    return sorted(entries)


def exporter_tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in strict_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in strict_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            payload = path.read_bytes()
            digest.update(len(payload).to_bytes(8, "big"))
            digest.update(payload)
    return digest.hexdigest()


def regular_file_map(root: Path) -> dict[str, str]:
    return {
        relative: file_hash(path)
        for relative, kind, path in strict_entries(root)
        if kind == "file"
    }


def check(label: str, actual, expected) -> None:
    if actual != expected:
        raise AssertionError(
            f"{label}: mismatch\n  actual={actual!r}\n  expected={expected!r}"
        )
    rendered = repr(actual)
    if len(rendered) > 500:
        encoded = json.dumps(
            actual, sort_keys=True, separators=(",", ":")
        ).encode()
        rendered = (
            f"<{type(actual).__name__} size={len(actual)} "
            f"canonical_sha256={hashlib.sha256(encoded).hexdigest()}>"
        )
    print(f"PASS {label}: {rendered}")


def main() -> None:
    audit = read_json(AUDIT_INPUT)
    resolution = audit["resolution"]
    hashes = resolution["hashes"]
    discovery = read_json(DISCOVERY)
    source_manifest = read_json(PRODUCERS / "source-manifest.json")
    input_manifest = read_json(GENERATION / "input-manifest.json")
    generator_manifest = read_json(GENERATION / "generator-manifest.json")
    export_result = read_json(GENERATION / "export-result.json")
    recorded_preflight = read_json(GENERATION / "preflight.json")

    print("== launcher and resolution ==")
    check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), "CLASSIFICATION_ONLY")
    check("resolution.mode", resolution["mode"], os.environ.get("AUDIT_MODE"))
    check("resolution.problem_id", resolution["problem_id"], "133-sum-squares")
    check("resolution.condition", resolution["condition"], "kit-semantics")
    check("resolution.semantics_mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")
    check(
        "resolved_input_sha256",
        canonical_json_sha256(resolution),
        audit["resolved_input_sha256"],
    )

    print("\n== producer provenance ==")
    actual_producer_hashes = {
        "klean.py": file_hash(PRODUCERS / "klean.py"),
        "klean_export.py": file_hash(PRODUCERS / "klean_export.py"),
    }
    check("source-manifest exact files", source_manifest["files"], actual_producer_hashes)
    check(
        "generator exporter_sha256",
        generator_manifest["exporter_sha256"],
        actual_producer_hashes["klean_export.py"],
    )
    check(
        "generator klean_py_sha256",
        generator_manifest["klean_py_sha256"],
        actual_producer_hashes["klean.py"],
    )
    image_id = generator_manifest["provenance"]["generator_image_id"]
    check("source/generator image ID", source_manifest["generator_image_id"], image_id)
    check(
        "audit producer path/image binding",
        Path(resolution["generation_producer_sources"]).name,
        image_id.removeprefix("sha256:"),
    )
    check(
        "producer bundle tree SHA-256",
        pipeline_tree_hash(PRODUCERS),
        hashes["generation_producer_sources_sha256"],
    )

    print("\n== Stage 3 inventory and manifest bijection ==")
    inventory = inventory_verification(K_PROOF)
    validated = validate_trust_boundary(K_PROOF, DISCOVERY)
    check("inventory_sha256", inventory["inventory_sha256"], discovery["inventory_sha256"])
    canonical_ids = [entry["source_rule_id"] for entry in inventory["rules"]]
    manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
    check("exact rule ID order", manifest_ids, canonical_ids)
    check("unique manifest IDs", len(manifest_ids), len(set(manifest_ids)))
    check("manifest/inventory rule count", len(manifest_ids), len(inventory["rules"]))
    check("verification SHA-256", inventory["verification_sha256"], file_hash(K_PROOF / "verification.k"))
    check("validated definition count", len(validated["definitions"]), 2)
    check("validated operational-rule count", len(validated["operational_rules"]), 0)
    check("validated proved-derived-lemma count", len(validated["proved_derived_lemmas"]), 0)
    check("validated domain-lemma count", len(validated["domain_lemmas"]), 0)
    for index, rule in enumerate(inventory["rules"]):
        normalized = " ".join(rule["text"].split())
        normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
        check(f"rule {index} normalized_sha256", normalized_hash, rule["normalized_sha256"])
        check(f"rule {index} source_rule_id", rule["source_rule_id"], f"rule-{normalized_hash}")
        check(f"rule {index} source span", (rule["start_line"], rule["end_line"]), ((12, 12), (13, 14))[index])
        check(f"rule {index} classification", discovery["rules"][index]["classification"], "DEFINITION")

    print("\n== audit-input source and tree hashes ==")
    check("stage1 source hash map", regular_file_map(K_PROOF), resolution["stage1_source_hashes"])
    check("k_workspace_sha256", pipeline_tree_hash(K_PROOF), hashes["k_workspace_sha256"])
    check("stage1_export_sha256", exporter_tree_hash(K_PROOF), hashes["stage1_export_sha256"])
    check("k_audit_sha256", pipeline_tree_hash(K_AUDIT), hashes["k_audit_sha256"])
    check("klean_generation_sha256", pipeline_tree_hash(GENERATION), hashes["klean_generation_sha256"])
    check("discovery_manifest_sha256", file_hash(DISCOVERY), hashes["discovery_manifest_sha256"])
    check("generated_tree_sha256", exporter_tree_hash(GENERATED), hashes["generated_tree_sha256"])
    check("Lean workspace hash absent", hashes["lean_workspace_sha256"], None)
    check("Lean invocation hash absent", hashes["lean_invocation_sha256"], None)

    frozen_hash = exporter_tree_hash(K_PROOF)
    discovery_hash = file_hash(DISCOVERY)
    generated_hash = exporter_tree_hash(GENERATED)
    trust_hash = file_hash(GENERATION / "trust-inventory.json")
    verification_hash = file_hash(K_PROOF / "verification.k")
    obligation_map_hash = file_hash(GENERATED / "obligation-map.json")

    print("\n== Stage 4 sidecar hashes and identities ==")
    for label, value in (
        ("input frozen_input_sha256", input_manifest["frozen_input_sha256"]),
        ("input stage1_workspace_sha256", input_manifest["stage1_workspace_sha256"]),
        ("generator provenance stage1_workspace_sha256", generator_manifest["provenance"]["stage1_workspace_sha256"]),
        ("export frozen_input_sha256", export_result["frozen_input_sha256"]),
        ("preflight frozen_input_sha256", recorded_preflight["frozen_input_sha256"]),
        ("preflight stage1_workspace_sha256", recorded_preflight["stage1_workspace_sha256"]),
    ):
        check(label, value, frozen_hash)
    for label, value in (
        ("input discovery hash", input_manifest["stage3_discovery_manifest_sha256"]),
        ("generator provenance discovery hash", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"]),
        ("export discovery hash", export_result["stage3_discovery_manifest_sha256"]),
        ("preflight discovery hash", recorded_preflight["stage3_discovery_manifest_sha256"]),
    ):
        check(label, value, discovery_hash)
    for label, value in (
        ("generator generated-tree hash", generator_manifest["generated_tree_sha256"]),
        ("export generated-tree hash", export_result["generated_tree_sha256"]),
        ("preflight generated-tree hash", recorded_preflight["generated_tree_sha256"]),
    ):
        check(label, value, generated_hash)
    check("input verification hash", input_manifest["verification_sha256"], verification_hash)
    check("input inventory hash", input_manifest["inventory_sha256"], inventory["inventory_sha256"])
    check("generator inventory hash", generator_manifest["provenance"]["inventory_sha256"], inventory["inventory_sha256"])
    check("generator obligation-map hash", generator_manifest["obligation_map_sha256"], obligation_map_hash)
    check("export trust-inventory hash", export_result["trust_inventory_sha256"], trust_hash)
    check("generator toolchain lock", generator_manifest["toolchain"], read_json(REFERENCE / "klean-toolchain.lock.json"))
    check("input definition projection", input_manifest["definitions"], validated["definitions"])
    check("input operational projection", input_manifest["operational_rules"], [])
    check("input proved-derived projection", input_manifest["proved_derived_lemmas"], [])
    check("input source-rule obligations", input_manifest["source_rules"], [])
    check("generator obligation count", generator_manifest["obligation_count"], 0)
    check("export obligation count", export_result["obligation_count"], 0)
    check("preflight obligation count", recorded_preflight["obligation_count"], 0)
    check(
        "obligation map",
        read_json(GENERATED / "obligation-map.json"),
        {
            "obligations": [],
            "schema_version": 3,
            "source_rules": [],
            "trust_parameters": [],
        },
    )
    check("generator target", generator_manifest["target"], None)
    check("recorded preflight target", recorded_preflight["target"], None)
    check("audit-input target", resolution["target"], None)
    check("audit-input Stage 5 result", audit.get("stage5_result"), None)
    check("candidate absent", Path("/candidate").exists(), False)
    check("selected Stage 4 status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
    check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
    check("recorded preflight status", recorded_preflight["status"], "KLEAN_NO_OBLIGATIONS")

    print("\nALL INDEPENDENT STRUCTURAL CHECKS PASSED")


if __name__ == "__main__":
    main()
