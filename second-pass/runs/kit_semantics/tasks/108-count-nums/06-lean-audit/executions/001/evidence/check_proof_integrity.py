#!/usr/bin/env python3
"""Independent hashes, target identity, and candidate-source scan."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree


audit = json.loads(Path("/audit-input.json").read_text())
resolution = audit["resolution"]
manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
workspace = Path(
    "/audit-output/evidence/fresh-proof-workspace.txt"
).read_text().strip()
base = workspace / Path("Base")

reference_target = target_statement(
    Path("/reference/klean-generation/generated")
)
fresh_target = target_statement(base)
audit_target = resolution["target"]
manifest_target = manifest["target"]

candidate_sources: dict[str, str] = {}
for source in sorted(Path("/candidate").rglob("*.lean")):
    relative = source.relative_to("/candidate").as_posix()
    if relative.startswith("Base/"):
        continue
    candidate_sources[relative] = source.read_text()

forbidden_pattern = re.compile(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b")
forbidden = [
    {
        "file": relative,
        "token": match.group(0),
        "offset": match.start(),
    }
    for relative, text in candidate_sources.items()
    for match in forbidden_pattern.finditer(text)
]
proof_text = candidate_sources["Proof.lean"]
target_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    proof_text,
)
normalized_target_matches = [" ".join(item.split()) for item in target_matches]
normalized_fixed_statement = " ".join(manifest_target["statement"].split())
parameter_counts = {
    parameter["name"]: len(
        re.findall(
            rf"(?m)^\s*(?:@\[[^\n]*\]\s*)*"
            rf"(?:noncomputable\s+)?def\s+{re.escape(parameter['name'])}"
            rf"\s*(?::|\()",
            "\n".join(candidate_sources.values()),
        )
    )
    for parameter in manifest_target["parameters"]
}

result = {
    "audit_mode_environment": os.environ.get("AUDIT_MODE"),
    "audit_mode_recorded": resolution["mode"],
    "candidate_pipeline_tree_sha256": sha256_tree(Path("/candidate")),
    "candidate_pipeline_tree_expected": resolution["hashes"][
        "lean_workspace_sha256"
    ],
    "candidate_klean_tree_sha256": tree_digest(Path("/candidate")),
    "generation_pipeline_tree_sha256": sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_pipeline_tree_expected": resolution["hashes"][
        "klean_generation_sha256"
    ],
    "generated_reference_klean_tree_sha256": tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generated_reference_klean_tree_expected": resolution["hashes"][
        "generated_tree_sha256"
    ],
    "proof_sha256": hashlib.sha256(
        Path("/candidate/Proof.lean").read_bytes()
    ).hexdigest(),
    "fresh_base_target_file_sha256": hashlib.sha256(
        (base / manifest_target["file"]).read_bytes()
    ).hexdigest(),
    "reference_target_file_sha256": hashlib.sha256(
        (
            Path("/reference/klean-generation/generated")
            / manifest_target["file"]
        ).read_bytes()
    ).hexdigest(),
    "target_reference": reference_target,
    "target_fresh_base": fresh_target,
    "target_generator_manifest": manifest_target,
    "target_audit_input": audit_target,
    "all_four_targets_equal": (
        reference_target
        == fresh_target
        == manifest_target
        == audit_target
    ),
    "forbidden_candidate_tokens": forbidden,
    "parameter_definition_counts": parameter_counts,
    "final_theorem_count": len(target_matches),
    "final_theorem_normalized": normalized_target_matches,
    "fixed_statement_normalized": normalized_fixed_statement,
    "final_is_exact_fixed_statement": (
        normalized_target_matches == [normalized_fixed_statement]
    ),
}
result["all_integrity_checks_pass"] = all(
    (
        result["audit_mode_environment"] == "CLASSIFICATION_AND_PROOF",
        result["audit_mode_recorded"] == "CLASSIFICATION_AND_PROOF",
        result["candidate_pipeline_tree_sha256"]
        == result["candidate_pipeline_tree_expected"],
        result["generation_pipeline_tree_sha256"]
        == result["generation_pipeline_tree_expected"],
        result["generated_reference_klean_tree_sha256"]
        == result["generated_reference_klean_tree_expected"],
        result["fresh_base_target_file_sha256"]
        == result["reference_target_file_sha256"],
        result["all_four_targets_equal"],
        not forbidden,
        set(parameter_counts.values()) == {1},
        result["final_is_exact_fixed_statement"],
    )
)
Path("/audit-output/evidence/proof-integrity.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n"
)
print(json.dumps(result, indent=2, sort_keys=True))
