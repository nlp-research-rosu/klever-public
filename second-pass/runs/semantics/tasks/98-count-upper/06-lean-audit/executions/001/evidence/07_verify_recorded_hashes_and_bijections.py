#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.k_rule_inventory import inventory_verification
from tools.klean_audit_contract import verify_stage6_audit_input


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in pipeline_contract._walk_regular_files(root, "audited tree"):
        result[path.relative_to(root).as_posix()] = file_sha256(path)
    return dict(sorted(result.items()))


failures: list[str] = []
checks: list[dict[str, object]] = []


def check(label: str, observed: object, expected: object) -> None:
    passed = observed == expected
    checks.append(
        {
            "label": label,
            "passed": passed,
            "observed": observed,
            "expected": expected,
        }
    )
    if not passed:
        failures.append(label)


audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
resolution, resolved_digest = verify_stage6_audit_input(audit)
check("audit envelope resolved_input_sha256", resolved_digest, audit["resolved_input_sha256"])
check("AUDIT_MODE binding", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("problem binding", resolution["problem_id"], "98-count-upper")
check("condition binding", resolution["condition"], "semantics")
check("semantics mode binding", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")

k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery_path = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer_bundle = Path("/reference/generation-tools")
hashes = resolution["hashes"]

observed_tree_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(k_workspace),
    "stage1_export_sha256": klean_export.tree_digest(k_workspace),
    "discovery_manifest_sha256": file_sha256(discovery_path),
    "k_audit_sha256": pipeline_contract.sha256_tree(k_audit),
    "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        producer_bundle
    ),
    "generated_tree_sha256": klean_export.tree_digest(generated),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}
for key, observed in observed_tree_hashes.items():
    check(f"audit-input resolution.hashes.{key}", observed, hashes[key])

stage1_hashes = regular_file_hashes(k_workspace)
Path("/audit-output/evidence/actual-stage1-source-hashes.json").write_text(
    json.dumps(stage1_hashes, indent=2, sort_keys=True) + "\n"
)
expected_stage1_hashes = resolution["stage1_source_hashes"]
stage1_name_mismatches = sorted(
    set(stage1_hashes) ^ set(expected_stage1_hashes)
)
check(
    "all Stage 1 regular-file names",
    stage1_name_mismatches,
    [],
)
stage1_mismatches = [
    name
    for name in sorted(set(stage1_hashes) | set(expected_stage1_hashes))
    if stage1_hashes.get(name) != expected_stage1_hashes.get(name)
]
check("all Stage 1 regular-file hashes", stage1_mismatches, [])
checks.append(
    {
        "label": "Stage 1 source-hash map evidence",
        "passed": not stage1_mismatches,
        "entry_count": len(stage1_hashes),
        "expected_entry_count": len(expected_stage1_hashes),
        "canonical_map_sha256": canonical_sha256(stage1_hashes),
        "evidence_file": "/audit-output/evidence/actual-stage1-source-hashes.json",
    }
)

