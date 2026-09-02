#!/usr/bin/env python3
"""Independent checks of the remaining Stage 4 hash and null-target bindings."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.klean_audit_contract import verify_stage6_audit_input
from tools.klean_export import target_statement


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> None:
    passed = observed == expected
    print(f"CHECK {label}: {'PASS' if passed else 'FAIL'}")
    print(f"  observed={observed!r}")
    print(f"  expected={expected!r}")
    if not passed:
        raise SystemExit(1)


def main() -> None:
    generation = Path("/reference/klean-generation")
    generated = generation / "generated"
    audit = json.loads(Path("/audit-input.json").read_text())
    resolution, resolution_hash = verify_stage6_audit_input(audit)
    export_result = json.loads((generation / "export-result.json").read_text())
    generator = json.loads((generation / "generator-manifest.json").read_text())
    input_manifest = json.loads((generation / "input-manifest.json").read_text())
    mapping = json.loads((generated / "obligation-map.json").read_text())
    preflight = json.loads((generation / "preflight.json").read_text())
    lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())

    check("launcher resolved-input hash", resolution_hash, audit["resolved_input_sha256"])
    check("resolved audit mode", resolution["mode"], "CLASSIFICATION_ONLY")
    check("recorded Stage 4 status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
    check("launcher preflight document", resolution["stage4_preflight"], preflight)
    for index, diagnostic in enumerate(preflight["diagnostics"]):
        observed_output_hash = hashlib.sha256(diagnostic["output_tail"].encode()).hexdigest()
        check(f"preflight diagnostic[{index}] output hash", observed_output_hash, diagnostic["output_sha256"])
    check("generator toolchain lock", generator["toolchain"], lock)
    check("export frozen input hash", export_result["frozen_input_sha256"], input_manifest["frozen_input_sha256"])
    check("export discovery hash", export_result["stage3_discovery_manifest_sha256"], input_manifest["stage3_discovery_manifest_sha256"])
    check("export generated-tree hash", export_result["generated_tree_sha256"], generator["generated_tree_sha256"])
    check("export trust-inventory hash", export_result["trust_inventory_sha256"], digest(generation / "trust-inventory.json"))
    check("export obligation count", export_result["obligation_count"], len(mapping["obligations"]))
    check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
    check("input domain source rules", input_manifest["source_rules"], [])
    check("mapped source rules", mapping["source_rules"], [])
    check("mapped obligations", mapping["obligations"], [])
    check("mapped trust parameters", mapping["trust_parameters"], [])
    check("generator target", generator["target"], None)
    check("mechanically parsed target", target_statement(generated), None)
    check("launcher target", resolution["target"], None)
    check("Stage 5 result", resolution["stage5_result"], None)
    check("candidate mount absent", Path("/candidate").exists(), False)
    print("ALL_STAGE4_SIDECAR_CHECKS_PASS")


if __name__ == "__main__":
    main()
