#!/usr/bin/env python3
"""Independent Stage 5 candidate/target/trust structural checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, klean_final_gate, pipeline_contract


CANDIDATE = Path("/candidate")
GENERATION = Path("/reference/klean-generation")
GENERATED = GENERATION / "generated"
FRESH = Path("/tmp/audit-work/36-fizz-buzz-proof-audit.mGE0Os")
AUDIT_INPUT = Path("/audit-input.json")
AXIOM_LOG = Path("/audit-output/evidence/55_print_axioms_proof_final_exact.txt")


def load(path: Path) -> dict:
    value = json.loads(path.read_text())
    assert isinstance(value, dict)
    return value


manifest = load(GENERATION / "generator-manifest.json")
inventory = load(GENERATION / "trust-inventory.json")
audit_input = load(AUDIT_INPUT)
target = manifest["target"]
proof_text = (CANDIDATE / "Proof.lean").read_text()
checks: list[dict] = []


def check(name: str, condition: bool, detail: object) -> None:
    checks.append({"name": name, "pass": bool(condition), "detail": detail})


entries = klean_export._tree_entries(CANDIDATE)
lean_files = [
    (relative, path)
    for relative, kind, path in entries
    if kind == "file" and path.suffix == ".lean"
]
forbidden_hits = []
for relative, path in lean_files:
    for match in re.finditer(
        r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", path.read_text()
    ):
        forbidden_hits.append(
            {"file": relative, "token": match.group(0), "offset": match.start()}
        )
check(
    "candidate Lean sources contain no forbidden trust token",
    not forbidden_hits,
    {"lean_files": [relative for relative, _path in lean_files], "hits": forbidden_hits},
)
check(
    "candidate contains no generated-target declaration or shadow",
    re.search(r"(?m)^\s*def\s+targetStatement\b", proof_text) is None
    and "namespace Klean36FizzBuzz.Lemmas" not in proof_text,
    {"candidate_target_definition_count": proof_text.count("def targetStatement")},
)

parameter = target["parameters"][0]
binding = {
    "kore_symbol": parameter["kore_symbol"],
    "name": parameter["name"],
    "type": parameter["type"],
    "source_rule_ids": parameter["source_rule_ids"],
}
binding_hash = hashlib.sha256(
    json.dumps(binding, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()
check(
    "parameter binding hash and source identity",
    binding_hash == parameter["binding_sha256"]
    and parameter["kore_symbol"] == "Lbl'UndsPlus'Int'Unds'"
    and parameter["source_rule_ids"]
    == ["rule-115fa5a89504e993fee3020685d5cff1b9330768a167593911e0fbe3523b78f7"],
    {
        "binding": binding,
        "recomputed_binding_sha256": binding_hash,
        "recorded_binding_sha256": parameter["binding_sha256"],
    },
)

definition_matches = re.findall(
    r"(?m)^\s*def\s+«_\+Int_»\s*"
    r"\(x0 x1 : SortInt\)\s*:\s*SortInt\s*:=\s*(.+?)\s*$",
    proof_text,
)
check(
    "candidate defines the exact parameter once as integer addition",
    definition_matches == ["x0 + x1"],
    {"matched_bodies": definition_matches},
)

theorem_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b", proof_text
)
check(
    "Proof.final source statement is the exact fixed target",
    len(theorem_matches) == 1
    and " ".join(theorem_matches[0].split())
    == " ".join(target["statement"].split()),
    {
        "expected": target["statement"],
        "observed": theorem_matches,
    },
)

parsed_base_target = klean_export.target_statement(FRESH / "Base")
check(
    "fresh Base remains byte-for-byte the generated project",
    klean_export.tree_digest(FRESH / "Base")
    == klean_export.tree_digest(GENERATED),
    {
        "fresh_base": klean_export.tree_digest(FRESH / "Base"),
        "reference_generated": klean_export.tree_digest(GENERATED),
    },
)
check(
    "fresh Base target identity",
    parsed_base_target
    == target
    == audit_input["resolution"]["target"],
    {
        "fresh_base_target": parsed_base_target,
        "manifest_target": target,
        "audit_input_target": audit_input["resolution"]["target"],
    },
)
check(
    "mounted candidate tree hash is launcher-bound",
    pipeline_contract.sha256_tree(CANDIDATE)
    == audit_input["resolution"]["hashes"]["lean_workspace_sha256"],
    {
        "actual": pipeline_contract.sha256_tree(CANDIDATE),
        "recorded": audit_input["resolution"]["hashes"]["lean_workspace_sha256"],
    },
)

used_axioms = klean_final_gate._parse_axioms(AXIOM_LOG.read_text())
allowed_axioms = klean_final_gate._allowed_axioms(inventory)
check(
    "axiom accounting",
    "sorryAx" not in used_axioms and used_axioms <= allowed_axioms,
    {
        "used": sorted(used_axioms),
        "allowed_foundational": ["Classical.choice", "propext", "Quot.sound"],
        "used_generated_allowlist_entries": sorted(
            used_axioms
            & {entry["name"] for entry in inventory["allowlist"]}
        ),
        "unexpected": sorted(used_axioms - allowed_axioms),
    },
)

print(
    json.dumps(
        {
            "checks": checks,
            "all_checks_pass": all(item["pass"] for item in checks),
        },
        indent=2,
        ensure_ascii=False,
    )
)
