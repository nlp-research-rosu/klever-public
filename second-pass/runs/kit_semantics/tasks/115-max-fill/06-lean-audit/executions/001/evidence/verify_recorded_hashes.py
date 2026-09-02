#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]

tree_cases = [
    ("k_workspace_sha256", Path("/reference/k-proof")),
    ("k_audit_sha256", Path("/reference/k-audit")),
    ("klean_generation_sha256", Path("/reference/klean-generation")),
    ("generation_producer_sources_sha256", Path("/reference/generation-tools")),
    ("lean_workspace_sha256", Path("/candidate")),
]
print("PIPELINE TREE HASHES")
all_ok = True
for key, path in tree_cases:
    actual = pipeline_contract.sha256_tree(path)
    expected = recorded[key]
    ok = actual == expected
    all_ok &= ok
    print(f"{key}: expected={expected} actual={actual} match={ok}")

export_cases = [
    ("stage1_export_sha256", Path("/reference/k-proof")),
    ("generated_tree_sha256", Path("/reference/klean-generation/generated")),
]
print("\nEXPORT TREE HASHES")
for key, path in export_cases:
    actual = klean_export.tree_digest(path)
    expected = recorded[key]
    ok = actual == expected
    all_ok &= ok
    print(f"{key}: expected={expected} actual={actual} match={ok}")

file_cases = [
    ("discovery_manifest_sha256", Path("/reference/lemma-discovery.json")),
]
print("\nFILE HASHES")
for key, path in file_cases:
    actual = file_sha256(path)
    expected = recorded[key]
    ok = actual == expected
    all_ok &= ok
    print(f"{key}: expected={expected} actual={actual} match={ok}")

print("\nSTAGE 1 PER-FILE HASH MANIFEST")
expected_sources = resolution["stage1_source_hashes"]
actual_sources = {
    path.relative_to("/reference/k-proof").as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "Stage 1 source workspace"
    )
}
missing = sorted(set(expected_sources) - set(actual_sources))
extra = sorted(set(actual_sources) - set(expected_sources))
mismatched = sorted(
    key
    for key in set(expected_sources) & set(actual_sources)
    if expected_sources[key] != actual_sources[key]
)
source_ok = not missing and not extra and not mismatched
all_ok &= source_ok
print(f"expected_count={len(expected_sources)} actual_count={len(actual_sources)}")
print(f"missing={missing}")
print(f"extra={extra}")
print(f"mismatched={mismatched}")
print(f"exact_match={source_ok}")

source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
print("\nPRODUCER SOURCE AUTHENTICATION")
for name in ("klean_export.py", "klean.py"):
    actual = file_sha256(Path("/reference/generation-tools") / name)
    source_expected = source_manifest["files"][name]
    generator_key = "exporter_sha256" if name == "klean_export.py" else "klean_py_sha256"
    generator_expected = generator_manifest[generator_key]
    ok = actual == source_expected == generator_expected
    all_ok &= ok
    print(
        f"{name}: source_manifest={source_expected} "
        f"generator_manifest={generator_expected} actual={actual} match={ok}"
    )
source_image = source_manifest["generator_image_id"]
generator_image = generator_manifest["provenance"]["generator_image_id"]
audit_image = "sha256:" + Path(resolution["generation_producer_sources"]).name
image_ok = source_image == generator_image == audit_image
all_ok &= image_ok
print(
    f"image_id: source_manifest={source_image} "
    f"generator_manifest={generator_image} audit_input_path={audit_image} "
    f"match={image_ok}"
)

generated_target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
target_ok = (
    generated_target == generator_manifest["target"] == resolution["target"]
)
all_ok &= target_ok
print("\nTARGET RECORD")
print(json.dumps(generated_target, indent=2, sort_keys=True))
print(f"matches_generator_and_audit_input={target_ok}")

print(f"\nALL_AVAILABLE_RECORDED_HASHES_MATCH={all_ok}")
