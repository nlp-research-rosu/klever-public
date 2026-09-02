#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import inventory_verification


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode())


generation = Path("/reference/klean-generation")
generated = generation / "generated"
discovery_path = Path("/reference/lemma-discovery.json")
discovery_hash = sha256_bytes(discovery_path.read_bytes())
discovery = json.loads(discovery_path.read_text())
inventory = inventory_verification(Path("/reference/k-proof"))
inventory_by_id = {
    rule["source_rule_id"]: rule for rule in inventory["rules"]
}
classification_by_id = {
    rule["source_rule_id"]: rule for rule in discovery["rules"]
}
domain_rules = [
    {
        **rule,
        **classification_by_id[rule["source_rule_id"]],
        "inventory_sha256": inventory["inventory_sha256"],
        "discovery_manifest_sha256": discovery_hash,
    }
    for rule in inventory["rules"]
    if classification_by_id[rule["source_rule_id"]]["classification"]
    == "DOMAIN_LEMMA"
]

input_manifest = json.loads((generation / "input-manifest.json").read_text())
generator_manifest = json.loads(
    (generation / "generator-manifest.json").read_text()
)
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map_path = generated / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())
trust_inventory_path = generation / "trust-inventory.json"
toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]

obligations = obligation_map["obligations"]
parameters = obligation_map["trust_parameters"]
domain_ids = [rule["source_rule_id"] for rule in domain_rules]
obligation_ids = [
    obligation["source_rule_id"] for obligation in obligations
]

source_alignment = []
for source_rule, obligation in zip(domain_rules, obligations):
    source_alignment.append(
        {
            "source_rule_id": source_rule["source_rule_id"],
            "id_matches": (
                source_rule["source_rule_id"]
                == obligation["source_rule_id"]
            ),
            "source_span_matches": obligation["source_span"]
            == {
                "start_line": source_rule["start_line"],
                "end_line": source_rule["end_line"],
            },
            "normalized_hash_matches": (
                obligation["normalized_sha256"]
                == source_rule["normalized_sha256"]
            ),
            "inventory_hash_matches": (
                obligation["inventory_sha256"]
                == source_rule["inventory_sha256"]
            ),
            "discovery_hash_matches": (
                obligation["discovery_manifest_sha256"]
                == source_rule["discovery_manifest_sha256"]
            ),
            "conjunct_hash_matches": (
                obligation["lean_conjunct_sha256"]
                == sha256_text(obligation["lean_conjunct"])
            ),
        }
    )

expected_definition_lines = ["def targetStatement"]
for parameter in parameters:
    expected_definition_lines.append(
        f'    ({parameter["name"]} : {parameter["type"]})'
    )
expected_definition_lines.extend(
    (
        "    : Prop :=",
        "    "
        + "\n    ∧ ".join(
            f'({obligation["lean_conjunct"]})'
            for obligation in obligations
        ),
    )
)
expected_definition = "\n".join(expected_definition_lines)

lean_files = sorted(generated.rglob("*.lean"))
target_matches = []
raw_target_declaration_count = 0
for lean_file in lean_files:
    text = lean_file.read_text()
    raw_target_declaration_count += len(
        re.findall(r"(?m)^\s*def\s+targetStatement\b", text)
    )
    for match in re.finditer(
        r"(?ms)^\s*def\s+targetStatement\b.*?"
        r"(?=^\s*end\s+\S+\s*$)",
        text,
    ):
        target_matches.append(
            {
                "file": lean_file.relative_to(generated).as_posix(),
                "definition": match.group(0).strip(),
            }
        )

target_definition = (
    target_matches[0]["definition"]
    if len(target_matches) == 1
    else ""
)
target_file = (
    target_matches[0]["file"] if len(target_matches) == 1 else ""
)
target_declaration = (
    f"{Path(target_file).parent.name}.Lemmas.targetStatement"
    if target_file
    else ""
)
target_statement = " ".join(
    [target_declaration] + [parameter["name"] for parameter in parameters]
)
reconstructed_target = {
    "declaration": target_declaration,
    "file": target_file,
    "statement": target_statement,
    "statement_sha256": sha256_text(target_statement),
    "definition_sha256": sha256_text(target_definition),
    "parameters": parameters,
}

