#!/usr/bin/env python3
"""Independent hash, obligation-bijection, and target-identity audit."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def regular_entries(root: Path) -> list[tuple[str, str, Path]]:
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
                raise AssertionError(f"linked or unsupported entry: {path}")
    return sorted(entries)


def pipeline_tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in regular_entries(root):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            size = path.stat(follow_symlinks=False).st_size
            digest.update(size.to_bytes(8, "big"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def export_tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for relative, kind, path in regular_entries(root):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


checks: list[tuple[str, bool, object]] = []


def check(label: str, observed: object, expected: object) -> None:
    checks.append((label, observed == expected, (observed, expected)))


audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
recorded_hashes = resolution["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
obligation_map_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
obligation_map = json.loads(obligation_map_path.read_text())
inventory = json.loads(
    Path("/audit-output/evidence/reconstructed-rule-inventory.json").read_text()
)
discovery_path = Path("/reference/lemma-discovery.json")
discovery = json.loads(discovery_path.read_text())

# Launcher-recorded mounted-input hashes.
mounted_trees = {
    "k_workspace_sha256": Path("/reference/k-proof"),
    "k_audit_sha256": Path("/reference/k-audit"),
    "klean_generation_sha256": Path("/reference/klean-generation"),
    "generation_producer_sources_sha256": Path("/reference/generation-tools"),
    "lean_workspace_sha256": Path("/candidate"),
}
for field, path in mounted_trees.items():
    check(field, pipeline_tree_hash(path), recorded_hashes[field])
check(
    "stage1_export_sha256",
    export_tree_hash(Path("/reference/k-proof")),
    recorded_hashes["stage1_export_sha256"],
)
check(
    "discovery_manifest_sha256",
    sha256_file(discovery_path),
    recorded_hashes["discovery_manifest_sha256"],
)
check(
    "generated_tree_sha256",
    export_tree_hash(Path("/reference/klean-generation/generated")),
    recorded_hashes["generated_tree_sha256"],
)

# Every launcher-recorded Stage 1 regular-file hash.
source_hashes = resolution["stage1_source_hashes"]
for relative, expected in source_hashes.items():
    path = Path("/reference/k-proof") / relative
    check(f"stage1_source_hash:{relative}", sha256_file(path), expected)
check(
    "stage1_source_hash file count",
    len(source_hashes),
    sum(kind == "file" for _, kind, _ in regular_entries(Path("/reference/k-proof"))),
)

# Producer provenance and immutable image identity.
producer_hashes = {
    name: sha256_file(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
check("producer files", producer_hashes, source_manifest["files"])
check("exporter hash", producer_hashes["klean_export.py"], generator["exporter_sha256"])
check("klean.py hash", producer_hashes["klean.py"], generator["klean_py_sha256"])
image_id = source_manifest["generator_image_id"]
check("generator image manifest", generator["provenance"]["generator_image_id"], image_id)
check(
    "generator image launcher path",
    Path(resolution["generation_producer_sources"]).name,
    image_id.removeprefix("sha256:"),
)

# Manifest provenance and sidecar hashes.
check(
    "generator generated tree",
    generator["generated_tree_sha256"],
    recorded_hashes["generated_tree_sha256"],
)
check(
    "generator obligation map hash",
    generator["obligation_map_sha256"],
    sha256_file(obligation_map_path),
)
check(
    "generator Stage 1 provenance",
    generator["provenance"]["stage1_workspace_sha256"],
    recorded_hashes["stage1_export_sha256"],
)
check(
    "generator Stage 3 provenance",
    generator["provenance"]["stage3_discovery_manifest_sha256"],
    recorded_hashes["discovery_manifest_sha256"],
)
check(
    "generator inventory provenance",
    generator["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "input manifest Stage 1",
    input_manifest["stage1_workspace_sha256"],
    recorded_hashes["stage1_export_sha256"],
)
check(
    "input manifest frozen input",
    input_manifest["frozen_input_sha256"],
    recorded_hashes["stage1_export_sha256"],
)
check(
    "input manifest Stage 3",
    input_manifest["stage3_discovery_manifest_sha256"],
    recorded_hashes["discovery_manifest_sha256"],
)
check("input manifest inventory", input_manifest["inventory_sha256"], inventory["inventory_sha256"])
check(
    "input manifest verification",
    input_manifest["verification_sha256"],
    sha256_file(Path("/reference/k-proof/verification.k")),
)
check(
    "export Stage 1",
    export_result["frozen_input_sha256"],
    recorded_hashes["stage1_export_sha256"],
)
check(
    "export Stage 3",
    export_result["stage3_discovery_manifest_sha256"],
    recorded_hashes["discovery_manifest_sha256"],
)
check(
    "export generated tree",
    export_result["generated_tree_sha256"],
    recorded_hashes["generated_tree_sha256"],
)
check(
    "export trust inventory",
    export_result["trust_inventory_sha256"],
    sha256_file(Path("/reference/klean-generation/trust-inventory.json")),
)

# Independently classified true domain set and exact source-rule bijection.
domain_ids = [
    "rule-9345c98e84d84ccfaeba7d804fe62d2d3a9744b1ef482585fa67ea3fb0a09b97",
    "rule-1bc30aceb4ec6e423c8f79079ea7b1c195de5d88396229aa8ee74794085384fa",
]
discovery_by_id = {item["source_rule_id"]: item for item in discovery["rules"]}
inventory_by_id = {item["source_rule_id"]: item for item in inventory["rules"]}
check(
    "independent domain classifications in Stage 3",
    [discovery_by_id[source_id]["classification"] for source_id in domain_ids],
    ["DOMAIN_LEMMA", "DOMAIN_LEMMA"],
)
check(
    "Stage 3 has no other domain classifications",
    [
        item["source_rule_id"]
        for item in discovery["rules"]
        if item["classification"] == "DOMAIN_LEMMA"
    ],
    domain_ids,
)
check(
    "input source rule IDs",
    [item["source_rule_id"] for item in input_manifest["source_rules"]],
    domain_ids,
)
check(
    "obligation-map source rule IDs",
    [item["source_rule_id"] for item in obligation_map["source_rules"]],
    domain_ids,
)
check("source rules copied identically", obligation_map["source_rules"], input_manifest["source_rules"])

expected_conjuncts = [
    "∀ (C : SortValSeq) (B : SortValSeq) (A : SortValSeq), "
    "(«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» "
    "(«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A B) C : SortValSeq) = "
    "(«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A "
    "(«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» B C) : SortValSeq)",
    "∀ (A : SortValSeq), "
    "(«valSeqConcat(_,_)_MPY-LIST_ValSeq_ValSeq_ValSeq» A "
    "SortValSeq.«.ValSeq_MPY-CORE_ValSeq» : SortValSeq) = (A : SortValSeq)",
]
obligations = obligation_map["obligations"]
check("obligation count", len(obligations), 2)
check(
    "obligation ordered IDs",
    [item["source_rule_id"] for item in obligations],
    domain_ids,
)
check(
    "obligation IDs unique",
    len({item["source_rule_id"] for item in obligations}),
    len(obligations),
)
check(
    "exact non-weakened Lean conjuncts",
    [item["lean_conjunct"] for item in obligations],
    expected_conjuncts,
)
for item, source_id in zip(obligations, domain_ids, strict=True):
    source = inventory_by_id[source_id]
    check(
        f"{source_id}:source span",
        item["source_span"],
        {"start_line": source["start_line"], "end_line": source["end_line"]},
    )
    check(f"{source_id}:normalized hash", item["normalized_sha256"], source["normalized_sha256"])
    check(f"{source_id}:inventory hash", item["inventory_sha256"], inventory["inventory_sha256"])
    check(
        f"{source_id}:discovery hash",
        item["discovery_manifest_sha256"],
        sha256_file(discovery_path),
    )
    check(
        f"{source_id}:conjunct hash",
        item["lean_conjunct_sha256"],
        sha256_bytes(item["lean_conjunct"].encode()),
    )

# Exact target definition, parameter binding, and cross-manifest identity.
parameter = obligation_map["trust_parameters"][0]
binding = {
    key: parameter[key]
    for key in ("kore_symbol", "name", "type", "source_rule_ids")
}
binding_json = json.dumps(binding, sort_keys=True, separators=(",", ":"))
check("target parameter binding hash", parameter["binding_sha256"], sha256_bytes(binding_json.encode()))
check("target parameter source IDs", parameter["source_rule_ids"], domain_ids)
check("single target parameter", len(obligation_map["trust_parameters"]), 1)

expected_definition = (
    "def targetStatement\n"
    f"    ({parameter['name']} : {parameter['type']})\n"
    "    : Prop :=\n"
    f"    ({expected_conjuncts[0]})\n"
    f"    ∧ ({expected_conjuncts[1]})"
)
lemmas_text = Path(
    "/reference/klean-generation/generated/Klean96CountUpTo/Lemmas.lean"
).read_text()
raw_targets = re.findall(r"(?m)^\s*def\s+targetStatement\b", lemmas_text)
target_matches = re.findall(
    r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
    lemmas_text,
)
check("single generated target declaration", len(raw_targets), 1)
check("single generated target definition", len(target_matches), 1)
actual_definition = target_matches[0].strip()
check("exact target definition", actual_definition, expected_definition)

statement = f"Klean96CountUpTo.Lemmas.targetStatement {parameter['name']}"
target = {
    "declaration": "Klean96CountUpTo.Lemmas.targetStatement",
    "file": "Klean96CountUpTo/Lemmas.lean",
    "statement": statement,
    "statement_sha256": sha256_bytes(statement.encode()),
    "definition_sha256": sha256_bytes(actual_definition.encode()),
    "parameters": [parameter],
}
check("generator target identity", generator["target"], target)
check("audit-input target identity", resolution["target"], target)
check("audit-input preflight target identity", resolution["stage4_preflight"]["target"], target)
check("generator obligation count", generator["obligation_count"], 2)
check("export obligation count", export_result["obligation_count"], 2)
check("preflight obligation count", resolution["stage4_preflight"]["obligation_count"], 2)
check("export status", export_result["status"], "OK")

failures = []
for label, passed, values in checks:
    if not passed:
        failures.append((label, values))
        print(f"FAIL: {label}\n  observed={values[0]!r}\n  expected={values[1]!r}")
print(f"CHECK_COUNT={len(checks)}")
print(f"FAILURE_COUNT={len(failures)}")
print(f"RESULT={'FAIL' if failures else 'PASS'}")
raise SystemExit(1 if failures else 0)
