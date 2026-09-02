#!/usr/bin/env python3
"""Static candidate, target-identity, and operational-binding checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/lean-proof-audit-2")
generated = Path("/reference/klean-generation/generated")
audit = load(Path("/audit-input.json"))["resolution"]
manifest = load(Path("/reference/klean-generation/generator-manifest.json"))
inventory = load(Path("/reference/klean-generation/trust-inventory.json"))
target = target_statement(generated)
assert target is not None

assert sha256_tree(candidate) == audit["hashes"]["lean_workspace_sha256"]
assert sha(candidate / "Proof.lean") == sha(fresh / "Proof.lean")
assert sha(generated / target["file"]) == sha(fresh / "Base" / target["file"])
assert target == manifest["target"] == audit["target"]
assert tree_digest(generated) == audit["hashes"]["generated_tree_sha256"]
print("candidate, Base target, and signed target hashes: OK")

lean_sources = [candidate / "Proof.lean", candidate / "lakefile.lean"]
combined = "\n".join(path.read_text() for path in lean_sources)
for token in ("sorry", "admit", "unsafe", "axiom", "opaque"):
    assert re.search(rf"\b{token}\b", combined) is None, token
assert re.search(r"(?m)^\s*def\s+targetStatement\b", combined) is None
assert "namespace Klean118GetClosestVowel" not in combined
assert len(re.findall(r"(?m)^theorem\s+final\b", combined)) == 1
print("candidate forbidden-token/shadow scan: OK")

proof = (candidate / "Proof.lean").read_text()
match = re.search(r"(?ms)^theorem\s+final\s*:\s*(.*?)\s*:=\s*by\s*$", proof)
assert match is not None
proof_type = " ".join(match.group(1).split())
assert proof_type == target["statement"]
print("Proof.final exact fixed statement: OK")

public_defs = re.findall(r"(?m)^def\s+(«[^\n]+?»|\S+)", proof)
expected_names = [parameter["name"] for parameter in target["parameters"]]
assert public_defs == expected_names
assert len(set(public_defs)) == len(public_defs) == 8
print("exact public operational definitions: OK", public_defs)

required_fragments = {
    "_andBool_": "left && right",
    "«_>=Int_»": "decide (left ≥ right)",
    "«_<Int_»": "decide (left < right)",
    "«_<=Int_»": "decide (left ≤ right)",
    "«_+Int_»": "left + right",
    "«isLen(_)_MPY-CORE_Int_IntSeq»":
        "Int.ofNat (intSeqNatLengthOperational codes)",
    "«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»":
        "if index ≤ 0 then some result",
    "«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?»":
        "intSeqAtOperational codes index",
}
for name, fragment in required_fragments.items():
    assert fragment in proof, (name, fragment)

assert "if index = 0 then some head" in proof
assert "else if index > 0 then intSeqAtOperational rest (index - 1)" in proof
assert "code = 97 ∨ code = 101 ∨ code = 105 ∨ code = 111 ∨ code = 117 ∨" in proof
assert "code = 65 ∨ code = 69 ∨ code = 73 ∨ code = 79 ∨ code = 85" in proof
assert "closestScanNatOperational codes index result found" in proof
assert ".«iCons(_,_)_MPY-CORE_IntSeq_Int_IntSeq» current" in proof
print("operational implementation shape: OK")

source_bindings = {
    "_andBool_": "K BOOL.and; foundation.k guards 183-191",
    "«_>=Int_»": "K INT.ge; foundation.k 188-191",
    "«_<Int_»": "K INT.lt; foundation.k 183-191",
    "«_<=Int_»": "K INT.le; foundation.k 183-186",
    "«_+Int_»": "K INT.add; foundation.k 188-191",
    "«isLen(_)_MPY-CORE_Int_IntSeq»":
        "reference-semantics/semantics/core.k 227-229",
    "«closestScan(_,_,_,_)_FOUNDATION-SYNTAX_IntSeq_IntSeq_Int_IntSeq_Bool?»":
        "foundation.k 140-175",
    "«intSeqAt(_,_)_MPY-SUBSCRIPT_Int_IntSeq_Int?»":
        "reference-semantics/semantics/subscript.k 16-19",
}
for parameter in target["parameters"]:
    print(
        "BINDING",
        parameter["name"],
        parameter["kore_symbol"],
        parameter["source_rule_ids"],
        source_bindings[parameter["name"]],
    )

allowlist_names = {entry["name"] for entry in inventory["allowlist"]}
assert len(allowlist_names) == len(inventory["allowlist"]) == 41
axiom_output = Path("/audit-output/evidence/stage5_print_axioms.log").read_text()
assert "sorryAx" not in axiom_output
assert "[propext, Quot.sound]" in axiom_output
assert not any(name in axiom_output for name in allowlist_names)
print("axiom accounting: only Lean core propext and Quot.sound; no allowlisted generated axiom used")
