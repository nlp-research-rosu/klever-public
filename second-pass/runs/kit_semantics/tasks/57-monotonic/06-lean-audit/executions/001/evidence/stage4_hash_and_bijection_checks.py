#!/usr/bin/env python3
"""Independent Stage 4 hash and source/obligation bijection checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export


GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
DISCOVERY = Path("/reference/lemma-discovery.json")
VERIFICATION = Path("/reference/k-proof/verification.k")


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(label: str, actual: object, expected: object) -> bool:
    match = actual == expected
    print(
        json.dumps(
            {
                "check": label,
                "actual": actual,
                "expected": expected,
                "match": match,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return match


generator = json.loads((GENERATION / "generator-manifest.json").read_text())
inputs = json.loads((GENERATION / "input-manifest.json").read_text())
export = json.loads((GENERATION / "export-result.json").read_text())
preflight = json.loads((GENERATION / "preflight.json").read_text())
obligation_map_path = GENERATED / "obligation-map.json"
obligation_map = json.loads(obligation_map_path.read_text())

overall = True
overall &= checked(
    "obligation-map file SHA-256",
    sha_file(obligation_map_path),
    generator["obligation_map_sha256"],
)
overall &= checked(
    "trust-inventory file SHA-256",
    sha_file(GENERATION / "trust-inventory.json"),
    export["trust_inventory_sha256"],
)
overall &= checked(
    "generated project tree SHA-256",
    klean_export.tree_digest(GENERATED),
    generator["generated_tree_sha256"],
)
overall &= checked(
    "export generated tree SHA-256",
    export["generated_tree_sha256"],
    generator["generated_tree_sha256"],
)
overall &= checked(
    "published preflight generated tree SHA-256",
    preflight["generated_tree_sha256"],
    generator["generated_tree_sha256"],
)
overall &= checked(
    "input verification.k SHA-256",
    inputs["verification_sha256"],
    sha_file(VERIFICATION),
)
overall &= checked(
    "Stage 3 file SHA-256 across sidecars",
    [
        inputs["stage3_discovery_manifest_sha256"],
        generator["provenance"]["stage3_discovery_manifest_sha256"],
        export["stage3_discovery_manifest_sha256"],
        preflight["stage3_discovery_manifest_sha256"],
    ],
    [sha_file(DISCOVERY)] * 4,
)

expected_conjuncts = [
    (
        "rule-9da3d0e2a43f2a59d88512067068ed2de6ddc5b6972e73b0a57e10a6e46fc33d",
        "∀ (B : SortBool) (A : SortBool) (h : (A) = true), "
        "(«_==Bool_» A (_orBool_ A B) : SortBool) = "
        "(true : SortBool)",
    ),
    (
        "rule-26e479bca972e68e6643e9eb5546744b4b881a595b804fd4fd237f23c16a00d4",
        "∀ (B : SortBool) (A : SortBool) "
        "(h : (notBool_ A) = true), "
        "(«_==Bool_» B (_orBool_ A B) : SortBool) = "
        "(true : SortBool)",
    ),
]
obligations = obligation_map["obligations"]
source_rules = obligation_map["source_rules"]
observed_ids = [entry["source_rule_id"] for entry in obligations]
source_ids = [entry["source_rule_id"] for entry in source_rules]
input_ids = [entry["source_rule_id"] for entry in inputs["source_rules"]]
expected_ids = [source_rule_id for source_rule_id, _ in expected_conjuncts]
overall &= checked(
    "source-rule/obligation identity order",
    (input_ids, source_ids, observed_ids),
    (expected_ids, expected_ids, expected_ids),
)
overall &= checked(
    "obligation identities unique",
    len(set(observed_ids)),
    len(observed_ids),
)
overall &= checked(
    "obligation count across sidecars",
    (
        len(obligations),
        generator["obligation_count"],
        export["obligation_count"],
        preflight["obligation_count"],
    ),
    (2, 2, 2, 2),
)

for index, (expected_id, expected_conjunct) in enumerate(expected_conjuncts):
    obligation = obligations[index]
    source_rule = source_rules[index]
    overall &= checked(
        f"obligation {index} exact Lean translation",
        obligation["lean_conjunct"],
        expected_conjunct,
    )
    overall &= checked(
        f"obligation {index} Lean conjunct SHA-256",
        obligation["lean_conjunct_sha256"],
        klean_export.sha256_text(expected_conjunct),
    )
    overall &= checked(
        f"obligation {index} source identity",
        obligation["source_rule_id"],
        expected_id,
    )
    overall &= checked(
        f"obligation {index} source span",
        obligation["source_span"],
        {
            "start_line": source_rule["start_line"],
            "end_line": source_rule["end_line"],
        },
    )
    for field in (
        "normalized_sha256",
        "inventory_sha256",
        "discovery_manifest_sha256",
    ):
        overall &= checked(
            f"obligation {index} {field}",
            obligation[field],
            source_rule[field],
        )

target = klean_export.target_statement(GENERATED)
expected_target_definition = klean_export.expected_target_definition(
    obligation_map
)
overall &= checked("recomputed target object", target, generator["target"])
overall &= checked(
    "target definition is exact obligation conjunction",
    target["definition_sha256"],
    klean_export.sha256_text(expected_target_definition),
)
overall &= checked(
    "target statement SHA-256",
    target["statement_sha256"],
    klean_export.sha256_text(target["statement"]),
)

print(
    "guard_satisfiability="
    "rule0 has A=true with either B; rule1 has A=false with either B"
)
print(
    "mathematical_translation="
    "rule0 states A=(A or B) when A; rule1 states B=(A or B) "
    "when not A; both are relevant Boolean identities"
)
print(f"STAGE4_HASH_AND_BIJECTION_OVERALL={'PASS' if overall else 'FAIL'}")
raise SystemExit(0 if overall else 1)
