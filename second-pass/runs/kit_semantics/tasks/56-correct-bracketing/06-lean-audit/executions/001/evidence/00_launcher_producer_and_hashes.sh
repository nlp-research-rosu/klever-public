#!/usr/bin/env bash
set -o errexit -o nounset -o pipefail

printf 'COMMAND: printf AUDIT_MODE from environment\n'
printf 'AUDIT_MODE=%s\n' "${AUDIT_MODE-<unset>}"

printf '\nCOMMAND: test candidate presence and type\n'
if [[ -e /candidate || -L /candidate ]]; then
  stat -c 'candidate exists: type=%F mode=%a path=%n' /candidate
else
  printf 'candidate absent\n'
fi

printf '\nCOMMAND: sha256sum producer files and producer source manifest\n'
sha256sum \
  /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json

printf '\nCOMMAND: display producer source manifest\n'
python -m json.tool /reference/generation-tools/source-manifest.json

printf '\nCOMMAND: display Stage 4 generator manifest\n'
python -m json.tool /reference/klean-generation/generator-manifest.json

printf '\nCOMMAND: extract launcher producer/image/hash bindings\n'
python - <<'PY'
import json
from pathlib import Path

audit = json.loads(Path('/audit-input.json').read_text())
resolution = audit['resolution']
print(json.dumps({
    'audit_mode_environment': __import__('os').environ.get('AUDIT_MODE'),
    'resolution.mode': resolution['mode'],
    'resolution.semantics_mode': resolution['semantics_mode'],
    'resolution.selection_status': resolution['selections']['klean_generation']['status'],
    'resolution.generation_producer_sources': resolution['generation_producer_sources'],
    'resolution.hashes.generation_producer_sources_sha256': resolution['hashes']['generation_producer_sources_sha256'],
    'resolution.hashes.generated_tree_sha256': resolution['hashes']['generated_tree_sha256'],
    'resolution.hashes.klean_generation_sha256': resolution['hashes']['klean_generation_sha256'],
    'resolution.hashes.k_workspace_sha256': resolution['hashes']['k_workspace_sha256'],
    'resolution.hashes.stage1_export_sha256': resolution['hashes']['stage1_export_sha256'],
}, indent=2, sort_keys=True))
PY

printf '\nCOMMAND: recompute pipeline tree hashes with trusted code\n'
PYTHONPATH=/reference python - <<'PY'
from pathlib import Path
from tools.klean_export import tree_digest
from tools.pipeline_contract import sha256_tree

for path in (
    Path('/reference/generation-tools'),
    Path('/reference/k-proof'),
    Path('/reference/klean-generation'),
    Path('/reference/klean-generation/generated'),
):
    print(f'pipeline_contract.sha256_tree({path}) = {sha256_tree(path)}')
for path in (
    Path('/reference/k-proof'),
    Path('/reference/klean-generation/generated'),
):
    print(f'klean_export.tree_digest({path}) = {tree_digest(path)}')
PY

printf '\nCOMMAND: authenticate exact file set, hashes, image ID, and launcher tree binding\n'
PYTHONPATH=/reference python - <<'PY'
import hashlib
import json
import os
from pathlib import Path
from tools.pipeline_contract import sha256_tree

bundle = Path('/reference/generation-tools')
source = json.loads((bundle / 'source-manifest.json').read_text())
generator = json.loads(Path('/reference/klean-generation/generator-manifest.json').read_text())
audit = json.loads(Path('/audit-input.json').read_text())['resolution']
expected_names = {'source-manifest.json', 'klean_export.py', 'klean.py'}
observed_names = {p.name for p in bundle.iterdir()}
checks = {
    'audit_mode_matches_environment': audit['mode'] == os.environ.get('AUDIT_MODE'),
    'producer_exact_file_set': observed_names == expected_names,
    'source_manifest_schema': source.get('schema_version') == 1,
    'source_manifest_image_matches_generator': source.get('generator_image_id') == generator.get('provenance', {}).get('generator_image_id'),
    'launcher_path_image_key_matches_generator': Path(audit['generation_producer_sources']).name == generator.get('provenance', {}).get('generator_image_id', '').removeprefix('sha256:'),
    'source_manifest_files_match_generator': source.get('files') == {
        'klean_export.py': generator.get('exporter_sha256'),
        'klean.py': generator.get('klean_py_sha256'),
    },
    'launcher_producer_tree_hash': sha256_tree(bundle) == audit['hashes']['generation_producer_sources_sha256'],
}
for name in ('klean_export.py', 'klean.py'):
    observed = hashlib.sha256((bundle / name).read_bytes()).hexdigest()
    checks[f'{name}_hash_matches_source_manifest'] = observed == source['files'][name]
    manifest_key = 'exporter_sha256' if name == 'klean_export.py' else 'klean_py_sha256'
    checks[f'{name}_hash_matches_generator_manifest'] = observed == generator[manifest_key]
for key, value in checks.items():
    print(f'{key}: {value}')
if not all(checks.values()):
    raise SystemExit('PRODUCER_AUTHENTICATION_FAILED')
print('PRODUCER_AUTHENTICATION: PASS')
PY
