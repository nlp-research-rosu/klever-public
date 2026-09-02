#!/usr/bin/env python3
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools import klean_export
from tools.klean_final_gate import _candidate_gate

generation = Path("/reference/klean-generation")
generated = generation / "generated"
candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/stage5-fresh")
fresh_base = fresh / "Base"
manifest = json.loads((generation / "generator-manifest.json").read_text())
target = manifest["target"]

_candidate_gate(candidate, target)

candidate_sources = [
    path
    for relative, kind, path in klean_export._tree_entries(candidate)
    if kind == "file"
    and path.suffix == ".lean"
    and Path(relative).parts[0] != "Base"
]
forbidden_matches = []
target_shadow_matches = []
for path in candidate_sources:
    text = path.read_text()
    for match in re.finditer(
        r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text
    ):
        forbidden_matches.append(
            {
                "file": path.relative_to(candidate).as_posix(),
                "token": match.group(0),
                "offset": match.start(),
            }
        )
    for match in re.finditer(
        r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+"
        r"(?:Klean15StringSequence\.Lemmas\.)?targetStatement\b",
        text,
    ):
        target_shadow_matches.append(
            {
                "file": path.relative_to(candidate).as_posix(),
                "offset": match.start(),
            }
        )

missing = []
changed = []
for relative, kind, source in klean_export._tree_entries(generated):
    destination = fresh_base / relative
    if kind == "directory":
        if not destination.is_dir() or destination.is_symlink():
            missing.append(relative)
    elif not destination.is_file() or destination.is_symlink():
        missing.append(relative)
    elif hashlib.sha256(source.read_bytes()).hexdigest() != hashlib.sha256(
        destination.read_bytes()
    ).hexdigest():
        changed.append(relative)

fresh_target = klean_export.target_statement(fresh_base)
checks = {
    "trusted_candidate_gate_passed": True,
    "no_forbidden_candidate_tokens": not forbidden_matches,
    "candidate_does_not_redeclare_target": not target_shadow_matches,
    "fresh_base_has_all_generated_entries": not missing,
    "fresh_base_generated_entries_unchanged": not changed,
    "fresh_base_target_exact": fresh_target == target,
}
print(
    json.dumps(
        {
            "candidate_sources": [
                path.relative_to(candidate).as_posix()
                for path in candidate_sources
            ],
            "forbidden_matches": forbidden_matches,
            "target_shadow_matches": target_shadow_matches,
            "fresh_base_missing": missing,
            "fresh_base_changed": changed,
            "fresh_target": fresh_target,
            "generator_target": target,
            "checks": checks,
            "all_checks_pass": all(checks.values()),
        },
        indent=2,
        sort_keys=True,
    )
)
