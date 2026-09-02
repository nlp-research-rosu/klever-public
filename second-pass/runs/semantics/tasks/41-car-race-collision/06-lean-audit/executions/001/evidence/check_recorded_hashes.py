#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


audit = json.loads(Path("/audit-input.json").read_text())
resolution, signed_digest = stage6_resolution_contract.verify_audit_input(audit)
recorded = resolution["hashes"]


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


checks: list[tuple[str, str | None, str | None]] = []


def check(label: str, actual: str | None, expected: str | None) -> None:
    checks.append((label, actual, expected))


check("AUDIT_MODE", __import__("os").environ.get("AUDIT_MODE"), resolution["mode"])
check(
    "resolved_input_sha256",
    stage6_resolution_contract.canonical_json_sha256(resolution),
    signed_digest,
)
check(
    "k_workspace_sha256",
    pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    recorded["k_workspace_sha256"],
)
check(
    "stage1_export_sha256",
    klean_export.tree_digest(Path("/reference/k-proof")),
    recorded["stage1_export_sha256"],
)
check(
    "discovery_manifest_sha256",
    sha_file(Path("/reference/lemma-discovery.json")),
    recorded["discovery_manifest_sha256"],
)
check(
    "k_audit_sha256",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    recorded["k_audit_sha256"],
)
check(
    "klean_generation_sha256",
    pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
    recorded["klean_generation_sha256"],
)
check(
    "generated_tree_sha256",
    klean_export.tree_digest(Path("/reference/klean-generation/generated")),
    recorded["generated_tree_sha256"],
)
check(
    "generation_producer_sources_sha256",
    pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
    recorded["generation_producer_sources_sha256"],
)

producer_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
producer_files = producer_manifest["files"]
check(
    "producer klean_export.py vs source-manifest",
    sha_file(Path("/reference/generation-tools/klean_export.py")),
    producer_files["klean_export.py"],
)
check(
    "producer klean.py vs source-manifest",
    sha_file(Path("/reference/generation-tools/klean.py")),
    producer_files["klean.py"],
)
check(
    "producer klean_export.py vs generator-manifest",
    sha_file(Path("/reference/generation-tools/klean_export.py")),
    generator_manifest["exporter_sha256"],
)
check(
    "producer klean.py vs generator-manifest",
    sha_file(Path("/reference/generation-tools/klean.py")),
    generator_manifest["klean_py_sha256"],
)
image_id = generator_manifest["provenance"]["generator_image_id"]
check(
    "generator image ID source-manifest",
    producer_manifest["generator_image_id"],
    image_id,
)
check(
    "generator image ID audit-input path",
    "sha256:" + Path(resolution["generation_producer_sources"]).name,
    image_id,
)

source_root = Path("/reference/k-proof")
recorded_sources = resolution["stage1_source_hashes"]
actual_sources = {
    path.relative_to(source_root).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        source_root, "mounted Stage 1 source workspace"
    )
}
check(
    "stage1 source path set",
    json.dumps(sorted(actual_sources)),
    json.dumps(sorted(recorded_sources)),
)
for relative in sorted(set(actual_sources) | set(recorded_sources)):
    check(
        f"stage1 source {relative}",
        actual_sources.get(relative),
        recorded_sources.get(relative),
    )

for label, actual, expected in checks:
    status = "MATCH" if actual == expected else "MISMATCH"
    print(f"{status}\t{label}")
    print(f"  actual:   {actual}")
    print(f"  expected: {expected}")

mismatches = [label for label, actual, expected in checks if actual != expected]
print(f"TOTAL_CHECKS={len(checks)}")
print(f"TOTAL_MISMATCHES={len(mismatches)}")
if mismatches:
    print("MISMATCH_LABELS=" + json.dumps(mismatches))
    raise SystemExit(1)
