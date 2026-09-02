#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools import lemma_discovery_contract


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(
    checks: list[dict[str, object]],
    label: str,
    observed: object,
    expected: object,
) -> None:
    checks.append(
        {
            "label": label,
            "observed": observed,
            "expected": expected,
            "match": observed == expected,
        }
    )


k_workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_bundle = Path("/reference/generation-tools")

audit_input = json.loads(Path("/audit-input.json").read_text())
resolution = audit_input["resolution"]
validated = lemma_discovery_contract.validate_trust_boundary(
    k_workspace, discovery_path
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
trust_inventory_path = generation / "trust-inventory.json"
recorded_preflight = json.loads((generation / "preflight.json").read_text())
source_manifest = json.loads(
    (producer_bundle / "source-manifest.json").read_text()
)

# This is the result of the independent semantic classification recorded in
# 04_classification_semantics_audit.py, not a value derived from Stage 3.
independent_domain_source_rule_ids: list[str] = []
independent_domain_source_rules: list[dict[str, object]] = []

checks: list[dict[str, object]] = []
record(
    checks,
    "validated Stage 3 domain IDs vs independent domain IDs",
    [rule["source_rule_id"] for rule in validated["domain_lemmas"]],
    independent_domain_source_rule_ids,
)
record(
    checks,
    "input-manifest definitions",
    input_manifest["definitions"],
    validated["definitions"],
)
record(
    checks,
    "input-manifest operational rules",
    input_manifest["operational_rules"],
    validated["operational_rules"],
)
record(
    checks,
    "input-manifest proved derived lemmas",
    input_manifest["proved_derived_lemmas"],
    validated["proved_derived_lemmas"],
)
record(
    checks,
    "input-manifest domain source rules",
    input_manifest["source_rules"],
    independent_domain_source_rules,
)
record(
    checks,
    "obligation-map source rules",
    obligation_map["source_rules"],
    independent_domain_source_rules,
)
record(checks, "obligation list", obligation_map["obligations"], [])
record(checks, "trust parameter list", obligation_map["trust_parameters"], [])
record(
    checks,
    "generator obligation count",
    generator_manifest["obligation_count"],
    0,
)
record(
    checks,
    "generator obligation-map hash",
    generator_manifest["obligation_map_sha256"],
    sha256_file(obligation_map_path),
)
record(
    checks,
    "generator inventory provenance",
    generator_manifest["provenance"]["inventory_sha256"],
    validated["inventory_sha256"],
)
record(
    checks,
    "input-manifest inventory",
    input_manifest["inventory_sha256"],
    validated["inventory_sha256"],
)
record(
    checks,
    "input-manifest verification hash",
    input_manifest["verification_sha256"],
    validated["verification_sha256"],
)
record(
    checks,
    "export status",
    export_result["status"],
    "KLEAN_NO_OBLIGATIONS",
)
record(checks, "export obligation count", export_result["obligation_count"], 0)
record(
    checks,
    "export frozen-input hash",
    export_result["frozen_input_sha256"],
    resolution["hashes"]["stage1_export_sha256"],
)
record(
    checks,
    "export discovery hash",
    export_result["stage3_discovery_manifest_sha256"],
    resolution["hashes"]["discovery_manifest_sha256"],
)
record(
    checks,
    "export generated-tree hash",
    export_result["generated_tree_sha256"],
    resolution["hashes"]["generated_tree_sha256"],
)
record(
    checks,
    "export trust-inventory hash",
    export_result["trust_inventory_sha256"],
    sha256_file(trust_inventory_path),
)
record(
    checks,
    "recorded preflight vs audit input",
    recorded_preflight,
    resolution["stage4_preflight"],
)
record(
    checks,
    "selected Stage 4 status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)
record(checks, "generator target", generator_manifest["target"], None)
record(checks, "audit-input target", resolution["target"], None)
record(checks, "recorded preflight target", recorded_preflight["target"], None)
record(
    checks,
    "trusted target parser",
    klean_export.target_statement(generated),
    None,
)
record(
    checks,
    "expected target definition",
    klean_export.expected_target_definition(obligation_map),
    None,
)

target_definitions: list[str] = []
lean_files: list[str] = []
for relative, kind, path in klean_export._tree_entries(generated):
    if kind == "file" and path.suffix == ".lean":
        lean_files.append(relative)
        for match in re.finditer(
            r"(?m)^\s*def\s+targetStatement\b", path.read_text()
        ):
            target_definitions.append(
                f"{relative}:{path.read_text()[:match.start()].count(chr(10)) + 1}"
            )
record(checks, "raw targetStatement declarations", target_definitions, [])

producer_files = sorted(
    path.relative_to(producer_bundle).as_posix()
    for path in producer_bundle.rglob("*")
    if path.is_file()
)
record(
    checks,
    "producer bundle exact file set",
    producer_files,
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
record(
    checks,
    "producer manifest exact file keys",
    sorted(source_manifest["files"]),
    ["klean.py", "klean_export.py"],
)

record(checks, "Stage 5 result", resolution["stage5_result"], None)
record(checks, "Stage 5 workspace", resolution["lean_workspace"], None)
record(checks, "Stage 5 invocation", resolution["lean_invocation"], None)
record(checks, "candidate directory exists", Path("/candidate").exists(), False)

result = {
    "independent_domain_source_rule_ids": independent_domain_source_rule_ids,
    "source_rule_count": len(obligation_map["source_rules"]),
    "obligation_count": len(obligation_map["obligations"]),
    "conjunct_count": len(obligation_map["obligations"]),
    "duplicate_obligation_ids": [],
    "irrelevant_or_weakened_conjuncts": [],
    "omitted_domain_rules": [],
    "extra_obligations": [],
    "target_definitions": target_definitions,
    "lean_files_scanned": lean_files,
    "checks": checks,
    "all_checks_match": all(check["match"] for check in checks),
}
print(json.dumps(result, indent=2, sort_keys=True))
if not result["all_checks_match"]:
    raise SystemExit("Stage 4 structural audit failed")
