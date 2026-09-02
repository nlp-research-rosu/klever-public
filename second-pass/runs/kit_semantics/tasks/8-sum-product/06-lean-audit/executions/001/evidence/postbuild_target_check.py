#!/usr/bin/env python3
import json
import re
from pathlib import Path

from tools import klean_export


def load(path: Path) -> dict:
    return json.loads(path.read_text())


base = Path("/tmp/audit-work/stage5-fresh-002/Base")
candidate = Path("/candidate/Proof.lean").read_text()
generator = load(Path("/reference/klean-generation/generator-manifest.json"))
audit = load(Path("/audit-input.json"))["resolution"]
target = klean_export.target_statement(base)

print(json.dumps(target, indent=2, sort_keys=True))
print("TARGET_EQUALS_GENERATOR", target == generator["target"])
print("TARGET_EQUALS_AUDIT_INPUT", target == audit["target"])

final_match = re.search(
    r"(?ms)^theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    candidate,
)
if final_match is None:
    raise SystemExit("Proof.final declaration not found")
final_type = " ".join(final_match.group(1).split())
print("PROOF_FINAL_TYPE", final_type)
print("PROOF_FINAL_TYPE_EQUALS_FIXED_STATEMENT", final_type == target["statement"])

direct_sources = [
    Path("/candidate/Proof.lean"),
    Path("/candidate/lakefile.lean"),
]
declarations = [
    declaration
    for source in direct_sources
    for declaration in klean_export.lean_trust_declarations(source)
]
print("CANDIDATE_TRUST_DECLARATIONS", json.dumps(declarations, sort_keys=True))
print(
    "CANDIDATE_TARGET_DECLARATION_COUNT",
    sum(
        len(re.findall(r"(?m)^\s*def\s+targetStatement\b", source.read_text()))
        for source in direct_sources
    ),
)
