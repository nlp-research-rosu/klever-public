#!/usr/bin/env python3
"""Independent hash and immutable-producer authentication for this audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


AUDIT_INPUT = Path("/audit-input.json")
K_PROOF = Path("/reference/k-proof")
K_AUDIT = Path("/reference/k-audit")
DISCOVERY = Path("/reference/lemma-discovery.json")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
PRODUCERS = Path("/reference/generation-tools")


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report(label: str, observed: object, expected: object) -> bool:
    ok = observed == expected
    print(f"{label}: {'MATCH' if ok else 'MISMATCH'}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")
    return ok


document = json.loads(AUDIT_INPUT.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(document)
print("audit envelope: VALID")
print(f"resolved_input_sha256={resolved_digest}")
print(f"mode={resolution['mode']}")
print(f"semantics_mode={resolution['semantics_mode']}")

checks: list[bool] = []
hashes = resolution["hashes"]

# Re-hash the complete frozen Stage 1 file set, not merely selected sources.
observed_stage1_files = {
    path.relative_to(K_PROOF).as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(K_PROOF, "Stage 1 source workspace")
}
expected_stage1_files = resolution["stage1_source_hashes"]
print(f"stage1 recorded file count={len(expected_stage1_files)}")
print(f"stage1 observed file count={len(observed_stage1_files)}")
missing = sorted(set(expected_stage1_files) - set(observed_stage1_files))
extra = sorted(set(observed_stage1_files) - set(expected_stage1_files))
changed = sorted(
    name
    for name in set(expected_stage1_files) & set(observed_stage1_files)
    if expected_stage1_files[name] != observed_stage1_files[name]
)
print(f"stage1 missing files={missing}")
print(f"stage1 extra files={extra}")
print(f"stage1 changed files={changed}")
checks.append(not missing and not extra and not changed)

tree_checks = (
    ("k_workspace_sha256", pipeline_contract.sha256_tree(K_PROOF)),
    ("stage1_export_sha256", klean_export.tree_digest(K_PROOF)),
    ("discovery_manifest_sha256", file_sha(DISCOVERY)),
    ("k_audit_sha256", pipeline_contract.sha256_tree(K_AUDIT)),
    ("klean_generation_sha256", pipeline_contract.sha256_tree(GENERATION)),
    ("generation_producer_sources_sha256", pipeline_contract.sha256_tree(PRODUCERS)),
    ("generated_tree_sha256", klean_export.tree_digest(GENERATED)),
)
for field, observed in tree_checks:
    checks.append(report(field, observed, hashes[field]))

checks.append(report("lean_workspace_sha256", None, hashes["lean_workspace_sha256"]))
checks.append(report("lean_invocation_sha256", None, hashes["lean_invocation_sha256"]))
checks.append(report("stage5_result", None, resolution["stage5_result"]))
checks.append(report("fixed target", None, resolution["target"]))

# Authenticate exactly the producer bundle recorded by immutable-image identity.
source_manifest = json.loads((PRODUCERS / "source-manifest.json").read_text())
generator_manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
producer_names = {
    path.relative_to(PRODUCERS).as_posix()
    for path in pipeline_contract._walk_regular_files(PRODUCERS, "producer source bundle")
}
checks.append(
    report(
        "producer file set",
        sorted(producer_names),
        ["klean.py", "klean_export.py", "source-manifest.json"],
    )
)
expected_source_files = {
    "klean_export.py": generator_manifest["exporter_sha256"],
    "klean.py": generator_manifest["klean_py_sha256"],
}
checks.append(report("source-manifest file map", source_manifest["files"], expected_source_files))
for name in ("klean_export.py", "klean.py"):
    actual = file_sha(PRODUCERS / name)
    checks.append(report(f"{name} vs source manifest", actual, source_manifest["files"][name]))
    checks.append(report(f"{name} vs generator manifest", actual, expected_source_files[name]))

image_from_generator = generator_manifest["provenance"]["generator_image_id"]
image_from_source = source_manifest["generator_image_id"]
image_from_audit_path = "sha256:" + Path(resolution["generation_producer_sources"]).name
checks.append(report("generator image: source vs generator manifest", image_from_source, image_from_generator))
checks.append(report("generator image: audit input path vs generator manifest", image_from_audit_path, image_from_generator))

# Bind Stage 4 manifests to the freshly observed immutable inputs.
checks.append(report("generator generated tree", generator_manifest["generated_tree_sha256"], hashes["generated_tree_sha256"]))
checks.append(report("generator Stage 1 provenance", generator_manifest["provenance"]["stage1_workspace_sha256"], hashes["stage1_export_sha256"]))
checks.append(report("generator Stage 3 provenance", generator_manifest["provenance"]["stage3_discovery_manifest_sha256"], hashes["discovery_manifest_sha256"]))
checks.append(report("generator target vs audit target", generator_manifest["target"], resolution["target"]))
checks.append(report("embedded preflight vs sidecar", resolution["stage4_preflight"], json.loads((GENERATION / "preflight.json").read_text())))
checks.append(report("selected K audit artifact", resolution["selections"]["k_audit"]["artifact_sha256"], hashes["k_audit_sha256"]))
checks.append(report("selected Stage 4 artifact", resolution["selections"]["klean_generation"]["artifact_sha256"], hashes["klean_generation_sha256"]))

print(f"TOTAL_CHECKS={len(checks)}")
print(f"FAILED_CHECKS={sum(not value for value in checks)}")
if not all(checks):
    raise SystemExit(1)