parameter_checks = []
for parameter in parameters:
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "type": parameter["type"],
        "source_rule_ids": parameter["source_rule_ids"],
    }
    parameter_checks.append(
        {
            "name": parameter["name"],
            "binding_sha256_matches": parameter["binding_sha256"]
            == sha256_text(
                json.dumps(
                    binding,
                    sort_keys=True,
                    separators=(",", ":"),
                )
            ),
            "source_rule_ids_equal_domain_set_in_order": (
                parameter["source_rule_ids"] == domain_ids
            ),
            "kore_symbol_is_valSeqConcat": parameter["kore_symbol"]
            == (
                "LblvalSeqConcat'LParUndsCommUndsRParUnds'"
                "MPY-LIST'Unds'ValSeq'Unds'ValSeq'Unds'ValSeq"
            ),
        }
    )

conjunct_nonvacuity = []
for obligation in obligations:
    conjunct = obligation["lean_conjunct"]
    binder_prefix, body = conjunct.split("), ", 1)
    binders = re.findall(
        r"\((\w+)\s*:\s*SortValSeq\)", binder_prefix + ")"
    )
    conjunct_nonvacuity.append(
        {
            "source_rule_id": obligation["source_rule_id"],
            "contains_true_or_false": bool(
                re.search(r"\b(?:True|False)\b", conjunct)
            ),
            "has_equality": "=" in conjunct,
            "quantified_variables": binders,
            "each_quantified_variable_used_after_binder": all(
                len(re.findall(rf"\b{re.escape(name)}\b", conjunct)) >= 2
                for name in binders
            ),
            "equality_sides_textually_distinct": (
                len(body.split(" = ", 1)) == 2
                and body.split(" = ", 1)[0] != body.split(" = ", 1)[1]
            ),
        }
    )

print(
    json.dumps(
        {
            "domain_rule_ids": domain_ids,
            "obligation_rule_ids": obligation_ids,
            "bijection": {
                "same_order": obligation_ids == domain_ids,
                "same_count": len(obligation_ids) == len(domain_ids),
                "no_duplicate_obligation_ids": len(set(obligation_ids))
                == len(obligation_ids),
                "input_manifest_source_rules_match": input_manifest[
                    "source_rules"
                ]
                == domain_rules,
                "obligation_map_source_rules_match": obligation_map[
                    "source_rules"
                ]
                == domain_rules,
            },
            "source_alignment": source_alignment,
            "conjunct_nonvacuity": conjunct_nonvacuity,
            "parameter_checks": parameter_checks,
            "target": {
                "raw_target_declaration_count": raw_target_declaration_count,
                "regex_target_count": len(target_matches),
                "expected_definition_equals_generated": (
                    expected_definition == target_definition
                ),
                "expected_definition_sha256": sha256_text(
                    expected_definition
                ),
                "generated_definition_sha256": sha256_text(
                    target_definition
                ),
                "reconstructed": reconstructed_target,
                "equals_generator_manifest": reconstructed_target
                == generator_manifest["target"],
                "equals_audit_input_target": reconstructed_target
                == audit["target"],
                "equals_audit_input_preflight_target": reconstructed_target
                == audit["stage4_preflight"]["target"],
            },
            "manifest_hashes": {
                "obligation_map": {
                    "observed": sha256_bytes(
                        obligation_map_path.read_bytes()
                    ),
                    "recorded": generator_manifest[
                        "obligation_map_sha256"
                    ],
                },
                "trust_inventory": {
                    "observed": sha256_bytes(
                        trust_inventory_path.read_bytes()
                    ),
                    "recorded": export_result[
                        "trust_inventory_sha256"
                    ],
                },
                "verification": {
                    "observed": sha256_bytes(
                        Path(
                            "/reference/k-proof/verification.k"
                        ).read_bytes()
                    ),
                    "recorded": input_manifest[
                        "verification_sha256"
                    ],
                },
                "generator_toolchain_equals_lock": generator_manifest[
                    "toolchain"
                ]
                == toolchain_lock,
                "generator_obligation_count_matches": generator_manifest[
                    "obligation_count"
                ]
                == len(obligations),
                "export_obligation_count_matches": export_result[
                    "obligation_count"
                ]
                == len(obligations),
            },
        },
        indent=2,
        sort_keys=True,
    )
)
