#!/usr/bin/env python3
"""Independent structural/hash audit of the selected Stage 4 generation."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path


AUDIT_INPUT = Path("/audit-input.json")
DISCOVERY = Path("/reference/lemma-discovery.json")
INVENTORY = Path("/audit-output/evidence/stage3/reconstructed-inventory.json")
KPROOF = Path("/reference/k-proof")
KAUDIT = Path("/reference/k-audit")
PRODUCERS = Path("/reference/generation-tools")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
CANDIDATE = Path("/candidate")


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    raw = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def producer_binding_hash(value: object) -> str:
    """Producer bindings use json.dumps' default ASCII escaping."""
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def pipeline_tree_hash(root: Path) -> str:
    """Reimplementation of the launcher's length-delimited tree contract."""
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
                raise RuntimeError(f"unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def klean_tree_hash(root: Path) -> str:
    """Reimplementation of the immutable producer's generated-tree contract."""
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
                raise RuntimeError(f"unsupported tree entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


def files_with_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"unexpected symlink: {path}")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = file_hash(path)
    return result


def check(name: str, actual: object, expected: object, report: dict) -> None:
    report[name] = {
        "actual": actual,
        "expected": expected,
        "ok": actual == expected,
    }


audit = json.loads(AUDIT_INPUT.read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
discovery = json.loads(DISCOVERY.read_text())
inventory = json.loads(INVENTORY.read_text())
input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
generator = json.loads((GENERATION / "generator-manifest.json").read_text())
obligation_map = json.loads((GENERATED / "obligation-map.json").read_text())
export_result = json.loads((GENERATION / "export-result.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
trust = json.loads((GENERATION / "trust-inventory.json").read_text())

report: dict[str, object] = {}

# Signed envelope and mounted launcher bindings.
check(
    "audit.resolved_input_sha256",
    canonical_hash(resolution),
    audit["resolved_input_sha256"],
    report,
)
check("launcher.discovery", file_hash(DISCOVERY), hashes["discovery_manifest_sha256"], report)
check("launcher.generated_tree", klean_tree_hash(GENERATED), hashes["generated_tree_sha256"], report)
check(
    "launcher.generation_producer_sources",
    pipeline_tree_hash(PRODUCERS),
    hashes["generation_producer_sources_sha256"],
    report,
)
check("launcher.k_audit", pipeline_tree_hash(KAUDIT), hashes["k_audit_sha256"], report)
check("launcher.k_workspace", pipeline_tree_hash(KPROOF), hashes["k_workspace_sha256"], report)
check(
    "launcher.klean_generation",
    pipeline_tree_hash(GENERATION),
    hashes["klean_generation_sha256"],
    report,
)
check("launcher.lean_workspace", pipeline_tree_hash(CANDIDATE), hashes["lean_workspace_sha256"], report)
check("launcher.stage1_export", klean_tree_hash(KPROOF), hashes["stage1_export_sha256"], report)
check(
    "launcher.stage1_source_hashes",
    files_with_hashes(KPROOF),
    resolution["stage1_source_hashes"],
    report,
)

# The successful invocation directory itself is deliberately not among the
# mounted audit inputs. Its digest therefore cannot be recomputed here; its
# file-level commitments remain covered by the signed resolution envelope.
report["launcher.lean_invocation"] = {
    "recorded": hashes["lean_invocation_sha256"],
    "mounted": False,
    "reason": "no Stage 5 invocation directory is present in the audit mount contract",
}

# Reconstruct exact Stage 3 records expected in the Stage 4 manifests.
inv_by_id = {rule["source_rule_id"]: rule for rule in inventory["rules"]}
discovery_by_id = {rule["source_rule_id"]: rule for rule in discovery["rules"]}
ordered_ids = [rule["source_rule_id"] for rule in inventory["rules"]]
domain_ids = [
    source_rule_id
    for source_rule_id in ordered_ids
    if discovery_by_id[source_rule_id]["classification"] == "DOMAIN_LEMMA"
]
definition_ids = [
    source_rule_id
    for source_rule_id in ordered_ids
    if discovery_by_id[source_rule_id]["classification"] == "DEFINITION"
]


def expected_source_record(source_rule_id: str, with_provenance: bool) -> dict:
    source = inv_by_id[source_rule_id]
    classified = discovery_by_id[source_rule_id]
    result = {
        "attributes": source["attributes"],
        "classification": classified["classification"],
        "end_line": source["end_line"],
        "module": source["module"],
        "normalized_sha256": source["normalized_sha256"],
        "rationale": classified["rationale"],
        "source_rule_id": source["source_rule_id"],
        "start_line": source["start_line"],
        "text": source["text"],
    }
    if with_provenance:
        result["discovery_manifest_sha256"] = file_hash(DISCOVERY)
        result["inventory_sha256"] = inventory["inventory_sha256"]
    return result


expected_domain = [expected_source_record(rule_id, True) for rule_id in domain_ids]
expected_defs = [expected_source_record(rule_id, False) for rule_id in definition_ids]
check("input.domain_records", input_manifest["source_rules"], expected_domain, report)
check("input.definition_records", input_manifest["definitions"], expected_defs, report)
check("input.no_operational_rules", input_manifest["operational_rules"], [], report)
check("input.no_proved_derived_lemmas", input_manifest["proved_derived_lemmas"], [], report)
check("obligation_map.source_rules", obligation_map["source_rules"], expected_domain, report)

# Exact source-rule/obligation bijection and obligation-level commitments.
obligations = obligation_map["obligations"]
obligation_ids = [item["source_rule_id"] for item in obligations]
check("obligations.ids_in_exact_source_order", obligation_ids, domain_ids, report)
check("obligations.unique", len(set(obligation_ids)), len(obligation_ids), report)
obligation_field_checks = []
for item in obligations:
    source = inv_by_id[item["source_rule_id"]]
    obligation_field_checks.append(
        {
            "source_rule_id": item["source_rule_id"],
            "span": item["source_span"]
            == {"start_line": source["start_line"], "end_line": source["end_line"]},
            "normalized_sha256": item["normalized_sha256"] == source["normalized_sha256"],
            "inventory_sha256": item["inventory_sha256"] == inventory["inventory_sha256"],
            "discovery_sha256": item["discovery_manifest_sha256"] == file_hash(DISCOVERY),
            "lean_conjunct_sha256": item["lean_conjunct_sha256"]
            == hashlib.sha256(item["lean_conjunct"].encode()).hexdigest(),
            "not_plain_true": item["lean_conjunct"].strip() not in {"True", "(True)"},
        }
    )
report["obligations.field_checks"] = obligation_field_checks
report["obligations.all_fields_ok"] = all(
    all(value for key, value in item.items() if key != "source_rule_id")
    for item in obligation_field_checks
)

# Rebuild target text, statement, and hashes without calling the preflight or
# producer helper.
parameters = obligation_map["trust_parameters"]
expected_lines = ["def targetStatement"]
for parameter in parameters:
    expected_lines.append(f"    ({parameter['name']} : {parameter['type']})")
expected_lines.extend(
    (
        "    : Prop :=",
        "    "
        + "\n    ∧ ".join(f"({item['lean_conjunct']})" for item in obligations),
    )
)
expected_definition = "\n".join(expected_lines)
lemma_text = (GENERATED / generator["target"]["file"]).read_text()
target_start = lemma_text.index("def targetStatement")
target_end = lemma_text.index("\n\nend ", target_start)
actual_definition = lemma_text[target_start:target_end].strip()
definition_hash = hashlib.sha256(actual_definition.encode()).hexdigest()
expected_definition_hash = hashlib.sha256(expected_definition.encode()).hexdigest()
statement = " ".join(
    [generator["target"]["declaration"]] + [parameter["name"] for parameter in parameters]
)
statement_hash = hashlib.sha256(statement.encode()).hexdigest()
check("target.actual_equals_rebuilt", actual_definition, expected_definition, report)
check("target.rebuilt_definition_hash", expected_definition_hash, generator["target"]["definition_sha256"], report)
check("target.actual_definition_hash", definition_hash, generator["target"]["definition_sha256"], report)
check("target.statement", statement, generator["target"]["statement"], report)
check("target.statement_hash", statement_hash, generator["target"]["statement_sha256"], report)
check("target.audit_input", generator["target"], resolution["target"], report)
check("target.preflight", generator["target"], preflight["target"], report)
check("target.single_declaration", lemma_text.count("def targetStatement"), 1, report)

binding_checks = []
for parameter in parameters:
    binding = {
        key: parameter[key]
        for key in ("kore_symbol", "name", "type", "source_rule_ids")
    }
    binding_checks.append(
        {
            "name": parameter["name"],
            "hash_ok": producer_binding_hash(binding) == parameter["binding_sha256"],
            "nonempty_sources": bool(parameter["source_rule_ids"]),
            "all_sources_are_domain": set(parameter["source_rule_ids"]).issubset(domain_ids),
            "unique_sources": len(set(parameter["source_rule_ids"]))
            == len(parameter["source_rule_ids"]),
        }
    )
report["target.binding_checks"] = binding_checks
report["target.all_bindings_ok"] = all(
    all(value for key, value in item.items() if key != "name")
    for item in binding_checks
)

# Cross-manifest/file hash commitments.
checks = {
    "verification_sha256": (file_hash(KPROOF / "verification.k"), input_manifest["verification_sha256"]),
    "inventory_sha256": (inventory["inventory_sha256"], input_manifest["inventory_sha256"]),
    "input.discovery_sha256": (file_hash(DISCOVERY), input_manifest["stage3_discovery_manifest_sha256"]),
    "input.stage1_sha256": (klean_tree_hash(KPROOF), input_manifest["stage1_workspace_sha256"]),
    "generator.stage1_sha256": (klean_tree_hash(KPROOF), generator["provenance"]["stage1_workspace_sha256"]),
    "generator.discovery_sha256": (file_hash(DISCOVERY), generator["provenance"]["stage3_discovery_manifest_sha256"]),
    "generator.inventory_sha256": (inventory["inventory_sha256"], generator["provenance"]["inventory_sha256"]),
    "generator.generated_tree_sha256": (klean_tree_hash(GENERATED), generator["generated_tree_sha256"]),
    "generator.obligation_map_sha256": (file_hash(GENERATED / "obligation-map.json"), generator["obligation_map_sha256"]),
    "generator.obligation_count": (len(obligations), generator["obligation_count"]),
    "export.generated_tree_sha256": (klean_tree_hash(GENERATED), export_result["generated_tree_sha256"]),
    "export.trust_inventory_sha256": (file_hash(GENERATION / "trust-inventory.json"), export_result["trust_inventory_sha256"]),
    "export.obligation_count": (len(obligations), export_result["obligation_count"]),
    "preflight.generated_tree_sha256": (klean_tree_hash(GENERATED), preflight["generated_tree_sha256"]),
    "preflight.obligation_count": (len(obligations), preflight["obligation_count"]),
    "preflight.audit_input": (preflight, resolution["stage4_preflight"]),
    "trust.designated_sorries": (trust["designated_sorries"], 0),
    "trust.other_sorries": (trust["other_sorries"], 0),
    "trust.allowlist_count": (len(trust["allowlist"]), len(trust["axioms"])),
}
for name, (actual, expected) in checks.items():
    check(name, actual, expected, report)

all_boolean_checks = []
for value in report.values():
    if isinstance(value, dict) and "ok" in value:
        all_boolean_checks.append(bool(value["ok"]))
all_boolean_checks.extend(
    [bool(report["obligations.all_fields_ok"]), bool(report["target.all_bindings_ok"])]
)
report["summary"] = {
    "domain_rule_count": len(domain_ids),
    "definition_rule_count": len(definition_ids),
    "obligation_count": len(obligations),
    "parameter_count": len(parameters),
    "all_mounted_hashes_and_structural_checks_ok": all(all_boolean_checks),
}

print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
if not all(all_boolean_checks):
    raise SystemExit(1)
