#!/usr/bin/env python3
"""Independent source/obligation/target bijection checks for Stage 4."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, lemma_discovery_contract


workspace = Path("/reference/k-proof")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"

validated = lemma_discovery_contract.validate_trust_boundary(workspace, discovery_path)
discovery_sha = hashlib.sha256(discovery_path.read_bytes()).hexdigest()
input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
obligation_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_path.read_text())
audit_input = json.loads(Path("/audit-input.json").read_text())["resolution"]


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: list[tuple[str, bool, object, object]] = []


def check(label: str, observed: object, expected: object) -> None:
    checks.append((label, observed == expected, observed, expected))


# Verify that deterministic input classification arrays are exact joined views
# of the frozen source plus the protected classifications.
check("definitions exact", input_manifest["definitions"], validated["definitions"])
check("operational rules exact", input_manifest["operational_rules"], validated["operational_rules"])
check("proved derived lemmas exact", input_manifest["proved_derived_lemmas"], validated["proved_derived_lemmas"])

expected_source_rules = klean_export._domain_source_rules(validated, discovery_sha)
check("input domain source rules exact", input_manifest["source_rules"], expected_source_rules)
check("obligation-map source rules exact", obligation_map["source_rules"], expected_source_rules)

expected_ids = [rule["source_rule_id"] for rule in expected_source_rules]
obligations = obligation_map["obligations"]
observed_ids = [obligation.get("source_rule_id") for obligation in obligations]
check("ordered source-rule/obligation IDs", observed_ids, expected_ids)
check("obligation IDs unique", len(observed_ids), len(set(observed_ids)))
check("obligation count", len(obligations), generator_manifest["obligation_count"])
check("obligation-map hash", file_sha(obligation_path), generator_manifest["obligation_map_sha256"])
check("trust parameters", obligation_map["trust_parameters"], [])

target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)
check("generated target vs generator manifest", target, generator_manifest["target"])
check("generated target vs audit input", target, audit_input["target"])
check("generated target vs preflight", target, preflight["target"])
check("zero-obligation target definition", expected_definition, None)
check("target presence iff obligations", bool(target), bool(obligations))

for label, document in (
    ("export", export_result),
    ("preflight", preflight),
):
    check(f"{label} status", document["status"], "KLEAN_NO_OBLIGATIONS")
    check(f"{label} obligation count", document["obligation_count"], 0)

check("selected Stage 4 status", audit_input["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
check("true domain lemma count", len(validated["domain_lemmas"]), 0)
check("candidate absent", Path("/candidate").exists(), False)
check("Stage 5 result absent", audit_input["stage5_result"], None)
check("Stage 5 workspace absent", audit_input["lean_workspace"], None)
check("Stage 5 invocation absent", audit_input["lean_invocation"], None)

print("INDEPENDENT STAGE 4 BIJECTION")
print(f"canonical rule count={len(validated['rules'])}")
print(f"definition count={len(validated['definitions'])}")
print(f"operational rule count={len(validated['operational_rules'])}")
print(f"proved derived lemma count={len(validated['proved_derived_lemmas'])}")
print(f"true domain lemma count={len(validated['domain_lemmas'])}")
print(f"expected source rule IDs={expected_ids}")
print(f"observed obligation IDs={observed_ids}")
print(f"generated target={target}")
print(f"expected target definition={expected_definition}")

for label, ok, observed, expected in checks:
    print(f"{label}: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(f"  observed={observed!r}")
        print(f"  expected={expected!r}")
print(f"TOTAL_CHECKS={len(checks)}")
print(f"FAILED_CHECKS={sum(not ok for _, ok, _, _ in checks)}")
if not all(ok for _, ok, _, _ in checks):
    raise SystemExit(1)
