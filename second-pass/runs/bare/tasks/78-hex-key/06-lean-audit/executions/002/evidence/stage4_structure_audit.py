#!/usr/bin/env python3
"""Independent structural checks for the selected deterministic Stage 4 output."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, lemma_discovery_contract
from tools.klean_preflight import check_generation


K_WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
LOCK = Path("/reference/klean-toolchain.lock.json")


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise SystemExit(f"expected object: {path}")
    return value


def check(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{label}: {status}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if observed != expected:
        raise SystemExit(f"Stage 4 structural audit failed at {label}")


audit_input = load(Path("/audit-input.json"))
resolution = audit_input["resolution"]
discovery_hash = hashlib.sha256(DISCOVERY.read_bytes()).hexdigest()
validated = lemma_discovery_contract.validate_trust_boundary(
    K_WORKSPACE, DISCOVERY
)
source_rules = klean_export._domain_source_rules(validated, discovery_hash)

input_manifest = load(GENERATION / "input-manifest.json")
generator_manifest = load(GENERATION / "generator-manifest.json")
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = load(obligation_map_path)
export_result = load(GENERATION / "export-result.json")
recorded_preflight = load(GENERATION / "preflight.json")

check("independently classified domain rules", source_rules, [])
check(
    "obligation-map key set",
    set(obligation_map),
    {"schema_version", "source_rules", "obligations", "trust_parameters"},
)
check("obligation-map schema", obligation_map["schema_version"], 3)
check("input-manifest source rules", input_manifest["source_rules"], source_rules)
check("obligation-map source rules", obligation_map["source_rules"], source_rules)
check("obligation-map obligations", obligation_map["obligations"], [])
check("obligation-map trust parameters", obligation_map["trust_parameters"], [])

obligation_map_hash = hashlib.sha256(obligation_map_path.read_bytes()).hexdigest()
check(
    "obligation-map SHA-256",
    obligation_map_hash,
    generator_manifest["obligation_map_sha256"],
)
check("generator obligation count", generator_manifest["obligation_count"], 0)
check("export-result obligation count", export_result["obligation_count"], 0)
check("export-result status", export_result["status"], "KLEAN_NO_OBLIGATIONS")

expected_definition = klean_export.expected_target_definition(obligation_map)
actual_target = klean_export.target_statement(GENERATED)
check("expected target definition", expected_definition, None)
check("actual target statement", actual_target, None)
check("generator target", generator_manifest["target"], None)
check("launcher target", resolution["target"], None)
check("launcher preflight target", resolution["stage4_preflight"]["target"], None)

raw_target_count = 0
for path in sorted(GENERATED.rglob("*.lean")):
    raw_target_count += len(
        re.findall(r"(?m)^\s*def\s+targetStatement\b", path.read_text())
    )
check("raw targetStatement declaration count", raw_target_count, 0)
check("Stage 5 candidate absent", Path("/candidate").exists(), False)
check("launcher Stage 5 result", resolution["stage5_result"], None)
check("launcher Lean workspace", resolution["lean_workspace"], None)
check("launcher Lean invocation", resolution["lean_invocation"], None)

fresh_preflight = check_generation(
    K_WORKSPACE,
    DISCOVERY,
    GENERATION,
    toolchain_lock=LOCK,
)
check("fresh preflight vs selected preflight", fresh_preflight, recorded_preflight)
check(
    "fresh preflight vs launcher evidence",
    fresh_preflight,
    resolution["stage4_preflight"],
)

print("EMPTY SOURCE/OBLIGATION BIJECTION AND NULL TARGET CONFIRMED")
