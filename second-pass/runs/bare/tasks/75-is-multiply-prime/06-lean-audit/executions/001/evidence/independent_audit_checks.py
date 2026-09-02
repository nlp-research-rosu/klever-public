#!/usr/bin/env python3
"""Independent structural, provenance, and mathematical checks for this audit."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
from pathlib import Path

from tools.k_rule_inventory import canonical_json_sha256, inventory_verification
from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree
from tools.stage6_resolution_contract import verify_audit_input


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(label: str, condition: bool, detail: object) -> None:
    print(f"{label}: {'PASS' if condition else 'FAIL'}")
    print(f"  {detail}")
    if not condition:
        raise AssertionError(label)


def source_equality_constants(path: Path) -> list[int]:
    tree = ast.parse(path.read_text())
    constants: list[int] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Compare)
            and len(node.ops) == 1
            and isinstance(node.ops[0], ast.Eq)
            and len(node.comparators) == 1
            and isinstance(node.left, ast.Name)
            and node.left.id == "a"
            and isinstance(node.comparators[0], ast.Constant)
            and isinstance(node.comparators[0].value, int)
        ):
            constants.append(node.comparators[0].value)
    return constants


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
obligation_map = json.loads(
    Path(
        "/reference/klean-generation/generated/obligation-map.json"
    ).read_text()
)
trust_inventory_path = Path(
    "/reference/klean-generation/trust-inventory.json"
)
inventory = inventory_verification(Path("/reference/k-proof"))

print("AUDIT MODE")
verified_resolution, verified_resolution_digest = verify_audit_input(audit)
require(
    "signed resolved-input digest",
    verified_resolution == resolution
    and verified_resolution_digest == audit["resolved_input_sha256"],
    {
        "recomputed": verified_resolution_digest,
        "recorded": audit["resolved_input_sha256"],
    },
)
require(
    "environment/launcher mode",
    os.environ.get("AUDIT_MODE") == resolution["mode"] == "CLASSIFICATION_ONLY",
    {
        "environment": os.environ.get("AUDIT_MODE"),
        "launcher": resolution["mode"],
    },
)
require(
    "no Stage 5 candidate in classification-only mode",
    not Path("/candidate").exists()
    and resolution["lean_workspace"] is None
    and resolution["lean_invocation"] is None
    and resolution["hashes"]["lean_workspace_sha256"] is None
    and resolution["hashes"]["lean_invocation_sha256"] is None
    and resolution["stage5_result"] is None,
    {
        "candidate_exists": Path("/candidate").exists(),
        "lean_workspace": resolution["lean_workspace"],
        "lean_invocation": resolution["lean_invocation"],
        "stage5_result": resolution["stage5_result"],
    },
)

print("\nPRODUCER PROVENANCE")
producer_actual = {
    name: sha256_file(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
require(
    "producer file hashes match source manifest",
    producer_actual == source_manifest["files"],
    {"actual": producer_actual, "recorded": source_manifest["files"]},
)
require(
    "producer hashes match generator manifest",
    producer_actual["klean_export.py"] == generator["exporter_sha256"]
    and producer_actual["klean.py"] == generator["klean_py_sha256"],
    {
        "actual": producer_actual,
        "generator_exporter": generator["exporter_sha256"],
        "generator_klean": generator["klean_py_sha256"],
    },
)
launcher_image_hex = Path(
    resolution["generation_producer_sources"]
).name
manifest_image_ids = {
    source_manifest["generator_image_id"],
    generator["provenance"]["generator_image_id"],
}
require(
    "immutable generator image identity",
    manifest_image_ids == {f"sha256:{launcher_image_hex}"},
    {
        "launcher_source_directory_id": launcher_image_hex,
        "manifest_ids": sorted(manifest_image_ids),
    },
)
require(
    "producer source tree hash",
    sha256_tree(Path("/reference/generation-tools"))
    == resolution["hashes"]["generation_producer_sources_sha256"],
    {
        "actual": sha256_tree(Path("/reference/generation-tools")),
        "recorded": resolution["hashes"][
            "generation_producer_sources_sha256"
        ],
    },
)

print("\nSTAGE 1 AND SELECTED-TREE HASHES")
actual_stage1_sources = {
    path.relative_to("/reference/k-proof").as_posix(): sha256_file(path)
    for path in Path("/reference/k-proof").rglob("*")
    if path.is_file() and not path.is_symlink()
}
require(
    "Stage 1 per-file source hashes",
    actual_stage1_sources == resolution["stage1_source_hashes"],
    {
        "actual": actual_stage1_sources,
        "recorded": resolution["stage1_source_hashes"],
    },
)
tree_checks = {
    "k_workspace_sha256": sha256_tree(Path("/reference/k-proof")),
    "k_audit_sha256": sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
}
for field, actual in tree_checks.items():
    require(
        field,
        actual == resolution["hashes"][field],
        {"actual": actual, "recorded": resolution["hashes"][field]},
    )
require(
    "selected Stage 2 tree binding",
    tree_checks["k_audit_sha256"]
    == resolution["selections"]["k_audit"]["artifact_sha256"],
    {
        "actual": tree_checks["k_audit_sha256"],
        "selection": resolution["selections"]["k_audit"][
            "artifact_sha256"
        ],
    },
)
require(
    "selected Stage 4 tree binding",
    tree_checks["klean_generation_sha256"]
    == resolution["selections"]["klean_generation"]["artifact_sha256"],
    {
        "actual": tree_checks["klean_generation_sha256"],
        "selection": resolution["selections"]["klean_generation"][
            "artifact_sha256"
        ],
    },
)
require(
    "Stage 1 deterministic export hash",
    tree_digest(Path("/reference/k-proof"))
    == resolution["hashes"]["stage1_export_sha256"]
    == input_manifest["frozen_input_sha256"]
    == input_manifest["stage1_workspace_sha256"]
    == generator["provenance"]["stage1_workspace_sha256"],
    {
        "actual": tree_digest(Path("/reference/k-proof")),
        "launcher": resolution["hashes"]["stage1_export_sha256"],
        "input_manifest": input_manifest["stage1_workspace_sha256"],
        "generator": generator["provenance"]["stage1_workspace_sha256"],
    },
)
require(
    "Stage 4 preflight Stage 1 hash binding",
    tree_digest(Path("/reference/k-proof"))
    == resolution["stage4_preflight"]["frozen_input_sha256"]
    == resolution["stage4_preflight"]["stage1_workspace_sha256"],
    {
        "actual": tree_digest(Path("/reference/k-proof")),
        "preflight": resolution["stage4_preflight"][
            "stage1_workspace_sha256"
        ],
    },
)
discovery_hash = sha256_file(Path("/reference/lemma-discovery.json"))
require(
    "Stage 3 manifest hash",
    discovery_hash
    == resolution["hashes"]["discovery_manifest_sha256"]
    == input_manifest["stage3_discovery_manifest_sha256"]
    == generator["provenance"]["stage3_discovery_manifest_sha256"]
    == export_result["stage3_discovery_manifest_sha256"],
    {
        "actual": discovery_hash,
        "launcher": resolution["hashes"]["discovery_manifest_sha256"],
    },
)
require(
    "Stage 4 preflight Stage 3 hash binding",
    discovery_hash
    == resolution["stage4_preflight"][
        "stage3_discovery_manifest_sha256"
    ],
    {
        "actual": discovery_hash,
        "preflight": resolution["stage4_preflight"][
            "stage3_discovery_manifest_sha256"
        ],
    },
)
generated_hash = tree_digest(
    Path("/reference/klean-generation/generated")
)
require(
    "generated tree hash",
    generated_hash
    == resolution["hashes"]["generated_tree_sha256"]
    == generator["generated_tree_sha256"]
    == export_result["generated_tree_sha256"],
    {
        "actual": generated_hash,
        "launcher": resolution["hashes"]["generated_tree_sha256"],
    },
)
require(
    "Stage 4 preflight generated-tree hash binding",
    generated_hash
    == resolution["stage4_preflight"]["generated_tree_sha256"],
    {
        "actual": generated_hash,
        "preflight": resolution["stage4_preflight"][
            "generated_tree_sha256"
        ],
    },
)
require(
    "verification.k file-hash binding",
    sha256_file(Path("/reference/k-proof/verification.k"))
    == input_manifest["verification_sha256"],
    {
        "actual": sha256_file(Path("/reference/k-proof/verification.k")),
        "input_manifest": input_manifest["verification_sha256"],
    },
)
require(
    "pinned toolchain manifest identity",
    json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
    == generator["toolchain"],
    generator["toolchain"],
)
require(
    "trust inventory hash",
    sha256_file(trust_inventory_path)
    == export_result["trust_inventory_sha256"],
    {
        "actual": sha256_file(trust_inventory_path),
        "recorded": export_result["trust_inventory_sha256"],
    },
)

print("\nRULE INVENTORY AND STAGE 3 BIJECTION")
canonical_rules = inventory["rules"]
manifest_entries = discovery["rules"]
canonical_ids = [entry["source_rule_id"] for entry in canonical_rules]
manifest_ids = [entry["source_rule_id"] for entry in manifest_entries]
require(
    "inventory hash recomputation",
    canonical_json_sha256(canonical_rules)
    == inventory["inventory_sha256"]
    == discovery["inventory_sha256"]
    == input_manifest["inventory_sha256"]
    == generator["provenance"]["inventory_sha256"],
    {
        "actual": canonical_json_sha256(canonical_rules),
        "recorded": inventory["inventory_sha256"],
    },
)
require(
    "ordered source-rule identity bijection",
    canonical_ids == manifest_ids
    and len(manifest_ids) == len(set(manifest_ids)),
    {"canonical": canonical_ids, "manifest": manifest_ids},
)
require(
    "one reconstructed local rule",
    len(canonical_rules) == 1,
    canonical_rules,
)
rule = canonical_rules[0]
normalized = " ".join(rule["text"].split())
normalized_hash = hashlib.sha256(normalized.encode()).hexdigest()
require(
    "rule span, normalized hash, and source_rule_id",
    rule["module"] == "VERIFICATION"
    and rule["start_line"] == 11
    and rule["end_line"] == 34
    and normalized_hash == rule["normalized_sha256"]
    and rule["source_rule_id"] == f"rule-{normalized_hash}",
    rule,
)
require(
    "classification and simplification policy",
    manifest_entries[0]["classification"] == "DEFINITION"
    and "simplification" in rule["attributes"],
    {
        "classification": manifest_entries[0]["classification"],
        "attributes": rule["attributes"],
    },
)

print("\nINDEPENDENT MATHEMATICAL ADEQUACY")
primes = [number for number in range(2, 100) if is_prime(number)]
oracle_products = sorted(
    {
        p * q * r
        for i, p in enumerate(primes)
        for j, q in enumerate(primes[i:], start=i)
        for r in primes[j:]
        if p * q * r < 100
    }
)
solution_constants = source_equality_constants(
    Path("/reference/k-proof/solution.py")
)
rule_products = [
    int(left) * int(middle) * int(right)
    for left, middle, right in re.findall(
        r"\((\d+) \*Int (\d+) \*Int (\d+)\)", rule["text"]
    )
]
require(
    "source equality constants exactly characterize triple-prime products",
    solution_constants == oracle_products,
    {
        "source": solution_constants,
        "independent_oracle": oracle_products,
    },
)
require(
    "definition products exactly match source and oracle",
    rule_products == solution_constants == oracle_products,
    {
        "definition": rule_products,
        "source": solution_constants,
        "oracle": oracle_products,
    },
)
witnesses = [-7, 0, 1, 7, 8, 12, 30, 49, 97, 98, 99, 100]
for witness in witnesses:
    source_value = witness in solution_constants
    definition_value = witness in rule_products
    oracle_value = any(
        p * q * r == witness
        for p in primes
        for q in primes
        for r in primes
    )
    require(
        f"adversarial witness {witness}",
        source_value == definition_value == oracle_value,
        {
            "source": source_value,
            "definition": definition_value,
            "oracle": oracle_value,
        },
    )
require(
    "definition is referenced by the frozen postcondition",
    "Bool(isThreePrimeProductBelow100(A))"
    in Path("/reference/k-proof/spec.k").read_text(),
    "spec.k result cell",
)
require(
    "definition is non-operational and terminating",
    "<k>" not in rule["text"]
    and "isThreePrimeProductBelow100" not in rule["text"].split("=>", 1)[1],
    {
        "has_k_cell": "<k>" in rule["text"],
        "recursive_rhs": "isThreePrimeProductBelow100"
        in rule["text"].split("=>", 1)[1],
    },
)

print("\nSTAGE 4 OBLIGATION AND TARGET IDENTITY")
require(
    "genuinely empty domain set",
    input_manifest["source_rules"] == []
    and obligation_map["source_rules"] == []
    and obligation_map["obligations"] == []
    and generator["obligation_count"] == 0
    and export_result["obligation_count"] == 0,
    {
        "input_source_rules": input_manifest["source_rules"],
        "mapped_source_rules": obligation_map["source_rules"],
        "obligations": obligation_map["obligations"],
    },
)
require(
    "empty trust-parameter set",
    obligation_map["trust_parameters"] == [],
    obligation_map["trust_parameters"],
)
require(
    "obligation map hash",
    sha256_file(
        Path(
            "/reference/klean-generation/generated/obligation-map.json"
        )
    )
    == generator["obligation_map_sha256"],
    {
        "actual": sha256_file(
            Path(
                "/reference/klean-generation/generated/obligation-map.json"
            )
        ),
        "recorded": generator["obligation_map_sha256"],
    },
)
actual_target = target_statement(
    Path("/reference/klean-generation/generated")
)
require(
    "fixed generated target is absent",
    actual_target is None
    and generator["target"] is None
    and resolution["target"] is None
    and resolution["stage4_preflight"]["target"] is None,
    {
        "actual": actual_target,
        "generator": generator["target"],
        "launcher": resolution["target"],
    },
)
require(
    "KLEAN_NO_OBLIGATIONS status agreement",
    export_result["status"] == "KLEAN_NO_OBLIGATIONS"
    and resolution["selections"]["klean_generation"]["status"]
    == "KLEAN_NO_OBLIGATIONS"
    and resolution["stage4_preflight"]["status"]
    == "KLEAN_NO_OBLIGATIONS",
    {
        "export": export_result["status"],
        "selection": resolution["selections"]["klean_generation"]["status"],
        "launcher_preflight": resolution["stage4_preflight"]["status"],
    },
)

print("\nALL INDEPENDENT CHECKS PASSED")
