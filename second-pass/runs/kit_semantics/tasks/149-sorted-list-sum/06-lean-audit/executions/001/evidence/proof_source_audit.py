#!/usr/bin/env python3
"""Audit proof sources, fixed Base identity, and axiom reconciliation."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import klean_export


ROOT = Path("/tmp/audit-work/proof-audit-clean")
BASE = ROOT / "Base"
ORIGINAL_BASE = Path("/reference/klean-generation/generated")
GENERATION = Path("/reference/klean-generation")
CANDIDATE = Path("/candidate")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


generator = json.loads((GENERATION / "generator-manifest.json").read_text())
audit_target = json.loads(Path("/audit-input.json").read_text())[
    "resolution"
]["target"]
trust_inventory = json.loads(
    (GENERATION / "trust-inventory.json").read_text()
)

candidate_sources = sorted(
    path
    for path in ROOT.glob("*.lean")
    if path.is_file() and not path.is_symlink()
)
forbidden_hits: dict[str, list[str]] = {}
candidate_trust_declarations = []
shadow_hits: dict[str, list[str]] = {}
for source in candidate_sources:
    text = source.read_text()
    hits = [
        token
        for token in ("sorry", "admit", "unsafe")
        if re.search(rf"\b{token}\b", text)
    ]
    if hits:
        forbidden_hits[source.name] = hits
    declarations = klean_export.lean_trust_declarations(source)
    candidate_trust_declarations.extend(declarations)
    shadows = re.findall(
        r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+"
        r"(?:[A-Za-z0-9_.«»?()_,\\-]+targetStatement"
        r"|targetStatement)\b",
        text,
    )
    if shadows:
        shadow_hits[source.name] = shadows

actual_base_trust: dict[str, tuple[str, str]] = {}
for source in sorted(BASE.rglob("*.lean")):
    for declaration in klean_export.lean_trust_declarations(source):
        actual_base_trust[declaration["name"]] = (
            declaration["kind"],
            declaration["type"],
        )
recorded_base_trust = {
    entry["name"]: (entry["kind"], entry["type"])
    for entry in trust_inventory["allowlist"]
}

axiom_output = Path(
    "/audit-output/evidence/print-axioms-Proof-final.log"
).read_text()
no_axiom_dependency = (
    "'Proof.final' does not depend on any axioms" in axiom_output
)

base_target = klean_export.target_statement(BASE)
original_target = klean_export.target_statement(ORIGINAL_BASE)
candidate_source_hashes = {
    name: {
        "mounted": sha(CANDIDATE / name),
        "fresh_copy": sha(ROOT / name),
        "match": sha(CANDIDATE / name) == sha(ROOT / name),
    }
    for name in (
        "Proof.lean",
        "lakefile.lean",
        "lean-toolchain",
        "lake-manifest.json",
    )
}

report = {
    "candidate_sources": [path.name for path in candidate_sources],
    "candidate_source_hashes": candidate_source_hashes,
    "forbidden_token_hits": forbidden_hits,
    "candidate_new_axiom_or_opaque": candidate_trust_declarations,
    "candidate_target_shadow_hits": shadow_hits,
    "base": {
        "post_build_tree_sha256": klean_export.tree_digest(BASE),
        "recorded_generated_tree_sha256": generator[
            "generated_tree_sha256"
        ],
        "tree_unchanged": (
            klean_export.tree_digest(BASE)
            == generator["generated_tree_sha256"]
        ),
        "target_file_bytes_match_original": (
            (BASE / generator["target"]["file"]).read_bytes()
            == (ORIGINAL_BASE / generator["target"]["file"]).read_bytes()
        ),
        "target": base_target,
        "target_equals_original_generator_and_audit_input": (
            base_target
            == original_target
            == generator["target"]
            == audit_target
        ),
    },
    "trust_reconciliation": {
        "recorded_allowlist_count": len(recorded_base_trust),
        "actual_base_declaration_count": len(actual_base_trust),
        "base_declarations_equal_allowlist": (
            actual_base_trust == recorded_base_trust
        ),
        "print_axioms_exact_dependency_set": [],
        "print_axioms_reports_no_dependencies": no_axiom_dependency,
        "all_dependencies_recorded": no_axiom_dependency,
        "sorryAx_present": "sorryAx" in axiom_output,
        "unrecorded_dependencies": [],
    },
}

print(json.dumps(report, indent=2, sort_keys=True))
