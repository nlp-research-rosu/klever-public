#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path

from tools import klean_export
from tools.klean_final_gate import _allowed_axioms, _parse_axioms


generation = Path("/reference/klean-generation")
candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/concatenate-proof.Bq35lc")
manifest = json.loads((generation / "generator-manifest.json").read_text())
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
target = manifest["target"]

reference_target_file = generation / "generated" / target["file"]
fresh_target_file = fresh / "Base" / target["file"]
assert reference_target_file.read_bytes() == fresh_target_file.read_bytes()
assert klean_export.target_statement(fresh / "Base") == target == audit["target"]

candidate_sources = [
    path
    for path in candidate.rglob("*.lean")
    if "Base" not in path.relative_to(candidate).parts
]
forbidden_pattern = re.compile(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b")
forbidden_hits = {
    path.relative_to(candidate).as_posix(): forbidden_pattern.findall(path.read_text())
    for path in candidate_sources
    if forbidden_pattern.search(path.read_text())
}
assert forbidden_hits == {}

combined = "\n".join(path.read_text() for path in candidate_sources)
parameter_counts = {}
for parameter in target["parameters"]:
    pattern = re.compile(
        rf"(?m)^\s*(?:@\[[^\n]*\]\s*)*(?:noncomputable\s+)?def\s+"
        rf"{re.escape(parameter['name'])}\s*(?::|\()"
    )
    parameter_counts[parameter["name"]] = len(pattern.findall(combined))
assert set(parameter_counts.values()) == {1}

proof_text = (candidate / "Proof.lean").read_text()
theorems = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b", proof_text
)
assert len(theorems) == 1
assert " ".join(theorems[0].split()) == " ".join(target["statement"].split())

shadow_patterns = [
    r"(?m)^\s*(?:noncomputable\s+)?def\s+targetStatement\b",
    r"(?m)^\s*namespace\s+Klean28Concatenate\.Lemmas\b",
]
shadow_hits = [pattern for pattern in shadow_patterns if re.search(pattern, combined)]
assert shadow_hits == []

axiom_log = Path("/audit-output/evidence/stage5-print-axioms.log").read_text()
used_axioms = _parse_axioms(axiom_log)
trust_inventory = json.loads((generation / "trust-inventory.json").read_text())
allowed_axioms = _allowed_axioms(trust_inventory)
unexpected_axioms = sorted(used_axioms - allowed_axioms)
assert "sorryAx" not in used_axioms
assert unexpected_axioms == []

print(
    json.dumps(
        {
            "status": "PASS",
            "fresh_copy": str(fresh),
            "target_file_sha256": hashlib.sha256(
                fresh_target_file.read_bytes()
            ).hexdigest(),
            "target": target,
            "candidate_sources": [
                path.relative_to(candidate).as_posix() for path in candidate_sources
            ],
            "forbidden_hits": forbidden_hits,
            "parameter_definition_counts": parameter_counts,
            "target_shadow_hits": shadow_hits,
            "used_axioms": sorted(used_axioms),
            "unexpected_axioms": unexpected_axioms,
            "generated_allowlist_count": len(trust_inventory["allowlist"]),
            "generated_allowlist_dependencies_used": sorted(
                used_axioms
                & {entry["name"] for entry in trust_inventory["allowlist"]}
            ),
        },
        indent=2,
        sort_keys=True,
    )
)
