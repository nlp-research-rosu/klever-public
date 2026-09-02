#!/usr/bin/env python3
"""Independent candidate token, shadowing, binding, and theorem-shape audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools import klean_export


candidate = Path("/candidate")
fresh = Path("/tmp/audit-work/63-fibfib-proof.zz70ap")
generated = Path("/reference/klean-generation/generated")
target = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)["target"]

candidate_sources: dict[str, str] = {}
for path in sorted(candidate.rglob("*.lean")):
    relative = path.relative_to(candidate).as_posix()
    if relative.startswith("Base/"):
        continue
    candidate_sources[relative] = path.read_text()

combined = "\n".join(candidate_sources.values())
forbidden = [
    {
        "file": relative,
        "token": match.group(0),
        "offset": match.start(),
    }
    for relative, text in candidate_sources.items()
    for match in re.finditer(
        r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text
    )
]
shadow_declarations = [
    {
        "file": relative,
        "offset": match.start(),
    }
    for relative, text in candidate_sources.items()
    for match in re.finditer(
        r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b",
        text,
    )
]

binding_counts: dict[str, int] = {}
for parameter in target["parameters"]:
    name = parameter["name"]
    binding_counts[name] = sum(
        len(
            re.findall(
                rf"(?m)^\s*(?:noncomputable\s+)?def\s+"
                rf"{re.escape(name)}\s*(?::|\()",
                text,
            )
        )
        for text in candidate_sources.values()
    )

proof_text = candidate_sources["Proof.lean"]
theorem_types = re.findall(
    r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b",
    proof_text,
)
normalized_theorem_types = [
    " ".join(theorem_type.split()) for theorem_type in theorem_types
]
normalized_target_statement = " ".join(target["statement"].split())

fresh_target = fresh / "Base" / target["file"]
reference_target = generated / target["file"]
fresh_target_definition = klean_export.target_statement(fresh / "Base")

checks = {
    "candidate_has_no_forbidden_tokens": not forbidden,
    "candidate_has_no_target_shadow": not shadow_declarations,
    "each_target_parameter_defined_once": all(
        count == 1 for count in binding_counts.values()
    ),
    "exactly_one_final_theorem": len(theorem_types) == 1,
    "final_theorem_has_exact_fixed_type": (
        normalized_theorem_types == [normalized_target_statement]
    ),
    "fresh_base_target_byte_exact": (
        fresh_target.read_bytes() == reference_target.read_bytes()
    ),
    "fresh_base_target_manifest_exact": (
        fresh_target_definition == target
    ),
    "candidate_lakefile_requires_only_fresh_base": (
        candidate.joinpath("lakefile.lean").read_text()
        == (
            "import Lake\n"
            "open Lake DSL\n"
            "package \"proof\"\n"
            "require «klean-63-fibfib» from \"./Base\"\n"
            "@[default_target]\n"
            "lean_lib Proof\n"
        )
    ),
    "copied_candidate_sources_byte_exact": all(
        fresh.joinpath(relative).read_bytes()
        == candidate.joinpath(relative).read_bytes()
        for relative in candidate_sources
    ),
    "fresh_target_file_sha256": (
        hashlib.sha256(fresh_target.read_bytes()).hexdigest()
        == hashlib.sha256(reference_target.read_bytes()).hexdigest()
    ),
}
checks["all_checks_pass"] = all(checks.values())
result = {
    "checks": checks,
    "candidate_sources": sorted(candidate_sources),
    "forbidden": forbidden,
    "shadow_declarations": shadow_declarations,
    "binding_counts": binding_counts,
    "normalized_final_type": normalized_theorem_types,
    "normalized_target_statement": normalized_target_statement,
    "fresh_target_source_sha256": hashlib.sha256(
        fresh_target.read_bytes()
    ).hexdigest(),
}
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
raise SystemExit(0 if checks["all_checks_pass"] else 1)
