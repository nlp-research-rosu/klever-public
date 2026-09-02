#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.stage6_resolution_contract import verify_audit_input


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed, expected) -> None:
    if observed != expected:
        raise AssertionError(
            f"{label}: observed {observed!r}, expected {expected!r}"
        )
    print(f"PASS {label}: {observed}")


audit = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = verify_audit_input(audit)
print(f"PASS audit-input envelope: {resolved_digest}")

hashes = resolution["hashes"]
check(
    "Stage 1 pipeline tree",
    pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    hashes["k_workspace_sha256"],
)
check(
    "Stage 1 export tree",
    klean_export.tree_digest(Path("/reference/k-proof")),
    hashes["stage1_export_sha256"],
)
check(
    "Stage 2 selected audit tree",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    hashes["k_audit_sha256"],
)
check(
    "Stage 3 manifest file",
    sha256(Path("/reference/lemma-discovery.json")),
    hashes["discovery_manifest_sha256"],
)
check(
    "Stage 4 selected generation tree",
    pipeline_contract.sha256_tree(Path("/reference/klean-generation")),
    hashes["klean_generation_sha256"],
)
check(
    "Stage 4 generated export tree",
    klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    hashes["generated_tree_sha256"],
)
check(
    "Stage 4 producer-source tree",
    pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
    hashes["generation_producer_sources_sha256"],
)
check(
    "Stage 5 workspace tree",
    pipeline_contract.sha256_tree(Path("/candidate")),
    hashes["lean_workspace_sha256"],
)

observed_sources = {
    path.relative_to("/reference/k-proof").as_posix(): sha256(path)
    for path in sorted(Path("/reference/k-proof").rglob("*"))
    if path.is_file() and not path.is_symlink()
}
check(
    "Stage 1 per-file source hashes",
    observed_sources,
    resolution["stage1_source_hashes"],
)

generation = Path("/reference/klean-generation")
generator = json.loads((generation / "generator-manifest.json").read_text())
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
expected_image = generator["provenance"]["generator_image_id"]
path_image = (
    "sha256:"
    + Path(resolution["generation_producer_sources"]).name
)
check("generator image: manifest/source manifest", source_manifest["generator_image_id"], expected_image)
check("generator image: audit-input path/manifest", path_image, expected_image)
check(
    "producer source manifest file set",
    set(source_manifest["files"]),
    {"klean_export.py", "klean.py"},
)
check(
    "producer klean_export.py",
    sha256(Path("/reference/generation-tools/klean_export.py")),
    source_manifest["files"]["klean_export.py"],
)
check(
    "producer klean.py",
    sha256(Path("/reference/generation-tools/klean.py")),
    source_manifest["files"]["klean.py"],
)
check(
    "producer klean_export.py/generator manifest",
    source_manifest["files"]["klean_export.py"],
    generator["exporter_sha256"],
)
check(
    "producer klean.py/generator manifest",
    source_manifest["files"]["klean.py"],
    generator["klean_py_sha256"],
)

lock = json.loads(Path("/reference/klean-toolchain.lock.json").read_text())
check("pinned toolchain", generator["toolchain"], lock)

input_manifest = json.loads(
    (generation / "input-manifest.json").read_text()
)
check(
    "input manifest Stage 1 export",
    input_manifest["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "input manifest frozen input",
    input_manifest["frozen_input_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "input manifest Stage 3",
    input_manifest["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)

obligation_map = generation / "generated/obligation-map.json"
check(
    "obligation-map file",
    sha256(obligation_map),
    generator["obligation_map_sha256"],
)
export_result = json.loads((generation / "export-result.json").read_text())
trust_inventory = generation / "trust-inventory.json"
check(
    "trust-inventory file",
    sha256(trust_inventory),
    export_result["trust_inventory_sha256"],
)
check(
    "export result Stage 1",
    export_result["frozen_input_sha256"],
    hashes["stage1_export_sha256"],
)
check(
    "export result Stage 3",
    export_result["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
check(
    "export result generated tree",
    export_result["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)

computed_target = klean_export.target_statement(generation / "generated")
check("computed/generator target", computed_target, generator["target"])
check("computed/audit-input target", computed_target, resolution["target"])
check(
    "recorded Stage 4 preflight",
    json.loads((generation / "preflight.json").read_text()),
    resolution["stage4_preflight"],
)

print(
    "NOTE historical Stage 5 invocation tree is not mounted; "
    "lean_invocation_sha256 cannot be re-hashed and is not used as proof evidence."
)
