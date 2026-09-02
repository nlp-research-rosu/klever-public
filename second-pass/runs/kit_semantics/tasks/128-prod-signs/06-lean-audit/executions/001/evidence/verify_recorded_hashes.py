#!/usr/bin/env python3
"""Independent integrity checks for the mounted Stage 3/4 audit inputs."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, "/reference")
from tools import klean_export, pipeline_contract  # noqa: E402


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(label: str, observed: object, expected: object) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{status} {label}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")
    if status != "MATCH":
        raise SystemExit(1)


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
hashes = resolution["hashes"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
input_manifest = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
export_result = json.loads(
    Path("/reference/klean-generation/export-result.json").read_text()
)
preflight = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)

check("environment audit mode", os.environ.get("AUDIT_MODE"), resolution["mode"])
check("problem", resolution["problem_id"], "128-prod-signs")
check("condition", resolution["condition"], "kit-semantics")
check("semantics mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")

producer_hashes = {
    name: file_sha(Path("/reference/generation-tools") / name)
    for name in ("klean_export.py", "klean.py")
}
check("producer hashes vs source manifest", producer_hashes, source_manifest["files"])
check("klean_export.py vs generator manifest", producer_hashes["klean_export.py"], generator["exporter_sha256"])
check("klean.py vs generator manifest", producer_hashes["klean.py"], generator["klean_py_sha256"])
check("generator image: source vs generator", source_manifest["generator_image_id"], generator["provenance"]["generator_image_id"])
audit_image_key = Path(resolution["generation_producer_sources"]).name
check("generator image: audit path vs manifest", f"sha256:{audit_image_key}", generator["provenance"]["generator_image_id"])
check(
    "producer source tree",
    pipeline_contract.sha256_tree(Path("/reference/generation-tools")),
    hashes["generation_producer_sources_sha256"],
)

check("Stage 3 discovery file", file_sha(Path("/reference/lemma-discovery.json")), hashes["discovery_manifest_sha256"])
check("Stage 1 pipeline tree", pipeline_contract.sha256_tree(Path("/reference/k-proof")), hashes["k_workspace_sha256"])
check("Stage 1 exporter tree", klean_export.tree_digest(Path("/reference/k-proof")), hashes["stage1_export_sha256"])
check("Stage 2 audit tree", pipeline_contract.sha256_tree(Path("/reference/k-audit")), hashes["k_audit_sha256"])
check("Stage 4 generation tree", pipeline_contract.sha256_tree(Path("/reference/klean-generation")), hashes["klean_generation_sha256"])
check("generated exporter tree", klean_export.tree_digest(Path("/reference/klean-generation/generated")), hashes["generated_tree_sha256"])

actual_stage1_files = {
    path.relative_to("/reference/k-proof").as_posix(): file_sha(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "mounted Stage 1 workspace"
    )
}
check("Stage 1 regular-file name set", sorted(actual_stage1_files), sorted(resolution["stage1_source_hashes"]))
check("Stage 1 complete source hash map", actual_stage1_files, resolution["stage1_source_hashes"])
print(f"Stage 1 source files checked: {len(actual_stage1_files)}")

discovery_sha = hashes["discovery_manifest_sha256"]
stage1_export_sha = hashes["stage1_export_sha256"]
generated_sha = hashes["generated_tree_sha256"]
check("generator provenance Stage 3", generator["provenance"]["stage3_discovery_manifest_sha256"], discovery_sha)
check("generator provenance Stage 1", generator["provenance"]["stage1_workspace_sha256"], stage1_export_sha)
check("input manifest Stage 3", input_manifest["stage3_discovery_manifest_sha256"], discovery_sha)
check("input manifest Stage 1", input_manifest["frozen_input_sha256"], stage1_export_sha)
check("export result Stage 3", export_result["stage3_discovery_manifest_sha256"], discovery_sha)
check("export result Stage 1", export_result["frozen_input_sha256"], stage1_export_sha)
check("export result generated tree", export_result["generated_tree_sha256"], generated_sha)
check("preflight Stage 3", preflight["stage3_discovery_manifest_sha256"], discovery_sha)
check("preflight Stage 1 frozen", preflight["frozen_input_sha256"], stage1_export_sha)
check("preflight Stage 1 workspace", preflight["stage1_workspace_sha256"], stage1_export_sha)
check("preflight generated tree", preflight["generated_tree_sha256"], generated_sha)
check("audit embedded preflight", resolution["stage4_preflight"], preflight)

obligation_sha = file_sha(Path("/reference/klean-generation/generated/obligation-map.json"))
check("obligation map file", obligation_sha, generator["obligation_map_sha256"])
trust_sha = file_sha(Path("/reference/klean-generation/trust-inventory.json"))
check("trust inventory file", trust_sha, export_result["trust_inventory_sha256"])

check("selected Stage 4 status", resolution["selections"]["klean_generation"]["status"], "KLEAN_NO_OBLIGATIONS")
check("export status", export_result["status"], "KLEAN_NO_OBLIGATIONS")
check("preflight status", preflight["status"], "KLEAN_NO_OBLIGATIONS")
check("generator obligation count", generator["obligation_count"], 0)
check("export obligation count", export_result["obligation_count"], 0)
check("preflight obligation count", preflight["obligation_count"], 0)
check("generator target", generator["target"], None)
check("preflight target", preflight["target"], None)
check("audit target", resolution["target"], None)
check("audit Stage 5 result", resolution["stage5_result"], None)
check("audit Lean workspace", resolution["lean_workspace"], None)
check("audit Lean invocation", resolution["lean_invocation"], None)
check("candidate absent", Path("/candidate").exists(), False)
print("ALL_RECORDED_HASH_AND_PRODUCER_CHECKS_PASS")
