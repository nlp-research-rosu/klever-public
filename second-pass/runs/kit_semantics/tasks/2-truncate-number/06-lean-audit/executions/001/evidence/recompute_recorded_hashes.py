#!/usr/bin/env python3
"""Recompute every launcher-recorded Stage 3/4 classification-only hash."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(
    checks: list[dict[str, object]],
    name: str,
    observed: object,
    expected: object,
) -> None:
    checks.append(
        {
            "name": name,
            "observed": observed,
            "expected": expected,
            "match": observed == expected,
        }
    )


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    resolution = audit["resolution"]
    expected_hashes = resolution["hashes"]
    generator = json.loads((GENERATION / "generator-manifest.json").read_text())
    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    export_result = json.loads((GENERATION / "export-result.json").read_text())

    checks: list[dict[str, object]] = []
    record(
        checks,
        "pipeline k_workspace_sha256",
        pipeline_contract.sha256_tree(K_PROOF),
        expected_hashes["k_workspace_sha256"],
    )
    record(
        checks,
        "export stage1_export_sha256",
        klean_export.tree_digest(K_PROOF),
        expected_hashes["stage1_export_sha256"],
    )
    record(
        checks,
        "discovery_manifest_sha256",
        file_sha256(DISCOVERY),
        expected_hashes["discovery_manifest_sha256"],
    )
    record(
        checks,
        "pipeline k_audit_sha256",
        pipeline_contract.sha256_tree(K_AUDIT),
        expected_hashes["k_audit_sha256"],
    )
    record(
        checks,
        "pipeline klean_generation_sha256",
        pipeline_contract.sha256_tree(GENERATION),
        expected_hashes["klean_generation_sha256"],
    )
    record(
        checks,
        "pipeline generation_producer_sources_sha256",
        pipeline_contract.sha256_tree(PRODUCERS),
        expected_hashes["generation_producer_sources_sha256"],
    )
    record(
        checks,
        "export generated_tree_sha256",
        klean_export.tree_digest(GENERATED),
        expected_hashes["generated_tree_sha256"],
    )
    record(
        checks,
        "generator generated_tree_sha256",
        klean_export.tree_digest(GENERATED),
        generator["generated_tree_sha256"],
    )

    stage1_files = {
        path.relative_to(K_PROOF).as_posix(): file_sha256(path)
        for path in pipeline_contract._walk_regular_files(
            K_PROOF, "mounted Stage 1 workspace"
        )
    }
    expected_stage1_files = resolution["stage1_source_hashes"]
    stage1_missing = sorted(set(expected_stage1_files) - set(stage1_files))
    stage1_extra = sorted(set(stage1_files) - set(expected_stage1_files))
    stage1_mismatches = sorted(
        name
        for name in set(stage1_files) & set(expected_stage1_files)
        if stage1_files[name] != expected_stage1_files[name]
    )
    checks.append(
        {
            "name": "all stage1_source_hashes",
            "observed_count": len(stage1_files),
            "expected_count": len(expected_stage1_files),
            "missing": stage1_missing,
            "extra": stage1_extra,
            "mismatches": stage1_mismatches,
            "match": not stage1_missing
            and not stage1_extra
            and not stage1_mismatches,
        }
    )

    producer_files = {
        "klean_export.py": file_sha256(PRODUCERS / "klean_export.py"),
        "klean.py": file_sha256(PRODUCERS / "klean.py"),
    }
    record(checks, "producer files vs source manifest", producer_files, source_manifest["files"])
    record(
        checks,
        "klean_export.py vs generator manifest",
        producer_files["klean_export.py"],
        generator["exporter_sha256"],
    )
    record(
        checks,
        "klean.py vs generator manifest",
        producer_files["klean.py"],
        generator["klean_py_sha256"],
    )
    image_id = generator["provenance"]["generator_image_id"]
    record(
        checks,
        "generator image vs source manifest",
        source_manifest["generator_image_id"],
        image_id,
    )
    record(
        checks,
        "generator image vs audit-input producer path",
        Path(resolution["generation_producer_sources"]).name,
        image_id.removeprefix("sha256:"),
    )
    record(
        checks,
        "Stage 1 provenance across generator/input/audit",
        {
            "generator": generator["provenance"]["stage1_workspace_sha256"],
            "input_manifest": input_manifest["stage1_workspace_sha256"],
            "export_result": export_result["frozen_input_sha256"],
        },
        {
            "generator": expected_hashes["stage1_export_sha256"],
            "input_manifest": expected_hashes["stage1_export_sha256"],
            "export_result": expected_hashes["stage1_export_sha256"],
        },
    )
    record(
        checks,
        "Stage 3 provenance across generator/input/export/audit",
        {
            "generator": generator["provenance"][
                "stage3_discovery_manifest_sha256"
            ],
            "input_manifest": input_manifest[
                "stage3_discovery_manifest_sha256"
            ],
            "export_result": export_result[
                "stage3_discovery_manifest_sha256"
            ],
        },
        {
            "generator": expected_hashes["discovery_manifest_sha256"],
            "input_manifest": expected_hashes["discovery_manifest_sha256"],
            "export_result": expected_hashes["discovery_manifest_sha256"],
        },
    )
    record(
        checks,
        "generated provenance across generator/export/audit",
        {
            "generator": generator["generated_tree_sha256"],
            "export_result": export_result["generated_tree_sha256"],
        },
        {
            "generator": expected_hashes["generated_tree_sha256"],
            "export_result": expected_hashes["generated_tree_sha256"],
        },
    )
    record(
        checks,
        "classification-only Lean hashes are null",
        {
            "lean_workspace_sha256": expected_hashes[
                "lean_workspace_sha256"
            ],
            "lean_invocation_sha256": expected_hashes[
                "lean_invocation_sha256"
            ],
        },
        {
            "lean_workspace_sha256": None,
            "lean_invocation_sha256": None,
        },
    )

    result = {
        "checks": checks,
        "all_match": all(check["match"] is True for check in checks),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["all_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
