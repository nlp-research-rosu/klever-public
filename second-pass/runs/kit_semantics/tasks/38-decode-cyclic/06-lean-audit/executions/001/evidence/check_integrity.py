#!/usr/bin/env python3
"""Independent read-only integrity checks for mounted audit inputs."""

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "discovery_manifest_sha256": file_sha256(Path("/reference/lemma-discovery.json")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": None,
    "lean_invocation_sha256": None,
}

all_ok = True
print("RECORDED HASH COMPARISON")
for name in recorded:
    ok = observed.get(name) == recorded[name]
    all_ok &= ok
    print(f"{name}: {'MATCH' if ok else 'MISMATCH'}")
    print(f"  recorded={recorded[name]}")
    print(f"  observed={observed.get(name)}")

workspace = Path("/reference/k-proof")
observed_sources = {
    path.relative_to(workspace).as_posix(): file_sha256(path)
    for path in pipeline_contract._walk_regular_files(
        workspace, "mounted Stage 1 workspace"
    )
}
recorded_sources = resolution["stage1_source_hashes"]
missing = sorted(set(recorded_sources) - set(observed_sources))
extra = sorted(set(observed_sources) - set(recorded_sources))
changed = sorted(
    name
    for name in set(recorded_sources) & set(observed_sources)
    if recorded_sources[name] != observed_sources[name]
)
source_ok = not (missing or extra or changed)
all_ok &= source_ok
print("STAGE1 SOURCE MANIFEST")
print(f"  recorded_count={len(recorded_sources)}")
print(f"  observed_count={len(observed_sources)}")
print(f"  missing={missing}")
print(f"  extra={extra}")
print(f"  changed={changed}")
print(f"  status={'MATCH' if source_ok else 'MISMATCH'}")

producer = Path("/reference/generation-tools")
source_manifest = json.loads((producer / "source-manifest.json").read_text())
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
expected_file_hashes = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
actual_names = sorted(path.name for path in producer.iterdir())
expected_names = ["klean.py", "klean_export.py", "source-manifest.json"]
name_ok = actual_names == expected_names
manifest_files_ok = source_manifest.get("files") == expected_file_hashes
file_hashes_ok = all(
    file_sha256(producer / name) == digest
    for name, digest in expected_file_hashes.items()
)
generator_image = generator_manifest["provenance"]["generator_image_id"]
source_image = source_manifest.get("generator_image_id")
path_image = "sha256:" + Path(resolution["generation_producer_sources"]).name
image_ok = generator_image == source_image == path_image
producer_ok = name_ok and manifest_files_ok and file_hashes_ok and image_ok
all_ok &= producer_ok
print("PRODUCER PROVENANCE")
print(f"  actual_names={actual_names}")
print(f"  expected_names={expected_names}")
for name, expected in expected_file_hashes.items():
    actual = file_sha256(producer / name)
    print(f"  {name}: recorded={expected} observed={actual}")
print(f"  generator_manifest_image={generator_image}")
print(f"  source_manifest_image={source_image}")
print(f"  audit_input_path_image={path_image}")
print(f"  status={'MATCH' if producer_ok else 'MISMATCH'}")

print(f"OVERALL={'PASS' if all_ok else 'FAIL'}")
raise SystemExit(0 if all_ok else 1)
