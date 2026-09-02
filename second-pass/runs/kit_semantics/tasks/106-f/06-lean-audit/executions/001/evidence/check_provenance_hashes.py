#!/usr/bin/env python3
"""Check immutable Stage 4 producer and mounted-input provenance."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)

producer_dir = Path("/reference/generation-tools")
exporter = producer_dir / "klean_export.py"
klean = producer_dir / "klean.py"
actual_exporter = file_sha256(exporter)
actual_klean = file_sha256(klean)
source_exporter = source_manifest["files"]["klean_export.py"]
source_klean = source_manifest["files"]["klean.py"]
generator_exporter = generator_manifest["exporter_sha256"]
generator_klean = generator_manifest["klean_py_sha256"]

source_image = source_manifest["generator_image_id"]
generator_image = generator_manifest["provenance"]["generator_image_id"]
audit_sources = Path(audit["generation_producer_sources"])
audit_image = f"sha256:{audit_sources.name}"

digests = {
    "generation_tools_tree": sha256_tree(producer_dir),
    "k_proof_tree": tree_digest(Path("/reference/k-proof")),
    "generated_tree": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generation_tree": sha256_tree(Path("/reference/klean-generation")),
}

checks = {
    "exporter_hash_all_equal": actual_exporter
    == source_exporter
    == generator_exporter,
    "klean_hash_all_equal": actual_klean == source_klean == generator_klean,
    "generator_image_all_equal": source_image
    == generator_image
    == audit_image,
    "producer_tree_matches_audit": digests["generation_tools_tree"]
    == audit["hashes"]["generation_producer_sources_sha256"],
    "stage1_tree_matches_stage1_export": digests["k_proof_tree"]
    == audit["hashes"]["stage1_export_sha256"],
    "stage1_tree_matches_generator": digests["k_proof_tree"]
    == generator_manifest["provenance"]["stage1_workspace_sha256"],
    "generated_tree_matches_audit": digests["generated_tree"]
    == audit["hashes"]["generated_tree_sha256"],
    "generated_tree_matches_generator": digests["generated_tree"]
    == generator_manifest["generated_tree_sha256"],
    "generation_tree_matches_audit": digests["generation_tree"]
    == audit["hashes"]["klean_generation_sha256"],
    "discovery_file_matches_audit": file_sha256(
        Path("/reference/lemma-discovery.json")
    )
    == audit["hashes"]["discovery_manifest_sha256"],
    "verification_file_matches_audit": file_sha256(
        Path("/reference/k-proof/verification.k")
    )
    == audit["stage1_source_hashes"]["verification.k"],
}

print(
    json.dumps(
        {
            "actual": {
                "klean_export.py": actual_exporter,
                "klean.py": actual_klean,
                "source_manifest_generator_image_id": source_image,
                "generator_manifest_generator_image_id": generator_image,
                "audit_input_generator_image_id_from_producer_path": audit_image,
                **digests,
            },
            "recorded": {
                "source_manifest_files": source_manifest["files"],
                "generator_manifest_exporter_sha256": generator_exporter,
                "generator_manifest_klean_py_sha256": generator_klean,
                "audit_input_hashes": audit["hashes"],
            },
            "checks": checks,
            "result": "PASS" if all(checks.values()) else "AUDIT_ERROR",
        },
        indent=2,
        sort_keys=True,
    )
)
raise SystemExit(0 if all(checks.values()) else 1)
