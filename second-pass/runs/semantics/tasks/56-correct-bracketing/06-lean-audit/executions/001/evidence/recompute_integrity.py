#!/usr/bin/env python3
"""Independent recomputation of all audit-input and Stage 4 provenance hashes."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract


AUDIT_INPUT = Path("/audit-input.json")
STAGE1 = Path("/reference/k-proof")
STAGE2 = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def load(path: Path) -> dict:
    return json.loads(path.read_bytes())


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def regular_file_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISLNK(mode):
            raise RuntimeError(f"unexpected symlink: {root}/{relative}")
        if stat.S_ISREG(mode):
            result[relative] = file_sha(path)
        elif not stat.S_ISDIR(mode):
            raise RuntimeError(f"unexpected non-file tree entry: {root}/{relative}")
    return result


def check(label: str, actual: object, expected: object) -> dict:
    return {
        "label": label,
        "actual": actual,
        "expected": expected,
        "match": actual == expected,
    }


def main() -> None:
    audit = load(AUDIT_INPUT)
    resolution = audit["resolution"]
    hashes = resolution["hashes"]
    generator = load(GENERATION / "generator-manifest.json")
    input_manifest = load(GENERATION / "input-manifest.json")
    export_result = load(GENERATION / "export-result.json")
    source_manifest = load(PRODUCERS / "source-manifest.json")
    obligation_map_path = GENERATED / "obligation-map.json"
    generator_image_id = generator["provenance"]["generator_image_id"]
    audit_producer_path = Path(resolution["generation_producer_sources"])
    inferred_audit_image_id = f"sha256:{audit_producer_path.name}"

    actual_stage1_files = regular_file_hashes(STAGE1)
    expected_stage1_files = resolution["stage1_source_hashes"]

    checks = [
        check("AUDIT_MODE env vs launcher JSON", os.environ.get("AUDIT_MODE"), resolution["mode"]),
        check("problem id", resolution["problem_id"], "56-correct-bracketing"),
        check("condition", resolution["condition"], "semantics"),
        check("semantics mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS"),
        check(
            "klean_export.py producer hash vs generator manifest",
            file_sha(PRODUCERS / "klean_export.py"),
            generator["exporter_sha256"],
        ),
        check(
            "klean.py producer hash vs generator manifest",
            file_sha(PRODUCERS / "klean.py"),
            generator["klean_py_sha256"],
        ),
        check(
            "klean_export.py producer hash vs source manifest",
            file_sha(PRODUCERS / "klean_export.py"),
            source_manifest["files"]["klean_export.py"],
        ),
        check(
            "klean.py producer hash vs source manifest",
            file_sha(PRODUCERS / "klean.py"),
            source_manifest["files"]["klean.py"],
        ),
        check(
            "generator image: generator vs source manifest",
            generator_image_id,
            source_manifest["generator_image_id"],
        ),
        check(
            "generator image: generator vs audit-input producer path",
            generator_image_id,
            inferred_audit_image_id,
        ),
        check(
            "producer bundle tree vs audit input",
            pipeline_contract.sha256_tree(PRODUCERS),
            hashes["generation_producer_sources_sha256"],
        ),
        check(
            "Stage 1 canonical audit tree vs audit input",
            pipeline_contract.sha256_tree(STAGE1),
            hashes["k_workspace_sha256"],
        ),
        check(
            "Stage 1 exporter tree vs audit input",
            klean_export.tree_digest(STAGE1),
            hashes["stage1_export_sha256"],
        ),
        check(
            "Stage 1 exporter tree vs input manifest",
            klean_export.tree_digest(STAGE1),
            input_manifest["stage1_workspace_sha256"],
        ),
        check(
            "Stage 1 exporter tree vs generator provenance",
            klean_export.tree_digest(STAGE1),
            generator["provenance"]["stage1_workspace_sha256"],
        ),
        check(
            "Stage 2 audit tree vs audit input",
            pipeline_contract.sha256_tree(STAGE2),
            hashes["k_audit_sha256"],
        ),
        check(
            "Stage 3 discovery file vs audit input",
            file_sha(DISCOVERY),
            hashes["discovery_manifest_sha256"],
        ),
        check(
            "Stage 3 discovery file vs input manifest",
            file_sha(DISCOVERY),
            input_manifest["stage3_discovery_manifest_sha256"],
        ),
        check(
            "Stage 3 discovery file vs generator provenance",
            file_sha(DISCOVERY),
            generator["provenance"]["stage3_discovery_manifest_sha256"],
        ),
        check(
            "Stage 4 whole generation tree vs audit input",
            pipeline_contract.sha256_tree(GENERATION),
            hashes["klean_generation_sha256"],
        ),
        check(
            "generated project exporter tree vs audit input",
            klean_export.tree_digest(GENERATED),
            hashes["generated_tree_sha256"],
        ),
        check(
            "generated project exporter tree vs generator manifest",
            klean_export.tree_digest(GENERATED),
            generator["generated_tree_sha256"],
        ),
        check(
            "generated project exporter tree vs export result",
            klean_export.tree_digest(GENERATED),
            export_result["generated_tree_sha256"],
        ),
        check(
            "obligation map bytes vs generator manifest",
            file_sha(obligation_map_path),
            generator["obligation_map_sha256"],
        ),
        check(
            "trust inventory bytes vs export result",
            file_sha(GENERATION / "trust-inventory.json"),
            export_result["trust_inventory_sha256"],
        ),
        check(
            "Stage 1 exact regular-file path set",
            sorted(actual_stage1_files),
            sorted(expected_stage1_files),
        ),
        check(
            "Stage 1 exact regular-file hashes",
            actual_stage1_files,
            expected_stage1_files,
        ),
    ]

    producer_names = sorted(
        path.relative_to(PRODUCERS).as_posix()
        for path in PRODUCERS.rglob("*")
        if path.is_file()
    )
    checks.append(
        check(
            "producer bundle exact file set",
            producer_names,
            ["klean.py", "klean_export.py", "source-manifest.json"],
        )
    )

    output = {
        "checks": checks,
        "all_match": all(item["match"] for item in checks),
        "stage1_file_count": len(actual_stage1_files),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
