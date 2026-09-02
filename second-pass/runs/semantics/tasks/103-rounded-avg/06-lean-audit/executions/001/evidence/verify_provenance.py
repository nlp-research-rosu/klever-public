#!/usr/bin/env python3
"""Independent hash and provenance reconciliation for this mounted audit."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import klean_export, pipeline_contract
from tools.stage6_resolution_contract import verify_audit_input


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
    return value


results: dict[str, Any] = {}
failures: list[str] = []


def check(name: str, observed: Any, expected: Any) -> None:
    passed = observed == expected
    results[name] = {
        "observed": observed,
        "expected": expected,
        "pass": passed,
    }
    if not passed:
        failures.append(name)


audit_input = load_json(Path("/audit-input.json"))
resolution, resolved_digest = verify_audit_input(audit_input)
source_manifest = load_json(
    Path("/reference/generation-tools/source-manifest.json")
)
generator_manifest = load_json(
    Path("/reference/klean-generation/generator-manifest.json")
)
input_manifest = load_json(
    Path("/reference/klean-generation/input-manifest.json")
)
export_result = load_json(
    Path("/reference/klean-generation/export-result.json")
)
preflight = load_json(Path("/reference/klean-generation/preflight.json"))
trust_inventory = Path("/reference/klean-generation/trust-inventory.json")
obligation_map = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
toolchain_lock = load_json(Path("/reference/klean-toolchain.lock.json"))

pipeline_trees = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
}
for field, observed in pipeline_trees.items():
    check(
        f"audit_input.hashes.{field}",
        observed,
        resolution["hashes"][field],
    )

stage1_export = klean_export.tree_digest(Path("/reference/k-proof"))
generated_tree = klean_export.tree_digest(
    Path("/reference/klean-generation/generated")
)
discovery_hash = file_sha256(Path("/reference/lemma-discovery.json"))
check(
    "audit_input.hashes.stage1_export_sha256",
    stage1_export,
    resolution["hashes"]["stage1_export_sha256"],
)
check(
    "audit_input.hashes.generated_tree_sha256",
    generated_tree,
    resolution["hashes"]["generated_tree_sha256"],
)
check(
    "audit_input.hashes.discovery_manifest_sha256",
    discovery_hash,
    resolution["hashes"]["discovery_manifest_sha256"],
)
check(
    "audit_input.hashes.lean_workspace_sha256",
    resolution["hashes"]["lean_workspace_sha256"],
    None,
)
check(
    "audit_input.hashes.lean_invocation_sha256",
    resolution["hashes"]["lean_invocation_sha256"],
    None,
)
check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("audit_input.resolved_input_sha256", resolved_digest, audit_input[
    "resolved_input_sha256"
])

observed_stage1_sources = {
    path.relative_to("/reference/k-proof").as_posix(): file_sha256(path)
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file() and not path.is_symlink()
}
check(
    "audit_input.stage1_source_hashes",
    observed_stage1_sources,
    resolution["stage1_source_hashes"],
)

producer_files = {
    path.relative_to("/reference/generation-tools").as_posix()
    for path in Path("/reference/generation-tools").iterdir()
    if path.is_file() and not path.is_symlink()
}
check(
    "producer_bundle.exact_file_set",
    sorted(producer_files),
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
producer_hashes = {
    "klean_export.py": file_sha256(
        Path("/reference/generation-tools/klean_export.py")
    ),
    "klean.py": file_sha256(
        Path("/reference/generation-tools/klean.py")
    ),
}
check(
    "producer_source_manifest.exact_keys",
    sorted(source_manifest),
    ["files", "generator_image_id", "schema_version"],
)
check("producer_source_manifest.schema_version", source_manifest.get(
    "schema_version"
), 1)
check(
    "producer_source_manifest.files",
    producer_hashes,
    source_manifest.get("files"),
)
check(
    "generator_manifest.exporter_sha256",
    producer_hashes["klean_export.py"],
    generator_manifest.get("exporter_sha256"),
)
check(
    "generator_manifest.klean_py_sha256",
    producer_hashes["klean.py"],
    generator_manifest.get("klean_py_sha256"),
)
generator_image = generator_manifest.get("provenance", {}).get(
    "generator_image_id"
)
check(
    "producer_source_manifest.generator_image_id",
    source_manifest.get("generator_image_id"),
    generator_image,
)
check(
    "audit_input.generator_image_id_path_binding",
    "sha256:" + Path(resolution[
        "generation_producer_sources"
    ]).name,
    generator_image,
)

check(
    "generator_manifest.generated_tree_sha256",
    generated_tree,
    generator_manifest.get("generated_tree_sha256"),
)
check(
    "generator_manifest.obligation_map_sha256",
    file_sha256(obligation_map),
    generator_manifest.get("obligation_map_sha256"),
)
check(
    "generator_manifest.toolchain",
    generator_manifest.get("toolchain"),
    toolchain_lock,
)
check(
    "generator_manifest.provenance.stage1_workspace_sha256",
    stage1_export,
    generator_manifest.get("provenance", {}).get(
        "stage1_workspace_sha256"
    ),
)
check(
    "generator_manifest.provenance.stage3_discovery_manifest_sha256",
    discovery_hash,
    generator_manifest.get("provenance", {}).get(
        "stage3_discovery_manifest_sha256"
    ),
)
check(
    "generator_manifest.provenance.inventory_sha256",
    input_manifest.get("inventory_sha256"),
    generator_manifest.get("provenance", {}).get("inventory_sha256"),
)

verification_hash = file_sha256(Path("/reference/k-proof/verification.k"))
for name, document in (
    ("input_manifest.frozen_input_sha256", input_manifest),
    ("input_manifest.stage1_workspace_sha256", input_manifest),
    ("export_result.frozen_input_sha256", export_result),
    ("preflight.frozen_input_sha256", preflight),
    ("preflight.stage1_workspace_sha256", preflight),
):
    field = name.rsplit(".", 1)[1]
    check(name, document.get(field), stage1_export)
for name, document in (
    (
        "input_manifest.stage3_discovery_manifest_sha256",
        input_manifest,
    ),
    (
        "export_result.stage3_discovery_manifest_sha256",
        export_result,
    ),
    (
        "preflight.stage3_discovery_manifest_sha256",
        preflight,
    ),
):
    field = name.rsplit(".", 1)[1]
    check(name, document.get(field), discovery_hash)
for name, document in (
    ("generator_manifest.generated_tree_sha256_again", generator_manifest),
    ("export_result.generated_tree_sha256", export_result),
    ("preflight.generated_tree_sha256", preflight),
):
    field = (
        "generated_tree_sha256"
        if name.endswith("_again")
        else name.rsplit(".", 1)[1]
    )
    check(name, document.get(field), generated_tree)
check(
    "input_manifest.verification_sha256",
    input_manifest.get("verification_sha256"),
    verification_hash,
)
check(
    "export_result.trust_inventory_sha256",
    export_result.get("trust_inventory_sha256"),
    file_sha256(trust_inventory),
)
check(
    "audit_input.stage4_preflight",
    resolution.get("stage4_preflight"),
    preflight,
)
check(
    "audit_input.target",
    resolution.get("target"),
    generator_manifest.get("target"),
)
check(
    "audit_input.classification_only_stage5",
    {
        "mode": resolution.get("mode"),
        "lean_workspace": resolution.get("lean_workspace"),
        "lean_invocation": resolution.get("lean_invocation"),
        "stage5_result": resolution.get("stage5_result"),
        "candidate_exists": Path("/candidate").exists(),
    },
    {
        "mode": "CLASSIFICATION_ONLY",
        "lean_workspace": None,
        "lean_invocation": None,
        "stage5_result": None,
        "candidate_exists": False,
    },
)
check(
    "selection.k_audit.artifact_sha256",
    pipeline_trees["k_audit_sha256"],
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
check(
    "selection.klean_generation.artifact_sha256",
    pipeline_trees["klean_generation_sha256"],
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)
check(
    "selection.klean_generation.status",
    resolution["selections"]["klean_generation"]["status"],
    "KLEAN_NO_OBLIGATIONS",
)

target_statement = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
check(
    "fixed_generated_target_absent",
    {
        "generator_manifest": generator_manifest.get("target"),
        "audit_input": resolution.get("target"),
        "preflight": preflight.get("target"),
        "mechanically_reconstructed": target_statement,
    },
    {
        "generator_manifest": None,
        "audit_input": None,
        "preflight": None,
        "mechanically_reconstructed": None,
    },
)

summary = {
    "status": "PASS" if not failures else "FAIL",
    "failure_count": len(failures),
    "failures": failures,
    "checks": results,
}
print(json.dumps(summary, indent=2, sort_keys=True))
raise SystemExit(0 if not failures else 1)
