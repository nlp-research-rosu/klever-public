#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools import klean_export, klean_final_gate, pipeline_contract


generation = Path("/reference/klean-generation")
candidate = Path("/candidate")
fresh_base = Path("/tmp/audit-work/39-prime-fib-independent-audit/Base")
manifest = json.loads((generation / "generator-manifest.json").read_text())
audit = json.loads(Path("/audit-input.json").read_text())
target = manifest["target"]

klean_final_gate._candidate_gate(candidate, target)
text = (candidate / "Proof.lean").read_text()
forbidden = re.findall(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text)
assert forbidden == []
assert not re.search(r"(?m)^\s*(?:def|theorem)\s+targetStatement\b", text)
assert klean_export.tree_digest(fresh_base) == manifest["generated_tree_sha256"]
assert klean_export.target_statement(fresh_base) == target
assert target == audit["resolution"]["target"]

print("CANDIDATE_TREE_SHA256", pipeline_contract.sha256_tree(candidate))
print("PROOF_LEAN_SHA256", hashlib.sha256((candidate / "Proof.lean").read_bytes()).hexdigest())
print("FORBIDDEN_CANDIDATE_TOKENS", forbidden)
print("EXACT_PARAMETER_DEFINITION_GATE", "PASS")
print("EXACT_FINAL_STATEMENT_GATE", "PASS")
print("TARGET_SHADOW_DECLARATIONS", 0)
print("FRESH_BASE_TREE_SHA256", klean_export.tree_digest(fresh_base))
print("FRESH_BASE_TARGET", json.dumps(klean_export.target_statement(fresh_base), sort_keys=True))
print("CANDIDATE_STATIC_GATE", "PASS")
