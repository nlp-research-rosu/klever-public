#!/usr/bin/env python3
"""Audit-authored post-build binding and exact-target checks."""

from __future__ import annotations

import json
import os
from pathlib import Path

from tools import klean_export, klean_final_gate, pipeline_contract
from tools.stage6_resolution_contract import verify_audit_input


AUDIT = Path("/audit-input.json")
GENERATION = Path("/reference/klean-generation")
FRESH = Path("/tmp/audit-work/stage5-90-next-smallest-audit-001")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


audit_doc = json.loads(AUDIT.read_text())
resolution, resolved_digest = verify_audit_input(audit_doc)
expected = resolution["hashes"]
manifest = json.loads((GENERATION / "generator-manifest.json").read_text())

observed_pipeline = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "discovery_manifest_sha256": pipeline_contract.sha256_file(
        Path("/reference/lemma-discovery.json")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(GENERATION),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(Path("/candidate")),
}
for key, digest in observed_pipeline.items():
    require(digest == expected[key], f"audit-input mismatch for {key}")

reference_target = klean_export.target_statement(GENERATION / "generated")
fresh_target = klean_export.target_statement(FRESH / "Base")
require(reference_target == manifest["target"], "reference target differs from manifest")
require(fresh_target == manifest["target"], "fresh Base target differs from manifest")
require(fresh_target == resolution["target"], "fresh Base target differs from audit input")
require(
    klean_export.tree_digest(FRESH / "Base") == expected["generated_tree_sha256"],
    "fresh Base tree differs from audit input",
)

# This trusted structural gate accepts the candidate-only tree (before Base is
# injected) and checks exact definitions once plus the exact theorem text.
klean_final_gate._candidate_gate(Path("/candidate"), manifest["target"])

require(os.environ.get("AUDIT_MODE") == resolution["mode"], "AUDIT_MODE mismatch")

print("resolved_input_sha256:", resolved_digest)
print("mode:", resolution["mode"])
for key, digest in observed_pipeline.items():
    print(f"{key}: {digest}")
print("fresh_base_tree_sha256:", klean_export.tree_digest(FRESH / "Base"))
print("target_declaration:", fresh_target["declaration"])
print("target_statement_sha256:", fresh_target["statement_sha256"])
print("target_definition_sha256:", fresh_target["definition_sha256"])
print("target_parameter_count:", len(fresh_target["parameters"]))
print("candidate_exact_binding_gate: PASS")
print("post_build_checks: PASS")
