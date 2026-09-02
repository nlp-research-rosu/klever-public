#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


def report(label: str, observed, expected) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{status} {label}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")
    if observed != expected:
        raise SystemExit(1)


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

validated = lemma_discovery_contract.validate_trust_boundary(
    workspace, discovery_path
)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
trust_inventory = json.loads((generation / "trust-inventory.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]

report("input definitions", input_manifest["definitions"], validated["definitions"])
report(
    "input operational rules",
    input_manifest["operational_rules"],
    validated["operational_rules"],
)
report(
    "input proved derived lemmas",
    input_manifest["proved_derived_lemmas"],
    validated["proved_derived_lemmas"],
)
report("independent true domain set", validated["domain_lemmas"], [])
report("input domain source_rules", input_manifest["source_rules"], [])
report("obligation-map source_rules", obligation_map["source_rules"], [])
report("obligation-map obligations", obligation_map["obligations"], [])
report("obligation-map trust_parameters", obligation_map["trust_parameters"], [])

source_ids = [entry["source_rule_id"] for entry in obligation_map["source_rules"]]
obligation_ids = [entry["source_rule_id"] for entry in obligation_map["obligations"]]
report("source-rule/obligation identity order", obligation_ids, source_ids)
report("source-rule IDs unique", len(set(source_ids)), len(source_ids))
report("obligation IDs unique", len(set(obligation_ids)), len(obligation_ids))

report("generator obligation_count", generator_manifest["obligation_count"], 0)
report("export obligation_count", export_result["obligation_count"], 0)
report("preflight obligation_count", preflight["obligation_count"], 0)
report("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
report("preflight status", preflight["status"], "KLEAN_NO_OBLIGATIONS")
report(
    "selected status",
    audit["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)

expected_definition = klean_export.expected_target_definition(obligation_map)
observed_target = klean_export.target_statement(generated)
report("expected target definition", expected_definition, None)
report("generated target declaration", observed_target, None)
report("generator target", generator_manifest["target"], None)
report("preflight target", preflight["target"], None)
report("audit-input target", audit["target"], None)

lean_sources = [
    path
    for _relative, kind, path in klean_export._tree_entries(generated)
    if kind == "file" and path.suffix == ".lean"
]
forbidden = {}
for source in lean_sources:
    text = source.read_text()
    hits = re.findall(r"\b(?:sorry|admit|unsafe)\b", text)
    if hits:
        forbidden[source.relative_to(generated).as_posix()] = hits
report("generated forbidden proof tokens", forbidden, {})
report("trust inventory designated_sorries", trust_inventory["designated_sorries"], 0)
report("trust inventory other_sorries", trust_inventory["other_sorries"], 0)
report(
    "generated target/vacuous-conjunct absence",
    any(
        re.search(r"(?m)^\s*(?:def|theorem)\s+target\b", source.read_text())
        for source in lean_sources
    ),
    False,
)
report("classification-only candidate absent", Path("/candidate").exists(), False)

print("OBLIGATION_BIJECTION_EMPTY_AND_TARGET_ABSENT")
