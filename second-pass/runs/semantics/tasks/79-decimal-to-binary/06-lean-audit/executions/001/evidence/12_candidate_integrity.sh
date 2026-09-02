#!/usr/bin/env bash
set -euo pipefail

echo '$ sha256sum /candidate/Proof.lean /tmp/audit-work/stage5-fresh/Proof.lean /candidate/lakefile.lean /tmp/audit-work/stage5-fresh/lakefile.lean /candidate/lean-toolchain /tmp/audit-work/stage5-fresh/lean-toolchain'
sha256sum \
  /candidate/Proof.lean \
  /tmp/audit-work/stage5-fresh/Proof.lean \
  /candidate/lakefile.lean \
  /tmp/audit-work/stage5-fresh/lakefile.lean \
  /candidate/lean-toolchain \
  /tmp/audit-work/stage5-fresh/lean-toolchain

echo '$ PYTHONPATH=/reference python3 - <<PY  # candidate hygiene, target non-shadowing, trust reconciliation'
PYTHONPATH=/reference python3 - <<'PY'
import json
import re
from pathlib import Path
from tools.klean_export import (
    lean_trust_declarations,
    target_statement,
    tree_digest,
)

candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/stage5-fresh")
generation = Path("/reference/klean-generation")
manifest = json.loads((generation / "generator-manifest.json").read_text())
inventory = json.loads((generation / "trust-inventory.json").read_text())

for name in ("Proof.lean", "lakefile.lean", "lean-toolchain"):
    assert (candidate / name).read_bytes() == (fresh / name).read_bytes()

actual_base_hash = tree_digest(fresh / "Base")
expected_base_hash = manifest["generated_tree_sha256"]
print("fresh Base tree hash: expected=", expected_base_hash,
      "observed=", actual_base_hash, "match=", expected_base_hash == actual_base_hash)
assert actual_base_hash == expected_base_hash

target = target_statement(fresh / "Base")
print("fresh Base target =", json.dumps(target, sort_keys=True))
assert target == manifest["target"]

candidate_sources = sorted(candidate.glob("*.lean"))
trust = [
    declaration
    for source in candidate_sources
    for declaration in lean_trust_declarations(source)
]
print("candidate axiom/opaque declarations =", json.dumps(trust, sort_keys=True))
assert trust == []

forbidden = {}
for source in candidate_sources:
    text = source.read_text()
    found = sorted(set(re.findall(
        r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text
    )))
    if found:
        forbidden[source.name] = found
print("candidate forbidden tokens =", json.dumps(forbidden, sort_keys=True))
assert forbidden == {}

proof_text = (candidate / "Proof.lean").read_text()
target_definitions = re.findall(r"(?m)^\s*def\s+targetStatement\b", proof_text)
target_namespaces = re.findall(
    r"(?m)^\s*namespace\s+Klean79DecimalToBinary\.Lemmas\b", proof_text
)
print("candidate targetStatement definitions =", len(target_definitions))
print("candidate target namespace openings =", len(target_namespaces))
assert target_definitions == []
assert target_namespaces == []
assert len(re.findall(r"(?m)^\s*theorem\s+final\s*:", proof_text)) == 1
assert proof_text.count(
    "def «doSlice(_,_,_,_)_MPY-SUBSCRIPT_Val_Val_OptInt_OptInt_OptInt»"
) == 1

print("generated trust allowlist count =", len(inventory["allowlist"]))
print("generated declared axiom count =", len(inventory["axioms"]))
assert len(inventory["allowlist"]) == 47
assert len(inventory["axioms"]) == 47
print("Proof.final used axioms = []  # exact Lean output in 08_axiom_audit.log")
print("sorryAx present = False")
print("CANDIDATE_INTEGRITY_CHECK = PASS")
PY

echo '$ rg -n targetStatement /candidate/Proof.lean'
rg -n 'targetStatement' /candidate/Proof.lean

echo '$ rg -n "\\b(sorry|admit|unsafe|axiom|opaque)\\b" /candidate --glob "*.lean" || true'
rg -n '\b(sorry|admit|unsafe|axiom|opaque)\b' /candidate --glob '*.lean' || true
