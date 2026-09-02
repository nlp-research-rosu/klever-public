#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path


ROOT = Path("/reference/klean-generation")
GENERATED = ROOT / "generated"


def read_json(path: Path):
    return json.loads(path.read_text())


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, condition: bool, detail=None):
    result = {"check": label, "pass": bool(condition)}
    if detail is not None:
        result["detail"] = detail
    print(json.dumps(result, sort_keys=True))
    return bool(condition)


audit = read_json(Path("/audit-input.json"))
resolution = audit["resolution"]
discovery = read_json(Path("/reference/lemma-discovery.json"))
input_manifest = read_json(ROOT / "input-manifest.json")
generator = read_json(ROOT / "generator-manifest.json")
export = read_json(ROOT / "export-result.json")
preflight = read_json(ROOT / "preflight.json")
trust = read_json(ROOT / "trust-inventory.json")
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = read_json(obligation_map_path)

results = []
results.append(check(
    "input classifications are all empty",
    all(input_manifest[name] == [] for name in (
        "definitions",
        "operational_rules",
        "proved_derived_lemmas",
        "source_rules",
    )),
))
results.append(check(
    "protected classification is empty",
    discovery["rules"] == [],
))
results.append(check(
    "inventory hash agrees everywhere",
    len({
        discovery["inventory_sha256"],
        input_manifest["inventory_sha256"],
        generator["provenance"]["inventory_sha256"],
    }) == 1,
))
results.append(check(
    "verification.k hash is bound",
    input_manifest["verification_sha256"]
        == sha256_file(Path("/reference/k-proof/verification.k")),
))
results.append(check(
    "obligation-map exact zero-obligation shape",
    set(obligation_map) == {
        "schema_version", "source_rules", "obligations", "trust_parameters"
    }
    and obligation_map["schema_version"] == 3
    and obligation_map["source_rules"] == []
    and obligation_map["obligations"] == []
    and obligation_map["trust_parameters"] == [],
    obligation_map,
))
results.append(check(
    "obligation-map hash is bound",
    generator["obligation_map_sha256"] == sha256_file(obligation_map_path),
))
results.append(check(
    "all obligation counts are zero",
    generator["obligation_count"] == 0
    and export["obligation_count"] == 0
    and preflight["obligation_count"] == 0
    and resolution["stage4_preflight"]["obligation_count"] == 0,
))
results.append(check(
    "all generation statuses are KLEAN_NO_OBLIGATIONS",
    export["status"] == "KLEAN_NO_OBLIGATIONS"
    and preflight["status"] == "KLEAN_NO_OBLIGATIONS"
    and resolution["stage4_preflight"]["status"] == "KLEAN_NO_OBLIGATIONS"
    and resolution["selections"]["klean_generation"]["status"]
        == "KLEAN_NO_OBLIGATIONS",
))
results.append(check(
    "trust inventory hash is bound",
    export["trust_inventory_sha256"] == sha256_file(ROOT / "trust-inventory.json"),
))
results.append(check(
    "recorded preflight sidecar equals signed audit copy",
    preflight == resolution["stage4_preflight"],
))
results.append(check(
    "every target record is null",
    generator["target"] is None
    and preflight["target"] is None
    and resolution["target"] is None
    and resolution["stage4_preflight"]["target"] is None,
))

lean_sources = sorted(GENERATED.rglob("*.lean"))
target_hits = []
for source in lean_sources:
    for match in re.finditer(r"(?m)^\s*def\s+targetStatement\b", source.read_text()):
        target_hits.append({
            "file": source.relative_to(GENERATED).as_posix(),
            "offset": match.start(),
        })
results.append(check(
    "no generated target declaration",
    target_hits == [],
    target_hits,
))
results.append(check(
    "classification-only mode and no Stage 5 inputs",
    resolution["mode"] == "CLASSIFICATION_ONLY"
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["stage5_result"] is None
    and not Path("/candidate").exists(),
))
results.append(check(
    "no vacuous or duplicated conjunct exists",
    obligation_map["obligations"] == [],
))

print(json.dumps({
    "all_checks_pass": all(results),
    "lean_source_count": len(lean_sources),
    "trust_allowlist_count": len(trust["allowlist"]),
    "target_declaration_count": len(target_hits),
}, sort_keys=True))
raise SystemExit(0 if all(results) else 1)
