#!/usr/bin/env python3
"""Read-only Stage 5 identity, source, and trust checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, pipeline_contract


GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
CANDIDATE = Path("/candidate")
FRESH = Path("/tmp/audit-work/161-solve-proof-audit-2")
AUDIT_INPUT = Path("/audit-input.json")


def load(path: Path) -> dict:
    document = json.loads(path.read_text())
    assert isinstance(document, dict)
    return document


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(condition: bool, label: str) -> dict[str, object]:
    return {"check": label, "pass": bool(condition)}


def main() -> None:
    audit = load(AUDIT_INPUT)["resolution"]
    manifest = load(GENERATION / "generator-manifest.json")
    inventory = load(GENERATION / "trust-inventory.json")
    target = klean_export.target_statement(GENERATED)
    fresh_target = klean_export.target_statement(FRESH / "Base")

    original_entries = klean_export._tree_entries(CANDIDATE)
    candidate_lean_sources = [
        (relative, path.read_text())
        for relative, kind, path in original_entries
        if kind == "file"
        and path.suffix == ".lean"
        and Path(relative).parts[0] != "Base"
    ]
    forbidden_matches = [
        {
            "file": relative,
            "token": match.group(0),
            "offset": match.start(),
        }
        for relative, text in candidate_lean_sources
        for match in re.finditer(
            r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text
        )
    ]
    target_shadow_matches = [
        {
            "file": relative,
            "text": match.group(0),
            "offset": match.start(),
        }
        for relative, text in candidate_lean_sources
        for match in re.finditer(
            r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b",
            text,
        )
    ]
    parameter_definitions: dict[str, list[str]] = {}
    for parameter in target["parameters"]:
        name = parameter["name"]
        parameter_definitions[name] = [
            relative
            for relative, text in candidate_lean_sources
            if re.search(
                rf"(?m)^\s*(?:noncomputable\s+)?def\s+"
                rf"{re.escape(name)}\s*(?::|\()",
                text,
            )
        ]

    proof_text = (CANDIDATE / "Proof.lean").read_text()
    theorem_matches = re.findall(
        r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
        proof_text,
    )
    observed_final_type = (
        " ".join(theorem_matches[0].split())
        if len(theorem_matches) == 1
        else None
    )
    expected_final_type = " ".join(target["statement"].split())

    copied_files = (
        "Proof.lean",
        "lakefile.lean",
        "lake-manifest.json",
        "lean-toolchain",
    )
    copy_hashes = {
        name: {
            "mounted": file_sha256(CANDIDATE / name),
            "fresh": file_sha256(FRESH / name),
        }
        for name in copied_files
    }

    used_axioms = {"propext", "Classical.choice", "Quot.sound"}
    generated_allowlist = {
        entry["name"] for entry in inventory["allowlist"]
    }
    trusted_gate_core_axioms = {
        "propext",
        "Classical.choice",
        "Quot.sound",
    }
    permitted_axioms = generated_allowlist | trusted_gate_core_axioms

    checks = [
        check(
            pipeline_contract.sha256_tree(CANDIDATE)
            == audit["hashes"]["lean_workspace_sha256"],
            "mounted candidate tree equals audit-input hash",
        ),
        check(
            klean_export.tree_digest(FRESH / "Base")
            == klean_export.tree_digest(GENERATED),
            "fresh Base source tree equals immutable generated project",
        ),
        check(
            all(item["mounted"] == item["fresh"] for item in copy_hashes.values()),
            "fresh candidate control/source files equal mounted candidate",
        ),
        check(
            target == manifest["target"],
            "immutable target equals generator manifest",
        ),
        check(
            target == audit["target"],
            "immutable target equals audit input",
        ),
        check(
            fresh_target == target,
            "fresh Base target equals immutable generated target",
        ),
        check(
            not forbidden_matches,
            "candidate Lean source has no forbidden trust token",
        ),
        check(
            not target_shadow_matches,
            "candidate does not declare or shadow targetStatement",
        ),
        check(
            all(len(files) == 1 for files in parameter_definitions.values()),
            "candidate defines each exact target parameter once",
        ),
        check(
            observed_final_type == expected_final_type,
            "Proof.final type is the exact fixed target statement",
        ),
        check(
            "sorryAx" not in used_axioms,
            "Proof.final has no sorryAx dependency",
        ),
        check(
            used_axioms <= permitted_axioms,
            "every observed axiom is permitted by the trusted gate policy",
        ),
        check(
            used_axioms.isdisjoint(generated_allowlist),
            "Proof.final uses none of the generated Klean trust axioms",
        ),
    ]
    print(
        json.dumps(
            {
                "checks": checks,
                "all_checks_pass": all(item["pass"] for item in checks),
                "candidate_lean_sources": [
                    relative for relative, _text in candidate_lean_sources
                ],
                "forbidden_matches": forbidden_matches,
                "target_shadow_matches": target_shadow_matches,
                "parameter_definitions": parameter_definitions,
                "observed_final_type": observed_final_type,
                "expected_final_type": expected_final_type,
                "copy_hashes": copy_hashes,
                "target": target,
                "used_axioms": sorted(used_axioms),
                "generated_allowlist_count": len(generated_allowlist),
                "generated_allowlist_dependencies_used": sorted(
                    used_axioms & generated_allowlist
                ),
                "trusted_gate_core_axioms_used": sorted(
                    used_axioms & trusted_gate_core_axioms
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
