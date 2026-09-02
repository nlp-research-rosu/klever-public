#!/usr/bin/env bash
set -uo pipefail

PYTHONPATH=/reference python3 - <<'PY'
import hashlib
import json
from pathlib import Path

from tools import klean_export
from tools.lemma_discovery_contract import validate_trust_boundary
from tools.pipeline_contract import sha256_tree

audit = json.loads(Path("/audit-input.json").read_text())["resolution"]
generation = Path("/reference/klean-generation")
generated = generation / "generated"
generator = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
obligation_map = json.loads(
    (generated / "obligation-map.json").read_text()
)
validated = validate_trust_boundary(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
)
discovery_hash = hashlib.sha256(
    Path("/reference/lemma-discovery.json").read_bytes()
).hexdigest()
domain_rules = klean_export._domain_source_rules(
    validated, discovery_hash
)
target = klean_export.target_statement(generated)
expected_definition = klean_export.expected_target_definition(obligation_map)

tree_checks = {
    "k_workspace_pipeline_tree": (
        sha256_tree(Path("/reference/k-proof"))
        == audit["hashes"]["k_workspace_sha256"]
    ),
    "stage1_export_tree": (
        klean_export.tree_digest(Path("/reference/k-proof"))
        == audit["hashes"]["stage1_export_sha256"]
    ),
    "k_audit_pipeline_tree": (
        sha256_tree(Path("/reference/k-audit"))
        == audit["hashes"]["k_audit_sha256"]
    ),
    "generation_pipeline_tree": (
        sha256_tree(generation)
        == audit["hashes"]["klean_generation_sha256"]
    ),
    "generated_export_tree": (
        klean_export.tree_digest(generated)
        == audit["hashes"]["generated_tree_sha256"]
        == generator["generated_tree_sha256"]
    ),
    "producer_pipeline_tree": (
        sha256_tree(Path("/reference/generation-tools"))
        == audit["hashes"]["generation_producer_sources_sha256"]
    ),
    "candidate_pipeline_tree": (
        sha256_tree(Path("/candidate"))
        == audit["hashes"]["lean_workspace_sha256"]
    ),
    "discovery_file": (
        discovery_hash == audit["hashes"]["discovery_manifest_sha256"]
    ),
}

source_hash_mismatches = []
for relative, expected in audit["stage1_source_hashes"].items():
    path = Path("/reference/k-proof") / relative
    observed = (
        hashlib.sha256(path.read_bytes()).hexdigest()
        if path.is_file() and not path.is_symlink()
        else None
    )
    if observed != expected:
        source_hash_mismatches.append({
            "path": relative,
            "expected": expected,
            "observed": observed,
        })

obligations = obligation_map["obligations"]
domain_ids = [r["source_rule_id"] for r in domain_rules]
mapped_ids = [r["source_rule_id"] for r in obligation_map["source_rules"]]
obligation_ids = [o["source_rule_id"] for o in obligations]
per_obligation_hashes = all(
    o["lean_conjunct_sha256"]
    == klean_export.sha256_text(o["lean_conjunct"])
    for o in obligations
)
per_obligation_provenance = all(
    o["normalized_sha256"] == r["normalized_sha256"]
    and o["inventory_sha256"] == r["inventory_sha256"]
    and o["discovery_manifest_sha256"]
        == r["discovery_manifest_sha256"]
    and o["source_span"] == {
        "start_line": r["start_line"],
        "end_line": r["end_line"],
    }
    for o, r in zip(obligations, domain_rules, strict=True)
)

mathematical_review = {
    74: "Exact nonvacuous cast-definedness iff. The nested True is the exact "
        "translation of #Ceil(V) for an already typed V; it does not turn the "
        "top-level obligation into True.",
    82: "Exact guarded reverse cast/projection equality.",
    87: "Exact unguarded projectIntTotal idempotence equality.",
    93: "Exact guarded applyCmp(\">\", V, I) dispatch equality.",
    98: "Exact guarded applyCmp(\">=\", V, I) dispatch equality.",
    103: "Exact guarded applyCmp(\"<\", I, V) dispatch equality.",
    108: "Exact guarded applyBin(\"%\", V, I) dispatch equality.",
    113: "Exact guarded applyBin(\"+\", V, I) dispatch equality.",
    133: "Exact zero-remainder primeTail conclusion under all three guards.",
    138: "Exact backward primeTail fold under all three guards.",
    174: "Exact positive-N digitSum reverse recurrence.",
    179: "Exact positive-N normalized-remainder digitSum reverse recurrence.",
    185: "Exact positive-N accumulator-lifted digitSum equality.",
}
obligation_review = []
for obligation, source in zip(obligations, domain_rules, strict=True):
    obligation_review.append({
        "source_rule_id": source["source_rule_id"],
        "source_span": [source["start_line"], source["end_line"]],
        "judgment": mathematical_review[source["start_line"]],
        "top_level_vacuous": (
            obligation["lean_conjunct"].strip() in {"True", "(True)"}
        ),
        "has_bound_variables": "∀ " in obligation["lean_conjunct"],
    })

checks = {
    **tree_checks,
    "all_recorded_stage1_source_hashes_match": not source_hash_mismatches,
    "domain_source_rule_count_is_13": len(domain_rules) == 13,
    "ordered_source_rule_bijection": (
        domain_ids == mapped_ids == obligation_ids
        and len(domain_ids) == len(set(domain_ids))
    ),
    "per_obligation_hashes_match": per_obligation_hashes,
    "per_obligation_provenance_matches": per_obligation_provenance,
    "generator_obligation_count_matches": (
        generator["obligation_count"] == len(obligations)
    ),
    "obligation_map_hash_matches": (
        hashlib.sha256(
            (generated / "obligation-map.json").read_bytes()
        ).hexdigest() == generator["obligation_map_sha256"]
    ),
    "target_matches_generator_manifest": target == generator["target"],
    "target_matches_audit_input": target == audit["target"],
    "target_definition_is_exact_generated_conjunction": (
        target["definition_sha256"]
        == klean_export.sha256_text(expected_definition)
    ),
    "target_statement_hash_matches": (
        target["statement_sha256"]
        == klean_export.sha256_text(target["statement"])
    ),
    "no_top_level_vacuous_obligation": not any(
        row["top_level_vacuous"] for row in obligation_review
    ),
    "all_obligations_bind_variables": all(
        row["has_bound_variables"] for row in obligation_review
    ),
    "input_manifest_source_rules_match": (
        input_manifest["source_rules"] == domain_rules
    ),
}
print(json.dumps({
    "checks": checks,
    "all_checks_pass": all(checks.values()),
    "stage1_source_hash_count": len(audit["stage1_source_hashes"]),
    "stage1_source_hash_mismatches": source_hash_mismatches,
    "ordered_domain_source_rule_ids": domain_ids,
    "ordered_obligation_ids": obligation_ids,
    "obligation_mathematical_review": obligation_review,
    "target": target,
    "lean_invocation_hash_note": (
        "audit-input records lean_invocation_sha256, but the launcher does not "
        "mount that invocation among the declared audit inputs; it is therefore "
        "not independently re-hashable here."
    ),
}, indent=2, sort_keys=True))
PY
