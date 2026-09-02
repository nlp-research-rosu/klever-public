import hashlib
import json
import re
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification


WORKSPACE = Path("/reference/k-proof")
DISCOVERY = Path("/reference/lemma-discovery.json")


def normalized(text):
    return " ".join(text.split())


def required_closure(entry):
    pending = [entry]
    visited = []
    while pending:
        path = pending.pop()
        path = path.resolve()
        if path in visited:
            continue
        visited.append(path)
        text = path.read_text()
        for required in re.findall(r'(?m)^\s*requires\s+"([^"]+)"', text):
            child = (path.parent / required).resolve()
            if child.is_file():
                pending.append(child)
    return visited


inventory = inventory_verification(WORKSPACE)
discovery = json.loads(DISCOVERY.read_text())
rules = inventory["rules"]
rule = rules[0]
rule_lines = rule["text"].splitlines()
assert rule_lines[0].strip() == "rule"
assert rule_lines[-1].strip() == "[priority(40)]"
rule_body = "\n".join(rule_lines[1:-1])

claim_text = (WORKSPACE / "loop-connection-spec.k").read_text()
claim_match = re.search(
    r"(?ms)^\s*claim\s+\[filter-loop-connection\]:\s*\n"
    r"(?P<body>.*?)^\s*endmodule\s*$",
    claim_text,
)
assert claim_match
claim_body = claim_match.group("body").rstrip()

verification_text = (WORKSPACE / "verification.k").read_text()
span_text = "\n".join(
    verification_text.splitlines()[
        rule["start_line"] - 1 : rule["end_line"]
    ]
)
manual_normalized_sha = hashlib.sha256(
    normalized(span_text).encode()
).hexdigest()

closure = required_closure(WORKSPACE / "verification-core.k")
closure_relative = [
    path.relative_to(WORKSPACE).as_posix()
    for path in closure
    if path.is_relative_to(WORKSPACE)
]
prove_script = (WORKSPACE / "prove.sh").read_text()
order_markers = {
    "compile_bridge_free_core": prove_script.index(
        "kompile --backend haskell verification-core.k"
    ),
    "prove_auxiliary_claim": prove_script.index(
        "kprove loop-connection-spec.k"
    ),
    "compile_rule_installed": prove_script.index(
        "kompile --backend haskell verification.k"
    ),
    "prove_later_spec": prove_script.index("kprove spec.k"),
}

discovery_ids = [entry["source_rule_id"] for entry in discovery["rules"]]
inventory_ids = [entry["source_rule_id"] for entry in rules]
classification = discovery["rules"][0]["classification"]

result = {
    "inventory_rule_count": len(rules),
    "inventory_module_closure": inventory["verification_modules"],
    "inventory_ids": inventory_ids,
    "discovery_ids": discovery_ids,
    "bijective_same_order": (
        discovery_ids == inventory_ids
        and len(discovery_ids) == len(set(discovery_ids))
    ),
    "source_span": {
        "start_line": rule["start_line"],
        "end_line": rule["end_line"],
        "exact_text_match": span_text == rule["text"],
    },
    "normalized_sha256_recorded": rule["normalized_sha256"],
    "normalized_sha256_manual": manual_normalized_sha,
    "normalized_sha256_match": (
        manual_normalized_sha == rule["normalized_sha256"]
    ),
    "source_rule_id_match": (
        rule["source_rule_id"] == f"rule-{manual_normalized_sha}"
    ),
    "inventory_sha256_recorded": inventory["inventory_sha256"],
    "inventory_sha256_manual": canonical_json_sha256(rules),
    "inventory_sha256_discovery": discovery["inventory_sha256"],
    "inventory_hash_chain_match": (
        inventory["inventory_sha256"]
        == canonical_json_sha256(rules)
        == discovery["inventory_sha256"]
    ),
    "attributes": rule["attributes"],
    "is_simplification": "simplification" in rule["attributes"],
    "recorded_classification": classification,
    "exact_auxiliary_claim_body_match": (
        normalized(rule_body) == normalized(claim_body)
    ),
    "bridge_free_required_closure": closure_relative,
    "verification_rule_absent_from_auxiliary_closure": (
        "verification.k" not in closure_relative
        and normalized(rule_body)
        not in normalized(
            "\n".join(path.read_text() for path in closure)
        )
    ),
    "stage1_source_order_offsets": order_markers,
    "stage1_source_order_is_derive_then_install_then_use": (
        order_markers["compile_bridge_free_core"]
        < order_markers["prove_auxiliary_claim"]
        < order_markers["compile_rule_installed"]
        < order_markers["prove_later_spec"]
    ),
    "fresh_auxiliary_proof_top": (
        "#Top"
        in Path(
            "/audit-output/evidence/fresh-loop-connection-kprove.log"
        ).read_text()
        and "EXIT_CODE: 0"
        in Path(
            "/audit-output/evidence/fresh-loop-connection-kprove.log"
        ).read_text()
    ),
    "fresh_iterator_connection_top": (
        "#Top"
        in Path(
            "/audit-output/evidence/fresh-iterator-connection-kprove.log"
        ).read_text()
        and "EXIT_CODE: 0"
        in Path(
            "/audit-output/evidence/fresh-iterator-connection-kprove.log"
        ).read_text()
    ),
    "fresh_later_proof_top": (
        "#Top"
        in Path("/audit-output/evidence/fresh-final-kprove.log").read_text()
        and "EXIT_CODE: 0"
        in Path("/audit-output/evidence/fresh-final-kprove.log").read_text()
    ),
    "fresh_false_result_mutation_rejected": (
        "WarnStuckClaimState"
        in Path(
            "/audit-output/evidence/fresh-vacuity-mutation-kprove.log"
        ).read_text()
        and "EXIT_CODE: 1"
        in Path(
            "/audit-output/evidence/fresh-vacuity-mutation-kprove.log"
        ).read_text()
    ),
    "independent_classification": "PROVED_DERIVED_LEMMA",
    "domain_lemma_count": 0,
}

required_true = [
    "bijective_same_order",
    "normalized_sha256_match",
    "source_rule_id_match",
    "inventory_hash_chain_match",
    "exact_auxiliary_claim_body_match",
    "verification_rule_absent_from_auxiliary_closure",
    "stage1_source_order_is_derive_then_install_then_use",
    "fresh_auxiliary_proof_top",
    "fresh_iterator_connection_top",
    "fresh_later_proof_top",
    "fresh_false_result_mutation_rejected",
]
result["all_checks_pass"] = (
    all(result[key] for key in required_true)
    and classification == result["independent_classification"]
)

print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["all_checks_pass"] else 1)
