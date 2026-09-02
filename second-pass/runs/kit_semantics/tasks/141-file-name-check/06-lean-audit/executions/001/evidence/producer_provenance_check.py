#!/usr/bin/env python3
import hashlib
import json
import stat
from pathlib import Path

from tools import pipeline_contract


AUDIT_INPUT = Path("/audit-input.json")
BUNDLE = Path("/reference/generation-tools")
GENERATOR_MANIFEST = Path("/reference/klean-generation/generator-manifest.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads(AUDIT_INPUT.read_text())
source_manifest = json.loads((BUNDLE / "source-manifest.json").read_text())
generator = json.loads(GENERATOR_MANIFEST.read_text())

expected_names = {"source-manifest.json", "klean_export.py", "klean.py"}
observed_names = {path.name for path in BUNDLE.iterdir()}
file_kinds = {
    path.name: {
        "regular": stat.S_ISREG(path.stat(follow_symlinks=False).st_mode),
        "symlink": path.is_symlink(),
    }
    for path in BUNDLE.iterdir()
}
observed_files = {
    name: sha256(BUNDLE / name) for name in ("klean_export.py", "klean.py")
}
manifest_files = source_manifest["files"]
generator_files = {
    "klean_export.py": generator["exporter_sha256"],
    "klean.py": generator["klean_py_sha256"],
}
source_image = source_manifest["generator_image_id"]
generator_image = generator["provenance"]["generator_image_id"]
audit_bundle_path = Path(audit["resolution"]["generation_producer_sources"])
audit_image = f"sha256:{audit_bundle_path.name}"
observed_tree = pipeline_contract.sha256_tree(BUNDLE)
audit_tree = audit["resolution"]["hashes"][
    "generation_producer_sources_sha256"
]

checks = {
    "bundle_has_exact_expected_names": observed_names == expected_names,
    "bundle_entries_are_regular_non_symlinks": all(
        item["regular"] and not item["symlink"] for item in file_kinds.values()
    ),
    "observed_hashes_equal_source_manifest": observed_files == manifest_files,
    "observed_hashes_equal_generator_manifest": observed_files == generator_files,
    "source_manifest_equal_generator_manifest": manifest_files == generator_files,
    "image_id_source_equal_generator": source_image == generator_image,
    "image_id_source_equal_audit_input_path": source_image == audit_image,
    "producer_tree_equal_audit_input": observed_tree == audit_tree,
}

result = {
    "observed_files": observed_files,
    "source_manifest_files": manifest_files,
    "generator_manifest_files": generator_files,
    "source_manifest_image_id": source_image,
    "generator_manifest_image_id": generator_image,
    "audit_input_image_id_from_bundle_path": audit_image,
    "observed_bundle_tree_sha256": observed_tree,
    "audit_input_bundle_tree_sha256": audit_tree,
    "bundle_names": sorted(observed_names),
    "bundle_file_kinds": file_kinds,
    "checks": checks,
    "overall": "PASS" if all(checks.values()) else "FAIL",
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if all(checks.values()) else 1)
