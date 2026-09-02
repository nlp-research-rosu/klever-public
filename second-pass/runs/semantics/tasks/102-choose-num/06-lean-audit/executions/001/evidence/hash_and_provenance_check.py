#!/usr/bin/env python3
"""Independently recompute the launcher-recorded immutable-input hashes."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_files(root: Path) -> list[Path]:
    return pipeline_contract._walk_regular_files(root, str(root))


def main() -> int:
    document = json.loads(AUDIT_INPUT.read_text())
    resolution, resolved_digest = (
        stage6_resolution_contract.verify_audit_input(document)
    )
    recorded = resolution["hashes"]
    generator = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    input_manifest = json.loads(
        (GENERATION / "input-manifest.json").read_text()
    )
    export_result = json.loads(
        (GENERATION / "export-result.json").read_text()
    )
    preflight = json.loads((GENERATION / "preflight.json").read_text())
    source_manifest = json.loads(
        (PRODUCERS / "source-manifest.json").read_text()
    )
    lock = json.loads(TOOLCHAIN_LOCK.read_text())

    checks: dict[str, dict[str, Any]] = {}

    def check(name: str, observed: Any, expected: Any) -> None:
        checks[name] = {
            "observed": observed,
            "expected": expected,
            "match": observed == expected,
        }

    check(
        "resolved_input_sha256",
        stage6_resolution_contract.canonical_json_sha256(resolution),
        resolved_digest,
    )
    check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
    check("problem_id", resolution["problem_id"], "102-choose-num")
    check("condition", resolution["condition"], "semantics")
    check(
        "semantics_mode",
        resolution["semantics_mode"],
        "SUPPLIED_SEMANTICS",
    )

    pipeline_workspace_hash = pipeline_contract.sha256_tree(K_WORKSPACE)
    export_workspace_hash = klean_export.tree_digest(K_WORKSPACE)
    discovery_hash = sha256_file(DISCOVERY)
    k_audit_hash = pipeline_contract.sha256_tree(K_AUDIT)
    generation_hash = pipeline_contract.sha256_tree(GENERATION)
    producer_hash = pipeline_contract.sha256_tree(PRODUCERS)
    generated_hash = klean_export.tree_digest(GENERATED)

    check(
        "hashes.k_workspace_sha256",
        pipeline_workspace_hash,
        recorded["k_workspace_sha256"],
    )
    check(
        "hashes.stage1_export_sha256",
        export_workspace_hash,
        recorded["stage1_export_sha256"],
    )
    check(
        "hashes.discovery_manifest_sha256",
        discovery_hash,
        recorded["discovery_manifest_sha256"],
    )
    check(
        "hashes.k_audit_sha256",
        k_audit_hash,
        recorded["k_audit_sha256"],
    )
    check(
        "hashes.klean_generation_sha256",
        generation_hash,
        recorded["klean_generation_sha256"],
    )
    check(
        "hashes.generation_producer_sources_sha256",
        producer_hash,
        recorded["generation_producer_sources_sha256"],
    )
    check(
        "hashes.generated_tree_sha256",
        generated_hash,
        recorded["generated_tree_sha256"],
    )
    check("hashes.lean_workspace_sha256", None, recorded["lean_workspace_sha256"])
    check(
        "hashes.lean_invocation_sha256",
        None,
        recorded["lean_invocation_sha256"],
    )

    observed_stage1_sources = {
        path.relative_to(K_WORKSPACE).as_posix(): sha256_file(path)
        for path in regular_files(K_WORKSPACE)
    }
    check(
        "stage1_source_hashes",
        observed_stage1_sources,
        resolution["stage1_source_hashes"],
    )

    producer_files = {
        path.relative_to(PRODUCERS).as_posix()
        for path in regular_files(PRODUCERS)
    }
    check(
        "producer_bundle_file_set",
        sorted(producer_files),
        ["klean.py", "klean_export.py", "source-manifest.json"],
    )
    check(
        "producer.klean_export.py",
        sha256_file(PRODUCERS / "klean_export.py"),
        generator["exporter_sha256"],
    )
    check(
        "producer.klean.py",
        sha256_file(PRODUCERS / "klean.py"),
        generator["klean_py_sha256"],
    )
    check(
        "source_manifest.schema_version",
        source_manifest.get("schema_version"),
        1,
    )
    check(
        "source_manifest.files",
        source_manifest.get("files"),
        {
            "klean_export.py": generator["exporter_sha256"],
            "klean.py": generator["klean_py_sha256"],
        },
    )
    generator_image_id = generator["provenance"]["generator_image_id"]
    check(
        "source_manifest.generator_image_id",
        source_manifest.get("generator_image_id"),
        generator_image_id,
    )
    check(
        "audit_input.generator_image_path_key",
        Path(resolution["generation_producer_sources"]).name,
        generator_image_id.removeprefix("sha256:"),
    )

    check("generator.toolchain", generator["toolchain"], lock)
    check(
        "generator.generated_tree_sha256",
        generator["generated_tree_sha256"],
        generated_hash,
    )
    check(
        "generator.stage1_workspace_sha256",
        generator["provenance"]["stage1_workspace_sha256"],
        export_workspace_hash,
    )
    check(
        "generator.stage3_discovery_manifest_sha256",
        generator["provenance"]["stage3_discovery_manifest_sha256"],
        discovery_hash,
    )
    check(
        "input_manifest.frozen_input_sha256",
        input_manifest["frozen_input_sha256"],
        export_workspace_hash,
    )
    check(
        "input_manifest.stage1_workspace_sha256",
        input_manifest["stage1_workspace_sha256"],
        export_workspace_hash,
    )
    check(
        "input_manifest.stage3_discovery_manifest_sha256",
        input_manifest["stage3_discovery_manifest_sha256"],
        discovery_hash,
    )
    check(
        "input_manifest.verification_sha256",
        input_manifest["verification_sha256"],
        sha256_file(K_WORKSPACE / "verification.k"),
    )
    check(
        "export_result.frozen_input_sha256",
        export_result["frozen_input_sha256"],
        export_workspace_hash,
    )
    check(
        "export_result.stage3_discovery_manifest_sha256",
        export_result["stage3_discovery_manifest_sha256"],
        discovery_hash,
    )
    check(
        "export_result.generated_tree_sha256",
        export_result["generated_tree_sha256"],
        generated_hash,
    )
    check(
        "export_result.trust_inventory_sha256",
        export_result["trust_inventory_sha256"],
        sha256_file(GENERATION / "trust-inventory.json"),
    )
    check(
        "generator.obligation_map_sha256",
        generator["obligation_map_sha256"],
        sha256_file(GENERATED / "obligation-map.json"),
    )

    check(
        "audit_input.stage4_preflight",
        resolution["stage4_preflight"],
        preflight,
    )
    check("audit_input.target", resolution["target"], generator["target"])
    check("audit_input.stage5_result", resolution["stage5_result"], None)
    check("candidate_absent", Path("/candidate").exists(), False)
    check("audit_input.lean_workspace", resolution["lean_workspace"], None)
    check("audit_input.lean_invocation", resolution["lean_invocation"], None)
    check(
        "selection.k_audit.artifact_sha256",
        resolution["selections"]["k_audit"]["artifact_sha256"],
        k_audit_hash,
    )
    check(
        "selection.klean_generation.artifact_sha256",
        resolution["selections"]["klean_generation"]["artifact_sha256"],
        generation_hash,
    )
    check(
        "selection.klean_generation.status",
        resolution["selections"]["klean_generation"]["status"],
        "KLEAN_NO_OBLIGATIONS",
    )

    failures = [name for name, item in checks.items() if not item["match"]]
    print(
        json.dumps(
            {
                "schema_version": 1,
                "checks": checks,
                "failure_count": len(failures),
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
