import hashlib
import json
from pathlib import Path

from tools.pipeline_contract import sha256_tree


root = Path("/reference/generation-tools")
audit = json.loads(Path("/audit-input.json").read_text())
source = json.loads((root / "source-manifest.json").read_text())
generator = json.loads(
    Path("/reference/klean-generation/generator-manifest.json").read_text()
)
actual = {
    path.name: hashlib.sha256(path.read_bytes()).hexdigest()
    for path in (root / "klean_export.py", root / "klean.py")
}
recorded_source_path = Path(
    audit["resolution"]["generation_producer_sources"]
)
audit_image = f"sha256:{recorded_source_path.name}"
result = {
    "hash_algorithm": "tools.pipeline_contract.sha256_tree",
    "actual_file_sha256": actual,
    "source_manifest_files": source["files"],
    "generator_manifest_exporter_sha256": generator["exporter_sha256"],
    "generator_manifest_klean_py_sha256": generator["klean_py_sha256"],
    "source_manifest_generator_image_id": source["generator_image_id"],
    "generator_manifest_generator_image_id": generator["provenance"][
        "generator_image_id"
    ],
    "audit_input_generator_image_id_from_recorded_source_path": audit_image,
    "actual_source_tree_sha256": sha256_tree(root),
    "audit_input_source_tree_sha256": audit["resolution"]["hashes"][
        "generation_producer_sources_sha256"
    ],
}
result["all_match"] = (
    actual == source["files"]
    and actual["klean_export.py"] == generator["exporter_sha256"]
    and actual["klean.py"] == generator["klean_py_sha256"]
    and source["generator_image_id"]
    == generator["provenance"]["generator_image_id"]
    == audit_image
    and result["actual_source_tree_sha256"]
    == result["audit_input_source_tree_sha256"]
)

print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["all_match"] else 1)
