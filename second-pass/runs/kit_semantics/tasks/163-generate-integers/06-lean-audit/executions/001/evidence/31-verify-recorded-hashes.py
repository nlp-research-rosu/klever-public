#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.stage6_resolution_contract import canonical_json_sha256


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")
manifest = json.loads((generation / "generator-manifest.json").read_text())
source_manifest = json.loads((producer / "source-manifest.json").read_text())

checks: list[tuple[str, object, object]] = []


def check(label: str, actual: object, expected: object) -> None:
    checks.append((label, actual, expected))


check("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
check(
    "signed resolution envelope hash",
    canonical_json_sha256(resolution),
    audit["resolved_input_sha256"],
)
check("problem_id", resolution["problem_id"], "163-generate-integers")
check("condition", resolution["condition"], "kit-semantics")
check("semantics_mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")

exporter = file_sha(producer / "klean_export.py")
klean_py = file_sha(producer / "klean.py")
check("producer.klean_export vs generator manifest", exporter, manifest["exporter_sha256"])
check("producer.klean.py vs generator manifest", klean_py, manifest["klean_py_sha256"])
check("producer.klean_export vs source manifest", exporter, source_manifest["files"]["klean_export.py"])
check("producer.klean.py vs source manifest", klean_py, source_manifest["files"]["klean.py"])
check("source manifest exact file set", sorted(source_manifest["files"]), ["klean.py", "klean_export.py"])

image_id = manifest["provenance"]["generator_image_id"]
check("generator image vs source manifest", image_id, source_manifest["generator_image_id"])
audit_bundle_component = Path(resolution["generation_producer_sources"]).name
check("generator image vs audit input producer path", image_id, "sha256:" + audit_bundle_component)

check(
    "generation producer tree hash",
    pipeline_contract.sha256_tree(producer),
    recorded["generation_producer_sources_sha256"],
)
check(
    "Stage 1 pipeline tree hash",
    pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    recorded["k_workspace_sha256"],
)
check(
    "Stage 1 deterministic export tree hash",
    klean_export.tree_digest(Path("/reference/k-proof")),
    recorded["stage1_export_sha256"],
)
check(
    "Stage 2 selected audit tree hash",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    recorded["k_audit_sha256"],
)
check(
    "Stage 2 selection artifact hash",
    pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
check(
    "Stage 3 discovery file hash",
    file_sha(Path("/reference/lemma-discovery.json")),
    recorded["discovery_manifest_sha256"],
)
check(
    "Stage 4 selected generation tree hash",
    pipeline_contract.sha256_tree(generation),
    recorded["klean_generation_sha256"],
)
check(
    "Stage 4 selection artifact hash",
    pipeline_contract.sha256_tree(generation),
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)
check(
    "generated project deterministic tree hash",
    klean_export.tree_digest(generated),
    recorded["generated_tree_sha256"],
)
check(
    "generated tree vs generator manifest",
    klean_export.tree_digest(generated),
    manifest["generated_tree_sha256"],
)

actual_stage1_files = {
    path.relative_to("/reference/k-proof").as_posix(): file_sha(path)
    for path in Path("/reference/k-proof").rglob("*")
    if path.is_file() and not path.is_symlink()
}
recorded_stage1_files = resolution["stage1_source_hashes"]
check("Stage 1 source file name set", sorted(actual_stage1_files), sorted(recorded_stage1_files))
bad_stage1 = [
    name
    for name in sorted(actual_stage1_files)
    if actual_stage1_files[name] != recorded_stage1_files.get(name)
]
check("Stage 1 per-file hashes", bad_stage1, [])

check("proof candidate absent", Path("/candidate").exists(), False)
check("audit Lean workspace absent", resolution["lean_workspace"], None)
check("audit Lean invocation absent", resolution["lean_invocation"], None)
check("audit target absent", resolution["target"], None)
check("generator target absent", manifest["target"], None)
check("Stage 5 result absent", resolution["stage5_result"], None)

for label, actual, expected in checks:
    status = "PASS" if actual == expected else "FAIL"
    print(f"{status}: {label}")
    if status == "FAIL" or label in {
        "generator image vs source manifest",
        "generation producer tree hash",
        "Stage 1 pipeline tree hash",
        "Stage 1 deterministic export tree hash",
        "Stage 2 selected audit tree hash",
        "Stage 3 discovery file hash",
        "Stage 4 selected generation tree hash",
        "generated project deterministic tree hash",
    }:
        print(f"  actual={actual!r}")
        print(f"  expected={expected!r}")

failed = [label for label, actual, expected in checks if actual != expected]
print(f"checks={len(checks)}")
print(f"failures={len(failed)}")
if failed:
    print("failed_labels=" + ", ".join(failed))
    raise SystemExit(1)
