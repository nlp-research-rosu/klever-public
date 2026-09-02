import hashlib
import json
import re
from pathlib import Path

from tools import (
    klean_export,
    pipeline_contract,
    stage6_resolution_contract,
)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit_document = json.loads(Path("/audit-input.json").read_text())
resolution, resolved_digest = stage6_resolution_contract.verify_audit_input(
    audit_document
)
expected_hashes = resolution["hashes"]

observed_hashes = {
    "k_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-proof")
    ),
    "stage1_export_sha256": klean_export.tree_digest(
        Path("/reference/k-proof")
    ),
    "discovery_manifest_sha256": file_hash(
        Path("/reference/lemma-discovery.json")
    ),
    "k_audit_sha256": pipeline_contract.sha256_tree(
        Path("/reference/k-audit")
    ),
    "klean_generation_sha256": pipeline_contract.sha256_tree(
        Path("/reference/klean-generation")
    ),
    "generation_producer_sources_sha256": pipeline_contract.sha256_tree(
        Path("/reference/generation-tools")
    ),
    "generated_tree_sha256": klean_export.tree_digest(
        Path("/reference/klean-generation/generated")
    ),
    "lean_workspace_sha256": pipeline_contract.sha256_tree(
        Path("/candidate")
    ),
}

print("resolved_input_sha256", resolved_digest)
print("resolved_input_matches", resolved_digest == audit_document["resolved_input_sha256"])
for name, observed in observed_hashes.items():
    print(name, observed, "MATCH", observed == expected_hashes[name])

stage1_hashes = {
    path.relative_to("/reference/k-proof").as_posix(): file_hash(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "Stage 1 source workspace"
    )
}
expected_stage1_hashes = resolution["stage1_source_hashes"]
print("stage1_source_file_count", len(stage1_hashes))
print(
    "stage1_source_hashes_exact",
    stage1_hashes == expected_stage1_hashes,
)
print(
    "stage1_source_missing",
    sorted(set(expected_stage1_hashes) - set(stage1_hashes)),
)
print(
    "stage1_source_extra",
    sorted(set(stage1_hashes) - set(expected_stage1_hashes)),
)
print(
    "stage1_source_mismatched",
    sorted(
        name
        for name in set(stage1_hashes) & set(expected_stage1_hashes)
        if stage1_hashes[name] != expected_stage1_hashes[name]
    ),
)

generator_manifest = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
source_manifest = json.loads(
    Path("/reference/generation-tools/source-manifest.json").read_text()
)
producer_hashes = {
    "klean_export.py": file_hash(
        Path("/reference/generation-tools/klean_export.py")
    ),
    "klean.py": file_hash(Path("/reference/generation-tools/klean.py")),
}
image_id = generator_manifest["provenance"]["generator_image_id"]
audit_image_id = "sha256:" + Path(
    resolution["generation_producer_sources"]
).name
print("producer_hashes", json.dumps(producer_hashes, sort_keys=True))
print("producer_source_manifest_files_match", producer_hashes == source_manifest["files"])
print(
    "producer_generator_manifest_match",
    producer_hashes["klean_export.py"] == generator_manifest["exporter_sha256"]
    and producer_hashes["klean.py"] == generator_manifest["klean_py_sha256"],
)
print("generator_image_id", image_id)
print("source_manifest_image_match", source_manifest["generator_image_id"] == image_id)
print("audit_input_image_match", audit_image_id == image_id)

toolchain_lock = json.loads(
    Path("/reference/klean-toolchain.lock.json").read_text()
)
print("toolchain_lock_exact", generator_manifest["toolchain"] == toolchain_lock)

obligation_map_path = Path(
    "/reference/klean-generation/generated/obligation-map.json"
)
print(
    "obligation_map_hash",
    file_hash(obligation_map_path),
    "MATCH",
    file_hash(obligation_map_path) == generator_manifest["obligation_map_sha256"],
)

actual_target = klean_export.target_statement(
    Path("/reference/klean-generation/generated")
)
print("actual_target", json.dumps(actual_target, sort_keys=True))
print("target_matches_generator_manifest", actual_target == generator_manifest["target"])
print("target_matches_audit_input", actual_target == resolution["target"])

candidate_sources = []
for path in sorted(Path("/candidate").rglob("*.lean")):
    if path.is_file() and not path.is_symlink():
        candidate_sources.append(path)
candidate_text = "\n".join(path.read_text() for path in candidate_sources)
for token in ("sorry", "admit", "unsafe", "axiom", "opaque"):
    print(
        f"candidate_forbidden_{token}_count",
        len(re.findall(rf"\b{token}\b", candidate_text)),
    )
print(
    "candidate_target_definition_count",
    len(re.findall(r"(?m)^\s*def\s+targetStatement\b", candidate_text)),
)
print(
    "candidate_final_theorem_count",
    len(re.findall(r"(?m)^\s*theorem\s+final\b", candidate_text)),
)
for name in ("_orBool_", "«_==K_»", "notBool_"):
    print(
        "candidate_parameter_definition_count",
        name,
        len(
            re.findall(
                rf"(?m)^\s*(?:noncomputable\s+)?def\s+{re.escape(name)}"
                rf"\s*(?::|\()",
                candidate_text,
            )
        ),
    )
