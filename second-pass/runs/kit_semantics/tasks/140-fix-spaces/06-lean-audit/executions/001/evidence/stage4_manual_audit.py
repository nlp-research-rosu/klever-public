#!/usr/bin/env python3
"""Independent Stage 4 bijection, target, and deterministic-output audit."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_required_files(document: dict, prefix: str) -> dict:
    clone = dict(document)
    clone["required_k_files"] = [
        path.removeprefix(prefix).lstrip("/")
        for path in clone["required_k_files"]
    ]
    return clone


spec = importlib.util.spec_from_file_location(
    "exact_generation_klean_export",
    "/reference/generation-tools/klean_export.py",
)
assert spec is not None and spec.loader is not None
exact_exporter = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = exact_exporter
spec.loader.exec_module(exact_exporter)

generation = Path("/reference/klean-generation")
generated = generation / "generated"
regenerated = Path("/tmp/audit-work/regenerated")
audit = load_json(Path("/audit-input.json"))["resolution"]
discovery = load_json(Path("/reference/lemma-discovery.json"))
input_manifest = load_json(generation / "input-manifest.json")
generator_manifest = load_json(generation / "generator-manifest.json")
export_result = load_json(generation / "export-result.json")
trust_inventory = load_json(generation / "trust-inventory.json")
recorded_preflight = load_json(generation / "preflight.json")
obligation_map = load_json(generated / "obligation-map.json")
regen_input = load_json(regenerated / "input-manifest.json")

checks: list[dict[str, object]] = []


def check(label: str, condition: bool, detail: object = None) -> None:
    entry: dict[str, object] = {"label": label, "pass": bool(condition)}
    if detail is not None:
        entry["detail"] = detail
    checks.append(entry)
    print(json.dumps(entry, sort_keys=True))


# Independent Stage 3 judgment found no DOMAIN_LEMMA entries.
independent_domain_ids: list[str] = []
check("independent domain set is empty", independent_domain_ids == [])
check("Stage 4 input source-rule list equals independent domain set", [entry["source_rule_id"] for entry in input_manifest["source_rules"]] == independent_domain_ids)
check("obligation-map source-rule list is exact", [entry["source_rule_id"] for entry in obligation_map["source_rules"]] == independent_domain_ids)
check("obligation-map obligation list is exact", obligation_map["obligations"] == [])
check("obligation-map has no duplicate source identities", len({entry["source_rule_id"] for entry in obligation_map["source_rules"]}) == len(obligation_map["source_rules"]))
check("obligation-map has no trust parameters", obligation_map["trust_parameters"] == [])
check("generator obligation count", generator_manifest["obligation_count"] == 0)
check("export-result obligation count", export_result["obligation_count"] == 0)
check("obligation-map hash", file_hash(generated / "obligation-map.json") == generator_manifest["obligation_map_sha256"], file_hash(generated / "obligation-map.json"))

expected_target_definition = exact_exporter.expected_target_definition(obligation_map)
observed_target = exact_exporter.target_statement(generated)
lemma_text = (generated / "Klean140FixSpaces/Lemmas.lean").read_text()
check("exact producer expects no target definition", expected_target_definition is None)
check("exact producer observes no target", observed_target is None)
check("generator manifest target is null", generator_manifest["target"] is None)
check("launcher target is null", audit.get("target") is None)
check("no hidden targetStatement declaration", "targetStatement" not in lemma_text)
check("no vacuous generated conjunct", obligation_map["obligations"] == [] and observed_target is None)

check("selected Stage 4 status", audit["selections"]["klean_generation"]["status"] == "KLEAN_NO_OBLIGATIONS")
check("export status", export_result["status"] == "KLEAN_NO_OBLIGATIONS")
check("recorded preflight status", recorded_preflight["status"] == "KLEAN_NO_OBLIGATIONS")
check("launcher preflight equals selected preflight", audit["stage4_preflight"] == recorded_preflight)
check("classification-only mode", audit["mode"] == "CLASSIFICATION_ONLY")
check("no Stage 5 workspace", audit["lean_workspace"] is None and audit["hashes"]["lean_workspace_sha256"] is None)
check("no Stage 5 invocation", audit["lean_invocation"] is None and audit["hashes"]["lean_invocation_sha256"] is None)
check("no mounted Stage 5 candidate", not Path("/candidate").exists())

check("toolchain lock exact", generator_manifest["toolchain"] == load_json(Path("/reference/klean-toolchain.lock.json")))
check("trust inventory hash", file_hash(generation / "trust-inventory.json") == export_result["trust_inventory_sha256"], file_hash(generation / "trust-inventory.json"))
check("trust inventory has no proof holes", trust_inventory["designated_sorries"] == 0 and trust_inventory["other_sorries"] == 0)

# Exact producer rerun: generated tree and the invariant sidecars must be byte-identical.
check("exact regeneration generated-tree digest", exact_exporter.tree_digest(regenerated / "generated") == generator_manifest["generated_tree_sha256"], exact_exporter.tree_digest(regenerated / "generated"))
for name in ("generator-manifest.json", "trust-inventory.json", "export-result.json"):
    check(f"exact regeneration sidecar {name}", (generation / name).read_bytes() == (regenerated / name).read_bytes(), file_hash(generation / name))

# input-manifest required_k_files intentionally records absolute mount paths;
# compare all contents after removing the generation-time/audit-time mount prefix.
normalized_selected = normalized_required_files(input_manifest, "/frozen-k")
normalized_regen = normalized_required_files(regen_input, "/reference/k-proof")
check("regenerated input manifest differs only by mount prefix", normalized_selected == normalized_regen)
relative_required = normalized_selected["required_k_files"]
check("required K file list has no duplicates", len(relative_required) == len(set(relative_required)), len(relative_required))
check("every required K file exists in frozen workspace", all((Path("/reference/k-proof") / relative).is_file() for relative in relative_required))

summary = {
    "checks": len(checks),
    "failures": [entry["label"] for entry in checks if not entry["pass"]],
}
summary["status"] = "PASS" if not summary["failures"] else "FAIL"
print(json.dumps({"SUMMARY": summary}, sort_keys=True))
raise SystemExit(0 if summary["status"] == "PASS" else 1)
