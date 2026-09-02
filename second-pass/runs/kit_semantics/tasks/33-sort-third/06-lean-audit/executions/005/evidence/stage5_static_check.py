#!/usr/bin/env python3
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/reference")
from tools.pipeline_contract import sha256_tree

producer_path = Path("/reference/generation-tools/klean_export.py")
spec = importlib.util.spec_from_file_location("generation_klean_export", producer_path)
producer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = producer
spec.loader.exec_module(producer)

audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
manifest = json.loads(Path("/reference/klean-generation/generator-manifest.json").read_text())
candidate = Path("/candidate")
proof = candidate / "Proof.lean"
text = proof.read_text()

observed = producer.target_statement(Path("/reference/klean-generation/generated"))
statement = observed["statement"]
definition_hash = observed["definition_sha256"]
statement_hash = hashlib.sha256(statement.encode()).hexdigest()

print("MODE", audit["mode"])
print("TARGET_DECLARATION", observed["declaration"])
print("TARGET_DEFINITION_SHA256", definition_hash)
print("TARGET_STATEMENT_SHA256", statement_hash)
print("TARGET_MATCHES_GENERATOR_MANIFEST", observed == manifest["target"])
print("TARGET_MATCHES_AUDIT_INPUT", observed == audit["target"])

candidate_digest = sha256_tree(candidate)
generated_digest = sha256_tree(Path("/reference/klean-generation"))
print("CANDIDATE_TREE_SHA256", candidate_digest)
print("CANDIDATE_TREE_MATCHES_AUDIT_INPUT", candidate_digest == audit["hashes"]["lean_workspace_sha256"])
print("GENERATED_TREE_SHA256", generated_digest)
print("GENERATED_TREE_MATCHES_AUDIT_INPUT", generated_digest == audit["hashes"]["klean_generation_sha256"])

lean_files = sorted(p for p in candidate.rglob("*.lean") if "Base" not in p.parts)
joined = "\n".join(p.read_text() for p in lean_files)
forbidden = {}
patterns = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "unsafe": r"\bunsafe\b",
    "axiom": r"(?m)^\s*axiom\b",
    "opaque": r"(?m)^\s*opaque\b",
}
for name, pattern in patterns.items():
    forbidden[name] = len(re.findall(pattern, joined))
print("CANDIDATE_LEAN_FILES", [str(p.relative_to(candidate)) for p in lean_files])
print("FORBIDDEN_COUNTS", forbidden)
print("TARGET_DEFINITION_SHADOW_COUNT", len(re.findall(r"(?m)^\s*(?:def|theorem|axiom|opaque)\s+targetStatement\b", joined)))
print("TARGET_NAMESPACE_REOPEN_COUNT", len(re.findall(r"(?m)^\s*namespace\s+Klean33SortThird\.Lemmas\b", joined)))

params = [p["name"] for p in manifest["target"]["parameters"]]
param_counts = []
for name in params:
    count = len(re.findall(rf"(?m)^\s*def\s+{re.escape(name)}(?=\s|:)", text))
    param_counts.append(count)
    print("PARAMETER_DEF_COUNT", name, count)

final_match = re.search(
    r"theorem\s+final\s*:\s*(.*?)\s*:=",
    text,
    re.S,
)
normalize = lambda value: " ".join(value.split())
final_exact = bool(final_match) and normalize(final_match.group(1)) == normalize(statement)
print("FINAL_EXACT_FIXED_TARGET", final_exact)
print(
    "ALL_STATIC_CHECKS_PASS",
    all(forbidden[x] == 0 for x in forbidden)
    and all(count == 1 for count in param_counts)
    and final_exact,
)
