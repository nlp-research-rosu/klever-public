#!/usr/bin/env bash
set -euo pipefail

work=$(mktemp -d /tmp/audit-work/stage4-regeneration.XXXXXX)
mkdir -p "$work/reproducer/tools"
cp /reference/generation-tools/klean_export.py "$work/reproducer/tools/"
cp /reference/generation-tools/klean.py "$work/reproducer/tools/"

echo "work=$work"
echo "COMMAND sha256sum authenticated producer copies"
sha256sum \
  "$work/reproducer/tools/klean_export.py" \
  "$work/reproducer/tools/klean.py"

export PATH=/tmp/audit-work/tool-bin:$PATH
export PYTHONPATH="$work/reproducer:/reference"
echo "COMMAND python3 authenticated-klean_export.py --input /reference/k-proof --discovery-manifest /reference/lemma-discovery.json --output TEMP/generation --problem 78-hex-key --generator-image-id sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda --toolchain-lock /reference/klean-toolchain.lock.json"
python3 "$work/reproducer/tools/klean_export.py" \
  --input /reference/k-proof \
  --discovery-manifest /reference/lemma-discovery.json \
  --output "$work/generation" \
  --problem 78-hex-key \
  --generator-image-id sha256:e18301a8220fb0b62fabf56feffcb5e621049daa7c7a0b79eacb60cae5e57fda \
  --toolchain-lock /reference/klean-toolchain.lock.json
echo "exit_code=$?"

echo "COMMAND compare regenerated and selected generated project trees"
python3 - "$work/generation/generated" <<'PY'
from pathlib import Path
import sys
from tools.klean_export import tree_digest

selected = Path("/reference/klean-generation/generated")
regenerated = Path(sys.argv[1])
selected_hash = tree_digest(selected)
regenerated_hash = tree_digest(regenerated)
print(f"selected_generated_tree_sha256={selected_hash}")
print(f"regenerated_generated_tree_sha256={regenerated_hash}")
if selected_hash != regenerated_hash:
    raise SystemExit("generated tree hashes differ")
PY
diff -ru \
  /reference/klean-generation/generated \
  "$work/generation/generated"
echo "generated_tree_diff_exit=$?"

echo "COMMAND compare deterministic sidecars"
for sidecar in generator-manifest.json trust-inventory.json export-result.json; do
  sha256sum \
    "/reference/klean-generation/$sidecar" \
    "$work/generation/$sidecar"
  cmp -s \
    "/reference/klean-generation/$sidecar" \
    "$work/generation/$sidecar"
  echo "$sidecar cmp_exit=$?"
done

echo "COMMAND compare input manifest after normalizing mount-specific required_k_files"
python3 - "$work/generation/input-manifest.json" <<'PY'
import json
from pathlib import Path
import sys

selected = json.loads(
    Path("/reference/klean-generation/input-manifest.json").read_text()
)
regenerated = json.loads(Path(sys.argv[1]).read_text())
selected["required_k_files"] = [
    Path(path).name for path in selected["required_k_files"]
]
regenerated["required_k_files"] = [
    Path(path).name for path in regenerated["required_k_files"]
]
print(
    "normalized_input_manifest_equal="
    + str(selected == regenerated).lower()
)
if selected != regenerated:
    raise SystemExit("normalized input manifests differ")
PY

echo "stage4_regeneration_match=true"
