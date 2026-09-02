#!/usr/bin/env python3
"""Compare freshly compiled derived claims with their later installed rules."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path


WORK = Path("/tmp/audit-work/stage1-recheck")
MANIFEST = Path("/reference/lemma-discovery.json")


def load(path: Path) -> dict:
    return json.loads(path.read_text())


compiled = load(WORK / "verification-json-kompiled/compiled.json")
claims: dict[str, dict] = {}
for path in (WORK / "connection-spec.json", WORK / "loop-connection-spec.json"):
    document = load(path)
    for module in document["term"]["term"]:
        for sentence in module.get("localSentences", []):
            if sentence["node"] == "KClaim":
                claims[sentence["att"]["att"]["label"]] = sentence

rules: dict[tuple[str, int], dict] = {}
for module in compiled["term"]["modules"]:
    for sentence in module.get("localSentences", []):
        attributes = sentence.get("att", {}).get("att", {})
        source = str(attributes.get("org.kframework.attributes.Source", ""))
        location = attributes.get("org.kframework.attributes.Location")
        if sentence.get("node") != "KRule" or not isinstance(location, list):
            continue
        if source.endswith("/helper-verification.k") and location[0] in (15, 56):
            rules[("helper", location[0])] = sentence
        if source.endswith("/verification.k") and location[0] == 13:
            rules[("loop", 13)] = sentence


def without_counter(body: dict) -> dict:
    body = copy.deepcopy(body)
    assert body["node"] == "KApply"
    assert body["label"]["name"] == "<generatedTop>"
    assert len(body["args"]) == 11
    body["args"] = body["args"][:10]
    body["arity"] = 10
    return body


def rewrite_side(term, side: str):
    if isinstance(term, list):
        return [rewrite_side(item, side) for item in term]
    if isinstance(term, dict):
        if term.get("node") == "KRewrite":
            return rewrite_side(term[side], side)
        return {key: rewrite_side(value, side) for key, value in term.items()}
    return term


def alpha_canonical(term, variables: dict[str, str]):
    if isinstance(term, list):
        return [alpha_canonical(item, variables) for item in term]
    if isinstance(term, dict):
        if term.get("node") == "KVariable":
            name = term["name"]
            variables.setdefault(name, f"V{len(variables)}")
            result = {
                key: alpha_canonical(value, variables)
                for key, value in term.items()
                if key != "name"
            }
            result["name"] = variables[name]
            return result
        return {
            key: alpha_canonical(value, variables)
            for key, value in term.items()
        }
    return term


def side_digest(sentence: dict, side: str) -> str:
    bundle = {
        "term": rewrite_side(without_counter(sentence["body"]), side),
        "requires": sentence["requires"],
        "ensures": sentence["ensures"],
    }
    canonical = alpha_canonical(bundle, {})
    encoded = json.dumps(
        canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


pairs = [
    (
        "CONNECTION-SPEC.helper-vowel",
        ("helper", 15),
        "rule-284c4c4d20e7564f3b85f9ae093aa32298e088fc96aae41906f05d8ef3f0ef15",
    ),
    (
        "CONNECTION-SPEC.helper-consonant",
        ("helper", 56),
        "rule-08d6a79c00e8974a6bd055b18bc2d39ca1d25c682c2008be19c209f460d89d5d",
    ),
    (
        "LOOP-CONNECTION-SPEC.loop-invariant",
        ("loop", 13),
        "rule-c20cac6fc636336fce2d7dbc24f7aa987c09ce9dd8b4b8e10851db71031a2574",
    ),
]

manifest_by_id = {
    entry["source_rule_id"]: entry for entry in load(MANIFEST)["rules"]
}
comparisons = []
for claim_name, rule_key, source_rule_id in pairs:
    claim = claims[claim_name]
    rule = rules[rule_key]
    claim_counter = claim["body"]["args"][10]
    rule_counter = rule["body"]["args"][10]
    rationale = manifest_by_id[source_rule_id]["rationale"]
    lhs_claim = side_digest(claim, "lhs")
    lhs_rule = side_digest(rule, "lhs")
    rhs_claim = side_digest(claim, "rhs")
    rhs_rule = side_digest(rule, "rhs")
    comparisons.append(
        {
            "claim": claim_name,
            "source_rule_id": source_rule_id,
            "ordinary_lhs_guard_cells_claim_sha256": lhs_claim,
            "ordinary_lhs_guard_cells_rule_sha256": lhs_rule,
            "ordinary_rhs_guard_cells_claim_sha256": rhs_claim,
            "ordinary_rhs_guard_cells_rule_sha256": rhs_rule,
            "ordinary_lhs_matches": lhs_claim == lhs_rule,
            "ordinary_rhs_matches": rhs_claim == rhs_rule,
            "claim_generated_counter": claim_counter,
            "rule_generated_counter": rule_counter,
            "claim_counter_is_fresh_existential_rewrite": (
                claim_counter.get("node") == "KApply"
                and claim_counter.get("label", {}).get("name")
                == "<generatedCounter>"
                and claim_counter["args"][0].get("node") == "KRewrite"
                and claim_counter["args"][0]["lhs"].get("name") == "_Gen0"
                and claim_counter["args"][0]["rhs"].get("name", "").startswith("?")
            ),
            "installed_counter_is_one_preserved_dot_variable": (
                rule_counter.get("node") == "KVariable"
                and rule_counter.get("name", "").startswith("_DotVar")
                and rule_counter.get("sort", {}).get("name")
                == "GeneratedCounterCell"
            ),
            "mandatory_residual_caveat_recorded": all(
                fragment in rationale.lower()
                for fragment in (
                    "final counter existential",
                    "counter preservation is uncredited",
                    "no fresh-variable allocation",
                )
            ),
        }
    )

fixed_semantics_counter_mentions = []
for path in sorted((WORK / "reference-semantics").rglob("*.k")):
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if "generatedCounter" in line:
            fixed_semantics_counter_mentions.append(
                f"{path.relative_to(WORK)}:{number}:{line}"
            )

connection_compiled = (WORK / "connection-kompiled/compiled.txt").read_text()
loop_compiled = (WORK / "loop-connection-kompiled/compiled.txt").read_text()
helper_source_marker = f"Source({WORK / 'helper-verification.k'})"
final_source_marker = f"Source({WORK / 'verification.k'})"
result = {
    "connection_definition_main_module": (
        WORK / "connection-kompiled/mainModule.txt"
    ).read_text().strip(),
    "loop_connection_definition_main_module": (
        WORK / "loop-connection-kompiled/mainModule.txt"
    ).read_text().strip(),
    "connection_definition_contains_helper_installed_source": (
        helper_source_marker in connection_compiled
    ),
    "connection_definition_contains_final_loop_installed_source": (
        final_source_marker in connection_compiled
    ),
    "loop_connection_definition_contains_helper_installed_source": (
        helper_source_marker in loop_compiled
    ),
    "loop_connection_definition_contains_final_loop_installed_source": (
        final_source_marker in loop_compiled
    ),
    "fixed_semantics_generated_counter_mentions": fixed_semantics_counter_mentions,
    "comparisons": comparisons,
}
print(json.dumps(result, indent=2, sort_keys=True))

if not (
    result["connection_definition_main_module"] == "FOUNDATION"
    and result["loop_connection_definition_main_module"]
    == "HELPER-VERIFICATION"
    and not result["connection_definition_contains_helper_installed_source"]
    and not result["connection_definition_contains_final_loop_installed_source"]
    and result["loop_connection_definition_contains_helper_installed_source"]
    and not result["loop_connection_definition_contains_final_loop_installed_source"]
    and not fixed_semantics_counter_mentions
    and all(
        comparison["ordinary_lhs_matches"]
        and comparison["ordinary_rhs_matches"]
        and comparison["claim_counter_is_fresh_existential_rewrite"]
        and comparison["installed_counter_is_one_preserved_dot_variable"]
        and comparison["mandatory_residual_caveat_recorded"]
        for comparison in comparisons
    )
):
    raise SystemExit(1)
