import json
import re
from pathlib import Path

from tools import klean_final_gate
from tools.klean_export import target_statement, tree_digest
from tools.pipeline_contract import sha256_tree


candidate = Path("/candidate")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
fresh = Path("/tmp/audit-work/stage5-proof-audit.0I7s5N")
manifest = json.loads((generation / "generator-manifest.json").read_text())
inventory = json.loads((generation / "trust-inventory.json").read_text())
audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
proof = (candidate / "Proof.lean").read_text()

print("CANDIDATE IMMUTABILITY AND STATIC GATE")
print("candidate_pipeline_tree_sha256", sha256_tree(candidate))
print("audit_input_candidate_sha256", audit["hashes"]["lean_workspace_sha256"])
print("candidate_hash_match", sha256_tree(candidate) == audit["hashes"]["lean_workspace_sha256"])
print("candidate_klean_tree_sha256", tree_digest(candidate))
klean_final_gate._candidate_gate(candidate, manifest["target"])
print("trusted_candidate_gate", "PASS")
forbidden = []
for path in candidate.rglob("*.lean"):
    text = path.read_text()
    for match in re.finditer(r"\b(?:sorry|admit|unsafe|axiom|opaque)\b", text):
        forbidden.append((path.relative_to(candidate).as_posix(), match.group(0), match.start()))
print("forbidden_Lean_tokens", forbidden)
print("candidate_targetStatement_definition_count", len(re.findall(r"(?m)^\s*def\s+targetStatement\b", proof)))
print("candidate_targetStatement_reference_count", proof.count("Klean129Minpath.Lemmas.targetStatement"))
print("candidate_final_theorem_count", len(re.findall(r"(?m)^\s*theorem\s+final\b", proof)))

matches = re.findall(r"(?ms)^\s*theorem\s+final\s*:\s*(.*?)\s*:=\s*by\b", proof)
candidate_statement = " ".join(matches[0].split())
fixed_statement = " ".join(manifest["target"]["statement"].split())
print("candidate_final_statement", candidate_statement)
print("fixed_generated_statement", fixed_statement)
print("candidate_final_exactly_fixed_target", candidate_statement == fixed_statement)

print("\nGENERATED BASE AND TARGET IDENTITY")
reference_target = target_statement(generated)
fresh_target = target_statement(fresh / "Base")
print("reference_target", json.dumps(reference_target, sort_keys=True))
print("fresh_Base_target", json.dumps(fresh_target, sort_keys=True))
print("target_equals_manifest", reference_target == manifest["target"])
print("fresh_Base_target_equals_reference", fresh_target == reference_target)
reference_sources = {
    p.relative_to(generated).as_posix(): p.read_bytes()
    for p in generated.rglob("*")
    if p.is_file() and ".lake" not in p.relative_to(generated).parts
}
fresh_sources = {
    p.relative_to(fresh / "Base").as_posix(): p.read_bytes()
    for p in (fresh / "Base").rglob("*")
    if p.is_file() and ".lake" not in p.relative_to(fresh / "Base").parts
}
print("fresh_Base_nonbuild_files_equal_generated", fresh_sources == reference_sources)

print("\nEXACT PARAMETER DECLARATIONS")
for parameter in manifest["target"]["parameters"]:
    name = parameter["name"]
    occurrences = list(re.finditer(
        rf"(?m)^\s*(?:noncomputable\s+)?def\s+{re.escape(name)}\s*(?::|\()",
        proof,
    ))
    line = proof.count("\n", 0, occurrences[0].start()) + 1
    print(json.dumps({
        "name": name,
        "kore_symbol": parameter["kore_symbol"],
        "source_rule_ids": parameter["source_rule_ids"],
        "count": len(occurrences),
        "line": line,
    }, sort_keys=True))

print("\nAXIOM ACCOUNTING")
used = {"propext", "Classical.choice", "Quot.sound"}
allowlisted_generated = set(inventory["axioms"])
kernel_allowed = {"Classical.choice", "propext", "Quot.sound"}
allowed = klean_final_gate._allowed_axioms(inventory)
print("print_axioms_used", sorted(used))
print("standard_Lean_kernel_axioms_allowed_by_trusted_gate", sorted(kernel_allowed))
print("recorded_generated_axiom_count", len(allowlisted_generated))
print("used_recorded_generated_axioms", sorted(used & allowlisted_generated))
print("unexpected_axioms", sorted(used - allowed))
print("sorryAx_used", "sorryAx" in used)
print("axiom_accounting_result", "PASS" if not (used - allowed) and "sorryAx" not in used else "FAIL")
