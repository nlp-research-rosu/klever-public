#!/usr/bin/env python3
"""Independent zero-obligation and target-identity checks using the frozen producer."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from tools.lemma_discovery_contract import validate_trust_boundary


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_frozen_exporter(path: Path):
    spec = importlib.util.spec_from_file_location("frozen_stage4_klean_export", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load frozen producer")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def emit(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{label}: {status}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
exporter = load_frozen_exporter(Path("/reference/generation-tools/klean_export.py"))

validated = validate_trust_boundary(workspace, discovery_path)
discovery_hash = sha256_file(discovery_path)
independent_domain_rules = exporter._domain_source_rules(validated, discovery_hash)
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
trust_inventory = json.loads((generation / "trust-inventory.json").read_text())
obligation_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_path.read_text())
preflight = json.loads((generation / "preflight.json").read_text())

print("OBLIGATION_MAP")
print(json.dumps(obligation_map, indent=2, sort_keys=True))
print("INDEPENDENT_DOMAIN_RULES")
print(json.dumps(independent_domain_rules, indent=2, sort_keys=True))

emit("input definitions", input_manifest["definitions"], validated["definitions"])
emit("input operational rules", input_manifest["operational_rules"], validated["operational_rules"])
emit(
    "input proved derived lemmas",
    input_manifest["proved_derived_lemmas"],
    validated["proved_derived_lemmas"],
)
emit("input source rules", input_manifest["source_rules"], independent_domain_rules)
emit("obligation-map source rules", obligation_map["source_rules"], independent_domain_rules)
emit("obligation-map obligations", obligation_map["obligations"], [])
emit("obligation-map trust parameters", obligation_map["trust_parameters"], [])
emit("obligation-map schema", obligation_map["schema_version"], 3)
emit("generator obligation count", generator_manifest["obligation_count"], 0)
emit("export obligation count", export_result["obligation_count"], 0)
emit("preflight obligation count", preflight["obligation_count"], 0)
emit("generator obligation-map hash", generator_manifest["obligation_map_sha256"], sha256_file(obligation_path))
emit(
    "export trust-inventory hash",
    export_result["trust_inventory_sha256"],
    sha256_file(generation / "trust-inventory.json"),
)
emit("input inventory hash", input_manifest["inventory_sha256"], validated["inventory_sha256"])
emit(
    "generator inventory hash",
    generator_manifest["provenance"]["inventory_sha256"],
    validated["inventory_sha256"],
)
emit(
    "input verification hash",
    input_manifest["verification_sha256"],
    sha256_file(workspace / "verification.k"),
)
emit("expected target definition", exporter.expected_target_definition(obligation_map), None)
emit("parsed generated target", exporter.target_statement(generated), None)
emit("generator target", generator_manifest["target"], None)
emit("preflight target", preflight["target"], None)
emit("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
emit("preflight status", preflight["status"], "KLEAN_NO_OBLIGATIONS")

target_declaration_count = 0
for path in generated.rglob("*.lean"):
    target_declaration_count += path.read_text().count("def targetStatement")
emit("raw generated target declaration count", target_declaration_count, 0)

module, functions = exporter.parse_verification((workspace / "verification.k").read_text())
summary_functions = [
    {
        "name": function.name,
        "return_sort": function.ret,
        "argument_sorts": function.args,
    }
    for function in functions
]
emit("parsed verification module", module, input_manifest["verification_module"])
emit("parsed summary functions", summary_functions, input_manifest["summary_functions"])
emit("trust designated sorries", trust_inventory["designated_sorries"], 0)
emit("trust other sorries", trust_inventory["other_sorries"], 0)
emit("trust allowlist count", len(trust_inventory["allowlist"]), preflight["trust_declaration_count"])
print(f"independent_domain_rule_count={len(independent_domain_rules)}")
print(f"obligation_count={len(obligation_map['obligations'])}")
print(f"source_rule_ids={ [entry['source_rule_id'] for entry in independent_domain_rules] }")
print(f"obligation_ids={ [entry['source_rule_id'] for entry in obligation_map['obligations']] }")
