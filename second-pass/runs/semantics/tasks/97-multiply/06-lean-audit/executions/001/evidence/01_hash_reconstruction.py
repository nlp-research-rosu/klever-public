#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

from tools import klean_export, pipeline_contract, stage6_resolution_contract


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report(label: str, observed, expected) -> None:
    status = "MATCH" if observed == expected else "MISMATCH"
    print(f"{status} {label}")
    print(f"  observed={observed}")
    print(f"  expected={expected}")
    if observed != expected:
        raise SystemExit(1)


audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(audit)
report(
    "resolved_input_sha256",
    stage6_resolution_contract.canonical_json_sha256(resolution),
    audit["resolved_input_sha256"],
)
report("AUDIT_MODE", os.environ.get("AUDIT_MODE"), resolution["mode"])
report("problem_id", resolution["problem_id"], "97-multiply")
report("condition", resolution["condition"], "semantics")
report("semantics_mode", resolution["semantics_mode"], "SUPPLIED_SEMANTICS")

hashes = resolution["hashes"]
k_workspace = Path("/reference/k-proof")
k_audit = Path("/reference/k-audit")
discovery = Path("/reference/lemma-discovery.json")
generation = Path("/reference/klean-generation")
generated = generation / "generated"
producer = Path("/reference/generation-tools")

report(
    "k_workspace_sha256 (pipeline tree)",
    pipeline_contract.sha256_tree(k_workspace),
    hashes["k_workspace_sha256"],
)
report(
    "stage1_export_sha256 (Klean tree)",
    klean_export.tree_digest(k_workspace),
    hashes["stage1_export_sha256"],
)
report(
    "discovery_manifest_sha256",
    file_sha(discovery),
    hashes["discovery_manifest_sha256"],
)
report(
    "k_audit_sha256 (pipeline tree)",
    pipeline_contract.sha256_tree(k_audit),
    hashes["k_audit_sha256"],
)
report(
    "k_audit selection artifact_sha256",
    pipeline_contract.sha256_tree(k_audit),
    resolution["selections"]["k_audit"]["artifact_sha256"],
)
report(
    "klean_generation_sha256 (pipeline tree)",
    pipeline_contract.sha256_tree(generation),
    hashes["klean_generation_sha256"],
)
report(
    "klean generation selection artifact_sha256",
    pipeline_contract.sha256_tree(generation),
    resolution["selections"]["klean_generation"]["artifact_sha256"],
)
report(
    "generated_tree_sha256 (Klean tree)",
    klean_export.tree_digest(generated),
    hashes["generated_tree_sha256"],
)
report(
    "generation_producer_sources_sha256 (pipeline tree)",
    pipeline_contract.sha256_tree(producer),
    hashes["generation_producer_sources_sha256"],
)

observed_source_hashes = {
    path.relative_to(k_workspace).as_posix(): file_sha(path)
    for path in pipeline_contract._walk_regular_files(
        k_workspace, "mounted Stage 1 source workspace"
    )
}
report(
    "stage1_source_hashes exact key/hash map",
    observed_source_hashes,
    resolution["stage1_source_hashes"],
)
for name in sorted(observed_source_hashes):
    print(f"MATCH stage1_source_hash {name} {observed_source_hashes[name]}")

source_manifest = json.loads((producer / "source-manifest.json").read_text())
generator_manifest = json.loads((generation / "generator-manifest.json").read_text())
input_manifest = json.loads((generation / "input-manifest.json").read_text())
export_result = json.loads((generation / "export-result.json").read_text())
provenance = generator_manifest["provenance"]

report(
    "source-manifest exact keys",
    sorted(source_manifest),
    ["files", "generator_image_id", "schema_version"],
)
report(
    "source-manifest exact producer bindings",
    source_manifest["files"],
    {
        "klean_export.py": generator_manifest["exporter_sha256"],
        "klean.py": generator_manifest["klean_py_sha256"],
    },
)
report(
    "producer bundle exact file set",
    sorted(
        path.relative_to(producer).as_posix()
        for path in pipeline_contract._walk_regular_files(
            producer, "mounted Stage 4 producer source bundle"
        )
    ),
    ["klean.py", "klean_export.py", "source-manifest.json"],
)
report("source-manifest schema_version", source_manifest["schema_version"], 1)
report(
    "generator image ID source-manifest/generator-manifest",
    source_manifest["generator_image_id"],
    provenance["generator_image_id"],
)
report(
    "generator image ID audit-input path",
    Path(resolution["generation_producer_sources"]).name,
    provenance["generator_image_id"].removeprefix("sha256:"),
)
report(
    "klean_export.py source hash/source-manifest",
    file_sha(producer / "klean_export.py"),
    source_manifest["files"]["klean_export.py"],
)
report(
    "klean_export.py source hash/generator-manifest",
    file_sha(producer / "klean_export.py"),
    generator_manifest["exporter_sha256"],
)
report(
    "klean.py source hash/source-manifest",
    file_sha(producer / "klean.py"),
    source_manifest["files"]["klean.py"],
)
report(
    "klean.py source hash/generator-manifest",
    file_sha(producer / "klean.py"),
    generator_manifest["klean_py_sha256"],
)

report(
    "generator generated_tree_sha256",
    klean_export.tree_digest(generated),
    generator_manifest["generated_tree_sha256"],
)
report(
    "generator Stage 1 provenance",
    provenance["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
report(
    "generator Stage 3 provenance",
    provenance["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
report(
    "input manifest frozen_input_sha256",
    input_manifest["frozen_input_sha256"],
    hashes["stage1_export_sha256"],
)
report(
    "input manifest stage1_workspace_sha256",
    input_manifest["stage1_workspace_sha256"],
    hashes["stage1_export_sha256"],
)
report(
    "input manifest Stage 3 provenance",
    input_manifest["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
report(
    "input manifest verification_sha256",
    input_manifest["verification_sha256"],
    file_sha(k_workspace / "verification.k"),
)
report(
    "generator obligation_map_sha256",
    generator_manifest["obligation_map_sha256"],
    file_sha(generated / "obligation-map.json"),
)
report(
    "export frozen_input_sha256",
    export_result["frozen_input_sha256"],
    hashes["stage1_export_sha256"],
)
report(
    "export Stage 3 provenance",
    export_result["stage3_discovery_manifest_sha256"],
    hashes["discovery_manifest_sha256"],
)
report(
    "export generated_tree_sha256",
    export_result["generated_tree_sha256"],
    hashes["generated_tree_sha256"],
)
report(
    "export trust_inventory_sha256",
    export_result["trust_inventory_sha256"],
    file_sha(generation / "trust-inventory.json"),
)
report(
    "embedded Stage 4 preflight",
    resolution["stage4_preflight"],
    json.loads((generation / "preflight.json").read_text()),
)
for index, diagnostic in enumerate(resolution["stage4_preflight"]["diagnostics"]):
    report(
        f"recorded preflight diagnostic output_sha256 {index}",
        hashlib.sha256(diagnostic["output_tail"].encode()).hexdigest(),
        diagnostic["output_sha256"],
    )
report("audit target", resolution["target"], generator_manifest["target"])
report("classification-only lean_workspace", resolution["lean_workspace"], None)
report("classification-only lean_invocation", resolution["lean_invocation"], None)
report("classification-only Stage 5 result", resolution["stage5_result"], None)
report("classification-only candidate absence", Path("/candidate").exists(), False)
print(f"VERIFIED_RESOLVED_DIGEST={resolved_digest}")
print("ALL_RECORDED_INPUT_HASHES_AND_PRODUCER_BINDINGS_MATCH")
