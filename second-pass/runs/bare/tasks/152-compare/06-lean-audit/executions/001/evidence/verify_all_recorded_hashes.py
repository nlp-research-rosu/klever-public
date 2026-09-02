#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import klean_export
from tools import lemma_discovery_contract
from tools import pipeline_contract
from tools import stage6_resolution_contract


def read_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_bytes())
    assert isinstance(document, dict)
    return document


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: list[dict[str, Any]] = []


def check(name: str, observed: Any, expected: Any) -> None:
    passed = observed == expected
    checks.append(
        {
            "name": name,
            "pass": passed,
            "observed": observed,
            "expected": expected,
        }
    )
    if not passed:
        raise AssertionError(
            f"{name}: observed {observed!r}, expected {expected!r}"
        )


audit_input = read_json(Path("/audit-input.json"))
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_input
)
checks.append(
    {
        "name": "Stage 6 envelope and canonical resolution digest",
        "pass": True,
        "observed": resolved_digest,
        "expected": audit_input["resolved_input_sha256"],
    }
)
mechanical_lock_path = Path(
    "/opt/humaneval/data/klean-audit-tools.lock.json"
)
mechanical_lock = read_json(mechanical_lock_path)
check(
    "mechanical checker lock SHA-256",
    sha256_file(mechanical_lock_path),
    audit_input["audit"]["mechanical_checker_lock_sha256"],
)
check("mechanical checker lock schema", mechanical_lock["schema_version"], 1)
check(
    "mechanical checker lock bundle",
    mechanical_lock["bundle"],
    "stage6-mechanical-checker",
)
for relative, expected in mechanical_lock["files"].items():
    check(
        f"mechanical checker file {relative}",
        sha256_file(Path("/reference") / relative),
        expected,
    )
check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("problem ID", resolution["problem_id"], "152-compare")
check("condition", resolution["condition"], "bare")
check(
    "semantics mode",
    resolution["semantics_mode"],
    "GENERATED_SEMANTICS",
)

generator_manifest = read_json(
    Path("/reference/klean-generation/generator-manifest.json")
)
source_manifest = read_json(
    Path("/reference/generation-tools/source-manifest.json")
)
input_manifest = read_json(
    Path("/reference/klean-generation/input-manifest.json")
)
export_result = read_json(
    Path("/reference/klean-generation/export-result.json")
)
stored_preflight = read_json(
    Path("/reference/klean-generation/preflight.json")
)
trust_inventory = read_json(
    Path("/reference/klean-generation/trust-inventory.json")
)
obligation_map = read_json(
    Path("/reference/klean-generation/generated/obligation-map.json")
)
toolchain_lock = read_json(Path("/reference/klean-toolchain.lock.json"))

producer_expected = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
check("producer manifest schema", source_manifest["schema_version"], 1)
check(
    "producer bundle exact file set",
    sorted(path.name for path in Path("/reference/generation-tools").iterdir()),
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
check("producer source file map", source_manifest["files"], producer_expected)
for name, expected in producer_expected.items():
    check(
        f"producer SHA-256 {name}",
        sha256_file(Path("/reference/generation-tools") / name),
        expected,
    )
image_id = generator_manifest["provenance"]["generator_image_id"]
check("producer image ID", source_manifest["generator_image_id"], image_id)
check(
    "audit producer bundle image key",
    Path(resolution["generation_producer_sources"]).name,
    image_id.removeprefix("sha256:"),
)

hashes = resolution["hashes"]
check(
    "Stage 1 pipeline tree SHA-256",
    pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    hashes["k_workspace_sha256"],
)
check(
    "Stage 1 exporter tree SHA-256",
    klean_export.tree_digest(Path("/reference/k-proof")),
    hashes["stage1_export_sha256"],
)
check(
    "Stage 2 selected-audit tree SHA-256",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    hashes["k_audit_sha256"],
)
check(
    "Stage 3 manifest SHA-256",
    sha256_file(Path("/reference/lemma-discovery.json")),
    hashes["discovery_manifest_sha256"],
)
check(
    "Stage 4 generation tree SHA-256",
    pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
    hashes["klean_generation_sha256"],
)
check(
    "producer-source bundle tree SHA-256",
    pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
    hashes["generation_producer_sources_sha256"],
)
check(
    "generated project exporter tree SHA-256",
    klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    hashes["generated_tree_sha256"],
)
check("classification-only Lean workspace hash", hashes["lean_workspace_sha256"], None)
check(
    "classification-only Lean invocation hash",
    hashes["lean_invocation_sha256"],
    None,
)

source_hashes = {
    path.relative_to("/reference/k-proof").as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "Stage 1 source workspace"
    )
}
check("Stage 1 exact source file/hash map", source_hashes, resolution["stage1_source_hashes"])

