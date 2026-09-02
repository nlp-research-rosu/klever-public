#!/usr/bin/env python3
import json
import re
from pathlib import Path

from tools.klean_export import target_statement, tree_digest
from tools.klean_final_gate import _candidate_gate


generation = Path("/reference/klean-generation")
candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/stage5-clean-project")
manifest = json.loads((generation / "generator-manifest.json").read_text())
target = manifest["target"]

# Run the trusted model-free candidate source gate.
_candidate_gate(candidate, target)

candidate_sources = [
    path
    for path in candidate.rglob("*.lean")
    if path.relative_to(candidate).parts[0] != "Base"
]
candidate_text = "\n".join(path.read_text() for path in candidate_sources)
parameter_counts = {}
for parameter in target["parameters"]:
    name = parameter["name"]
    pattern = (
        rf"(?m)^\s*(?:@\[[^\n]*\]\s*)*"
        rf"(?:noncomputable\s+)?def\s+{re.escape(name)}\s*(?::|\()"
    )
    parameter_counts[name] = len(re.findall(pattern, candidate_text))

final_match = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    (candidate / "Proof.lean").read_text(),
)
checks = {
    "trusted_candidate_gate": True,
    "fresh_base_tree_exact": (
        tree_digest(fresh / "Base")
        == tree_digest(generation / "generated")
        == manifest["generated_tree_sha256"]
    ),
    "fresh_base_target_exact": (
        target_statement(fresh / "Base") == target
    ),
    "candidate_does_not_define_targetStatement": (
        re.search(
            r"(?m)^\s*(?:def|theorem|lemma|axiom|opaque)\s+"
            r"targetStatement\b",
            candidate_text,
        )
        is None
    ),
    "each_parameter_defined_exactly_once": all(
        count == 1 for count in parameter_counts.values()
    ),
    "one_final_theorem": len(final_match) == 1,
    "final_statement_exact": (
        len(final_match) == 1
        and " ".join(final_match[0].split())
        == " ".join(target["statement"].split())
    ),
    "no_forbidden_candidate_tokens": (
        re.search(
            r"\b(?:sorry|admit|unsafe|axiom|opaque)\b",
            candidate_text,
        )
        is None
    ),
}
result = {
    "parameter_definition_counts": parameter_counts,
    "target": target,
    "checks": checks,
    "status": "PASS" if all(checks.values()) else "FAIL",
}
print(json.dumps(result, indent=2, sort_keys=True))
