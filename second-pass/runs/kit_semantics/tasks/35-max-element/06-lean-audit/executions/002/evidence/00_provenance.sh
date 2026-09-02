#!/usr/bin/env bash
set -euo pipefail
set -x

sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json

python3 - <<'PY'
import json
from pathlib import Path

paths = [
    Path('/reference/generation-tools/source-manifest.json'),
    Path('/reference/klean-generation/generator-manifest.json'),
]
for path in paths:
    document = json.loads(path.read_text())
    print(f'### {path}')
    if path.name == 'source-manifest.json':
        print(json.dumps(document, indent=2, sort_keys=True))
    else:
        print(json.dumps({
            'exporter_sha256': document.get('exporter_sha256'),
            'klean_py_sha256': document.get('klean_py_sha256'),
            'generator_image_id': document.get('provenance', {}).get('generator_image_id'),
            'generated_tree_sha256': document.get('generated_tree_sha256'),
            'inventory_sha256': document.get('provenance', {}).get('inventory_sha256'),
            'stage1_workspace_sha256': document.get('provenance', {}).get('stage1_workspace_sha256'),
            'stage3_discovery_manifest_sha256': document.get('provenance', {}).get('stage3_discovery_manifest_sha256'),
            'obligation_count': document.get('obligation_count'),
            'obligation_map_sha256': document.get('obligation_map_sha256'),
            'target': document.get('target'),
            'toolchain': document.get('toolchain'),
        }, indent=2, sort_keys=True))

audit = json.loads(Path('/audit-input.json').read_text())
resolution = audit['resolution']
print('### /audit-input.json focused fields')
print(json.dumps({
    'mode': resolution.get('mode'),
    'problem_id': resolution.get('problem_id'),
    'condition': resolution.get('condition'),
    'semantics_mode': resolution.get('semantics_mode'),
    'generation_producer_sources': resolution.get('generation_producer_sources'),
    'hashes': resolution.get('hashes'),
}, indent=2, sort_keys=True))
PY
