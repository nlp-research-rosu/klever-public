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


REFERENCE = Path("/reference")
AUDIT_INPUT = Path("/audit-input.json")


def read_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text())
    if not isinstance(document, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return document


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_tree_entries(root: Path) -> list[tuple[str, str, Path]]:
    if not root.is_dir() or root.is_symlink():
        raise AssertionError(f"unsafe tree root: {root}")
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
                raise AssertionError(f"linked or unsupported tree entry: {path}")
    return sorted(entries)


def pipeline_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in regular_tree_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            content = path.read_bytes()
            digest.update(len(content).to_bytes(8, "big"))
            digest.update(content)
    return digest.hexdigest()


def klean_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in regular_tree_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def canonical_json_sha256(document: Any) -> str:
    encoded = json.dumps(
        document,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


checks: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    checks.append((name, condition, detail))


audit = read_json(AUDIT_INPUT)
resolution = audit["resolution"]
audit_hashes = resolution["hashes"]
source_manifest = read_json(REFERENCE / "generation-tools/source-manifest.json")
discovery = read_json(REFERENCE / "lemma-discovery.json")
reconstructed = read_json(
    Path("/audit-output/evidence/reconstructed-inventory.json")
)
input_manifest = read_json(
    REFERENCE / "klean-generation/input-manifest.json"
)
generator_manifest = read_json(
    REFERENCE / "klean-generation/generator-manifest.json"
)
export_result = read_json(
    REFERENCE / "klean-generation/export-result.json"
)
recorded_preflight = read_json(
    REFERENCE / "klean-generation/preflight.json"
)
trust_inventory = read_json(
    REFERENCE / "klean-generation/trust-inventory.json"
)
obligation_map = read_json(
    REFERENCE / "klean-generation/generated/obligation-map.json"
)
toolchain_lock = read_json(REFERENCE / "klean-toolchain.lock.json")

producer_exporter = REFERENCE / "generation-tools/klean_export.py"
producer_klean = REFERENCE / "generation-tools/klean.py"
exporter_hash = sha256_file(producer_exporter)
klean_hash = sha256_file(producer_klean)
check(
    "producer klean_export.py hash agrees everywhere",
    exporter_hash
    == source_manifest["files"]["klean_export.py"]
    == generator_manifest["exporter_sha256"],
    exporter_hash,
)
check(
    "producer klean.py hash agrees everywhere",
    klean_hash
    == source_manifest["files"]["klean.py"]
    == generator_manifest["klean_py_sha256"],
    klean_hash,
)
producer_tree_hash = pipeline_tree_sha256(
    REFERENCE / "generation-tools"
)
check(
    "producer source tree matches audit input",
    producer_tree_hash
    == audit_hashes["generation_producer_sources_sha256"],
    producer_tree_hash,
)
image_from_path = Path(
    resolution["generation_producer_sources"]
).name
image_from_source_manifest = source_manifest["generator_image_id"]
image_from_generator = generator_manifest["provenance"][
    "generator_image_id"
]
check(
    "immutable generator image identity agrees",
    image_from_source_manifest
    == image_from_generator
    == f"sha256:{image_from_path}",
    image_from_generator,
)

pipeline_trees = {
    "k_workspace_sha256": REFERENCE / "k-proof",
    "k_audit_sha256": REFERENCE / "k-audit",
    "klean_generation_sha256": REFERENCE / "klean-generation",
}
for field, path in pipeline_trees.items():
    actual = pipeline_tree_sha256(path)
    check(
        f"{field} matches audit input",
        actual == audit_hashes[field],
        actual,
    )

stage1_export_hash = klean_tree_sha256(REFERENCE / "k-proof")
generated_tree_hash = klean_tree_sha256(
    REFERENCE / "klean-generation/generated"
)
discovery_hash = sha256_file(REFERENCE / "lemma-discovery.json")
verification_hash = sha256_file(
    REFERENCE / "k-proof/verification.k"
)
obligation_map_hash = sha256_file(
    REFERENCE / "klean-generation/generated/obligation-map.json"
)
trust_inventory_hash = sha256_file(
    REFERENCE / "klean-generation/trust-inventory.json"
)

check(
    "Stage 1 export tree hash matches audit input",
    stage1_export_hash == audit_hashes["stage1_export_sha256"],
    stage1_export_hash,
)
check(
    "generated tree hash matches audit input",
    generated_tree_hash == audit_hashes["generated_tree_sha256"],
    generated_tree_hash,
)
check(
    "discovery file hash matches audit input",
    discovery_hash == audit_hashes["discovery_manifest_sha256"],
    discovery_hash,
)

stage1_observers = [
    input_manifest["frozen_input_sha256"],
    input_manifest["stage1_workspace_sha256"],
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    export_result["frozen_input_sha256"],
    recorded_preflight["frozen_input_sha256"],
    recorded_preflight["stage1_workspace_sha256"],
    resolution["stage4_preflight"]["frozen_input_sha256"],
    resolution["stage4_preflight"]["stage1_workspace_sha256"],
]
check(
    "Stage 1 export hash agrees across all Stage 4 records",
    all(value == stage1_export_hash for value in stage1_observers),
)
discovery_observers = [
    input_manifest["stage3_discovery_manifest_sha256"],
    generator_manifest["provenance"][
        "stage3_discovery_manifest_sha256"
    ],
    export_result["stage3_discovery_manifest_sha256"],
    recorded_preflight["stage3_discovery_manifest_sha256"],
    resolution["stage4_preflight"][
        "stage3_discovery_manifest_sha256"
    ],
]
check(
    "Stage 3 manifest hash agrees across all Stage 4 records",
    all(value == discovery_hash for value in discovery_observers),
)
generated_observers = [
    generator_manifest["generated_tree_sha256"],
    export_result["generated_tree_sha256"],
    recorded_preflight["generated_tree_sha256"],
    resolution["stage4_preflight"]["generated_tree_sha256"],
]
check(
    "generated tree hash agrees across all Stage 4 records",
    all(value == generated_tree_hash for value in generated_observers),
)
check(
    "verification.k hash agrees with deterministic input manifest",
    input_manifest["verification_sha256"] == verification_hash,
    verification_hash,
)
check(
    "obligation map file hash agrees with generator manifest",
    generator_manifest["obligation_map_sha256"] == obligation_map_hash,
    obligation_map_hash,
)
check(
    "trust inventory file hash agrees with export result",
    export_result["trust_inventory_sha256"] == trust_inventory_hash,
    trust_inventory_hash,
)
check(
    "pinned toolchain object agrees with generator manifest",
    generator_manifest["toolchain"] == toolchain_lock,
)

recorded_stage1_files = resolution["stage1_source_hashes"]
current_stage1_files = {
    relative: sha256_file(path)
    for relative, kind, path in regular_tree_entries(
        REFERENCE / "k-proof"
    )
    if kind == "file"
}
check(
    "complete Stage 1 source file map is exact",
    current_stage1_files == recorded_stage1_files,
    (
        f"recorded={len(recorded_stage1_files)} "
        f"current={len(current_stage1_files)}"
    ),
)
check(
    "resolved audit input canonical hash is exact",
    canonical_json_sha256(resolution) == audit["resolved_input_sha256"],
    canonical_json_sha256(resolution),
)
check(
    "selected Stage 2 artifact hash agrees",
    resolution["selections"]["k_audit"]["artifact_sha256"]
    == audit_hashes["k_audit_sha256"],
)
check(
    "selected Stage 4 artifact hash agrees",
    resolution["selections"]["klean_generation"]["artifact_sha256"]
    == audit_hashes["klean_generation_sha256"],
)

rules = reconstructed["rules"]
discovery_rules = discovery["rules"]
rule_ids = [rule["source_rule_id"] for rule in rules]
discovery_ids = [rule["source_rule_id"] for rule in discovery_rules]
check(
    "reconstructed inventory hash is canonical over ordered rules",
    canonical_json_sha256(rules) == reconstructed["inventory_sha256"],
    reconstructed["inventory_sha256"],
)
check(
    "reconstructed and Stage 3 inventory hashes agree",
    reconstructed["inventory_sha256"]
    == discovery["inventory_sha256"]
    == input_manifest["inventory_sha256"]
    == generator_manifest["provenance"]["inventory_sha256"],
)
check(
    "reconstructed and Stage 3 ordered identities are bijective",
    rule_ids == discovery_ids
    and len(rule_ids) == len(set(rule_ids))
    and len(discovery_ids) == len(set(discovery_ids)),
)

# This is the audit's independent semantic classification, not copied from
# Stage 3: the sole rule is the ordinary verifyBF execution-scheduling step.
independent_classification = {
    "rule-6f56e984cb3d0fc19ad90190688aabe5b4fa9cd665cd8ddc4bb1e7b98d9eb69f":
        "OPERATIONAL_RULE"
}
observed_classification = {
    rule["source_rule_id"]: rule["classification"]
    for rule in discovery_rules
}
check(
    "independent classifications agree exactly with Stage 3",
    observed_classification == independent_classification,
)
check(
    "all simplification rules have permitted classifications",
    all(
        "simplification" not in rule["attributes"]
        or independent_classification[rule["source_rule_id"]]
        in {"DEFINITION", "DOMAIN_LEMMA"}
        for rule in rules
    ),
)

discovery_by_id = {
    rule["source_rule_id"]: rule for rule in discovery_rules
}
merged_rules = [
    {
        **rule,
        "classification": discovery_by_id[rule["source_rule_id"]][
            "classification"
        ],
        "rationale": discovery_by_id[rule["source_rule_id"]][
            "rationale"
        ],
    }
    for rule in rules
]
expected_operational = [
    rule
    for rule in merged_rules
    if rule["classification"] == "OPERATIONAL_RULE"
]
check(
    "deterministic input operational-rule list is exact",
    input_manifest["operational_rules"] == expected_operational,
)
check(
    "deterministic input has no unaccounted classifications",
    input_manifest["definitions"] == []
    and input_manifest["proved_derived_lemmas"] == []
    and input_manifest["source_rules"] == []
    and input_manifest["summary_functions"] == [],
)

independent_domain_ids: list[str] = []
map_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]
check(
    "independent domain set maps bijectively to source rules",
    map_source_ids == independent_domain_ids
    and len(map_source_ids) == len(set(map_source_ids)),
)
check(
    "source rules map bijectively and in order to obligations",
    obligation_ids == independent_domain_ids
    and len(obligation_ids) == len(set(obligation_ids)),
)
check(
    "zero obligations have no trust parameters or conjuncts",
    obligation_map["trust_parameters"] == []
    and obligation_map["obligations"] == [],
)
check(
    "all obligation counts are exactly zero",
    generator_manifest["obligation_count"]
    == export_result["obligation_count"]
    == recorded_preflight["obligation_count"]
    == resolution["stage4_preflight"]["obligation_count"]
    == 0,
)
check(
    "all Stage 4 statuses are KLEAN_NO_OBLIGATIONS",
    export_result["status"]
    == recorded_preflight["status"]
    == resolution["stage4_preflight"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
)

target_declarations: list[str] = []
for relative, kind, path in regular_tree_entries(
    REFERENCE / "klean-generation/generated"
):
    if kind == "file" and path.suffix == ".lean":
        for match in re.finditer(
            r"(?m)^\s*def\s+targetStatement\b",
            path.read_text(),
        ):
            target_declarations.append(
                f"{relative}:{path.read_text().count(chr(10), 0, match.start()) + 1}"
            )
check(
    "zero obligations generate no target declaration",
    target_declarations == [],
    repr(target_declarations),
)
check(
    "all recorded target identities are null",
    generator_manifest["target"] is None
    and recorded_preflight["target"] is None
    and resolution["stage4_preflight"]["target"] is None
    and resolution["target"] is None,
)
check(
    "classification-only mode has no Stage 5 candidate",
    resolution["mode"] == "CLASSIFICATION_ONLY"
    and resolution["stage5_result"] is None
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and not Path("/candidate").exists(),
)
check(
    "problem, condition, and semantics mode are exact",
    resolution["problem_id"] == "148-bf"
    and resolution["condition"] == "bare"
    and resolution["semantics_mode"] == "GENERATED_SEMANTICS",
)
check(
    "trust inventory has no proof holes",
    trust_inventory["designated_sorries"] == 0
    and trust_inventory["other_sorries"] == 0,
)

for name, passed, detail in checks:
    suffix = f" [{detail}]" if detail else ""
    print(f"{'PASS' if passed else 'FAIL'}: {name}{suffix}")

failed = [name for name, passed, _detail in checks if not passed]
print(f"TOTAL_CHECKS={len(checks)}")
print(f"FAILED_CHECKS={len(failed)}")
if failed:
    print("FAILED_NAMES=" + json.dumps(failed))
    sys.exit(1)
