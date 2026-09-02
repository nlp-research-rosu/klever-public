import json
from pathlib import Path

from tools import klean_audit_contract
from tools import klean_export
from tools import pipeline_contract
from tools import stage6_resolution_contract


audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(audit)
recorded = resolution["hashes"]

observed = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(Path("/reference/k-proof")),
    "stage1_export_sha256": klean_export.tree_digest(Path("/reference/k-proof")),
    "discovery_manifest_sha256": pipeline_contract.sha256_file(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(Path("/reference/k-audit")),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(Path("/candidate")),
}

print("audit-input envelope: PASS")
print(f"resolved_input_sha256 recorded={audit['resolved_input_sha256']}")
print(f"resolved_input_sha256 observed={resolved_digest}")
for key in sorted(observed):
    print(
        f"{key}: recorded={recorded.get(key)} observed={observed[key]} "
        f"match={recorded.get(key) == observed[key]}"
    )

source_recorded = resolution["stage1_source_hashes"]
source_observed = klean_audit_contract._stage1_source_hashes(
    Path("/reference/k-proof")
)
missing = sorted(set(source_recorded) - set(source_observed))
extra = sorted(set(source_observed) - set(source_recorded))
changed = sorted(
    name
    for name in set(source_recorded) & set(source_observed)
    if source_recorded[name] != source_observed[name]
)
print(f"stage1_source_hashes recorded_count={len(source_recorded)}")
print(f"stage1_source_hashes observed_count={len(source_observed)}")
print(f"stage1_source_hashes missing={missing}")
print(f"stage1_source_hashes extra={extra}")
print(f"stage1_source_hashes changed={changed}")

unmounted = {
    "lean_invocation_sha256": recorded.get("lean_invocation_sha256"),
}
print(f"recorded hashes whose originating artifact is not mounted: {unmounted}")
