#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, "/reference")
from tools.k_rule_inventory import inventory_verification


def fail(message: str) -> None:
    raise AssertionError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def read_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"unsafe JSON: {path}")
    value = json.loads(path.read_text())
    require(isinstance(value, dict), f"non-object JSON: {path}")
    return value


def file_sha256(path: Path) -> str:
    require(path.is_file() and not path.is_symlink(), f"unsafe file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: Any) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def tree_entries(root: Path) -> list[tuple[str, str, Path, int]]:
    require(root.is_dir() and not root.is_symlink(), f"unsafe tree root: {root}")
    result: list[tuple[str, str, Path, int]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for entry in os.scandir(directory):
            info = entry.stat(follow_symlinks=False)
            mode = info.st_mode
            if stat.S_ISDIR(mode):
                kind = "directory"
            elif stat.S_ISREG(mode):
                kind = "file"
            elif stat.S_ISLNK(mode):
                kind = "symlink"
            elif stat.S_ISFIFO(mode):
                kind = "fifo"
            elif stat.S_ISSOCK(mode):
                kind = "socket"
            elif stat.S_ISBLK(mode):
                kind = "block-device"
            elif stat.S_ISCHR(mode):
                kind = "character-device"
            else:
                kind = "unknown"
            path = Path(entry.path)
            result.append((path.relative_to(root).as_posix(), kind, path, info.st_size))
            if kind == "directory":
                pending.append(path)
    return sorted(result, key=lambda item: item[0])


def framed_update(digest: Any, value: bytes) -> None:
    digest.update(len(value).to_bytes(8, "big"))
    digest.update(value)


def pipeline_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path, size in tree_entries(root):
        require(kind in {"directory", "file"}, f"unsupported pipeline entry: {path}")
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            raw = path.read_bytes()
            require(len(raw) == size, f"file changed while hashing: {path}")
            digest.update(size.to_bytes(8, "big"))
            digest.update(raw)
    return digest.hexdigest()


def export_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path, _size in tree_entries(root):
        require(kind in {"directory", "file"}, f"unsupported export entry: {path}")
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


audit = read_json(Path("/audit-input.json"))
resolution = audit["resolution"]
hashes = resolution["hashes"]
require(
    audit["resolved_input_sha256"] == canonical_json_sha256(resolution),
    "signed audit resolution digest mismatch",
)

observed_trees = {
    "k_workspace_sha256": pipeline_tree_sha256(Path("/reference/k-proof")),
    "stage1_export_sha256": export_tree_sha256(Path("/reference/k-proof")),
    "k_audit_sha256": pipeline_tree_sha256(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_tree_sha256(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_tree_sha256(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": export_tree_sha256(
        Path("/reference/klean-generation/generated")
    ),
}
for name, observed in observed_trees.items():
    require(hashes[name] == observed, f"audit tree hash mismatch: {name}")

for relative, expected in resolution["stage1_source_hashes"].items():
    require(
        file_sha256(Path("/reference/k-proof") / relative) == expected,
        f"Stage 1 source hash mismatch: {relative}",
    )
require(
    sorted(resolution["stage1_source_hashes"])
    == sorted(
        relative
        for relative, kind, _path, _size in tree_entries(Path("/reference/k-proof"))
        if kind == "file"
    ),
    "Stage 1 source hash manifest has omissions or extras",
)

discovery_path = Path("/reference/lemma-discovery.json")
discovery = read_json(discovery_path)
discovery_sha = file_sha256(discovery_path)
require(
    discovery_sha == hashes["discovery_manifest_sha256"],
    "discovery manifest hash mismatch",
)

inventory = inventory_verification(Path("/reference/k-proof"))
verification_lines = Path("/reference/k-proof/verification.k").read_text().splitlines()
for rule in inventory["rules"]:
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    require(digest == rule["normalized_sha256"], "normalized rule hash mismatch")
    require(rule["source_rule_id"] == f"rule-{digest}", "source_rule_id mismatch")
    source_text = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    ).rstrip()
    require(source_text == rule["text"], "rule source span mismatch")
require(
    canonical_json_sha256(inventory["rules"]) == inventory["inventory_sha256"],
    "whole inventory hash mismatch",
)
require(
    inventory["inventory_sha256"] == discovery["inventory_sha256"],
    "inventory/discovery hash mismatch",
)

inventory_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
require(inventory_ids == discovery_ids, "discovery rule identities reordered or changed")
require(len(inventory_ids) == len(set(inventory_ids)), "duplicate inventory identity")
require(len(discovery_ids) == len(set(discovery_ids)), "duplicate discovery identity")

allowed_classes = {
    "DEFINITION",
    "OPERATIONAL_RULE",
    "PROVED_DERIVED_LEMMA",
    "DOMAIN_LEMMA",
}
for record in discovery["rules"]:
    require(
        record["classification"] in allowed_classes,
        "unknown Stage 3 classification",
    )
classes = [record["classification"] for record in discovery["rules"]]
require(classes == ["DEFINITION"] * 9 + ["OPERATIONAL_RULE"] * 3, "unexpected classes")
require(
    all("simplification" not in rule["attributes"] for rule in inventory["rules"]),
    "unexpected simplification rule",
)

source_manifest = read_json(Path("/reference/generation-tools/source-manifest.json"))
generator = read_json(Path("/reference/klean-generation/generator-manifest.json"))
input_manifest = read_json(Path("/reference/klean-generation/input-manifest.json"))
export_result = read_json(Path("/reference/klean-generation/export-result.json"))
preflight = read_json(Path("/reference/klean-generation/preflight.json"))
trust_inventory = Path("/reference/klean-generation/trust-inventory.json")
obligation_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
obligation_map = read_json(obligation_path)
lock = read_json(Path("/reference/klean-toolchain.lock.json"))

for filename, expected in source_manifest["files"].items():
    observed = file_sha256(Path("/reference/generation-tools") / filename)
    require(observed == expected, f"producer source manifest mismatch: {filename}")
require(
    generator["exporter_sha256"] == source_manifest["files"]["klean_export.py"],
    "generator exporter source hash mismatch",
)
require(
    generator["klean_py_sha256"] == source_manifest["files"]["klean.py"],
    "generator klean.py source hash mismatch",
)
producer_id = source_manifest["generator_image_id"]
require(
    generator["provenance"]["generator_image_id"] == producer_id,
    "generator image IDs differ",
)
require(
    producer_id
    == "sha256:" + Path(resolution["generation_producer_sources"]).name,
    "audit input producer-source path does not bind the generator image ID",
)
require(generator["toolchain"] == lock, "generator toolchain lock mismatch")

require(
    input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == observed_trees["stage1_export_sha256"],
    "Stage 1 export hash mismatch in input manifest",
)
require(
    generator["provenance"]["stage1_workspace_sha256"]
    == export_result["frozen_input_sha256"]
    == preflight["stage1_workspace_sha256"]
    == observed_trees["stage1_export_sha256"],
    "Stage 1 provenance hash mismatch",
)
require(
    input_manifest["stage3_discovery_manifest_sha256"]
    == generator["provenance"]["stage3_discovery_manifest_sha256"]
    == export_result["stage3_discovery_manifest_sha256"]
    == preflight["stage3_discovery_manifest_sha256"]
    == discovery_sha,
    "Stage 3 provenance hash mismatch",
)
require(
    input_manifest["verification_sha256"]
    == inventory["verification_sha256"]
    == resolution["stage1_source_hashes"]["verification.k"],
    "verification.k hash mismatch",
)
require(
    input_manifest["inventory_sha256"]
    == generator["provenance"]["inventory_sha256"]
    == inventory["inventory_sha256"],
    "inventory provenance mismatch",
)
require(
    generator["generated_tree_sha256"]
    == export_result["generated_tree_sha256"]
    == preflight["generated_tree_sha256"]
    == observed_trees["generated_tree_sha256"],
    "generated tree hash mismatch",
)
require(
    generator["obligation_map_sha256"] == file_sha256(obligation_path),
    "obligation-map file hash mismatch",
)
require(
    export_result["trust_inventory_sha256"] == file_sha256(trust_inventory),
    "trust-inventory file hash mismatch",
)
require(preflight == resolution["stage4_preflight"], "preflight/audit input mismatch")
require(
    resolution["selections"]["k_audit"]["artifact_sha256"]
    == observed_trees["k_audit_sha256"],
    "selected K audit artifact hash mismatch",
)
require(
    resolution["selections"]["klean_generation"]["artifact_sha256"]
    == observed_trees["klean_generation_sha256"],
    "selected generation artifact hash mismatch",
)

by_id = {record["source_rule_id"]: record for record in discovery["rules"]}
expected_records = [
    {
        **rule,
        "classification": by_id[rule["source_rule_id"]]["classification"],
        "rationale": by_id[rule["source_rule_id"]]["rationale"],
    }
    for rule in inventory["rules"]
]
require(
    input_manifest["definitions"]
    == [record for record in expected_records if record["classification"] == "DEFINITION"],
    "generated input definitions differ from Stage 1/Stage 3",
)
require(
    input_manifest["operational_rules"]
    == [
        record
        for record in expected_records
        if record["classification"] == "OPERATIONAL_RULE"
    ],
    "generated input operational rules differ from Stage 1/Stage 3",
)
require(input_manifest["proved_derived_lemmas"] == [], "unexpected derived lemmas")
require(input_manifest["summary_functions"] == [], "unexpected summary functions")

domain_records = [
    record for record in expected_records if record["classification"] == "DOMAIN_LEMMA"
]
require(domain_records == [], "independent classification has domain lemmas")
require(input_manifest["source_rules"] == [], "unexpected generated domain source rules")
require(obligation_map["source_rules"] == [], "obligation map source rules not empty")
require(obligation_map["obligations"] == [], "obligation map obligations not empty")
require(obligation_map["trust_parameters"] == [], "unexpected target parameters")
require(
    generator["obligation_count"]
    == export_result["obligation_count"]
    == preflight["obligation_count"]
    == 0,
    "zero-obligation counts disagree",
)
require(
    export_result["status"] == preflight["status"] == "KLEAN_NO_OBLIGATIONS",
    "no-obligation status mismatch",
)
require(
    generator["target"] is None
    and preflight["target"] is None
    and resolution["target"] is None,
    "unexpected recorded generated target",
)

target_declarations: list[str] = []
for relative, kind, path, _size in tree_entries(
    Path("/reference/klean-generation/generated")
):
    if kind == "file" and path.suffix == ".lean":
        for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", path.read_text()):
            target_declarations.append(f"{relative}:{match.start()}")
require(target_declarations == [], "zero obligations generated targetStatement")

require(resolution["mode"] == os.environ.get("AUDIT_MODE"), "AUDIT_MODE mismatch")
require(resolution["mode"] == "CLASSIFICATION_ONLY", "unexpected proof mode")
require(resolution["lean_workspace"] is None, "classification-only Lean workspace")
require(resolution["lean_invocation"] is None, "classification-only Lean invocation")
require(hashes["lean_workspace_sha256"] is None, "classification-only Lean hash")
require(hashes["lean_invocation_sha256"] is None, "classification-only invocation hash")
require(resolution["stage5_result"] is None, "classification-only Stage 5 result")
require(not os.path.lexists("/candidate"), "classification-only candidate exists")

print("INDEPENDENT_INTEGRITY: PASS")
print(f"resolved_input_sha256={audit['resolved_input_sha256']}")
for name, observed in observed_trees.items():
    print(f"{name}={observed}")
print(f"discovery_manifest_sha256={discovery_sha}")
print(f"inventory_rule_count={len(inventory_ids)}")
print(f"inventory_sha256={inventory['inventory_sha256']}")
print("classification_counts=DEFINITION:9,OPERATIONAL_RULE:3,DOMAIN_LEMMA:0,PROVED_DERIVED_LEMMA:0")
print("simplification_rule_count=0")
print(f"producer_image_id={producer_id}")
print("source_rule_count=0")
print("obligation_count=0")
print("targetStatement_count=0")
print("candidate_present=false")
