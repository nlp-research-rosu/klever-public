from pathlib import Path
import hashlib
import json
import os

from tools import klean_export, pipeline_contract, stage6_resolution_contract

audit_path = Path("/audit-input.json")
audit = json.loads(audit_path.read_text())
resolution, canonical_hash = stage6_resolution_contract.verify_audit_input(audit)
recorded = resolution["hashes"]
paths = {
    "k_workspace_sha256": Path("/reference/k-proof"),
    "k_audit_sha256": Path("/reference/k-audit"),
    "klean_generation_sha256": Path("/reference/klean-generation"),
    "generation_producer_sources_sha256": Path("/reference/generation-tools"),
}
observed = {key: pipeline_contract.sha256_tree(path) for key, path in paths.items()}
observed["stage1_export_sha256"] = klean_export.tree_digest(Path("/reference/k-proof"))
observed["generated_tree_sha256"] = klean_export.tree_digest(
    Path("/reference/klean-generation/generated")
)
observed["discovery_manifest_sha256"] = hashlib.sha256(
    Path("/reference/lemma-discovery.json").read_bytes()
).hexdigest()
print("AUDIT_INPUT_VERIFY: PASS")
print("AUDIT_INPUT_CANONICAL_SHA256:", canonical_hash)
print(
    "AUDIT_INPUT_COPY_SHA256:",
    hashlib.sha256(Path("/audit-output/audit-input.json").read_bytes()).hexdigest(),
)
print("AUDIT_INPUT_ROOT_SHA256:", hashlib.sha256(audit_path.read_bytes()).hexdigest())
print("MODE_ENV:", os.environ.get("AUDIT_MODE"))
print("MODE_JSON:", resolution["mode"])
print("RECORDED_VS_OBSERVED_HASHES:")
for key in sorted(observed):
    print(
        key,
        "recorded=" + str(recorded[key]),
        "observed=" + observed[key],
        "match=" + str(recorded[key] == observed[key]),
    )
source_hashes = {
    path.relative_to("/reference/k-proof").as_posix(): pipeline_contract.sha256_file(path)
    for path in pipeline_contract._walk_regular_files(
        Path("/reference/k-proof"), "Stage 1 source workspace"
    )
}
expected = resolution["stage1_source_hashes"]
print("STAGE1_SOURCE_HASH_COUNT:", len(source_hashes))
print("STAGE1_SOURCE_MANIFEST_COUNT:", len(expected))
print("STAGE1_SOURCE_KEYS_EQUAL:", set(source_hashes) == set(expected))
print("STAGE1_SOURCE_HASHES_EQUAL:", source_hashes == expected)
producer = Path("/reference/generation-tools")
source_manifest = json.loads((producer / "source-manifest.json").read_text())
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
image_generator = generator["provenance"]["generator_image_id"]
image_source = source_manifest["generator_image_id"]
image_input_path = Path(resolution["generation_producer_sources"]).name
print(
    "PRODUCER_FILE_SET:",
    sorted(
        path.relative_to(producer).as_posix()
        for path in pipeline_contract._walk_regular_files(producer, "producer")
    ),
)
for name, field in (("klean_export.py", "exporter_sha256"), ("klean.py", "klean_py_sha256")):
    digest = hashlib.sha256((producer / name).read_bytes()).hexdigest()
    print(
        "PRODUCER",
        name,
        "observed=" + digest,
        "source_manifest=" + source_manifest["files"][name],
        "generator_manifest=" + generator[field],
        "all_match=" + str(digest == source_manifest["files"][name] == generator[field]),
    )
print("GENERATOR_IMAGE_ID_GENERATOR:", image_generator)
print("GENERATOR_IMAGE_ID_SOURCE:", image_source)
print("GENERATOR_IMAGE_ID_AUDIT_PATH_KEY:", "sha256:" + image_input_path)
print(
    "GENERATOR_IMAGE_IDS_MATCH:",
    image_generator == image_source == "sha256:" + image_input_path,
)
print("PRODUCER_TREE_RECORDED:", recorded["generation_producer_sources_sha256"])
print("PRODUCER_TREE_OBSERVED:", observed["generation_producer_sources_sha256"])
print(
    "PRODUCER_TREE_MATCH:",
    recorded["generation_producer_sources_sha256"]
    == observed["generation_producer_sources_sha256"],
)