check(
    "selected K audit artifact hash",
    resolution["selections"]["k_audit"]["artifact_sha256"],
    observed_tree_hashes["k_audit_sha256"],
)
check(
    "selected Stage 4 artifact hash",
    resolution["selections"]["klean_generation"]["artifact_sha256"],
    observed_tree_hashes["klean_generation_sha256"],
)
check(
    "selected Stage 4 status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)

generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
source_manifest = json.loads((producer_bundle / "source-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
preflight = json.loads((generation / "preflight.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
obligation_map = json.loads((generated / "obligation-map.json").read_text())
toolchain_lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())

producer_hashes = {
    "klean_export.py": file_sha256(producer_bundle / "klean_export.py"),
    "klean.py": file_sha256(producer_bundle / "klean.py"),
}
check("producer source-manifest exact files", source_manifest["files"], producer_hashes)
check(
    "producer klean_export.py hash in generator manifest",
    generator_manifest["exporter_sha256"],
    producer_hashes["klean_export.py"],
)
check(
    "producer klean.py hash in generator manifest",
    generator_manifest["klean_py_sha256"],
    producer_hashes["klean.py"],
)
generator_image_id = generator_manifest["provenance"]["generator_image_id"]
check(
    "producer image ID: generator vs source manifest",
    generator_image_id,
    source_manifest["generator_image_id"],
)
check(
    "producer image ID: audit-input source-bundle path",
    Path(resolution["generation_producer_sources"]).name,
    generator_image_id.removeprefix("sha256:"),
)
check(
    "producer bundle exact regular-file names",
    sorted(regular_file_hashes(producer_bundle)),
    ["klean.py", "klean_export.py", "source-manifest.json"],
)

check("generator toolchain equals lock", generator_manifest["toolchain"], toolchain_lock)
check(
    "generated tree: generator manifest",
    generator_manifest["generated_tree_sha256"],
    observed_tree_hashes["generated_tree_sha256"],
)
check(
    "generated tree: preflight",
    preflight["generated_tree_sha256"],
    observed_tree_hashes["generated_tree_sha256"],
)
check(
    "generated tree: export result",
    export_result["generated_tree_sha256"],
    observed_tree_hashes["generated_tree_sha256"],
)
check(
    "generated tree: audit-input stage4 preflight",
    resolution["stage4_preflight"]["generated_tree_sha256"],
    observed_tree_hashes["generated_tree_sha256"],
)
check(
    "stored preflight equals audit-input preflight",
    preflight,
    resolution["stage4_preflight"],
)

inventory = inventory_verification(k_workspace)
discovery = json.loads(discovery_path.read_text())
inventory_rules = inventory["rules"]
discovery_rules = discovery["rules"]
inventory_ids = [entry["source_rule_id"] for entry in inventory_rules]
discovery_ids = [entry["source_rule_id"] for entry in discovery_rules]
check("Stage 3 inventory hash", discovery["inventory_sha256"], inventory["inventory_sha256"])
check("Stage 3 ordered source-rule identities", discovery_ids, inventory_ids)
check("Stage 3 source-rule identity uniqueness", len(set(discovery_ids)), len(discovery_ids))
check("Stage 3 rule count", len(discovery_rules), len(inventory_rules))

for rule in inventory_rules:
    normalized = " ".join(rule["text"].split())
    digest = hashlib.sha256(normalized.encode()).hexdigest()
    check(
        f"{rule['source_rule_id']} normalized source hash",
        rule["normalized_sha256"],
        digest,
    )
    check(
        f"{rule['source_rule_id']} source_rule_id",
        rule["source_rule_id"],
        f"rule-{digest}",
    )

independent_classifications = [
    {
        "source_rule_id": inventory_ids[0],
        "classification": "DEFINITION",
        "basis": "base equation for the fresh named summary countUpperFrom",
    },
    {
        "source_rule_id": inventory_ids[1],
        "classification": "DEFINITION",
        "basis": "constructor-decreasing recurrence for the fresh named summary countUpperFrom",
    },
]
check(
    "independent classifications vs Stage 3",
    [
        {
            "source_rule_id": item["source_rule_id"],
            "classification": item["classification"],
        }
        for item in independent_classifications
    ],
    [
        {
            "source_rule_id": item["source_rule_id"],
            "classification": item["classification"],
        }
        for item in discovery_rules
    ],
)
expected_classified_rules = []
for inventory_rule, discovery_rule in zip(inventory_rules, discovery_rules):
    expected_classified_rules.append(
        {
            **inventory_rule,
            "classification": discovery_rule["classification"],
            "rationale": discovery_rule["rationale"],
        }
    )
check(
    "input-manifest ordered DEFINITION records",
    input_manifest["definitions"],
    expected_classified_rules,
)
check("input-manifest operational_rules", input_manifest["operational_rules"], [])
check(
    "input-manifest proved_derived_lemmas",
    input_manifest["proved_derived_lemmas"],
    [],
)
check(
    "input-manifest summary function signature",
    input_manifest["summary_functions"],
    [
        {
            "name": "countUpperFrom",
            "return_sort": "Int",
            "argument_sorts": ["IntSeq", "Bool"],
        }
    ],
)
check(
    "input-manifest verification module",
    input_manifest["verification_module"],
    inventory["verification_module"],
)
check(
    "input-manifest verification hash",
    input_manifest["verification_sha256"],
    inventory["verification_sha256"],
)
check(
    "input-manifest Stage 1 tree hash",
    input_manifest["stage1_workspace_sha256"],
    observed_tree_hashes["stage1_export_sha256"],
)
check(
    "input-manifest Stage 3 file hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    observed_tree_hashes["discovery_manifest_sha256"],
)
check(
    "generator provenance Stage 1 tree hash",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    observed_tree_hashes["stage1_export_sha256"],
)
check(
    "generator provenance Stage 3 file hash",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    observed_tree_hashes["discovery_manifest_sha256"],
)
simplification_ids = [
    rule["source_rule_id"]
    for rule in inventory_rules
    if "simplification" in rule["attributes"]
]
check("simplification rules requiring classification policy", simplification_ids, [])

domain_ids = [
    item["source_rule_id"]
    for item in independent_classifications
    if item["classification"] == "DOMAIN_LEMMA"
]
check("independently classified DOMAIN_LEMMA set", domain_ids, [])
check("input-manifest source_rules", input_manifest["source_rules"], [])
check("obligation-map source_rules", obligation_map["source_rules"], [])
check("obligation-map obligations", obligation_map["obligations"], [])
check("obligation-map trust_parameters", obligation_map["trust_parameters"], [])
check("generator obligation_count", generator_manifest["obligation_count"], 0)
check("preflight obligation_count", preflight["obligation_count"], 0)
check("export obligation_count", export_result["obligation_count"], 0)
check("generator target", generator_manifest["target"], None)
check("preflight target", preflight["target"], None)
check("audit-input target", resolution["target"], None)
check("audit-input Stage 4 preflight target", resolution["stage4_preflight"]["target"], None)
check("generated target declaration", klean_export.target_statement(generated), None)
check("candidate absence in classification-only mode", Path("/candidate").exists(), False)

check(
    "input-manifest inventory hash",
    input_manifest["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "generator provenance inventory hash",
    generator_manifest["provenance"]["inventory_sha256"],
    inventory["inventory_sha256"],
)
check(
    "generator obligation-map file hash",
    generator_manifest["obligation_map_sha256"],
    file_sha256(generated / "obligation-map.json"),
)
check(
    "export trust-inventory file hash",
    export_result["trust_inventory_sha256"],
    file_sha256(generation / "trust-inventory.json"),
)

result = {
    "status": "PASS" if not failures else "FAIL",
    "failure_count": len(failures),
    "failures": failures,
    "check_count": len(checks),
    "checks": checks,
    "independent_classifications": independent_classifications,
}
Path("/audit-output/evidence/recorded-hash-and-bijection-check.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n"
)
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if not failures else 1)
