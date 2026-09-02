#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.stage6_resolution_contract import verify_audit_input


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{label}: {status}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")


document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = verify_audit_input(document)
print("audit_input_envelope: VALID")
print(f"resolved_input_sha256={resolved_digest}")

hashes = resolution["hashes"]
report(
    "lemma_discovery_file_sha256",
    file_sha(Path("/reference/lemma-discovery.json")),
    hashes["discovery_manifest_sha256"],
)
report(
    "generation_producer_sources_pipeline_tree_sha256",
    pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
    hashes["generation_producer_sources_sha256"],
)
report(
    "k_audit_pipeline_tree_sha256",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    hashes["k_audit_sha256"],
)
report(
    "klean_generation_pipeline_tree_sha256",
    pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
    hashes["klean_generation_sha256"],
)
report(
    "generated_klean_tree_sha256",
    klean_export.tree_digest(Path("/reference/klean-generation/generated")),
    hashes["generated_tree_sha256"],
)
report(
    "canonical_stage1_export_sha256",
    klean_export.tree_digest(Path("/reference/k-proof")),
    hashes["stage1_export_sha256"],
)
report(
    "selected_stage1_workspace_pipeline_tree_sha256",
    pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    hashes["k_workspace_sha256"],
)

for relative, expected in sorted(resolution["stage1_source_hashes"].items()):
    path = Path("/reference/k-proof") / relative
    observed = file_sha(path) if path.is_file() else None
    report(f"stage1_source:{relative}", observed, expected)

source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
for name, expected in sorted(source_manifest["files"].items()):
    report(
        f"producer_file:{name}",
        file_sha(Path("/reference/generation-tools") / name),
        expected,
    )
report(
    "generator_manifest:klean.py",
    file_sha(Path("/reference/generation-tools/klean.py")),
    generator_manifest["klean_py_sha256"],
)
report(
    "generator_manifest:klean_export.py",
    file_sha(Path("/reference/generation-tools/klean_export.py")),
    generator_manifest["exporter_sha256"],
)
report(
    "generator_image_id:source_vs_generation",
    source_manifest["generator_image_id"],
    generator_manifest["provenance"]["generator_image_id"],
)
launcher_source_path = Path(resolution["generation_producer_sources"])
launcher_image_id = f"sha256:{launcher_source_path.name}"
report(
    "generator_image_id:launcher_path_vs_manifest",
    launcher_image_id,
    source_manifest["generator_image_id"],
)
