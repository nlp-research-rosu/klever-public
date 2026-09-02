#!/usr/bin/env python3
"""Recompute launcher, producer, Stage 1, and Stage 4 recorded hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
    hashes = audit["hashes"]
    generation = Path("/reference/klean-generation")
    producers = Path("/reference/generation-tools")
    generator = json.loads((generation / "generator-manifest.json").read_text())
    source_manifest = json.loads((producers / "source-manifest.json").read_text())

    observed = {
        "k_workspace_sha256": pipeline_contract.sha256_tree(
            Path("/reference/k-proof")
        ),
        "stage1_export_sha256": klean_export.tree_digest(
            Path("/reference/k-proof")
        ),
        "discovery_manifest_sha256": file_sha256(
            Path("/reference/lemma-discovery.json")
        ),
        "k_audit_sha256": pipeline_contract.sha256_tree(
            Path("/reference/k-audit")
        ),
        "klean_generation_sha256": pipeline_contract.sha256_tree(generation),
        "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
            producers
        ),
        "generated_tree_sha256": klean_export.tree_digest(
            generation / "generated"
        ),
        "lean_workspace_sha256": None,
        "lean_invocation_sha256": None,
    }
    launcher_hash_checks = {
        key: {
            "expected": hashes[key],
            "observed": value,
            "match": hashes[key] == value,
        }
        for key, value in observed.items()
    }

    stage1_recorded = audit["stage1_source_hashes"]
    stage1_observed = {
        path.relative_to("/reference/k-proof").as_posix(): file_sha256(path)
        for path in sorted(Path("/reference/k-proof").rglob("*"))
        if path.is_file() and not path.is_symlink()
    }
    stage1_keys_match = set(stage1_recorded) == set(stage1_observed)
    stage1_mismatches = {
        key: {"expected": stage1_recorded.get(key), "observed": stage1_observed.get(key)}
        for key in sorted(set(stage1_recorded) | set(stage1_observed))
        if stage1_recorded.get(key) != stage1_observed.get(key)
    }

    producer_files = {
        "klean_export.py": file_sha256(producers / "klean_export.py"),
        "klean.py": file_sha256(producers / "klean.py"),
    }
    generator_image = generator["provenance"]["generator_image_id"]
    source_image = source_manifest["generator_image_id"]
    audit_image = "sha256:" + Path(audit["generation_producer_sources"]).name
    producer_gate = {
        "file_set_exact": {
            p.relative_to(producers).as_posix()
            for p in producers.rglob("*")
            if p.is_file() and not p.is_symlink()
        }
        == {"source-manifest.json", "klean_export.py", "klean.py"},
        "observed_file_hashes": producer_files,
        "source_manifest_file_hashes": source_manifest["files"],
        "generator_manifest_file_hashes": {
            "klean_export.py": generator["exporter_sha256"],
            "klean.py": generator["klean_py_sha256"],
        },
        "all_file_hashes_match": producer_files
        == source_manifest["files"]
        == {
            "klean_export.py": generator["exporter_sha256"],
            "klean.py": generator["klean_py_sha256"],
        },
        "generator_image_id": generator_image,
        "source_manifest_image_id": source_image,
        "audit_input_image_id_from_producer_path": audit_image,
        "all_image_ids_match": generator_image == source_image == audit_image,
    }

    result = {
        "launcher_hash_checks": launcher_hash_checks,
        "all_launcher_hashes_match": all(
            item["match"] for item in launcher_hash_checks.values()
        ),
        "stage1_source_hashes": {
            "recorded_count": len(stage1_recorded),
            "observed_count": len(stage1_observed),
            "keys_match": stage1_keys_match,
            "mismatches": stage1_mismatches,
            "all_match": stage1_keys_match and not stage1_mismatches,
        },
        "producer_gate": producer_gate,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
