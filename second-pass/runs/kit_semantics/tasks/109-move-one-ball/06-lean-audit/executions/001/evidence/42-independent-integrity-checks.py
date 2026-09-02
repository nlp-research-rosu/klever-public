#!/usr/bin/env python3
"""Independent integrity checks for the 109-move-one-ball Stage 3-5 audit."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.stage6_resolution_contract import verify_audit_input


K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY_PATH = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
CANDIDATE = Path("/candidate")
FRESH = Path("/tmp/audit-work/fresh-proof-2")


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict)
    return value


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


checks: list[tuple[str, bool, str]] = []


def check(name: str, condition: bool, detail: object = "") -> None:
    checks.append((name, bool(condition), str(detail)))


audit_doc = load(Path("/audit-input.json"))
resolution, resolved_digest = verify_audit_input(audit_doc)
hashes = resolution["hashes"]
check("audit envelope and resolved-input digest", True, resolved_digest)
check("audit mode", resolution["mode"] == "CLASSIFICATION_AND_PROOF", resolution["mode"])
check("problem", resolution["problem_id"] == "109-move-one-ball", resolution["problem_id"])
check("condition", resolution["condition"] == "kit-semantics", resolution["condition"])
check(
    "semantics mode",
    resolution["semantics_mode"] == "SUPPLIED_SEMANTICS",
    resolution["semantics_mode"],
)

# Authenticate both producer sources against the source manifest, generator
# manifest, immutable image identifier, and signed launcher resolution.
source_manifest = load(PRODUCERS / "source-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
producer_actual = {
    name: file_sha(PRODUCERS / name)
    for name in ("klean_export.py", "klean.py")
}
check(
    "producer hashes match source manifest",
    producer_actual == source_manifest["files"],
    producer_actual,
)
check(
    "klean_export.py matches generator manifest",
    producer_actual["klean_export.py"] == generator_manifest["exporter_sha256"],
    producer_actual["klean_export.py"],
)
check(
    "klean.py matches generator manifest",
    producer_actual["klean.py"] == generator_manifest["klean_py_sha256"],
    producer_actual["klean.py"],
)
producer_image = source_manifest["generator_image_id"]
check(
    "generator image matches generator manifest",
    producer_image == generator_manifest["provenance"]["generator_image_id"],
    producer_image,
)
check(
    "generator image matches signed producer path",
    producer_image.removeprefix("sha256:")
    == Path(resolution["generation_producer_sources"]).name,
    resolution["generation_producer_sources"],
)

# Reconstruct the complete local verification-module inventory.
inventory = inventory_verification(K_PROOF)
discovery = load(DISCOVERY_PATH)
rules = inventory["rules"]
verification_lines = (K_PROOF / "verification.k").read_text().splitlines()
independent_rule_checks = []
for rule in rules:
    span_text = "\n".join(
        verification_lines[rule["start_line"] - 1 : rule["end_line"]]
    )
    normalized_digest = text_sha(" ".join(rule["text"].split()))
    independent_rule_checks.append(
        span_text == rule["text"]
        and normalized_digest == rule["normalized_sha256"]
        and rule["source_rule_id"] == "rule-" + normalized_digest
    )
check(
    "all reconstructed source spans, normalized hashes, and IDs",
    all(independent_rule_checks),
    f"{sum(independent_rule_checks)}/{len(rules)}",
)
check(
    "inventory hash independently recomputed",
    inventory["inventory_sha256"]
    == text_sha(
        json.dumps(
            rules, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        )
    ),
    inventory["inventory_sha256"],
)
check(
    "verification.k raw hash",
    inventory["verification_sha256"] == file_sha(K_PROOF / "verification.k"),
    inventory["verification_sha256"],
)
check(
    "verification closure",
    inventory["verification_module"] == "VERIFICATION"
    and inventory["verification_modules"] == ["VERIFICATION"],
    inventory["verification_modules"],
)

inventory_ids = [rule["source_rule_id"] for rule in rules]
discovery_ids = [rule["source_rule_id"] for rule in discovery["rules"]]
check("inventory IDs unique", len(inventory_ids) == len(set(inventory_ids)), len(rules))
check(
    "discovery IDs unique",
    len(discovery_ids) == len(set(discovery_ids)),
    len(discovery_ids),
)
check(
    "ordered discovery/inventory bijection",
    discovery_ids == inventory_ids,
    f"{len(discovery_ids)} == {len(inventory_ids)}",
)
check(
    "discovery inventory hash",
    discovery["inventory_sha256"] == inventory["inventory_sha256"],
    discovery["inventory_sha256"],
)

# Encode the audit's independent classification by source identity. The two
# guarded applyCmp simplifications are the only DOMAIN_LEMMAs; every other
# rule is a macro, named summary base equation, or named summary recurrence.
domain_ids = {
    "rule-f4bdada31cc091a93eafbccbe69892fe1124bf15cc9c0d653798acc812093b2d",
    "rule-1790939123173b0e0d0436b3ebbcacdb5e49ed4a87ef17f2f877dc7b6d6e1fd1",
}
independent_classes = {
    source_id: ("DOMAIN_LEMMA" if source_id in domain_ids else "DEFINITION")
    for source_id in inventory_ids
}
observed_classes = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
check(
    "independent classification equals protected classification",
    observed_classes == independent_classes,
    {
        category: sum(value == category for value in observed_classes.values())
        for category in sorted(set(observed_classes.values()))
    },
)
check(
    "every simplification is DEFINITION or DOMAIN_LEMMA",
    all(
        independent_classes[rule["source_rule_id"]]
        in {"DEFINITION", "DOMAIN_LEMMA"}
        for rule in rules
        if "simplification" in rule["attributes"]
    ),
)
check(
    "simplification set is exactly the independent domain set",
    {
        rule["source_rule_id"]
        for rule in rules
        if "simplification" in rule["attributes"]
    }
    == domain_ids,
)

# Every signed Stage 1 file hash is checked, with no omitted or extra regular
# file. This is separate from both tree hash formats.
actual_stage1_files: dict[str, str] = {}
for directory, subdirs, filenames in os.walk(K_PROOF):
    subdirs.sort()
    filenames.sort()
    for filename in filenames:
        path = Path(directory) / filename
        assert path.is_file() and not path.is_symlink()
        actual_stage1_files[path.relative_to(K_PROOF).as_posix()] = file_sha(path)
recorded_stage1_files = resolution["stage1_source_hashes"]
check(
    "all signed Stage 1 source hashes",
    actual_stage1_files == recorded_stage1_files,
    f"{len(actual_stage1_files)} files",
)

# Recompute each hash of an input actually mounted into the audit.
mounted_pipeline_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(K_PROOF),
    "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(PRODUCERS),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(CANDIDATE),
}
for name, digest in mounted_pipeline_hashes.items():
    check(f"signed mounted tree hash: {name}", digest == hashes[name], digest)
check(
    "signed discovery file hash",
    file_sha(DISCOVERY_PATH) == hashes["discovery_manifest_sha256"],
    file_sha(DISCOVERY_PATH),
)
check(
    "signed Stage 1 export tree hash",
    klean_export.tree_digest(K_PROOF) == hashes["stage1_export_sha256"],
    klean_export.tree_digest(K_PROOF),
)
check(
    "signed generated export tree hash",
    klean_export.tree_digest(GENERATED) == hashes["generated_tree_sha256"],
    klean_export.tree_digest(GENERATED),
)

# Reassemble Stage 4's split input manifest and compare it to the inventory and
# independent classification, including the original source order.
input_manifest = load(GENERATION / "input-manifest.json")
manifest_entries = sorted(
    input_manifest["definitions"] + input_manifest["source_rules"],
    key=lambda entry: (entry["start_line"], entry["end_line"]),
)
stripped_manifest_entries = [
    {
        key: entry[key]
        for key in (
            "source_rule_id",
            "module",
            "start_line",
            "end_line",
            "normalized_sha256",
            "attributes",
            "text",
        )
    }
    for entry in manifest_entries
]
check(
    "Stage 4 input manifest is exact ordered inventory",
    stripped_manifest_entries == rules,
    len(manifest_entries),
)
check(
    "Stage 4 input classifications",
    all(
        entry["classification"] == independent_classes[entry["source_rule_id"]]
        for entry in manifest_entries
    ),
)
check(
    "Stage 4 input inventory and source hashes",
    input_manifest["inventory_sha256"] == inventory["inventory_sha256"]
    and input_manifest["verification_sha256"] == inventory["verification_sha256"]
    and input_manifest["stage1_workspace_sha256"]
    == klean_export.tree_digest(K_PROOF)
    and input_manifest["stage3_discovery_manifest_sha256"]
    == file_sha(DISCOVERY_PATH),
)

# Independently verify the source-rule/obligation bijection and every recorded
# obligation hash and provenance field.
obligation_path = GENERATED / "obligation-map.json"
obligation_map = load(obligation_path)
obligations = obligation_map["obligations"]
source_rules = obligation_map["source_rules"]
obligation_ids = [entry["source_rule_id"] for entry in obligations]
source_rule_ids = [entry["source_rule_id"] for entry in source_rules]
check(
    "domain/source-rule exact ordered set",
    source_rule_ids == [source_id for source_id in inventory_ids if source_id in domain_ids],
    source_rule_ids,
)
check(
    "source-rule/obligation exact ordered bijection",
    obligation_ids == source_rule_ids
    and len(obligation_ids) == len(set(obligation_ids)) == 2,
    obligation_ids,
)
source_by_id = {entry["source_rule_id"]: entry for entry in source_rules}
obligation_hashes_ok = True
for obligation in obligations:
    source = source_by_id[obligation["source_rule_id"]]
    obligation_hashes_ok &= (
        obligation["lean_conjunct_sha256"] == text_sha(obligation["lean_conjunct"])
        and obligation["normalized_sha256"] == source["normalized_sha256"]
        and obligation["inventory_sha256"] == inventory["inventory_sha256"]
        and obligation["discovery_manifest_sha256"] == file_sha(DISCOVERY_PATH)
        and obligation["source_span"]
        == {"start_line": source["start_line"], "end_line": source["end_line"]}
    )
check("all obligation hashes, spans, and provenance", obligation_hashes_ok)
check(
    "obligation map raw hash",
    file_sha(obligation_path) == generator_manifest["obligation_map_sha256"],
    file_sha(obligation_path),
)
check(
    "obligation count is nonempty and exact",
    generator_manifest["obligation_count"] == len(obligations) == 2,
    len(obligations),
)

# Bindings are hashed independently and must mention only and collectively all
# exact obligation IDs.
binding_hashes_ok = True
bound_ids: set[str] = set()
for parameter in obligation_map["trust_parameters"]:
    binding = {
        key: parameter[key]
        for key in ("kore_symbol", "name", "type", "source_rule_ids")
    }
    binding_hashes_ok &= parameter["binding_sha256"] == text_sha(
        json.dumps(
            binding, sort_keys=True, separators=(",", ":")
        )
    )
    binding_hashes_ok &= set(parameter["source_rule_ids"]) <= domain_ids
    bound_ids.update(parameter["source_rule_ids"])
check("all target-parameter binding hashes and links", binding_hashes_ok)
check("target parameters cover both obligations", bound_ids == domain_ids, sorted(bound_ids))

# The generator target is recomputed from its file and obligation map. Its
# definition must be the exact conjunction generated by the obligation list,
# and all copies recorded by the launcher and preflight must be byte-for-byte
# equal as structured target records.
target = klean_export.target_statement(GENERATED)
expected_definition = klean_export.expected_target_definition(obligation_map)
assert target is not None and expected_definition is not None
check(
    "target definition is exact generated conjunction",
    target["definition_sha256"] == text_sha(expected_definition),
    target["definition_sha256"],
)
check(
    "target statement raw hash",
    target["statement_sha256"] == text_sha(target["statement"]),
    target["statement_sha256"],
)
check("generator-manifest target identity", generator_manifest["target"] == target)
check("audit-input target identity", resolution["target"] == target)
check("recorded Stage 4 preflight target identity", resolution["stage4_preflight"]["target"] == target)
check(
    "fresh Base target identity",
    klean_export.target_statement(FRESH / "Base") == target,
)

# Check other recorded export hashes and trust inventory accounting.
export_result = load(GENERATION / "export-result.json")
trust_inventory_path = GENERATION / "trust-inventory.json"
trust_inventory = load(trust_inventory_path)
check(
    "trust inventory raw hash",
    file_sha(trust_inventory_path) == export_result["trust_inventory_sha256"],
    file_sha(trust_inventory_path),
)
check(
    "trust inventory internally accounts declarations",
    len(trust_inventory["axioms"]) == len(trust_inventory["allowlist"]) == 42
    and {entry["name"] for entry in trust_inventory["allowlist"]}
    == set(trust_inventory["axioms"]),
    len(trust_inventory["axioms"]),
)
check(
    "no generated sorry/noncomputable repair escape",
    trust_inventory["designated_sorries"] == 0
    and trust_inventory["other_sorries"] == 0
    and trust_inventory["automatic_axiomatization"] == []
    and trust_inventory["automatic_noncomputable_repair"] is False,
)
check(
    "export-result identities",
    export_result["generated_tree_sha256"] == klean_export.tree_digest(GENERATED)
    and export_result["frozen_input_sha256"] == klean_export.tree_digest(K_PROOF)
    and export_result["stage3_discovery_manifest_sha256"] == file_sha(DISCOVERY_PATH)
    and export_result["obligation_count"] == 2
    and export_result["status"] == "OK",
)

# Candidate-only checks. Generated Base is separately authenticated above.
candidate_sources = []
for path in CANDIDATE.rglob("*"):
    if path.is_file() and not path.is_symlink() and "Base" not in path.parts:
        candidate_sources.append(path)
candidate_text = "\n".join(
    path.read_text(errors="replace")
    for path in candidate_sources
    if path.suffix in {".lean", ".toml", ""}
)
for forbidden in ("sorry", "admit", "unsafe", "axiom", "opaque"):
    check(
        f"candidate contains no forbidden token: {forbidden}",
        re.search(rf"(?i)\\b{forbidden}\\b", candidate_text) is None,
    )
check(
    "candidate does not shadow targetStatement",
    re.search(r"\\b(def|theorem|lemma|abbrev)\\s+targetStatement\\b", candidate_text)
    is None,
)
check(
    "candidate declares one Proof.final at fixed target",
    candidate_text.count("theorem final") == 1
    and "Klean109MoveOneBall.Lemmas.targetStatement _andBool_"
    in candidate_text,
)
check(
    "fresh proof source unchanged from candidate",
    file_sha(FRESH / "Proof.lean") == file_sha(CANDIDATE / "Proof.lean"),
    file_sha(FRESH / "Proof.lean"),
)
check(
    "fresh Base export tree unchanged",
    klean_export.tree_digest(FRESH / "Base") == klean_export.tree_digest(GENERATED),
    klean_export.tree_digest(FRESH / "Base"),
)

for name, passed, detail in checks:
    print(f"{'PASS' if passed else 'FAIL'} | {name} | {detail}")
failed = [name for name, passed, _detail in checks if not passed]
print(f"SUMMARY | checks={len(checks)} failed={len(failed)}")
if failed:
    print("FAILED | " + "; ".join(failed))
    raise SystemExit(1)
