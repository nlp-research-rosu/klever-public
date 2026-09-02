#!/usr/bin/env python3
"""Independent Stage 4 bijection/target checks and candidate static checks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from tools.klean_export import (
    expected_target_definition,
    sha256_text,
    target_statement,
)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


generation = Path("/reference/klean-generation")
generated = generation / "generated"
base = Path("/tmp/audit-work/proof-audit.2wTFR1/Base")
candidate = Path("/candidate")
audit = load(Path("/audit-input.json"))["resolution"]
generator = load(generation / "generator-manifest.json")
input_manifest = load(generation / "input-manifest.json")
obligation_map = load(generated / "obligation-map.json")

# This domain set is the result of the independent source/semantics
# classification, not copied from the discovery manifest.
independent_domain_ids = [
    "rule-fc66c723d628ad8e811c12c35a08f3b4345486c0dfef2593966c9dbe4c211ecf"
]
obligations = obligation_map["obligations"]
obligation_ids = [entry["source_rule_id"] for entry in obligations]

binding_checks = []
for parameter in obligation_map["trust_parameters"]:
    binding = {
        "kore_symbol": parameter["kore_symbol"],
        "name": parameter["name"],
        "type": parameter["type"],
        "source_rule_ids": parameter["source_rule_ids"],
    }
    observed = sha256_text(
        json.dumps(binding, sort_keys=True, separators=(",", ":"))
    )
    binding_checks.append(
        {
            "name": parameter["name"],
            "recorded": parameter["binding_sha256"],
            "recomputed": observed,
            "match": observed == parameter["binding_sha256"],
            "source_rule_ids": parameter["source_rule_ids"],
        }
    )

conjunct_checks = [
    {
        "source_rule_id": entry["source_rule_id"],
        "recorded": entry["lean_conjunct_sha256"],
        "recomputed": sha256_text(entry["lean_conjunct"]),
        "match": entry["lean_conjunct_sha256"]
        == sha256_text(entry["lean_conjunct"]),
    }
    for entry in obligations
]

expected_definition = expected_target_definition(obligation_map)
expected_definition_hash = (
    None if expected_definition is None else sha256_text(expected_definition)
)
generated_target = target_statement(generated)
base_target = target_statement(base)

reference_file_hashes = {
    path.relative_to(generated).as_posix(): sha(path)
    for path in sorted(generated.rglob("*"))
    if path.is_file() and not path.is_symlink()
}
base_source_hashes = {
    name: sha(base / name)
    for name in reference_file_hashes
    if (base / name).is_file() and not (base / name).is_symlink()
}

candidate_lean = sorted(candidate.rglob("*.lean"))
forbidden_patterns = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "unsafe": r"\bunsafe\b",
    "axiom": r"(?m)^\s*axiom\b",
    "opaque": r"(?m)^\s*opaque\b",
}
forbidden_hits = {
    token: [
        {
            "file": path.relative_to(candidate).as_posix(),
            "line": text.count("\n", 0, match.start()) + 1,
        }
        for path in candidate_lean
        for text in [path.read_text()]
        for match in re.finditer(pattern, text)
    ]
    for token, pattern in forbidden_patterns.items()
}
target_declaration_hits = [
    {
        "file": path.relative_to(candidate).as_posix(),
        "line": text.count("\n", 0, match.start()) + 1,
        "text": match.group(0),
    }
    for path in candidate_lean
    for text in [path.read_text()]
    for match in re.finditer(
        r"(?m)^\s*(?:def|theorem|lemma|axiom|opaque)\s+targetStatement\b",
        text,
    )
]

result = {
    "independent_domain_ids": independent_domain_ids,
    "obligation_ids": obligation_ids,
    "obligation_bijection": (
        obligation_ids == independent_domain_ids
        and len(set(obligation_ids)) == len(obligation_ids)
        and obligation_map["source_rules"] == input_manifest["source_rules"]
    ),
    "obligation_map_sha256": {
        "observed": sha(generated / "obligation-map.json"),
        "recorded": generator["obligation_map_sha256"],
        "match": sha(generated / "obligation-map.json")
        == generator["obligation_map_sha256"],
    },
    "conjunct_hash_checks": conjunct_checks,
    "binding_hash_checks": binding_checks,
    "expected_definition": expected_definition,
    "expected_definition_sha256": expected_definition_hash,
    "generated_target": generated_target,
    "base_target_after_clean_build": base_target,
    "target_matches_generator_manifest": generated_target
    == generator["target"],
    "target_matches_audit_input": generated_target == audit["target"],
    "base_target_matches_generated_target": base_target == generated_target,
    "target_definition_is_exact_obligation_conjunction": (
        expected_definition_hash == generated_target["definition_sha256"]
    ),
    "base_copy_source_files": {
        "reference_count": len(reference_file_hashes),
        "base_matched_count": len(base_source_hashes),
        "missing": sorted(set(reference_file_hashes) - set(base_source_hashes)),
        "mismatched": sorted(
            name
            for name in reference_file_hashes.keys() & base_source_hashes.keys()
            if reference_file_hashes[name] != base_source_hashes[name]
        ),
    },
    "candidate_lean_files": [
        path.relative_to(candidate).as_posix() for path in candidate_lean
    ],
    "candidate_forbidden_hits": forbidden_hits,
    "candidate_target_declaration_hits": target_declaration_hits,
}
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
