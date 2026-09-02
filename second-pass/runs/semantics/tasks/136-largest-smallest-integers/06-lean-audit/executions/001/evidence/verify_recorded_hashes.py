#!/usr/bin/env python3
"""Independently recompute the audit's recorded file and tree hashes."""

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
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    audit = json.loads(AUDIT_INPUT.read_text())
    resolution = audit["resolution"]
    launcher_hashes = resolution["hashes"]
    source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
    input_manifest = json.loads((GENERATION / "input-manifest.json").read_text())
    generator_manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    export_result = json.loads((GENERATION / "export-result.json").read_text())
    preflight = json.loads((GENERATION / "preflight.json").read_text())
    trust_inventory = GENERATION / "trust-inventory.json"
    obligation_map = GENERATED / "obligation-map.json"

    checks: list[dict[str, object]] = []

    def check(label: str, actual: object, expected: object) -> None:
        checks.append(
            {
                "label": label,
                "actual": actual,
                "expected": expected,
                "match": actual == expected,
            }
        )

    producer_exporter = file_sha256(PRODUCERS / "klean_export.py")
    producer_klean = file_sha256(PRODUCERS / "klean.py")
    producer_tree = pipeline_contract.sha256_tree(PRODUCERS)
    generated_tree = klean_export.tree_digest(GENERATED)
    stage1_export_tree = klean_export.tree_digest(K_PROOF)
    discovery_hash = file_sha256(DISCOVERY)

    check(
        "producer klean_export.py vs source manifest",
        producer_exporter,
        source_manifest["files"]["klean_export.py"],
    )
    check(
        "producer klean_export.py vs generator manifest",
        producer_exporter,
        generator_manifest["exporter_sha256"],
    )
    check(
        "producer klean.py vs source manifest",
        producer_klean,
        source_manifest["files"]["klean.py"],
    )
    check(
        "producer klean.py vs generator manifest",
        producer_klean,
        generator_manifest["klean_py_sha256"],
    )
    check(
        "producer source tree vs audit input",
        producer_tree,
        launcher_hashes["generation_producer_sources_sha256"],
    )

    source_image = source_manifest["generator_image_id"]
    generator_image = generator_manifest["provenance"]["generator_image_id"]
    launcher_source_dir = Path(resolution["generation_producer_sources"]).name
    check("generator image: source vs generator manifest", source_image, generator_image)
    check(
        "generator image: audit-input producer path vs source manifest",
        f"sha256:{launcher_source_dir}",
        source_image,
    )

    check(
        "Stage 1 pipeline tree vs audit input",
        pipeline_contract.sha256_tree(K_PROOF),
        launcher_hashes["k_workspace_sha256"],
    )
    check(
        "Stage 1 export tree vs audit input",
        stage1_export_tree,
        launcher_hashes["stage1_export_sha256"],
    )
    check(
        "Stage 1 export tree vs input manifest frozen_input",
        stage1_export_tree,
        input_manifest["frozen_input_sha256"],
    )
    check(
        "Stage 1 export tree vs input manifest stage1_workspace",
        stage1_export_tree,
        input_manifest["stage1_workspace_sha256"],
    )
    check(
        "Stage 1 export tree vs generator provenance",
        stage1_export_tree,
        generator_manifest["provenance"]["stage1_workspace_sha256"],
    )
    check(
        "Stage 1 export tree vs export result",
        stage1_export_tree,
        export_result["frozen_input_sha256"],
    )
    check(
        "Stage 1 export tree vs recorded preflight",
        stage1_export_tree,
        preflight["frozen_input_sha256"],
    )
    check(
        "Stage 1 export tree vs launcher preflight",
        stage1_export_tree,
        resolution["stage4_preflight"]["frozen_input_sha256"],
    )

    check(
        "selected Stage 2 K audit tree vs audit input",
        pipeline_contract.sha256_tree(K_AUDIT),
        launcher_hashes["k_audit_sha256"],
    )
    check(
        "selected Stage 4 tree vs audit input",
        pipeline_contract.sha256_tree(GENERATION),
        launcher_hashes["klean_generation_sha256"],
    )
    check(
        "generated project tree vs audit input",
        generated_tree,
        launcher_hashes["generated_tree_sha256"],
    )
    check(
        "generated project tree vs generator manifest",
        generated_tree,
        generator_manifest["generated_tree_sha256"],
    )
    check(
        "generated project tree vs export result",
        generated_tree,
        export_result["generated_tree_sha256"],
    )
    check(
        "generated project tree vs recorded preflight",
        generated_tree,
        preflight["generated_tree_sha256"],
    )
    check(
        "generated project tree vs launcher preflight",
        generated_tree,
        resolution["stage4_preflight"]["generated_tree_sha256"],
    )

    check(
        "Stage 3 manifest vs audit input",
        discovery_hash,
        launcher_hashes["discovery_manifest_sha256"],
    )
    check(
        "Stage 3 manifest vs input manifest",
        discovery_hash,
        input_manifest["stage3_discovery_manifest_sha256"],
    )
    check(
        "Stage 3 manifest vs generator provenance",
        discovery_hash,
        generator_manifest["provenance"]["stage3_discovery_manifest_sha256"],
    )
    check(
        "Stage 3 manifest vs export result",
        discovery_hash,
        export_result["stage3_discovery_manifest_sha256"],
    )
    check(
        "Stage 3 manifest vs recorded preflight",
        discovery_hash,
        preflight["stage3_discovery_manifest_sha256"],
    )
    check(
        "Stage 3 manifest vs launcher preflight",
        discovery_hash,
        resolution["stage4_preflight"]["stage3_discovery_manifest_sha256"],
    )

    verification_hash = file_sha256(K_PROOF / "verification.k")
    check(
        "verification.k vs input manifest",
        verification_hash,
        input_manifest["verification_sha256"],
    )
    check(
        "obligation map vs generator manifest",
        file_sha256(obligation_map),
        generator_manifest["obligation_map_sha256"],
    )
    check(
        "trust inventory vs export result",
        file_sha256(trust_inventory),
        export_result["trust_inventory_sha256"],
    )
    check(
        "toolchain lock vs generator manifest",
        json.loads(TOOLCHAIN_LOCK.read_text()),
        generator_manifest["toolchain"],
    )
    check(
        "launcher Stage 4 preflight vs mounted preflight",
        resolution["stage4_preflight"],
        preflight,
    )

    source_hash_mismatches: list[dict[str, object]] = []
    source_hashes = resolution["stage1_source_hashes"]
    for relative, expected in source_hashes.items():
        path = K_PROOF / relative
        if not path.is_file() or path.is_symlink():
            source_hash_mismatches.append(
                {"path": relative, "error": "missing, non-regular, or symlink"}
            )
            continue
        actual = file_sha256(path)
        if actual != expected:
            source_hash_mismatches.append(
                {"path": relative, "actual": actual, "expected": expected}
            )
    checks.append(
        {
            "label": "all audit-input Stage 1 per-file source hashes",
            "actual": {
                "checked": len(source_hashes),
                "mismatches": source_hash_mismatches,
            },
            "expected": {"checked": len(source_hashes), "mismatches": []},
            "match": not source_hash_mismatches,
        }
    )

    candidate = Path("/candidate")
    check(
        "classification-only launcher has no Stage 5 candidate directory",
        candidate.exists() or candidate.is_symlink(),
        False,
    )
    check("classification-only target in audit input", resolution["target"], None)
    check("classification-only Stage 5 result", resolution["stage5_result"], None)
    check(
        "classification-only Lean workspace hash",
        launcher_hashes["lean_workspace_sha256"],
        None,
    )
    check(
        "classification-only Lean invocation hash",
        launcher_hashes["lean_invocation_sha256"],
        None,
    )

    mismatches = [entry for entry in checks if not entry["match"]]
    report = {
        "check_count": len(checks),
        "mismatch_count": len(mismatches),
        "checks": checks,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
