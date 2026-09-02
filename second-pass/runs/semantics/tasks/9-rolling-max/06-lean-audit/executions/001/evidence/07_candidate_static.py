#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import stat
from pathlib import Path

from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_file


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/stage5-fresh")
base = fresh / "Base"
reference_base = Path("/reference/klean-generation/generated")
proof_path = fresh / "Proof.lean"
proof = proof_path.read_text()
manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)

candidate_source_names = {
    "Proof.lean",
    "lake-manifest.json",
    "lakefile.lean",
    "lean-toolchain",
}
mounted_source_hashes = {
    name: sha256_file(candidate / name) for name in sorted(candidate_source_names)
}
fresh_source_hashes = {
    name: sha256_file(fresh / name) for name in sorted(candidate_source_names)
}

all_entries_regular_or_directory = True
special_entries = []
for path in candidate.rglob("*"):
    mode = path.lstat().st_mode
    if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode)):
        all_entries_regular_or_directory = False
        special_entries.append(path.relative_to(candidate).as_posix())

patterns = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "unsafe": r"\bunsafe\b",
    "axiom_declaration": r"(?m)^\s*axiom\s+",
    "opaque_declaration": r"(?m)^\s*opaque\s+",
}
forbidden_matches = {
    name: [
        {"start": match.start(), "text": match.group(0)}
        for match in re.finditer(pattern, proof)
    ]
    for name, pattern in patterns.items()
}

checks = {
    "candidate_entries_regular_or_directory": all_entries_regular_or_directory,
    "fresh_source_hashes_match_mounted_candidate": (
        fresh_source_hashes == mounted_source_hashes
    ),
    "fresh_base_tree_matches_reference_generation": (
        tree_digest(base) == tree_digest(reference_base)
    ),
    "fresh_base_target_matches_generator_manifest": (
        target_statement(base) == manifest["target"]
    ),
    "candidate_does_not_define_targetStatement": (
        re.search(r"(?m)^\s*def\s+targetStatement\b", proof) is None
    ),
    "candidate_does_not_open_generated_target_namespace": (
        "namespace Klean9RollingMax.Lemmas" not in proof
    ),
    "candidate_has_exactly_one_parameter_definition": (
        len(
            re.findall(
                r"(?m)^def\s+«firstAfter\(_,_\)_VERIFICATION_"
                r"Bool_IntSeq_Bool»\s*:",
                proof,
            )
        )
        == 1
    ),
    "candidate_has_exactly_one_final_theorem": (
        len(re.findall(r"(?m)^theorem\s+final\s*:", proof)) == 1
    ),
    "final_names_fixed_generated_target": (
        "Klean9RollingMax.Lemmas.targetStatement "
        "«firstAfter(_,_)_VERIFICATION_Bool_IntSeq_Bool» := by"
        in proof
    ),
    "no_forbidden_candidate_tokens": all(
        not matches for matches in forbidden_matches.values()
    ),
}

result = {
    "checks": checks,
    "special_entries": special_entries,
    "forbidden_matches": forbidden_matches,
    "mounted_candidate_source_hashes": mounted_source_hashes,
    "fresh_candidate_source_hashes": fresh_source_hashes,
    "fresh_base_tree_sha256": tree_digest(base),
    "reference_base_tree_sha256": tree_digest(reference_base),
    "fresh_base_target": target_statement(base),
    "candidate_source": proof,
}
result["all_checks_pass"] = all(checks.values())
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["all_checks_pass"] else 1)
