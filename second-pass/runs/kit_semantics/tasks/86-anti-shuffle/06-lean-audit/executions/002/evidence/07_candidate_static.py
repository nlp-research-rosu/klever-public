#!/usr/bin/env python3
"""Static candidate, fixed-target, and forbidden-trust checks."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools import klean_export


root = Path("/tmp/audit-work/stage5-proof-audit")
base = root / "Base"
proof = root / "Proof.lean"
lakefile = root / "lakefile.lean"
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
audit_target = json.loads(Path("/audit-input.json").read_text())["resolution"][
    "target"
]
actual_target = klean_export.target_statement(base)

candidate_sources = [proof, lakefile]
forbidden_patterns = {
    "sorry": re.compile(r"\bsorry\b"),
    "admit": re.compile(r"\badmit\b"),
    "unsafe": re.compile(r"\bunsafe\b"),
    "axiom": re.compile(r"(?m)^\s*axiom\b"),
    "opaque": re.compile(r"(?m)^\s*opaque\b"),
}
forbidden_hits = {
    token: [
        source.relative_to(root).as_posix()
        for source in candidate_sources
        if pattern.search(source.read_text())
    ]
    for token, pattern in forbidden_patterns.items()
}
trust_declarations = [
    declaration
    for source in candidate_sources
    for declaration in klean_export.lean_trust_declarations(source)
]
proof_text = proof.read_text()
final_match = re.search(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b", proof_text
)
final_statement = (
    " ".join(final_match.group(1).split()) if final_match is not None else None
)
expected_statement = generator["target"]["statement"]

checks = {
    "base_tree_still_exact_after_build": (
        klean_export.tree_digest(base) == generator["generated_tree_sha256"]
    ),
    "base_target_matches_generator": actual_target == generator["target"],
    "base_target_matches_audit_input": actual_target == audit_target,
    "candidate_has_no_forbidden_tokens": not any(forbidden_hits.values()),
    "candidate_has_no_new_axiom_or_opaque_declaration": (
        trust_declarations == []
    ),
    "candidate_does_not_declare_targetStatement": (
        re.search(
            r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b",
            proof_text + "\n" + lakefile.read_text(),
        )
        is None
    ),
    "candidate_defines_each_parameter_exactly_once": (
        len(re.findall(r"(?m)^\s*def\s+«_<Int_»(?=\s|\()", proof_text)) == 1
        and len(
            re.findall(
                r"(?m)^\s*def\s+«strLt\(_,_\)_MPY-STR_Bool_IntSeq_IntSeq»(?=\s|:)",
                proof_text,
            )
        )
        == 1
    ),
    "Proof_final_statement_is_exact_fixed_target_application": (
        final_statement == expected_statement
    ),
    "lakefile_binds_only_local_Base_dependency": (
        'require «klean-86-anti-shuffle» from "./Base"'
        in lakefile.read_text()
    ),
}

result = {
    "actual_target": actual_target,
    "expected_Proof_final_statement": expected_statement,
    "observed_Proof_final_statement": final_statement,
    "forbidden_hits": forbidden_hits,
    "candidate_trust_declarations": trust_declarations,
    "checks": checks,
    "all_checks_pass": all(checks.values()),
}
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
if not result["all_checks_pass"]:
    raise SystemExit(1)
