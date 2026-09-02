#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, klean_audit_contract, pipeline_contract


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]

tree_cases = {
    "k_workspace_sha256": Path("/reference/k-proof"),
    "k_audit_sha256": Path("/reference/k-audit"),
    "klean_generation_sha256": Path("/reference/klean-generation"),
    "generation_producer_sources_sha256": Path("/reference/generation-tools"),
}
for field, path in tree_cases.items():
    observed = pipeline_contract.sha256_tree(path)
    print(field, "MATCH" if observed == recorded[field] else "MISMATCH")
    print("  recorded:", recorded[field])
    print("  observed:", observed)

export_cases = {
    "stage1_export_sha256": Path("/reference/k-proof"),
    "generated_tree_sha256": Path("/reference/klean-generation/generated"),
}
for field, path in export_cases.items():
    observed = klean_export.tree_digest(path)
    print(field, "MATCH" if observed == recorded[field] else "MISMATCH")
    print("  recorded:", recorded[field])
    print("  observed:", observed)

discovery = file_hash(Path("/reference/lemma-discovery.json"))
print(
    "discovery_manifest_sha256",
    "MATCH" if discovery == recorded["discovery_manifest_sha256"] else "MISMATCH",
)
print("  recorded:", recorded["discovery_manifest_sha256"])
print("  observed:", discovery)

observed_sources = klean_audit_contract._stage1_source_hashes(
    Path("/reference/k-proof")
)
recorded_sources = resolution["stage1_source_hashes"]
missing = sorted(set(recorded_sources) - set(observed_sources))
extra = sorted(set(observed_sources) - set(recorded_sources))
changed = sorted(
    name
    for name in set(recorded_sources) & set(observed_sources)
    if recorded_sources[name] != observed_sources[name]
)
print("stage1_source_hashes", "MATCH" if not (missing or extra or changed) else "MISMATCH")
print("  recorded_count:", len(recorded_sources))
print("  observed_count:", len(observed_sources))
print("  missing:", missing)
print("  extra:", extra)
print("  changed:", changed)

source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
for name, expected in source_manifest["files"].items():
    observed = file_hash(Path("/reference/generation-tools") / name)
    generator_field = (
        "exporter_sha256" if name == "klean_export.py" else "klean_py_sha256"
    )
    generator_expected = generator_manifest[generator_field]
    matched = observed == expected == generator_expected
    print("producer", name, "MATCH" if matched else "MISMATCH")
    print("  source_manifest:", expected)
    print("  generator_manifest:", generator_expected)
    print("  observed:", observed)

generator_image = generator_manifest["provenance"]["generator_image_id"]
source_image = source_manifest["generator_image_id"]
launcher_key = Path(resolution["generation_producer_sources"]).name
print(
    "generator_image_id",
    "MATCH"
    if generator_image == source_image
    and generator_image == "sha256:" + launcher_key
    else "MISMATCH",
)
print("  generator_manifest:", generator_image)
print("  source_manifest:", source_image)
print("  launcher_path_key:", launcher_key)

obligation_hash = file_hash(
    Path("/reference/klean-generation/generated/obligation-map.json")
)
print(
    "obligation_map_sha256",
    "MATCH"
    if obligation_hash == generator_manifest["obligation_map_sha256"]
    else "MISMATCH",
)
print("  recorded:", generator_manifest["obligation_map_sha256"])
print("  observed:", obligation_hash)

verification_hash = file_hash(Path("/reference/k-proof/verification.k"))
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
print(
    "verification_sha256",
    "MATCH" if verification_hash == input_manifest["verification_sha256"] else "MISMATCH",
)
print("  recorded:", input_manifest["verification_sha256"])
print("  observed:", verification_hash)

lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
print(
    "toolchain_lock",
    "MATCH" if lock == generator_manifest["toolchain"] else "MISMATCH",
)
