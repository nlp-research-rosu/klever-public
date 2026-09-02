#!/usr/bin/env python3
"""Recompute and compare every launcher/manifests hash relevant to this audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools import klean_export, pipeline_contract


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> dict[str, object]:
    result = {
        "label": label,
        "observed": observed,
        "expected": expected,
        "match": observed == expected,
    }
    print(json.dumps(result, sort_keys=True))
    return result


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
recorded = resolution["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)

results: list[dict[str, object]] = []

# The producer identity gate is intentionally first.
for name, manifest_key in (
    ("klean_export.py", "exporter_sha256"),
    ("klean.py", "klean_py_sha256"),
):
    observed = file_hash(Path("/reference/generation-tools") / name)
    results.append(check(f"producer file {name} vs source manifest", observed, source_manifest["files"][name]))
    results.append(check(f"producer file {name} vs generator manifest", observed, generator[manifest_key]))

generator_image = generator["provenance"]["generator_image_id"]
producer_path_image = "sha256:" + Path(resolution["generation_producer_sources"]).name
results.append(check("producer image: source vs generator manifest", source_manifest["generator_image_id"], generator_image))
results.append(check("producer image: launcher path vs generator manifest", producer_path_image, generator_image))
results.append(check("producer source bundle tree", pipeline_contract.sha256_tree(Path("/reference/generation-tools")), recorded["generation_producer_sources_sha256"]))
results.append(check("producer source file set", sorted(p.relative_to("/reference/generation-tools").as_posix() for p in Path("/reference/generation-tools").iterdir()), ["klean.py", "klean_export.py", "source-manifest.json"]))

# Launcher-recorded selection hashes use pipeline_contract.sha256_tree.
for label, path, key in (
    ("Stage 1 workspace selection tree", Path("/reference/k-proof"), "k_workspace_sha256"),
    ("Stage 2 selected audit tree", Path("/reference/k-audit"), "k_audit_sha256"),
    ("Stage 4 selected generation tree", Path("/reference/klean-generation"), "klean_generation_sha256"),
):
    results.append(check(label, pipeline_contract.sha256_tree(path), recorded[key]))

# Export/preflight tree hashes use klean_export.tree_digest.
stage1_export = klean_export.tree_digest(Path("/reference/k-proof"))
generated_tree = klean_export.tree_digest(Path("/reference/klean-generation/generated"))
discovery_hash = file_hash(Path("/reference/lemma-discovery.json"))
results.append(check("Stage 1 export tree", stage1_export, recorded["stage1_export_sha256"]))
results.append(check("Stage 1 export vs input manifest", stage1_export, input_manifest["stage1_workspace_sha256"]))
results.append(check("Stage 1 export vs generator provenance", stage1_export, generator["provenance"]["stage1_workspace_sha256"]))
results.append(check("Stage 3 discovery file", discovery_hash, recorded["discovery_manifest_sha256"]))
results.append(check("Stage 3 discovery vs input manifest", discovery_hash, input_manifest["stage3_discovery_manifest_sha256"]))
results.append(check("Stage 3 discovery vs generator provenance", discovery_hash, generator["provenance"]["stage3_discovery_manifest_sha256"]))
results.append(check("generated project tree vs launcher", generated_tree, recorded["generated_tree_sha256"]))
results.append(check("generated project tree vs generator manifest", generated_tree, generator["generated_tree_sha256"]))
results.append(check("generated project tree vs export result", generated_tree, export_result["generated_tree_sha256"]))

# The launcher records a complete per-file hash map for the frozen Stage 1 tree.
stage1_files = {
    p.relative_to("/reference/k-proof").as_posix(): file_hash(p)
    for p in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "frozen Stage 1 workspace"
    )
}
results.append(check("Stage 1 source file hash map (bijective)", stage1_files, resolution["stage1_source_hashes"]))

# Null hashes are required for absent Stage 5 inputs in classification-only mode.
results.append(check("launcher mode vs environment", resolution["mode"], __import__("os").environ.get("AUDIT_MODE")))
results.append(check("classification-only Lean workspace hash", recorded["lean_workspace_sha256"], None))
results.append(check("classification-only Lean invocation hash", recorded["lean_invocation_sha256"], None))
results.append(check("classification-only target", resolution.get("target"), None))

failed = [entry["label"] for entry in results if not entry["match"]]
summary = {"checks": len(results), "failures": failed, "status": "PASS" if not failed else "FAIL"}
print(json.dumps({"summary": summary}, sort_keys=True))
raise SystemExit(0 if not failed else 1)
