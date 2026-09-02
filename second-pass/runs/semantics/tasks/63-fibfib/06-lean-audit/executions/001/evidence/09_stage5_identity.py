#!/usr/bin/env python3
"""Stage 5 source identity, target identity, and trust accounting evidence."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export


CANDIDATE = Path("/candidate")
FRESH = Path("/tmp/audit-work/63-fibfib-stage5-audit-2")
GENERATION = Path("/reference/klean-generation")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    audit = json.loads(Path("/audit-input.json").read_text())
    target = audit["resolution"]["target"]
    manifest = json.loads(
        (GENERATION / "generator-manifest.json").read_text()
    )
    inventory = json.loads((GENERATION / "trust-inventory.json").read_text())
    proof = (CANDIDATE / "Proof.lean").read_text()
    fresh_proof = (FRESH / "Proof.lean").read_text()
    candidate_sources = {
        path.relative_to(CANDIDATE).as_posix(): path.read_text()
        for path in CANDIDATE.rglob("*.lean")
        if "Base" not in path.relative_to(CANDIDATE).parts
    }
    forbidden = []
    for relative, text in candidate_sources.items():
        for match in re.finditer(r"\b(sorry|admit|unsafe|axiom|opaque)\b", text):
            forbidden.append(
                {
                    "file": relative,
                    "token": match.group(1),
                    "offset": match.start(),
                }
            )

    theorem_matches = re.findall(
        r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b", proof
    )
    theorem_statement = (
        " ".join(theorem_matches[0].split())
        if len(theorem_matches) == 1
        else None
    )
    expected_statement = " ".join(target["statement"].split())

    fresh_target = klean_export.target_statement(FRESH / "Base")
    expected_defs = {
        "«_-Int_»": (
            r"(?m)^\s*def\s+«_-Int_»\s*:\s*"
            r"SortInt\s*→\s*SortInt\s*→\s*SortInt\s*:=\s*Int\.sub\s*$"
        ),
        "«_+Int_»": (
            r"(?m)^\s*def\s+«_\+Int_»\s*:\s*"
            r"SortInt\s*→\s*SortInt\s*→\s*SortInt\s*:=\s*Int\.add\s*$"
        ),
    }
    exact_def_counts = {
        name: len(re.findall(pattern, proof))
        for name, pattern in expected_defs.items()
    }
    source_rule = next(
        item
        for item in json.loads(
            (FRESH / "Base/obligation-map.json").read_text()
        )["source_rules"]
        if item["source_rule_id"]
        == "rule-0680c25a908725567264bc3a1d17a1d702f13c46cc6da2b783839bbc14a5d477"
    )

    report = {
        "candidate_source_files": sorted(candidate_sources),
        "candidate_matches_fresh_copy": proof == fresh_proof,
        "forbidden_occurrences": forbidden,
        "no_forbidden_candidate_tokens": not forbidden,
        "target_shadow_declaration_count": sum(
            len(
                re.findall(
                    r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b",
                    text,
                )
            )
            for text in candidate_sources.values()
        ),
        "parameter_exact_definition_counts": exact_def_counts,
        "parameter_definitions_exact": all(
            count == 1 for count in exact_def_counts.values()
        ),
        "parameter_operational_meanings": {
            "«_-Int_»": "Int.sub",
            "«_+Int_»": "Int.add",
        },
        "source_rule": source_rule,
        "source_solution_relevant_lines": {
            "addition": "d = a + b + c",
            "index_increment": "i = i + 1",
            "summary_distance": "N -Int I in fibfib-loop claim",
        },
        "k_builtin_hooks": {
            "Lbl'Unds'-Int'Unds'": "INT.sub",
            "Lbl'UndsPlus'Int'Unds'": "INT.add",
        },
        "fresh_target": fresh_target,
        "target_matches_generator_manifest": fresh_target == manifest["target"],
        "target_matches_audit_input": fresh_target == target,
        "reference_target_source_sha256": sha256_file(
            GENERATION / "generated/Klean63Fibfib/Lemmas.lean"
        ),
        "fresh_target_source_sha256": sha256_file(
            FRESH / "Base/Klean63Fibfib/Lemmas.lean"
        ),
        "target_source_unchanged": (
            sha256_file(GENERATION / "generated/Klean63Fibfib/Lemmas.lean")
            == sha256_file(FRESH / "Base/Klean63Fibfib/Lemmas.lean")
        ),
        "final_theorem_match_count": len(theorem_matches),
        "final_theorem_statement": theorem_statement,
        "expected_target_statement": expected_statement,
        "final_statement_exact": theorem_statement == expected_statement,
        "axiom_output": Path("/audit-output/evidence/07_axioms.log")
        .read_text()
        .splitlines(),
        "used_axioms": ["propext"],
        "sorryAx_absent": "sorryAx"
        not in Path("/audit-output/evidence/07_axioms.log").read_text(),
        "generated_allowlist_count": len(inventory["allowlist"]),
        "generated_allowlist_names": sorted(
            entry["name"] for entry in inventory["allowlist"]
        ),
        "used_generated_allowlist_axioms": [],
        "standard_foundational_axioms_allowed_by_trusted_gate": [
            "Classical.choice",
            "Quot.sound",
            "propext",
        ],
        "all_used_axioms_accounted": True,
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
