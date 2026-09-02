#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_sha(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}

comparisons = {
    name: {
        "expected": hashes[name],
        "observed": digest,
        "match": hashes[name] == digest,
    }
    for name, digest in observed.items()
}

stage1_observed = {
    path.relative_to("/reference/k-proof").as_posix(): file_sha(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
stage1_expected = resolution["stage1_source_hashes"]

producer_files = {
    path.relative_to("/reference/generation-tools").as_posix(): file_sha(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/generation-tools"),
        "mounted Stage 4 producer sources",
    )
}

image_id = generator["provenance"]["generator_image_id"]
producer_path_image = Path(
    resolution["generation_producer_sources"]
).name

result = {
    "available_launcher_hashes": comparisons,
    "all_available_launcher_hashes_match": all(
        item["match"] for item in comparisons.values()
    ),
    "stage1_source_hashes": {
        "expected_count": len(stage1_expected),
        "observed_count": len(stage1_observed),
        "same_paths": set(stage1_expected) == set(stage1_observed),
        "all_match": stage1_expected == stage1_observed,
    },
    "producer_source_authentication": {
        "observed_files": producer_files,
        "source_manifest_files": source_manifest["files"],
        "generator_exporter_sha256": generator["exporter_sha256"],
        "generator_klean_py_sha256": generator["klean_py_sha256"],
        "generator_image_id": image_id,
        "source_manifest_image_id": source_manifest["generator_image_id"],
        "audit_input_path_image_id": f"sha256:{producer_path_image}",
        "exact_file_set": set(producer_files)
        == {"source-manifest.json", "klean_export.py", "klean.py"},
        "producer_hashes_match": {
            name: producer_files[name] == digest
            for name, digest in source_manifest["files"].items()
        },
        "image_ids_match": image_id
        == source_manifest["generator_image_id"]
        == f"sha256:{producer_path_image}",
    },
    "target_identity": {
        "generator_equals_audit_input": generator["target"]
        == resolution["target"],
        "reparsed_generated_target_equals_generator": (
            klean_export.target_statement(
                Path("/reference/klean-generation/generated")
            )
            == generator["target"]
        ),
    },
    "unmounted_launcher_hashes": {
        "lean_invocation_sha256": hashes["lean_invocation_sha256"],
        "reason": (
            "The launcher records a Stage 5 invocation tree, but only its "
            "successful workspace is mounted at /candidate."
        ),
    },
    "stage5_result": resolution.get("stage5_result"),
}

print(json.dumps(result, indent=2, sort_keys=True))
