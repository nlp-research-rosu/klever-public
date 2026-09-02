#!/usr/bin/env python3
"""Static target, candidate trust, and #print-axioms reconciliation."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools import klean_export, pipeline_contract
from tools.klean_final_gate import _allowed_axioms, _parse_axioms


def check(name: str, condition: bool, details: object = None) -> None:
    record = {"check": name, "pass": bool(condition)}
    if details is not None:
        record["details"] = details
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    if not condition:
        raise SystemExit(1)


def mask_lean_noncode(text: str) -> str:
    output = list(text)
    index = 0
    block_depth = 0
    state = "code"
    while index < len(text):
        character = text[index]
        following = text[index + 1] if index + 1 < len(text) else ""
        if state == "line-comment":
            if character in "\r\n":
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "string":
            if character == "\\" and following:
                output[index] = output[index + 1] = " "
                index += 2
                continue
            if character == '"':
                state = "code"
            else:
                output[index] = " "
            index += 1
            continue
        if state == "block-comment":
            if character == "/" and following == "-":
                output[index] = output[index + 1] = " "
                block_depth += 1
                index += 2
                continue
            if character == "-" and following == "/":
                output[index] = output[index + 1] = " "
                block_depth -= 1
                index += 2
                if block_depth == 0:
                    state = "code"
                continue
            if character not in "\r\n":
                output[index] = " "
            index += 1
            continue
        if character == "-" and following == "-":
            output[index] = output[index + 1] = " "
            state = "line-comment"
            index += 2
            continue
        if character == "/" and following == "-":
            output[index] = output[index + 1] = " "
            state = "block-comment"
            block_depth = 1
            index += 2
            continue
        if character == '"':
            state = "string"
        index += 1
    return "".join(output)


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/stage5-audit.GWhMbC")
generation = Path("/reference/klean-generation")
manifest = json.loads((generation / "generator-manifest.json").read_text())
inventory = json.loads((generation / "trust-inventory.json").read_text())
target = manifest["target"]

check(
    "candidate mounted tree hash remains audit-bound",
    pipeline_contract.sha256_tree(candidate)
    == "1b1408a417df05d8147df5ece88b299205f0f6cebddb88e5d1c603505d3ef704",
)
check(
    "fresh Base remains exact generated project after build",
    klean_export.tree_digest(fresh / "Base") == manifest["generated_tree_sha256"],
    klean_export.tree_digest(fresh / "Base"),
)
observed_target = klean_export.target_statement(fresh / "Base")
check("fresh Base target identity", observed_target == target, observed_target)

candidate_lean_files = sorted(candidate.rglob("*.lean"))
check(
    "candidate has no target-module shadow file",
    all(path.relative_to(candidate).as_posix() != target["file"] for path in candidate_lean_files),
    [path.relative_to(candidate).as_posix() for path in candidate_lean_files],
)

all_candidate_text = "\n".join(path.read_text() for path in candidate_lean_files)
masked_candidate_text = mask_lean_noncode(all_candidate_text)
for token in ("sorry", "admit", "unsafe"):
    check(
        f"candidate code has no {token}",
        re.search(rf"\b{token}\b", masked_candidate_text) is None,
    )
trust_declarations = [
    {"file": path.relative_to(candidate).as_posix(), **declaration}
    for path in candidate_lean_files
    for declaration in klean_export.lean_trust_declarations(path)
]
check("candidate introduces no axiom or opaque declaration", not trust_declarations, trust_declarations)

proof_text = (candidate / "Proof.lean").read_text()
parameter_counts = {}
for parameter in target["parameters"]:
    name = parameter["name"]
    matches = re.findall(
        rf"(?m)^\s*(?:noncomputable\s+)?def\s+{re.escape(name)}\s*(?::|\()",
        proof_text,
    )
    parameter_counts[name] = len(matches)
check(
    "candidate defines each exact target parameter once",
    all(count == 1 for count in parameter_counts.values()),
    parameter_counts,
)
theorem_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b", proof_text
)
check(
    "Proof.final states the fixed target exactly",
    len(theorem_matches) == 1
    and " ".join(theorem_matches[0].split()) == " ".join(target["statement"].split()),
    theorem_matches,
)

axiom_output = (Path("/audit-output/evidence/08-print-axioms.txt")).read_text()
used_axioms = _parse_axioms(axiom_output)
allowed_axioms = _allowed_axioms(inventory)
check("Proof.final does not use sorryAx", "sorryAx" not in used_axioms, sorted(used_axioms))
check(
    "all Proof.final axioms are recorded or Lean foundational axioms",
    used_axioms <= allowed_axioms,
    {
        "used": sorted(used_axioms),
        "generated_inventory_dependencies": sorted(
            used_axioms & {entry["name"] for entry in inventory["allowlist"]}
        ),
        "Lean_foundational_allowlist": ["Classical.choice", "propext", "Quot.sound"],
        "unexpected": sorted(used_axioms - allowed_axioms),
    },
)

print("RESULT: STAGE5_STATIC_TARGET_TRUST_CHECKS_PASS")
