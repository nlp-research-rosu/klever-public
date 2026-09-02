#!/usr/bin/env python3
"""Static identity and trust-escape checks for the mounted Stage 5 candidate."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path


CANDIDATE = Path("/candidate")
FRESH = Path("/tmp/audit-work/proof-audit-final")
GENERATED = Path("/reference/klean-generation/generated")
GEN_MANIFEST = Path("/reference/klean-generation/generator-manifest.json")
AUDIT_INPUT = Path("/audit-input.json")


def pipeline_tree_hash(root: Path) -> str:
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"unsupported entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        encoded = relative.encode()
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(kind.encode() + b"\0")
        if kind == "file":
            data = path.read_bytes()
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def klean_tree_hash(root: Path) -> str:
    entries: list[tuple[str, str, Path]] = []
    pending = [root]
    while pending:
        directory = pending.pop()
        for child in os.scandir(directory):
            path = Path(child.path)
            mode = child.stat(follow_symlinks=False).st_mode
            relative = path.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                entries.append((relative, "directory", path))
                pending.append(path)
            elif stat.S_ISREG(mode):
                entries.append((relative, "file", path))
            else:
                raise RuntimeError(f"unsupported entry: {path}")
    digest = hashlib.sha256()
    for relative, kind, path in sorted(entries):
        digest.update(relative.encode() + b"\0" + kind.encode() + b"\0")
        if kind == "file":
            digest.update(path.read_bytes())
    return digest.hexdigest()


generator = json.loads(GEN_MANIFEST.read_text())
resolution = json.loads(AUDIT_INPUT.read_text())["resolution"]
target = generator["target"]
proof_text = (CANDIDATE / "Proof.lean").read_text()
operational_text = (CANDIDATE / "Proof/Operational.lean").read_text()
candidate_lean = proof_text + "\n" + operational_text

result: dict[str, object] = {}
result["mounted_workspace_hash"] = pipeline_tree_hash(CANDIDATE)
result["mounted_workspace_hash_expected"] = resolution["hashes"]["lean_workspace_sha256"]
result["mounted_workspace_hash_ok"] = (
    result["mounted_workspace_hash"] == result["mounted_workspace_hash_expected"]
)
result["fresh_Base_hash"] = klean_tree_hash(FRESH / "Base")
result["generated_hash"] = klean_tree_hash(GENERATED)
result["fresh_Base_exact"] = result["fresh_Base_hash"] == result["generated_hash"]

# Strip comments before token-level trust checks so evidence prose cannot cause
# a false positive. The raw rg scan is recorded separately as well.
without_block_comments = re.sub(r"/-.*?-/", "", candidate_lean, flags=re.DOTALL)
without_comments = re.sub(r"--[^\n]*", "", without_block_comments)
forbidden = re.findall(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", without_comments)
result["forbidden_tokens"] = forbidden
result["forbidden_tokens_absent"] = not forbidden
result["candidate_target_declaration_count"] = len(
    re.findall(r"\bdef\s+targetStatement\b", without_comments)
)
result["candidate_does_not_shadow_target"] = (
    result["candidate_target_declaration_count"] == 0
    and "namespace Klean94Skjkasdkd.Lemmas" not in without_comments
)

final_matches = re.findall(
    r"\btheorem\s+final\s*:\s*(.*?)\s*:=\s*by", proof_text, flags=re.DOTALL
)
result["final_declaration_count"] = len(final_matches)
actual_final_statement = (
    " ".join(final_matches[0].split()) if len(final_matches) == 1 else None
)
expected_statement = " ".join(target["statement"].split())
result["final_statement"] = actual_final_statement
result["fixed_statement"] = expected_statement
result["final_is_exact_fixed_statement"] = actual_final_statement == expected_statement

parameter_definition_checks = []
for parameter in target["parameters"]:
    name = parameter["name"]
    marker = f"def {name}"
    parameter_definition_checks.append(
        {
            "name": name,
            "kore_symbol": parameter["kore_symbol"],
            "source_rule_ids": parameter["source_rule_ids"],
            "definition_count": proof_text.count(marker),
            "exactly_one_definition": proof_text.count(marker) == 1,
        }
    )
result["parameter_definition_checks"] = parameter_definition_checks
result["all_parameters_have_one_candidate_definition"] = all(
    item["exactly_one_definition"] for item in parameter_definition_checks
)

target_file = GENERATED / target["file"]
lemma_text = target_file.read_text()
start = lemma_text.index("def targetStatement")
end = lemma_text.index("\n\nend ", start)
definition = lemma_text[start:end].strip()
result["generated_target_definition_sha256"] = hashlib.sha256(definition.encode()).hexdigest()
result["generated_target_definition_hash_expected"] = target["definition_sha256"]
result["generated_target_definition_hash_ok"] = (
    result["generated_target_definition_sha256"] == target["definition_sha256"]
)
result["target_manifest_equals_audit_input"] = target == resolution["target"]

boolean_keys = [
    "mounted_workspace_hash_ok",
    "fresh_Base_exact",
    "forbidden_tokens_absent",
    "candidate_does_not_shadow_target",
    "final_is_exact_fixed_statement",
    "all_parameters_have_one_candidate_definition",
    "generated_target_definition_hash_ok",
    "target_manifest_equals_audit_input",
]
result["all_checks_ok"] = all(bool(result[key]) for key in boolean_keys)
print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
if not result["all_checks_ok"]:
    raise SystemExit(1)
