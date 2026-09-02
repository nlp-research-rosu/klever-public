#!/usr/bin/env python3
"""Verify mounted Stage 4 producer sources against all recorded provenance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


BUNDLE = Path("/reference/generation-tools")
GENERATOR = Path("/reference/klean-generation/generator-manifest.json")
AUDIT_INPUT = Path("/audit-input.json")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source_manifest = json.loads((BUNDLE / "source-manifest.json").read_text())
    generator = json.loads(GENERATOR.read_text())
    audit_input = json.loads(AUDIT_INPUT.read_text())["resolution"]
    provenance = generator["provenance"]
    export_hash = file_sha256(BUNDLE / "klean_export.py")
    klean_hash = file_sha256(BUNDLE / "klean.py")
    tree_hash = sha256_tree(BUNDLE)
    image_id = provenance["generator_image_id"]
    image_key = image_id.removeprefix("sha256:")

    checks = {
        "bundle_exact_regular_files": sorted(
            path.relative_to(BUNDLE).as_posix()
            for path in BUNDLE.iterdir()
            if path.is_file() and not path.is_symlink()
        )
        == ["klean.py", "klean_export.py", "source-manifest.json"],
        "klean_export_hash_manifest": export_hash == generator["exporter_sha256"],
        "klean_export_hash_source_manifest": export_hash
        == source_manifest["files"]["klean_export.py"],
        "klean_hash_manifest": klean_hash == generator["klean_py_sha256"],
        "klean_hash_source_manifest": klean_hash
        == source_manifest["files"]["klean.py"],
        "image_id_source_manifest": image_id
        == source_manifest["generator_image_id"],
        "image_id_audit_input_path": Path(
            audit_input["generation_producer_sources"]
        ).name
        == image_key,
        "bundle_tree_hash_audit_input": tree_hash
        == audit_input["hashes"]["generation_producer_sources_sha256"],
    }
    result = {
        "klean_export.py_sha256": export_hash,
        "klean.py_sha256": klean_hash,
        "generator_image_id": image_id,
        "source_bundle_sha256": tree_hash,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
