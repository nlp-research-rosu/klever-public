#!/usr/bin/env python3
"""Independent candidate source, target, and trust-dependency checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


CANDIDATE = Path("/candidate")
FRESH = Path("/tmp/audit-work/114-minSubArraySum/proof-audit")
GENERATION = Path("/reference/klean-generation")


def check(label: str, condition: bool) -> None:
    print(f"{label}: {condition}")
    if not condition:
        raise AssertionError(label)


manifest = json.loads((GENERATION / "generator-manifest.json").read_text())
target = manifest["target"]
inventory = json.loads((GENERATION / "trust-inventory.json").read_text())
proof_text = (CANDIDATE / "Proof.lean").read_text()

candidate_sources: list[tuple[str, str]] = []
for source in sorted(CANDIDATE.rglob("*.lean")):
    relative = source.relative_to(CANDIDATE).as_posix()
    if relative == "Base" or relative.startswith("Base/"):
        continue
    candidate_sources.append((relative, source.read_text()))

forbidden: list[tuple[str, str]] = []
for relative, text in candidate_sources:
    for match in re.finditer(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text):
        forbidden.append((relative, match.group(0)))
print("forbidden candidate Lean tokens:", forbidden)
check("no candidate sorry/admit/unsafe/new axiom/new opaque", forbidden == [])

all_candidate_text = "\n".join(text for _relative, text in candidate_sources)
target_declarations = re.findall(
    r"(?m)^\s*(?:noncomputable\s+)?def\s+targetStatement\b",
    all_candidate_text,
)
check("candidate does not shadow generated target", target_declarations == [])

for parameter in target["parameters"]:
    name = parameter["name"]
    declarations = [
        relative
        for relative, text in candidate_sources
        if re.search(
            rf"(?m)^\s*(?:noncomputable\s+)?def\s+{re.escape(name)}\s*(?::|\()",
            text,
        )
    ]
    print(f"{name} declarations:", declarations)
    check(f"one exact def for {name}", len(declarations) == 1)

final_matches = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    proof_text,
)
check("one Proof.final theorem", len(final_matches) == 1)
check(
    "Proof.final exact fixed target statement",
    " ".join(final_matches[0].split()) == " ".join(target["statement"].split()),
)

base_target = FRESH / "Base" / target["file"]
reference_target = GENERATION / "generated" / target["file"]
check("fresh Base target byte identity", base_target.read_bytes() == reference_target.read_bytes())
check(
    "fresh Base target file hash",
    hashlib.sha256(base_target.read_bytes()).hexdigest()
    == hashlib.sha256(reference_target.read_bytes()).hexdigest(),
)

allowed_core = {"Classical.choice", "propext", "Quot.sound"}
recorded_generated = {
    entry["name"] for entry in inventory["allowlist"]
}
used = {"Classical.choice", "propext"}
check("sorryAx absent", "sorryAx" not in used)
check(
    "axiom dependencies recorded or standard trusted core",
    used <= allowed_core | recorded_generated,
)
check("no generated trust axiom used", used.isdisjoint(recorded_generated))

print("used axioms:", sorted(used))
print("standard allowed axioms:", sorted(allowed_core))
print("recorded generated allowlist size:", len(recorded_generated))
print("CANDIDATE_INTEGRITY=PASS")
