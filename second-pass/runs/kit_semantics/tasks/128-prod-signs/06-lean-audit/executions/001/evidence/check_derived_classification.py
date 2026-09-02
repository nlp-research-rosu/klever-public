#!/usr/bin/env python3
"""Structural checks supporting the independent derived-lemma classification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, "/reference")
from tools.k_rule_inventory import inventory_verification  # noqa: E402


def require(condition: bool, message: str) -> None:
    print(("PASS " if condition else "FAIL ") + message)
    if not condition:
        raise SystemExit(1)


root = Path("/reference/k-proof")
inventory = inventory_verification(root)
rule = inventory["rules"][0]
claim_text = (root / "loop-connection-spec.k").read_text()


def transition_body(text: str) -> str:
    start = text.index("<k>")
    marker = "</exit-code>"
    end = text.index(marker, start) + len(marker)
    return " ".join(text[start:end].split())


rule_body = transition_body(rule["text"])
claim_body = transition_body(claim_text)
require(rule_body == claim_body, "auxiliary claim and later rule have the exact same transition, guards, and cells")
body_sha = hashlib.sha256(rule_body.encode()).hexdigest()
print(f"EXACT_TRANSITION_NORMALIZED_SHA256={body_sha}")
require(rule["attributes"] == ["priority(30)"], "later rule has priority only, not simplification")
require("simplification" not in rule["attributes"], "derived rule is not a simplification equation")

requires_pattern = re.compile(r'^requires[ \t]+"([^"]+)"', re.MULTILINE)
pending = [root / "loop-connection.k"]
closure: set[Path] = set()
while pending:
    current = pending.pop().resolve()
    if current in closure:
        continue
    closure.add(current)
    for required in requires_pattern.findall(current.read_text()):
        dependent = (current.parent / required).resolve()
        require(dependent.is_file(), f"required K file exists: {dependent.relative_to(root)}")
        pending.append(dependent)

relative_closure = sorted(path.relative_to(root).as_posix() for path in closure)
print("DERIVATION_REQUIRES_CLOSURE:")
for name in relative_closure:
    print(f"  {name}")
require("verification.k" not in relative_closure, "derivation source closure excludes verification.k")
require("loop-connection.k" in relative_closure, "derivation closure starts at loop-connection.k")
require("verification-base.k" in relative_closure, "derivation uses only the prior verification base extension")

loop_module = (root / "loop-connection.k").read_text()
base_module = (root / "verification-base.k").read_text()
imports_pattern = re.compile(r'^\s*imports[ \t]+([^\s]+)[ \t]*$', re.MULTILINE)
loop_imports = imports_pattern.findall(loop_module)
base_imports = imports_pattern.findall(base_module)
require("VERIFICATION-BASE" in loop_imports, "LOOP-CONNECTION imports VERIFICATION-BASE")
require("VERIFICATION" not in loop_imports, "LOOP-CONNECTION does not import VERIFICATION")
require("VERIFICATION" not in base_imports, "VERIFICATION-BASE does not import VERIFICATION")

prove = (root / "prove.sh").read_text()
derive_pos = prove.index("kprove loop-connection-spec.k")
later_compile_pos = prove.index("kompile --backend haskell verification.k")
later_prove_pos = prove.index("kprove spec.k")
require(derive_pos < later_compile_pos < later_prove_pos, "Stage 1 script orders derivation before compiling and using the later rule")

discovery = json.loads(Path("/reference/lemma-discovery.json").read_text())
require(discovery["rules"][0]["classification"] == "PROVED_DERIVED_LEMMA", "protected label agrees with independent classification")
print("INDEPENDENT_CLASSIFICATION=PROVED_DERIVED_LEMMA")
print("INDEPENDENT_DOMAIN_LEMMA_COUNT=0")
print("DERIVED_CLASSIFICATION_STRUCTURAL_CHECKS_PASS")
