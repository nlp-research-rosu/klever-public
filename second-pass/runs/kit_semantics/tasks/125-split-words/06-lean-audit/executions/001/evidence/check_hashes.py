#!/usr/bin/env python3
"""Independent hash recomputation for the mounted audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, object]:
    document = json.loads(path.read_text())
    assert isinstance(document, dict)
    return document


def report(label: str, observed: object, expected: object) -> bool:
    ok = observed == expected
    print(f"{label}: {'MATCH' if ok else 'MISMATCH'}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")
    return ok


def regular_files(root: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    pending = [root]
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    pending.append(path)
                elif stat.S_ISREG(mode):
                    result[path.relative_to(root).as_posix()] = path
    return result


def main() -> None:
    audit = load(AUDIT_INPUT)
    resolution = audit["resolution"]
    assert isinstance(resolution, dict)
    expected_hashes = resolution["hashes"]
    assert isinstance(expected_hashes, dict)

    all_ok = True
    all_ok &= report(
        "launcher mode versus AUDIT_MODE",
        os.environ.get("AUDIT_MODE"),
        resolution["mode"],
    )
    all_ok &= report(
        "launcher semantics mode",
        resolution["semantics_mode"],
        "SUPPLIED_SEMANTICS",
    )
    all_ok &= report(
        "launcher problem",
        resolution["problem_id"],
        "125-split-words",
    )
    all_ok &= report(
        "launcher condition",
        resolution["condition"],
        "kit-semantics",
    )

    tree_checks = [
        (
            "pipeline k_workspace tree",
            pipeline_contract.sha256_tree(K_PROOF),
            expected_hashes["k_workspace_sha256"],
        ),
        (
            "pipeline k_audit tree",
            pipeline_contract.sha256_tree(K_AUDIT),
            expected_hashes["k_audit_sha256"],
        ),
        (
            "pipeline klean_generation tree",
            pipeline_contract.sha256_tree(GENERATION),
            expected_hashes["klean_generation_sha256"],
        ),
        (
            "pipeline generation producer tree",
            pipeline_contract.sha256_tree(PRODUCERS),
            expected_hashes["generation_producer_sources_sha256"],
        ),
        (
            "KLean frozen Stage 1 export tree",
            klean_export.tree_digest(K_PROOF),
            expected_hashes["stage1_export_sha256"],
        ),
        (
            "KLean generated project tree",
            klean_export.tree_digest(GENERATED),
            expected_hashes["generated_tree_sha256"],
        ),
        (
            "Stage 3 discovery file",
            sha256_file(DISCOVERY),
            expected_hashes["discovery_manifest_sha256"],
        ),
    ]
    for label, observed, expected in tree_checks:
        all_ok &= report(label, observed, expected)

    selections = resolution["selections"]
    assert isinstance(selections, dict)
    all_ok &= report(
        "selected K audit artifact hash",
        tree_checks[1][1],
        selections["k_audit"]["artifact_sha256"],
    )
    all_ok &= report(
        "selected KLean generation artifact hash",
        tree_checks[2][1],
        selections["klean_generation"]["artifact_sha256"],
    )

    expected_sources = resolution["stage1_source_hashes"]
    assert isinstance(expected_sources, dict)
    observed_paths = regular_files(K_PROOF)
    expected_paths = set(expected_sources)
    actual_paths = set(observed_paths)
    missing = sorted(expected_paths - actual_paths)
    extra = sorted(actual_paths - expected_paths)
    mismatched = []
    for relative in sorted(expected_paths & actual_paths):
        observed = sha256_file(observed_paths[relative])
        if observed != expected_sources[relative]:
            mismatched.append(
                (relative, observed, expected_sources[relative])
            )
    source_ok = not missing and not extra and not mismatched
    all_ok &= source_ok
    print(f"Stage 1 per-file source hashes: {'MATCH' if source_ok else 'MISMATCH'}")
    print(f"  expected_file_count={len(expected_paths)}")
    print(f"  observed_file_count={len(actual_paths)}")
    print(f"  missing={missing}")
    print(f"  extra={extra}")
    print(f"  mismatched={mismatched}")

    source_manifest = load(PRODUCERS / "source-manifest.json")
    generator_manifest = load(GENERATION / "generator-manifest.json")
    input_manifest = load(GENERATION / "input-manifest.json")
    export_result = load(GENERATION / "export-result.json")
    preflight = load(GENERATION / "preflight.json")
    obligation_map = GENERATED / "obligation-map.json"
    trust_inventory = GENERATION / "trust-inventory.json"

    producer_hashes = {
        "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
        "klean.py": sha256_file(PRODUCERS / "klean.py"),
    }
    all_ok &= report(
        "producer source file map versus source manifest",
        producer_hashes,
        source_manifest["files"],
    )
    all_ok &= report(
        "klean_export.py versus generator manifest",
        producer_hashes["klean_export.py"],
        generator_manifest["exporter_sha256"],
    )
    all_ok &= report(
        "klean.py versus generator manifest",
        producer_hashes["klean.py"],
        generator_manifest["klean_py_sha256"],
    )
    image_key = Path(str(resolution["generation_producer_sources"])).name
    image_from_launcher = f"sha256:{image_key}"
    image_from_generator = generator_manifest["provenance"]["generator_image_id"]
    all_ok &= report(
        "generator image: source manifest versus generator manifest",
        source_manifest["generator_image_id"],
        image_from_generator,
    )
    all_ok &= report(
        "generator image: launcher producer path versus manifest",
        image_from_launcher,
        image_from_generator,
    )

    frozen_hash = tree_checks[4][1]
    generated_hash = tree_checks[5][1]
    discovery_hash = tree_checks[6][1]
    nested_checks = [
        ("input frozen_input", input_manifest["frozen_input_sha256"], frozen_hash),
        ("input stage1_workspace", input_manifest["stage1_workspace_sha256"], frozen_hash),
        ("input discovery", input_manifest["stage3_discovery_manifest_sha256"], discovery_hash),
        ("generator generated_tree", generator_manifest["generated_tree_sha256"], generated_hash),
        ("generator provenance stage1", generator_manifest["provenance"]["stage1_workspace_sha256"], frozen_hash),
        ("generator provenance discovery", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"], discovery_hash),
        ("export frozen_input", export_result["frozen_input_sha256"], frozen_hash),
        ("export generated_tree", export_result["generated_tree_sha256"], generated_hash),
        ("export discovery", export_result["stage3_discovery_manifest_sha256"], discovery_hash),
        ("preflight frozen_input", preflight["frozen_input_sha256"], frozen_hash),
        ("preflight stage1_workspace", preflight["stage1_workspace_sha256"], frozen_hash),
        ("preflight generated_tree", preflight["generated_tree_sha256"], generated_hash),
        ("preflight discovery", preflight["stage3_discovery_manifest_sha256"], discovery_hash),
        ("generator obligation map", generator_manifest["obligation_map_sha256"], sha256_file(obligation_map)),
        ("export trust inventory", export_result["trust_inventory_sha256"], sha256_file(trust_inventory)),
    ]
    for label, observed, expected in nested_checks:
        all_ok &= report(label, observed, expected)

    print(f"OVERALL={'PASS' if all_ok else 'FAIL'}")
    if not all_ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
