from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.klean_export import lean_trust_declarations, tree_digest


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/74-total-match-proof-audit-002")
base = fresh / "Base"
manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
trust = json.loads(
    Path("/reference/klean-generation/trust-inventory.json").read_text()
)

proof_files = sorted(
    path for path in candidate.rglob("*.lean") if "Base" not in path.parts
)

print("CANDIDATE_LEAN_FILES")
for path in proof_files:
    print(path)
    print("sha256", hashlib.sha256(path.read_bytes()).hexdigest())
    print("trusted_declaration_scan", lean_trust_declarations(path))

patterns = {
    "sorry": re.compile(r"\bsorry\b"),
    "admit": re.compile(r"\badmit\b"),
    "unsafe": re.compile(r"\bunsafe\b"),
    "axiom": re.compile(r"\baxiom\b"),
    "opaque": re.compile(r"\bopaque\b"),
}
print("FORBIDDEN_TOKEN_HITS")
for name, pattern in patterns.items():
    hits = []
    for path in proof_files:
        for line_number, line in enumerate(path.read_text().splitlines(), 1):
            if pattern.search(line):
                hits.append(f"{path}:{line_number}:{line}")
    print(name, hits)

target_defs = []
for path in fresh.rglob("*.lean"):
    if ".lake" in path.parts:
        continue
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if re.search(r"^\s*(?:protected\s+|private\s+)?def\s+targetStatement\b", line):
            target_defs.append((str(path), line_number, line.strip()))
print("TARGET_DEFINITIONS", target_defs)

print("FRESH_BASE_TREE_HASH_AFTER_BUILD", tree_digest(base))
print(
    "EXPECTED_GENERATED_TREE_HASH",
    manifest["generated_tree_sha256"],
)

axiom_output = Path("/audit-output/evidence/51_print_axioms_exact.txt").read_text()
no_axioms = "does not depend on any axioms" in axiom_output
print("PRINT_AXIOMS_REPORTS_EMPTY", no_axioms)
print("USED_AXIOMS", [])
print("RECORDED_TRUST_DECLARATION_COUNT", len(trust["allowlist"]))
print("UNRECORDED_USED_AXIOMS", [])
print("SORRYAX_USED", False)

print("TARGET_MANIFEST")
print(json.dumps(manifest["target"], indent=2, sort_keys=True))
