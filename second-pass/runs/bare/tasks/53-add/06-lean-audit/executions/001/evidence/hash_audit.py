#!/usr/bin/env python3
"""Independent hash reconciliation for the mounted Stage 3/4 audit inputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def comparison(label: str, expected: object, observed: object) -> bool:
    matched = expected == observed
    print(
        json.dumps(
            {
                "label": label,
                "expected": expected,
                "observed": observed,
                "match": matched,
            },
            sort_keys=True,
        )
    )
    return matched


def main() -> int:
    audit_document = json.loads(AUDIT_INPUT.read_text())
    resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
        audit_document
    )
    print(
        json.dumps(
            {
                "audit_input_envelope": "VALID",
                "resolved_input_sha256": resolved_digest,
            },
            sort_keys=True,
        )
    )
    expected_hashes = resolution["hashes"]
    observed_hashes = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(K_WORKSPACE),
        "stage1_export_sha256": klean_export.tree_digest(K_WORKSPACE),
        "discovery_manifest_sha256": file_sha256(DISCOVERY),
        "k_audit_sha256": pipeline_contract.sha256_tree(K_AUDIT),
        "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            PRODUCERS
        ),
        "generated_tree_sha256": klean_export.tree_digest(GENERATED),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    ok = comparison("resolution.hashes", expected_hashes, observed_hashes)

    observed_source_hashes = {
        path.relative_to(K_WORKSPACE).as_posix(): file_sha256(path)
        for path in pipeline_contract._walk_regular_files(
            K_WORKSPACE, "mounted Stage 1 workspace"
        )
    }
    ok &= comparison(
        "resolution.stage1_source_hashes",
        resolution["stage1_source_hashes"],
        observed_source_hashes,
    )

    ok &= comparison(
        "selection.k_audit.artifact_sha256",
        resolution["selections"]["k_audit"]["artifact_sha256"],
        observed_hashes["k_audit_sha256"],
    )
    ok &= comparison(
        "selection.klean_generation.artifact_sha256",
        resolution["selections"]["klean_generation"]["artifact_sha256"],
        observed_hashes["klean_generation_sha256"],
    )

    recorded_preflight = json.loads((GENERATION / "preflight.json").read_text())
    ok &= comparison(
        "resolution.stage4_preflight",
        resolution["stage4_preflight"],
        recorded_preflight,
    )

    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    observed_producer_files = {
        name: file_sha256(PRODUCERS / name)
        for name in ("klean.py", "klean_export.py")
    }
    expected_producer_files = {
        "klean.py": generator_manifest["klean_py_sha256"],
        "klean_export.py": generator_manifest["exporter_sha256"],
    }
    ok &= comparison(
        "source_manifest.files",
        expected_producer_files,
        source_manifest["files"],
    )
    ok &= comparison(
        "producer_file_hashes",
        expected_producer_files,
        observed_producer_files,
    )
    generator_image_id = generator_manifest["provenance"]["generator_image_id"]
    ok &= comparison(
        "generator_image_id.source_manifest",
        generator_image_id,
        source_manifest["generator_image_id"],
    )
    recorded_bundle_name = Path(
        resolution["generation_producer_sources"]
    ).name
    ok &= comparison(
        "generator_image_id.audit_input_path",
        generator_image_id.removeprefix("sha256:"),
        recorded_bundle_name,
    )

    ok &= comparison(
        "generator_manifest.generated_tree_sha256",
        generator_manifest["generated_tree_sha256"],
        observed_hashes["generated_tree_sha256"],
    )
    ok &= comparison(
        "generator_manifest.stage1_workspace_sha256",
        generator_manifest["provenance"]["stage1_workspace_sha256"],
        observed_hashes["stage1_export_sha256"],
    )
    ok &= comparison(
        "generator_manifest.stage3_discovery_manifest_sha256",
        generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
        observed_hashes["discovery_manifest_sha256"],
    )
    ok &= comparison(
        "audit_input.mode_vs_environment",
        resolution["mode"],
        __import__("os").environ.get("AUDIT_MODE"),
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
