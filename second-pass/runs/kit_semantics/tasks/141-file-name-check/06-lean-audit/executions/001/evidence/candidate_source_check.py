#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

from tools.klean_export import lean_trust_declarations


def load_producer():
    path = Path("/reference/generation-tools/klean_export.py")
    spec = importlib.util.spec_from_file_location("gen_export_for_candidate", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/lean-audit.Bncwtt")
producer = load_producer()
candidate_sources = [
    candidate / "Proof.lean",
    candidate / "lakefile.lean",
]
forbidden = {}
trust_declarations = {}
target_shadow_locations = []
for path in candidate_sources:
    text = path.read_text()
    relative = path.relative_to(candidate).as_posix()
    forbidden[relative] = re.findall(
        r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text
    )
    trust_declarations[relative] = lean_trust_declarations(path)
    if re.search(r"(?m)^\s*def\s+targetStatement\b", text):
        target_shadow_locations.append(relative)

manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
fresh_target = producer.target_statement(fresh / "Base")
checks = {
    "candidate_proof_equals_fresh_proof": (
        (candidate / "Proof.lean").read_bytes()
        == (fresh / "Proof.lean").read_bytes()
    ),
    "candidate_lakefile_equals_fresh_lakefile": (
        (candidate / "lakefile.lean").read_bytes()
        == (fresh / "lakefile.lean").read_bytes()
    ),
    "no_forbidden_tokens_outside_base": all(
        not matches for matches in forbidden.values()
    ),
    "no_new_axiom_or_opaque_declarations": all(
        not declarations for declarations in trust_declarations.values()
    ),
    "no_target_shadow": not target_shadow_locations,
    "fresh_base_target_exact": fresh_target == manifest["target"],
    "exact_gt_definition_once": len(
        re.findall(
            r"(?m)^\s*def\s+«_>Int_»\s*"
            r"\(x0 x1 : SortInt\)\s*:\s*SortBool\s*:=\s*x0\s*>\s*x1\s*$",
            (candidate / "Proof.lean").read_text(),
        )
    )
    == 1,
    "exact_le_definition_once": len(
        re.findall(
            r"(?m)^\s*def\s+«_<=Int_»\s*"
            r"\(x0 x1 : SortInt\)\s*:\s*SortBool\s*:=\s*x0\s*<=\s*x1\s*$",
            (candidate / "Proof.lean").read_text(),
        )
    )
    == 1,
}
result = {
    "proof_sha256": hashlib.sha256(
        (candidate / "Proof.lean").read_bytes()
    ).hexdigest(),
    "forbidden_tokens": forbidden,
    "trust_declarations": trust_declarations,
    "target_shadow_locations": target_shadow_locations,
    "fresh_target": fresh_target,
    "checks": checks,
    "overall": "PASS" if all(checks.values()) else "FAIL",
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if all(checks.values()) else 1)
