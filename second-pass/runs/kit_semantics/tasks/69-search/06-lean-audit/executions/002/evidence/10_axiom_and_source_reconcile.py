#!/usr/bin/env python3
"""Reconcile Proof.final axioms and reject candidate-local trust escapes."""

from __future__ import annotations

import json
import re
from pathlib import Path

from tools import klean_export, klean_final_gate


candidate = Path("/candidate")
inventory = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)
axiom_output = Path("/audit-output/evidence/05_print_axioms.log").read_text()
used = klean_final_gate._parse_axioms(axiom_output)
allowed = klean_final_gate._allowed_axioms(inventory)
generated_allowlist = {entry["name"] for entry in inventory["allowlist"]}

print("USED_AXIOMS=", sorted(used))
print("LEAN_CORE_ALLOWED=", sorted({"Classical.choice", "propext", "Quot.sound"}))
print("USED_GENERATED_ALLOWLIST_AXIOMS=", sorted(used & generated_allowlist))
print("UNEXPECTED_AXIOMS=", sorted(used - allowed))
print("SORRY_AX_PRESENT=", "sorryAx" in used)
assert "sorryAx" not in used
assert not (used - allowed)

candidate_trust = []
for relative, kind, path in klean_export._tree_entries(candidate):
    if kind != "file" or path.suffix != ".lean":
        continue
    if Path(relative).parts[0] == "Base":
        continue
    text = path.read_text()
    for declaration in klean_export.lean_trust_declarations(path):
        candidate_trust.append((relative, declaration))
    forbidden = re.findall(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text)
    if forbidden:
        raise AssertionError((relative, forbidden))

print("CANDIDATE_NEW_AXIOM_OR_OPAQUE_DECLARATIONS=", candidate_trust)
print("CANDIDATE_FORBIDDEN_TOKENS=[]")
assert not candidate_trust

candidate_text = "\n".join(
    path.read_text()
    for relative, kind, path in klean_export._tree_entries(candidate)
    if kind == "file"
    and path.suffix == ".lean"
    and Path(relative).parts[0] != "Base"
)
shadow_patterns = [
    r"\bdef\s+Klean69Search\.Lemmas\.targetStatement\b",
    r"\bnamespace\s+Klean69Search\.Lemmas\b",
    r"\bdef\s+targetStatement\b",
]
shadow_hits = [pattern for pattern in shadow_patterns if re.search(pattern, candidate_text)]
print("TARGET_SHADOW_PATTERNS_FOUND=", shadow_hits)
assert not shadow_hits
print("AXIOM_AND_SOURCE_RECONCILIATION=PASS")
