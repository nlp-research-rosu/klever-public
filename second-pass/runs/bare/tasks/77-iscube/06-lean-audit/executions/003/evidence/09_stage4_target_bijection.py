import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


def load(path: str):
    return json.loads(Path(path).read_text())


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


audit = load("/audit-input.json")
discovery = load("/reference/lemma-discovery.json")
input_manifest = load("/reference/klean-generation/input-manifest.json")
generator_manifest = load(
    "/reference/klean-generation/generator-manifest.json"
)
obligation_map = load(
    "/reference/klean-generation/generated/obligation-map.json"
)
replayed_preflight = load(
    "/audit-output/evidence/06_check_generation_returned.json"
)
inventory = inventory_verification(Path("/reference/k-proof"))

domain_ids = [
    rule["source_rule_id"]
    for rule in discovery["rules"]
    if rule["classification"] == "DOMAIN_LEMMA"
]
reconstructed_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}
map_source_ids = [
    rule["source_rule_id"] for rule in obligation_map["source_rules"]
]
obligation_ids = [
    obligation["source_rule_id"]
    for obligation in obligation_map["obligations"]
]

parameters = obligation_map["trust_parameters"]
expected_lines = ["def targetStatement"]
for parameter in parameters:
    expected_lines.append(
        f'    ({parameter["name"]} : {parameter["type"]})'
    )
expected_lines.extend(
    (
        "    : Prop :=",
        "    "
        + "\n    ∧ ".join(
            f'({obligation["lean_conjunct"]})'
            for obligation in obligation_map["obligations"]
        ),
    )
)
expected_definition = "\n".join(expected_lines)

lemma_path = Path(
    "/reference/klean-generation/generated/Klean77Iscube/Lemmas.lean"
)
lemma_text = lemma_path.read_text()
start = lemma_text.index("def targetStatement")
end = lemma_text.index("\n\nend Klean77Iscube.Lemmas", start)
actual_definition = lemma_text[start:end].strip()

declaration = "Klean77Iscube.Lemmas.targetStatement"
statement = " ".join(
    [declaration, *[parameter["name"] for parameter in parameters]]
)
computed_target = {
    "declaration": declaration,
    "file": "Klean77Iscube/Lemmas.lean",
    "statement": statement,
    "statement_sha256": sha256_text(statement),
    "definition_sha256": sha256_text(actual_definition),
    "parameters": parameters,
}

manifest_targets = {
    "generator_manifest": generator_manifest["target"],
    "audit_input_target": audit["resolution"]["target"],
    "audit_input_stage4_preflight": audit["resolution"][
        "stage4_preflight"
    ]["target"],
    "replayed_preflight": replayed_preflight["target"],
}

source_rule_checks = []
for source_rule, obligation in zip(
    obligation_map["source_rules"],
    obligation_map["obligations"],
    strict=True,
):
    source_rule_id = source_rule["source_rule_id"]
    reconstructed = reconstructed_by_id[source_rule_id]
    source_rule_checks.append(
        {
            "source_rule_id": source_rule_id,
            "source_record_matches_reconstruction": all(
                source_rule[key] == reconstructed[key]
                for key in (
                    "source_rule_id",
                    "module",
                    "start_line",
                    "end_line",
                    "normalized_sha256",
                    "attributes",
                    "text",
                )
            ),
            "obligation_span_matches_reconstruction": (
                obligation["source_span"]
                == {
                    "start_line": reconstructed["start_line"],
                    "end_line": reconstructed["end_line"],
                }
            ),
            "obligation_normalized_hash_matches": (
                obligation["normalized_sha256"]
                == reconstructed["normalized_sha256"]
            ),
            "obligation_conjunct_hash_matches": (
                obligation["lean_conjunct_sha256"]
                == sha256_text(obligation["lean_conjunct"])
            ),
        }
    )

candidate_text = Path("/candidate/Proof.lean").read_text()
report = {
    "domain_source_rule_ids": domain_ids,
    "obligation_map_source_rule_ids": map_source_ids,
    "obligation_ids": obligation_ids,
    "ordered_bijection": (
        domain_ids == map_source_ids == obligation_ids
        and len(domain_ids) == len(set(domain_ids))
    ),
    "source_rule_checks": source_rule_checks,
    "input_manifest_domain_ids": [
        rule["source_rule_id"] for rule in input_manifest["source_rules"]
    ],
    "input_manifest_definition_ids": [
        rule["source_rule_id"] for rule in input_manifest["definitions"]
    ],
    "input_manifest_operational_ids": [
        rule["source_rule_id"]
        for rule in input_manifest["operational_rules"]
    ],
    "input_manifest_derived_ids": [
        rule["source_rule_id"]
        for rule in input_manifest["proved_derived_lemmas"]
    ],
    "obligation_count_matches_all_manifests": (
        len(domain_ids)
        == generator_manifest["obligation_count"]
        == replayed_preflight["obligation_count"]
        == 2
    ),
    "actual_target_definition": actual_definition,
    "expected_target_definition": expected_definition,
    "actual_definition_equals_obligation_assembly": (
        actual_definition == expected_definition
    ),
    "computed_target": computed_target,
    "all_recorded_targets_equal_computed": all(
        target == computed_target for target in manifest_targets.values()
    ),
    "recorded_targets": manifest_targets,
    "candidate_target_declaration_count": len(
        re.findall(r"(?m)^\s*def\s+targetStatement\b", candidate_text)
    ),
    "candidate_mentions_fixed_target_in_final_type": (
        "Klean77Iscube.Lemmas.targetStatement "
        "«_-Int_» _andBool_ «_>=Int_» «_<Int_» «_<=Int_» "
        "«_==Int_» «_+Int_» «_*Int_»"
        in candidate_text
    ),
}

print(json.dumps(report, indent=2, sort_keys=True))
