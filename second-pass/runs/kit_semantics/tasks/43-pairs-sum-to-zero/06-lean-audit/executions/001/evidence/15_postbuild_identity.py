#!/usr/bin/env python3
"""Post-build target identity and candidate trust/shadow audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.klean_export import target_statement


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


fresh = Path("/tmp/audit-work/stage5-fresh")
base = fresh / "Base"
manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())
expected_target = manifest["target"]
observed_target = target_statement(base)

reference_target_file = (
    Path("/reference/klean-generation/generated") / expected_target["file"]
)
fresh_target_file = base / expected_target["file"]

candidate_lean = [
    path
    for path in fresh.rglob("*.lean")
    if "Base" not in path.relative_to(fresh).parts
    and ".lake" not in path.relative_to(fresh).parts
    and path.name not in {"Axioms.lean", "BridgeChecks.lean"}
]
candidate_texts = {
    path.relative_to(fresh).as_posix(): path.read_text()
    for path in candidate_lean
}
forbidden_hits: list[dict[str, str]] = []
for relative, text in candidate_texts.items():
    for match in re.finditer(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text):
        forbidden_hits.append(
            {"file": relative, "token": match.group(0)}
        )

shadow_count = sum(
    len(re.findall(r"(?m)^\s*def\s+targetStatement\b", text))
    for text in candidate_texts.values()
)

proof_text = (fresh / "Proof.lean").read_text()
theorem_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    proof_text,
)
normalized_final = (
    " ".join(theorem_matches[0].split())
    if len(theorem_matches) == 1
    else None
)
normalized_target = " ".join(expected_target["statement"].split())

facts = {
    "observed_postbuild_target": observed_target,
    "generator_manifest_target_matches": observed_target == expected_target,
    "audit_input_target_matches": (
        observed_target == audit_input["resolution"]["target"]
    ),
    "target_file_reference_sha256": sha256_file(reference_target_file),
    "target_file_fresh_postbuild_sha256": sha256_file(fresh_target_file),
    "target_file_bytes_unchanged": (
        reference_target_file.read_bytes() == fresh_target_file.read_bytes()
    ),
    "candidate_lean_sources": sorted(candidate_texts),
    "candidate_forbidden_hits": forbidden_hits,
    "candidate_target_shadow_count": shadow_count,
    "candidate_final_theorem_count": len(theorem_matches),
    "candidate_final_normalized": normalized_final,
    "fixed_statement_normalized": normalized_target,
    "candidate_final_is_exact_fixed_statement": (
        normalized_final == normalized_target
    ),
}

print(json.dumps(facts, indent=2, sort_keys=True))
if not all(
    (
        facts["generator_manifest_target_matches"],
        facts["audit_input_target_matches"],
        facts["target_file_bytes_unchanged"],
        not facts["candidate_forbidden_hits"],
        facts["candidate_target_shadow_count"] == 0,
        facts["candidate_final_theorem_count"] == 1,
        facts["candidate_final_is_exact_fixed_statement"],
    )
):
    raise SystemExit("POSTBUILD_TARGET_AND_CANDIDATE_GATE: FAIL")
print("POSTBUILD_TARGET_AND_CANDIDATE_GATE: PASS")
