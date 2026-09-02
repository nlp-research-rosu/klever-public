#!/usr/bin/env python3
"""Read-only candidate source, fixed-Base, and proof-identity checks."""

from __future__ import annotations

import json
import re
import stat
from pathlib import Path

from tools import klean_export, pipeline_contract


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/lean-proof.6L7ByC")
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
proof_text = (candidate / "Proof.lean").read_text()
target = generator["target"]

entries = list(candidate.rglob("*"))
candidate_special_entries = [
    str(path)
    for path in entries
    if not (
        stat.S_ISREG(path.stat(follow_symlinks=False).st_mode)
        or stat.S_ISDIR(path.stat(follow_symlinks=False).st_mode)
    )
]
forbidden_pattern = re.compile(
    r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", re.IGNORECASE
)
forbidden_hits = []
for path in entries:
    if path.is_file() and path.suffix == ".lean":
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if forbidden_pattern.search(line):
                forbidden_hits.append(f"{path}:{number}:{line}")

theorem_match = re.search(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    proof_text,
)
theorem_statement = (
    " ".join(theorem_match.group(1).split())
    if theorem_match is not None
    else None
)
expected_statement = " ".join(target["statement"].split())

definition_counts = {}
for parameter in target["parameters"]:
    name = parameter["name"]
    definition_counts[name] = len(
        re.findall(
            rf"(?m)^\s*def\s+{re.escape(name)}(?:\s|:)",
            proof_text,
        )
    )

actual_base_target = klean_export.target_statement(fresh / "Base")
checks = {
    "candidate_full_tree_matches_audit_input": (
        pipeline_contract.sha256_tree(candidate)
        == audit["hashes"]["lean_workspace_sha256"]
        == audit["stage5_result"]["outputs"]["workspace_sha256"]
    ),
    "candidate_has_only_regular_files_and_directories": (
        candidate_special_entries == []
    ),
    "candidate_has_no_forbidden_lean_tokens": forbidden_hits == [],
    "candidate_does_not_declare_targetStatement": (
        re.search(r"(?m)^\s*def\s+targetStatement\b", proof_text)
        is None
    ),
    "candidate_does_not_open_generated_target_namespace": (
        "namespace Klean21RescaleToUnit.Lemmas" not in proof_text
    ),
    "each_target_parameter_has_exactly_one_candidate_def": all(
        count == 1 for count in definition_counts.values()
    ),
    "candidate_final_statement_exactly_matches_fixed_target_application": (
        theorem_statement == expected_statement
    ),
    "fresh_Base_tree_matches_generator_manifest": (
        klean_export.tree_digest(fresh / "Base")
        == generator["generated_tree_sha256"]
        == audit["hashes"]["generated_tree_sha256"]
    ),
    "fresh_Base_target_metadata_exact": (
        actual_base_target == target == audit["target"]
    ),
}

print("CANDIDATE_TREE_SHA256")
print(pipeline_contract.sha256_tree(candidate))
print()
print("FRESH_BASE_TREE_SHA256")
print(klean_export.tree_digest(fresh / "Base"))
print()
print("FORBIDDEN_HITS")
print(json.dumps(forbidden_hits, indent=2, ensure_ascii=False))
print()
print("SPECIAL_ENTRIES")
print(json.dumps(candidate_special_entries, indent=2))
print()
print("PARAMETER_DEFINITION_COUNTS")
print(json.dumps(definition_counts, indent=2, ensure_ascii=False))
print()
print("EXTRACTED_FINAL_STATEMENT")
print(theorem_statement)
print()
print("EXPECTED_FINAL_STATEMENT")
print(expected_statement)
print()
print("CHECKS")
for name, result in checks.items():
    print(f"{name}: {result}")
print()
print("ALL_STAGE5_SOURCE_CHECKS_PASS:", all(checks.values()))
