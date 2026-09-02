#!/usr/bin/env python3
"""Recompute every launcher-recorded hash for a mounted input."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


AUDIT_INPUT = Path("/audit-input.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def report(label: str, observed: str, expected: str | None) -> bool:
    ok = observed == expected
    print(f"{label}: {'MATCH' if ok else 'MISMATCH'}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")
    return ok


def main() -> int:
    document = json.loads(AUDIT_INPUT.read_text())
    resolution = document["resolution"]
    expected = resolution["hashes"]
    checks = [
        (
            "k_workspace_sha256",
            pipeline_contract.sha256_tree(Path("/reference/k-proof")),
            expected["k_workspace_sha256"],
        ),
        (
            "stage1_export_sha256",
            klean_export.tree_digest(Path("/reference/k-proof")),
            expected["stage1_export_sha256"],
        ),
        (
            "discovery_manifest_sha256",
            sha256_file(Path("/reference/lemma-discovery.json")),
            expected["discovery_manifest_sha256"],
        ),
        (
            "k_audit_sha256",
            pipeline_contract.sha256_tree(Path("/reference/k-audit")),
            expected["k_audit_sha256"],
        ),
        (
            "klean_generation_sha256",
            pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
            expected["klean_generation_sha256"],
        ),
        (
            "generation_producer_sources_sha256",
            pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
            expected["generation_producer_sources_sha256"],
        ),
        (
            "generated_tree_sha256",
            klean_export.tree_digest(
                Path("/reference/klean-generation/generated")
            ),
            expected["generated_tree_sha256"],
        ),
        (
            "lean_workspace_sha256",
            pipeline_contract.sha256_tree(Path("/candidate")),
            expected["lean_workspace_sha256"],
        ),
    ]

    all_ok = True
    for label, observed, wanted in checks:
        all_ok = report(label, observed, wanted) and all_ok

    source_hashes = resolution["stage1_source_hashes"]
    workspace = Path("/reference/k-proof")
    observed_names = {
        path.relative_to(workspace).as_posix()
        for path in pipeline_contract._walk_regular_files(
            workspace, "mounted Stage 1 workspace"
        )
    }
    expected_names = set(source_hashes)
    print(
        "stage1_source_file_set:",
        "MATCH" if observed_names == expected_names else "MISMATCH",
    )
    print(f"  observed_count={len(observed_names)}")
    print(f"  expected_count={len(expected_names)}")
    print(f"  missing={sorted(expected_names - observed_names)}")
    print(f"  extra={sorted(observed_names - expected_names)}")
    all_ok = observed_names == expected_names and all_ok

    mismatches: list[tuple[str, str, str]] = []
    for relative in sorted(observed_names & expected_names):
        observed = sha256_file(workspace / relative)
        wanted = source_hashes[relative]
        if observed != wanted:
            mismatches.append((relative, observed, wanted))
    print(
        "stage1_source_hashes:",
        "MATCH" if not mismatches else "MISMATCH",
    )
    print(f"  checked={len(observed_names & expected_names)}")
    print(f"  mismatch_count={len(mismatches)}")
    for relative, observed, wanted in mismatches:
        print(f"  {relative}: observed={observed} expected={wanted}")
    all_ok = not mismatches and all_ok

    producer_path = Path(resolution["generation_producer_sources"])
    producer_key = producer_path.name
    source_manifest = json.loads(
        Path("/reference/generation-tools/source-manifest.json").read_text()
    )
    generator_manifest = json.loads(
        Path("/reference/klean-generation/generator-manifest.json").read_text()
    )
    producer_image_ids = {
        "audit_input_path": f"sha256:{producer_key}",
        "source_manifest": source_manifest.get("generator_image_id"),
        "generator_manifest": generator_manifest.get("provenance", {}).get(
            "generator_image_id"
        ),
    }
    image_values = set(producer_image_ids.values())
    image_ok = len(image_values) == 1
    print("generator_image_id:", "MATCH" if image_ok else "MISMATCH")
    for source, value in producer_image_ids.items():
        print(f"  {source}={value}")
    all_ok = image_ok and all_ok

    expected_producers = {
        "klean_export.py": generator_manifest.get("exporter_sha256"),
        "klean.py": generator_manifest.get("klean_py_sha256"),
    }
    manifest_ok = source_manifest.get("files") == expected_producers
    print(
        "producer_hash_manifests:",
        "MATCH" if manifest_ok else "MISMATCH",
    )
    print(f"  source_manifest={source_manifest.get('files')}")
    print(f"  generator_manifest={expected_producers}")
    all_ok = manifest_ok and all_ok
    for name, wanted in expected_producers.items():
        all_ok = report(
            f"producer_file:{name}",
            sha256_file(Path("/reference/generation-tools") / name),
            wanted,
        ) and all_ok

    print("OVERALL:", "PASS" if all_ok else "FAIL")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
