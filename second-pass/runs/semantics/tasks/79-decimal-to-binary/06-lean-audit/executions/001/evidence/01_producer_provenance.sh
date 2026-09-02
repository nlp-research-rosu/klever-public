#!/usr/bin/env bash
set -euo pipefail

echo '$ sha256sum /reference/generation-tools/klean_export.py /reference/generation-tools/klean.py /reference/generation-tools/source-manifest.json /reference/klean-generation/generator-manifest.json /audit-input.json'
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /audit-input.json

echo '$ PYTHONPATH=/reference python3 - <<PY  # print provenance fields and trusted tree digest'
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree

audit = json.loads(Path("/audit-input.json").read_text())
source = json.loads(Path("/reference/generation-tools/source-manifest.json").read_text())
generator = json.loads(Path("/reference/klean-generation/generator-manifest.json").read_text())
resolution = audit["resolution"]

print("AUDIT_MODE =", resolution["mode"])
print("audit_input.generation_producer_sources =", resolution["generation_producer_sources"])
print("audit_input.generation_producer_sources_sha256 =", resolution["hashes"]["generation_producer_sources_sha256"])
print("audit_input.image_from_producer_path =", Path(resolution["generation_producer_sources"]).name)
print("source_manifest.generator_image_id =", source["generator_image_id"])
print("source_manifest.files =", json.dumps(source["files"], sort_keys=True))
print("generator_manifest.provenance.generator_image_id =", generator["provenance"]["generator_image_id"])
print("generator_manifest.exporter_sha256 =", generator["exporter_sha256"])
print("generator_manifest.klean_py_sha256 =", generator["klean_py_sha256"])
print("actual_generation_tools_pipeline_tree_sha256 =", sha256_tree(Path("/reference/generation-tools")))
print("actual_generation_tools_export_tree_sha256 (different algorithm, informational) =", tree_digest(Path("/reference/generation-tools")))

actual_exporter = __import__("hashlib").sha256(
    Path("/reference/generation-tools/klean_export.py").read_bytes()
).hexdigest()
actual_klean = __import__("hashlib").sha256(
    Path("/reference/generation-tools/klean.py").read_bytes()
).hexdigest()
image_key = source["generator_image_id"].removeprefix("sha256:")
assert actual_exporter == source["files"]["klean_export.py"] == generator["exporter_sha256"]
assert actual_klean == source["files"]["klean.py"] == generator["klean_py_sha256"]
assert source["generator_image_id"] == generator["provenance"]["generator_image_id"]
assert image_key == Path(resolution["generation_producer_sources"]).name
assert sha256_tree(Path("/reference/generation-tools")) == resolution["hashes"]["generation_producer_sources_sha256"]
assert set(path.name for path in Path("/reference/generation-tools").iterdir()) == {
    "klean_export.py", "klean.py", "source-manifest.json"
}
print("PRODUCER_PROVENANCE_CHECK = PASS")
PY
