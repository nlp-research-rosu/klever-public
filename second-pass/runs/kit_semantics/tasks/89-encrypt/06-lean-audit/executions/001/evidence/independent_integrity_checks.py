#!/usr/bin/env python3
"""Independent read-only integrity checks for the 89-encrypt audit."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path

from tools import (
    k_rule_inventory,
    lemma_discovery_contract,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
LOCK = Path("/reference/klean-toolchain.lock.json")


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict), path
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def generated_tree_digest(root: Path) -> str:
    """Reimplement the generation-time klean_export.tree_digest framing."""

    assert root.is_dir() and not root.is_symlink()
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
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
                raise AssertionError(f"unsupported generated entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def report(label: str, value: object = "PASS") -> None:
    print(f"{label}: {value}")


audit = load_json(AUDIT_INPUT)
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(audit)
assert resolved_digest == audit["resolved_input_sha256"]
assert canonical_sha256(resolution) == resolved_digest
assert os.environ.get("AUDIT_MODE") == "CLASSIFICATION_ONLY"
assert resolution["mode"] == "CLASSIFICATION_ONLY"
assert resolution["semantics_mode"] == "SUPPLIED_SEMANTICS"
assert resolution["problem_id"] == "89-encrypt"
assert resolution["condition"] == "kit-semantics"
report("signed audit-input envelope", resolved_digest)
report("launcher mode", resolution["mode"])

generator_manifest = load_json(GENERATION / "generator-manifest.json")
source_manifest = load_json(PRODUCERS / "source-manifest.json")
producer_names = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in PRODUCERS.iterdir()
)
assert producer_names == ["klean.py", "klean_export.py", "source-manifest.json"]
expected_producer_files = {
    "klean.py": generator_manifest["klean_py_sha256"],
    "klean_export.py": generator_manifest["exporter_sha256"],
}
assert source_manifest == {
    "schema_version": 1,
    "generator_image_id": generator_manifest["provenance"]["generator_image_id"],
    "files": expected_producer_files,
}
for name, expected_hash in expected_producer_files.items():
    assert sha256_file(PRODUCERS / name) == expected_hash
image_id = generator_manifest["provenance"]["generator_image_id"]
assert image_id.startswith("sha256:")
assert Path(resolution["generation_producer_sources"]).name == image_id.split(":", 1)[1]
producer_tree = pipeline_contract.sha256_tree(PRODUCERS)
assert producer_tree == resolution["hashes"]["generation_producer_sources_sha256"]
report("producer image", image_id)
report("producer tree SHA-256", producer_tree)
for name, digest in expected_producer_files.items():
    report(f"producer {name} SHA-256", digest)

inventory = k_rule_inventory.inventory_verification(WORKSPACE)
validated = lemma_discovery_contract.validate_trust_boundary(WORKSPACE, DISCOVERY)
discovery = load_json(DISCOVERY)
canonical_rules = inventory["rules"]
manifest_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
canonical_ids = [entry["source_rule_id"] for entry in canonical_rules]
assert manifest_ids == canonical_ids
assert len(canonical_ids) == len(set(canonical_ids)) == 9
assert canonical_sha256(canonical_rules) == inventory["inventory_sha256"]
assert discovery["inventory_sha256"] == inventory["inventory_sha256"]

verification_text = (WORKSPACE / "verification.k").read_text()
verification_lines = verification_text.splitlines()
for rule in canonical_rules:
    source_slice = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    assert source_slice == rule["text"]
    normalized = " ".join(source_slice.split())
    normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
    assert normalized_hash == rule["normalized_sha256"]
    assert rule["source_rule_id"] == f"rule-{normalized_hash}"

# This is the independent substantive reclassification used by this audit.
independent_classification = {source_rule_id: "DEFINITION" for source_rule_id in canonical_ids}
observed_classification = {
    entry["source_rule_id"]: entry["classification"] for entry in discovery["rules"]
}
assert observed_classification == independent_classification
assert not validated["operational_rules"]
assert not validated["proved_derived_lemmas"]
assert not validated["domain_lemmas"]
assert len(validated["definitions"]) == 9
assert all("simplification" not in rule["attributes"] for rule in canonical_rules)
assert all("<k>" not in rule["text"] for rule in canonical_rules)
report("verification module closure", inventory["verification_modules"])
report("canonical rule count", len(canonical_rules))
report("canonical inventory SHA-256", inventory["inventory_sha256"])
report("ordered Stage 3 identity bijection")
report("independent classifications", "9 DEFINITION; 0 DOMAIN_LEMMA")

hashes = resolution["hashes"]
workspace_pipeline_hash = pipeline_contract.sha256_tree(WORKSPACE)
workspace_export_hash = generated_tree_digest(WORKSPACE)
discovery_hash = sha256_file(DISCOVERY)
k_audit_hash = pipeline_contract.sha256_tree(K_AUDIT)
generation_hash = pipeline_contract.sha256_tree(GENERATION)
generated_hash = generated_tree_digest(GENERATED)
assert workspace_pipeline_hash == hashes["k_workspace_sha256"]
assert workspace_export_hash == hashes["stage1_export_sha256"]
assert discovery_hash == hashes["discovery_manifest_sha256"]
assert k_audit_hash == hashes["k_audit_sha256"]
assert generation_hash == hashes["klean_generation_sha256"]
assert generated_hash == hashes["generated_tree_sha256"]
assert generated_hash == generator_manifest["generated_tree_sha256"]

actual_source_hashes = {
    path.relative_to(WORKSPACE).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        WORKSPACE, "frozen Stage 1 workspace"
    )
}
assert actual_source_hashes == resolution["stage1_source_hashes"]
report("Stage 1 pipeline tree SHA-256", workspace_pipeline_hash)
report("Stage 1 export tree SHA-256", workspace_export_hash)
report("Stage 1 per-file hash map entries", len(actual_source_hashes))
report("Stage 2 selected tree SHA-256", k_audit_hash)
report("Stage 3 manifest SHA-256", discovery_hash)
report("Stage 4 selected tree SHA-256", generation_hash)
report("generated project SHA-256", generated_hash)

input_manifest = load_json(GENERATION / "input-manifest.json")
export_result = load_json(GENERATION / "export-result.json")
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = load_json(obligation_map_path)
trust_inventory_path = GENERATION / "trust-inventory.json"
preflight = load_json(GENERATION / "preflight.json")
lock = load_json(LOCK)

assert input_manifest["frozen_input_sha256"] == workspace_export_hash
assert input_manifest["stage1_workspace_sha256"] == workspace_export_hash
assert input_manifest["stage3_discovery_manifest_sha256"] == discovery_hash
assert input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
assert input_manifest["verification_sha256"] == sha256_file(WORKSPACE / "verification.k")
assert input_manifest["definitions"] == validated["definitions"]
assert input_manifest["operational_rules"] == validated["operational_rules"] == []
assert input_manifest["proved_derived_lemmas"] == validated["proved_derived_lemmas"] == []
assert input_manifest["source_rules"] == []
assert generator_manifest["toolchain"] == lock
assert generator_manifest["provenance"] == {
    "generator_image_id": image_id,
    "inventory_sha256": inventory["inventory_sha256"],
    "stage1_workspace_sha256": workspace_export_hash,
    "stage3_discovery_manifest_sha256": discovery_hash,
}

assert obligation_map == {
    "schema_version": 3,
    "source_rules": [],
    "obligations": [],
    "trust_parameters": [],
}
obligation_map_hash = sha256_file(obligation_map_path)
assert obligation_map_hash == generator_manifest["obligation_map_sha256"]
assert generator_manifest["obligation_count"] == 0
assert generator_manifest["target"] is None
assert export_result["status"] == "KLEAN_NO_OBLIGATIONS"
assert export_result["obligation_count"] == 0
assert export_result["frozen_input_sha256"] == workspace_export_hash
assert export_result["stage3_discovery_manifest_sha256"] == discovery_hash
assert export_result["generated_tree_sha256"] == generated_hash
assert export_result["trust_inventory_sha256"] == sha256_file(trust_inventory_path)

target_definitions: list[str] = []
for lean_file in sorted(GENERATED.rglob("*.lean")):
    assert lean_file.is_file() and not lean_file.is_symlink()
    target_definitions.extend(
        match.group(0)
        for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", lean_file.read_text())
    )
assert target_definitions == []

assert resolution["target"] is None
assert resolution["lean_workspace"] is None
assert resolution["lean_invocation"] is None
assert resolution["stage5_result"] is None
assert hashes["lean_workspace_sha256"] is None
assert hashes["lean_invocation_sha256"] is None
assert not Path("/candidate").exists()
assert preflight == resolution["stage4_preflight"]
assert preflight["status"] == "KLEAN_NO_OBLIGATIONS"
assert preflight["target"] is None
assert preflight["obligation_count"] == 0
assert resolution["selections"]["klean_generation"]["status"] == "KLEAN_NO_OBLIGATIONS"
assert resolution["selections"]["klean_generation"]["artifact_sha256"] == generation_hash
assert resolution["selections"]["k_audit"]["artifact_sha256"] == k_audit_hash
report("obligation-map SHA-256", obligation_map_hash)
report("source-rule/obligation bijection", "empty to empty")
report("generated target declarations", 0)
report("Stage 5 candidate", "absent")
report("all independent integrity checks")
