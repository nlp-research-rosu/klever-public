#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.k_rule_inventory import inventory_verification


def load(path: Path):
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


root = Path("/reference/klean-generation")
generated = root / "generated"
audit = load(Path("/audit-input.json"))["resolution"]
discovery_path = Path("/reference/lemma-discovery.json")
discovery = load(discovery_path)
inventory = inventory_verification(Path("/reference/k-proof"))
input_manifest = load(root / "input-manifest.json")
generator = load(root / "generator-manifest.json")
obligation_map_path = generated / "obligation-map.json"
obligation_map = load(obligation_map_path)
export_result = load(root / "export-result.json")
preflight = load(root / "preflight.json")
trust_path = root / "trust-inventory.json"
lock = load(Path("/reference/klean-toolchain.lock.json"))
rerun = load(Path("/audit-output/evidence/81-check-generation-final.log"))

classified_by_id = {
    entry["source_rule_id"]: entry["classification"]
    for entry in discovery["rules"]
}
independent_domain_rules = [
    rule for rule in inventory["rules"]
    if classified_by_id[rule["source_rule_id"]] == "DOMAIN_LEMMA"
]

checks = []


def check(label, actual, expected):
    checks.append((label, actual, expected))


check("verification hash", input_manifest["verification_sha256"], sha(Path("/reference/k-proof/verification.k")))
check("inventory hash", input_manifest["inventory_sha256"], inventory["inventory_sha256"])
check("Stage 3 manifest hash", input_manifest["stage3_discovery_manifest_sha256"], sha(discovery_path))
check("Stage 1 export hash", input_manifest["frozen_input_sha256"], audit["hashes"]["stage1_export_sha256"])
check("Stage 1 workspace export hash", input_manifest["stage1_workspace_sha256"], audit["hashes"]["stage1_export_sha256"])
check("definitions preserve canonical order", [r["source_rule_id"] for r in input_manifest["definitions"]], [r["source_rule_id"] for r in inventory["rules"]])
check("independent DOMAIN_LEMMA set", [r["source_rule_id"] for r in independent_domain_rules], [])
check("input source_rules exact domain set", input_manifest["source_rules"], independent_domain_rules)
check("obligation-map source rules", obligation_map["source_rules"], input_manifest["source_rules"])
check("obligation source-rule bijection", [o.get("source_rule_id") for o in obligation_map["obligations"]], [r["source_rule_id"] for r in input_manifest["source_rules"]])
check("unique obligation identities", len({o.get("source_rule_id") for o in obligation_map["obligations"]}), len(obligation_map["obligations"]))
check("no vacuous conjuncts", [o for o in obligation_map["obligations"] if not o.get("lean_conjunct") or not o.get("lean_conjunct", "").strip()], [])
check("trust parameters", obligation_map["trust_parameters"], [])
check("obligation count", generator["obligation_count"], len(obligation_map["obligations"]))
check("obligation map hash", generator["obligation_map_sha256"], sha(obligation_map_path))
check("toolchain lock", generator["toolchain"], lock)
check("generator inventory provenance", generator["provenance"]["inventory_sha256"], inventory["inventory_sha256"])
check("generator Stage 1 provenance", generator["provenance"]["stage1_workspace_sha256"], audit["hashes"]["stage1_export_sha256"])
check("generator Stage 3 provenance", generator["provenance"]["stage3_discovery_manifest_sha256"], sha(discovery_path))
check("generated tree", generator["generated_tree_sha256"], klean_export.tree_digest(generated))
check("export frozen input", export_result["frozen_input_sha256"], audit["hashes"]["stage1_export_sha256"])
check("export Stage 3", export_result["stage3_discovery_manifest_sha256"], sha(discovery_path))
check("export generated tree", export_result["generated_tree_sha256"], klean_export.tree_digest(generated))
check("export trust inventory", export_result["trust_inventory_sha256"], sha(trust_path))
check("export obligation count", export_result["obligation_count"], 0)
check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check("expected target definition", klean_export.expected_target_definition(obligation_map), None)
check("actual target statement", klean_export.target_statement(generated), None)
check("generator target", generator["target"], None)
check("audit target", audit["target"], None)
check("recorded preflight matches audit input", preflight, audit["stage4_preflight"])
check("fresh preflight matches recorded preflight", rerun, preflight)
check("fresh preflight status", rerun["status"], "KLEAN_NO_OBLIGATIONS")
check("fresh preflight obligations", rerun["obligation_count"], 0)
check("fresh preflight target", rerun["target"], None)

for label, actual, expected in checks:
    passed = actual == expected
    print(("PASS" if passed else "FAIL") + ": " + label)
    if not passed or label in {
        "independent DOMAIN_LEMMA set",
        "obligation source-rule bijection",
        "expected target definition",
        "actual target statement",
        "fresh preflight status",
    }:
        print(f"  actual={actual!r}")
        print(f"  expected={expected!r}")

failed = [label for label, actual, expected in checks if actual != expected]
print(f"checks={len(checks)}")
print(f"failures={len(failed)}")
if failed:
    raise SystemExit(1)