check(
    "generator Stage 1 provenance",
    generator_manifest["provenance"]["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "generator Stage 3 provenance",
    generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check(
    "generator generated-tree hash",
    generator_manifest["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)
check("generator toolchain lock", generator_manifest["toolchain"], toolchain_lock)
check(
    "generator obligation-map hash",
    generator_manifest["obligation_map_sha256"],
    sha256_file(
        Path("/reference/klean-generation/generated/obligation-map.json")
    ),
)

validated = lemma_discovery_contract.validate_trust_boundary(
    Path("/reference/k-proof"), Path("/reference/lemma-discovery.json")
)
check(
    "input inventory hash",
    input_manifest["inventory_sha256"],
    validated["inventory_sha256"],
)
check(
    "generator inventory provenance",
    generator_manifest["provenance"]["inventory_sha256"],
    validated["inventory_sha256"],
)
check(
    "input verification.k hash",
    input_manifest["verification_sha256"],
    sha256_file(Path("/reference/k-proof/verification.k")),
)
for label, field in (
    ("input frozen Stage 1", "frozen_input_sha256"),
    ("input Stage 1 workspace", "stage1_workspace_sha256"),
):
    check(label, input_manifest[field], hashes["stage1_export_sha256"])
check(
    "input Stage 3 manifest hash",
    input_manifest["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check("input definitions", input_manifest["definitions"], validated["definitions"])
check(
    "input operational rules",
    input_manifest["operational_rules"],
    validated["operational_rules"],
)
check(
    "input proved derived lemmas",
    input_manifest["proved_derived_lemmas"],
    validated["proved_derived_lemmas"],
)

expected_source_rules = klean_export._domain_source_rules(
    validated, hashes["discovery_manifest_sha256"]
)
check("input domain source rules", input_manifest["source_rules"], expected_source_rules)
check("obligation-map domain source rules", obligation_map["source_rules"], expected_source_rules)
check("obligation-map obligations", obligation_map["obligations"], [])
check("obligation-map trust parameters", obligation_map["trust_parameters"], [])
check("generator obligation count", generator_manifest["obligation_count"], 0)
check("generator target", generator_manifest["target"], None)
check(
    "generated target declaration",
    klean_export.target_statement(
        Path("/reference/klean-generation/generated")
    ),
    None,
)

check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check("export obligation count", export_result["obligation_count"], 0)
check(
    "export Stage 1 hash",
    export_result["frozen_input_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "export Stage 3 hash",
    export_result["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check(
    "export generated-tree hash",
    export_result["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)
check(
    "export trust-inventory hash",
    export_result["trust_inventory_sha256"],
    sha256_file(Path("/reference/klean-generation/trust-inventory.json")),
)
check("stored preflight equals signed preflight", stored_preflight, resolution["stage4_preflight"])
check("stored preflight status", stored_preflight["status"], "KLEAN_NO_OBLIGATIONS")
check("stored preflight obligation count", stored_preflight["obligation_count"], 0)
check("stored preflight target", stored_preflight["target"], None)
check(
    "stored preflight generated-tree hash",
    stored_preflight["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)
check(
    "stored preflight Stage 1 hash",
    stored_preflight["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "stored preflight Stage 3 hash",
    stored_preflight["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check(
    "stored trust count",
    stored_preflight["trust_declaration_count"],
    len(trust_inventory["allowlist"]),
)
check(
    "selected Stage 4 status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)
check("signed target", resolution["target"], None)
check("signed Stage 5 result", resolution["stage5_result"], None)
check("signed Lean workspace", resolution["lean_workspace"], None)
check("signed Lean invocation", resolution["lean_invocation"], None)
check("candidate mount absent", Path("/candidate").exists(), False)

print(json.dumps({"all_passed": True, "checks": checks}, indent=2, sort_keys=True))
