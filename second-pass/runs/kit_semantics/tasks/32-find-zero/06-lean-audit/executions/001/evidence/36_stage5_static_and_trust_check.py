#!/usr/bin/env python3
"""Static target/proof/trust audit after the clean Stage 5 build."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path

from tools import klean_export


FRESH = Path("/tmp/audit-work/stage5-fresh.HEsYTA")
BASE = FRESH / "Base"
AUTHENTICATED_BASE = Path("/reference/klean-generation/generated")
GENERATION = Path("/reference/klean-generation")
AUDIT_INPUT = Path("/audit-input.json")
AXIOM_LOG = Path("/audit-output/evidence/25_print_axioms_proof_final_exact.txt")

PARAMETER_NAME = "«numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq»"

EXPECTED_DEFINITION = """def «numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» : SortNumSeq → SortValSeq
  | SortNumSeq.«.NumSeq_VERIFICATION-SYNTAX_NumSeq» =>
      SortValSeq.«.ValSeq_MPY-CORE_ValSeq»
  | SortNumSeq.«nInt(_,_)_VERIFICATION-SYNTAX_NumSeq_Int_NumSeq» i rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortInt i)
        («numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» rest)
  | SortNumSeq.«nFloat(_,_)_VERIFICATION-SYNTAX_NumSeq_Float_NumSeq» f rest =>
      SortValSeq.«vCons(_,_)_MPY-CORE_ValSeq_Val_ValSeq»
        (SortVal.inj_SortFloat f)
        («numVals(_)_VERIFICATION-SYNTAX_ValSeq_NumSeq» rest)"""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def source_tree(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for root, dirs, files in os.walk(path, followlinks=False):
        root_path = Path(root)
        for name in dirs:
            child = root_path / name
            if not stat.S_ISDIR(child.lstat().st_mode):
                raise RuntimeError(f"unsafe directory entry: {child}")
        for name in files:
            child = root_path / name
            if not stat.S_ISREG(child.lstat().st_mode):
                raise RuntimeError(f"unsafe file entry: {child}")
            result[child.relative_to(path).as_posix()] = hashlib.sha256(
                child.read_bytes()
            ).hexdigest()
    return result


def target_definition(path: Path) -> str:
    text = path.read_text()
    matches = re.findall(
        r"(?ms)^\s*def\s+targetStatement\b.*?(?=^\s*end\s+\S+\s*$)",
        text,
    )
    if len(matches) != 1:
        raise RuntimeError(f"target count is {len(matches)}")
    return matches[0].strip()


def main() -> None:
    proof_path = FRESH / "Proof.lean"
    proof_text = proof_path.read_text()
    lake_text = (FRESH / "lakefile.lean").read_text()
    generator = json.loads((GENERATION / "generator-manifest.json").read_text())
    audit = json.loads(AUDIT_INPUT.read_text())
    trust = json.loads((GENERATION / "trust-inventory.json").read_text())
    axiom_output = AXIOM_LOG.read_text()

    definition_match = re.search(
        rf"(?ms)^def\s+{re.escape(PARAMETER_NAME)}\s*:.*?"
        r"(?=^\s*private\s+def\s+decodeNumVals\b)",
        proof_text,
    )
    candidate_definition = (
        definition_match.group(0).strip() if definition_match else None
    )
    final_type_match = re.search(
        r"(?ms)^theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
        proof_text,
    )
    final_type = (
        " ".join(final_type_match.group(1).split())
        if final_type_match is not None
        else None
    )
    expected_final_type = (
        "Klean32FindZero.Lemmas.targetStatement " + PARAMETER_NAME
    )

    axiom_match = re.search(
        r"'Proof\.final' depends on axioms: \[([^\]]*)\]", axiom_output
    )
    reported_axioms = (
        []
        if axiom_match is None or not axiom_match.group(1).strip()
        else [item.strip() for item in axiom_match.group(1).split(",")]
    )
    generated_allowlist = {entry["name"] for entry in trust["allowlist"]}

    base_target_definition = target_definition(
        BASE / "Klean32FindZero/Lemmas.lean"
    )
    target = generator["target"]

    controlled_lean = proof_text + "\n" + lake_text
    forbidden_matches = {
        token: [
            match.start()
            for match in re.finditer(rf"\b{re.escape(token)}\b", controlled_lean)
        ]
        for token in ("sorry", "admit", "unsafe", "axiom", "opaque")
    }
    controlled_declarations = re.findall(
        r"(?m)^\s*(axiom|opaque)\s+(\S+)", controlled_lean
    )

    checks: dict[str, object] = {
        "fresh_base_source_tree_matches_authenticated_generation": (
            source_tree(BASE) == source_tree(AUTHENTICATED_BASE)
        ),
        "fresh_base_generated_tree_hash": klean_export.tree_digest(BASE),
        "fresh_base_hash_matches_generator": (
            klean_export.tree_digest(BASE) == generator["generated_tree_sha256"]
        ),
        "candidate_definition_count": len(
            re.findall(
                rf"(?m)^def\s+{re.escape(PARAMETER_NAME)}\s*:", proof_text
            )
        ),
        "candidate_definition_exact": candidate_definition == EXPECTED_DEFINITION,
        "candidate_definition_sha256": (
            None
            if candidate_definition is None
            else sha256_text(candidate_definition)
        ),
        "final_theorem_count": len(
            re.findall(r"(?m)^theorem\s+final\s*:", proof_text)
        ),
        "final_type_exact": final_type == expected_final_type,
        "candidate_has_no_target_declaration": (
            re.search(r"(?m)^\s*def\s+targetStatement\b", controlled_lean) is None
        ),
        "forbidden_token_positions": forbidden_matches,
        "candidate_has_no_forbidden_tokens": all(
            not positions for positions in forbidden_matches.values()
        ),
        "candidate_new_axiom_or_opaque_declarations": controlled_declarations,
        "candidate_has_no_new_axiom_or_opaque": not controlled_declarations,
        "lake_dependency_is_only_local_authenticated_base": (
            'require «klean-32-find-zero» from "./Base"' in lake_text
            and re.findall(r"(?m)^\s*require\s+.*$", lake_text)
            == ['require «klean-32-find-zero» from "./Base"']
        ),
        "base_target_definition_sha256": sha256_text(base_target_definition),
        "base_target_definition_hash_matches_generator": (
            sha256_text(base_target_definition) == target["definition_sha256"]
        ),
        "base_target_identity_matches_audit_input": (
            target == audit["resolution"]["target"]
        ),
        "clean_exit_zero": (
            "EXIT_CODE=0"
            in Path(
                "/audit-output/evidence/23_stage5_lake_clean_complete.txt"
            ).read_text()
        ),
        "build_exit_zero": (
            "EXIT_CODE=0"
            in Path(
                "/audit-output/evidence/24_stage5_lake_build_complete.txt"
            ).read_text()
        ),
        "reported_axioms": reported_axioms,
        "reported_axioms_exactly_named_core_foundation": (
            reported_axioms == ["propext"]
        ),
        "sorryAx_absent": "sorryAx" not in reported_axioms,
        "generated_allowlisted_axioms_used_by_final": sorted(
            set(reported_axioms) & generated_allowlist
        ),
        "no_generated_allowlisted_axiom_used_by_final": not (
            set(reported_axioms) & generated_allowlist
        ),
        "trust_inventory_sorry_counts_zero": (
            trust["designated_sorries"] == 0 and trust["other_sorries"] == 0
        ),
        "trust_inventory_allowlist_count": len(generated_allowlist),
        "proof_identity_lean_check_exit_zero": (
            "EXIT_CODE=0"
            in Path(
                "/audit-output/evidence/35_proof_identity_lean_check.txt"
            ).read_text()
        ),
        "operational_bridge_universal_check_exit_zero": (
            "EXIT_CODE=0"
            in Path(
                "/audit-output/evidence/"
                "34_operational_bridge_universal_and_mutation_checks_final.txt"
            ).read_text()
        ),
    }

    required_numeric_checks = {
        "candidate_definition_count": 1,
        "final_theorem_count": 1,
    }
    errors = [
        name
        for name, value in checks.items()
        if isinstance(value, bool) and not value
    ]
    errors.extend(
        name
        for name, expected in required_numeric_checks.items()
        if checks[name] != expected
    )

    print(
        json.dumps(
            {
                "status": "PASS" if not errors else "FAIL",
                "errors": errors,
                "checks": checks,
                "axiom_reconciliation": {
                    "propext": (
                        "Lean core propositional extensionality, explicitly "
                        "reported by #print axioms; it is not declared by the "
                        "candidate and is outside the generated-declaration "
                        "allowlist inventoried by trust-inventory.json."
                    ),
                    "generated_trust_boundary": (
                        "All 50 generated declarations are inventoried, but "
                        "none occurs in the transitive axiom list of Proof.final."
                    ),
                    "proof_escapes": (
                        "No sorryAx, candidate axiom, candidate opaque, or "
                        "unallowlisted generated declaration is used."
                    ),
                },
            },
            indent=2,
            sort_keys=True,
        )
    )
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
