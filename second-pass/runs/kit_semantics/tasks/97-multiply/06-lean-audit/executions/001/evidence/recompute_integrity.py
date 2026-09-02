#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import (
    klean_export,
    pipeline_contract,
    stage6_resolution_contract,
)


AUDIT_INPUT = Path("/audit-input.json")
K_WORKSPACE = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")
TOOLCHAIN_LOCK = Path("/reference/klean-toolchain.lock.json")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def emit(label: str, observed, expected) -> bool:
    matched = observed == expected
    print(json.dumps({
        "check": label,
        "observed": observed,
        "expected": expected,
        "match": matched,
    }, sort_keys=True))
    return matched


document = json.loads(AUDIT_INPUT.read_text())
resolution, signed_digest = stage6_resolution_contract.verify_audit_input(document)
hashes = resolution["hashes"]
all_ok = True

all_ok &= emit(
    "resolved_input_sha256",
    stage6_resolution_contract.canonical_json_sha256(resolution),
    signed_digest,
)
all_ok &= emit(
    "k_workspace_sha256",
    pipeline_contract.sha256_tree(K_WORKSPACE),
    hashes["k_workspace_sha256"],
)
all_ok &= emit(
    "stage1_export_sha256",
    klean_export.tree_digest(K_WORKSPACE),
    hashes["stage1_export_sha256"],
)
all_ok &= emit(
    "k_audit_sha256",
    pipeline_contract.sha256_tree(K_AUDIT),
    hashes["k_audit_sha256"],
)
all_ok &= emit(
    "discovery_manifest_sha256",
    sha256_file(DISCOVERY),
    hashes["discovery_manifest_sha256"],
)
all_ok &= emit(
    "klean_generation_sha256",
    pipeline_contract.sha256_tree(GENERATION),
    hashes["klean_generation_sha256"],
)
all_ok &= emit(
    "generated_tree_sha256",
    klean_export.tree_digest(GENERATED),
    hashes["generated_tree_sha256"],
)
all_ok &= emit(
    "generation_producer_sources_sha256",
    pipeline_contract.sha256_tree(PRODUCERS),
    hashes["generation_producer_sources_sha256"],
)

observed_source_hashes = {
    path.relative_to(K_WORKSPACE).as_posix(): sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        K_WORKSPACE, "mounted Stage 1 workspace"
    )
}
expected_source_hashes = resolution["stage1_source_hashes"]
all_ok &= emit(
    "stage1_source_hashes_count",
    len(observed_source_hashes),
    len(expected_source_hashes),
)
all_ok &= emit(
    "stage1_source_hashes_exact_map",
    observed_source_hashes,
    expected_source_hashes,
)

generator = json.loads((GENERATION / "generator-manifest.json").read_text())
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
producer_files = sorted(
    path.relative_to(PRODUCERS).as_posix()
    for path in pipeline_contract._walk_regular_files(
        PRODUCERS, "mounted Stage 4 producer sources"
    )
)
all_ok &= emit(
    "producer_file_set",
    producer_files,
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
all_ok &= emit(
    "klean_export.py_sha256_vs_generator_manifest",
    sha256_file(PRODUCERS / "klean_export.py"),
    generator["exporter_sha256"],
)
all_ok &= emit(
    "klean.py_sha256_vs_generator_manifest",
    sha256_file(PRODUCERS / "klean.py"),
    generator["klean_py_sha256"],
)
all_ok &= emit(
    "producer_hashes_vs_source_manifest",
    {
        "klean.py": sha256_file(PRODUCERS / "klean.py"),
        "klean_export.py": sha256_file(PRODUCERS / "klean_export.py"),
    },
    source_manifest["files"],
)
generator_image_id = generator["provenance"]["generator_image_id"]
all_ok &= emit(
    "generator_image_id_vs_source_manifest",
    generator_image_id,
    source_manifest["generator_image_id"],
)
all_ok &= emit(
    "generator_image_id_vs_audit_input_bundle_path",
    generator_image_id.removeprefix("sha256:"),
    Path(resolution["generation_producer_sources"]).name,
)
all_ok &= emit(
    "generator_toolchain_vs_lock",
    generator["toolchain"],
    json.loads(TOOLCHAIN_LOCK.read_text()),
)
all_ok &= emit(
    "generator_generated_tree_sha256",
    generator["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)
all_ok &= emit(
    "generator_stage1_provenance",
    generator["provenance"]["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
all_ok &= emit(
    "generator_stage3_provenance",
    generator["provenance"]["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)

print(json.dumps({"all_checks_match": bool(all_ok)}, sort_keys=True))
raise SystemExit(0 if all_ok else 1)
