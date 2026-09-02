# Audit commands

All mounted candidate/provenance paths were read only. The only compiled local
helper is the narrow `/proc` compatibility shim preserved as
`lean_proc_exe_shim.c`.

## Reconcile hashes, inventory, manifests, obligations, and target

```sh
PYTHONPATH=/reference AUDIT_MODE="$AUDIT_MODE" \
  python3 /audit-output/evidence/reconcile.py \
  > /audit-output/evidence/reconciliation.json
```

## Raw producer provenance and canonical inventory

```sh
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.pipeline_contract import sha256_tree
source = json.loads(Path('/reference/generation-tools/source-manifest.json').read_text())
generator = json.loads(Path('/reference/klean-generation/generator-manifest.json').read_text())
audit = json.loads(Path('/audit-input.json').read_text())['resolution']
print('producer_bundle_pipeline_sha256=' + sha256_tree(Path('/reference/generation-tools')))
print('source_manifest_image_id=' + source['generator_image_id'])
print('generator_manifest_image_id=' + generator['provenance']['generator_image_id'])
print('audit_input_producer_path_basename=' + Path(audit['generation_producer_sources']).name)
print('audit_input_producer_bundle_sha256=' + audit['hashes']['generation_producer_sources_sha256'])
PY
```

The output is in `producer-provenance.txt`.

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.k_rule_inventory import inventory_verification
print(json.dumps(inventory_verification(Path('/reference/k-proof')), indent=2, sort_keys=True))
PY
```

The output is in `inventory.json`.

## Required preflight: first attempt

```sh
PYTHONPATH=/reference python3 - <<'PY'
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
)
print(json.dumps(result, indent=2, sort_keys=True))
PY
```

The exact failure is recorded in `preflight-initial-failure.txt`. Investigation
showed that this audit container's namespace-local PID is absent from the
mounted `/proc`; Lean 4.22 calls `readlink("/proc/<pid>/exe", ...)`, whereas
`/proc/self/exe` remains valid.

## Compile and check the narrow PID-namespace shim

```sh
cc -shared -fPIC -O2 /audit-output/evidence/lean_proc_exe_shim.c \
  -o /tmp/audit-work/lean_proc_exe_shim.so
LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lean --version
LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake --version
```

## Required preflight: successful rerun with pinned toolchain

```sh
LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so \
LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0 \
LEAN=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lean \
PYTHONPATH=/reference \
python3 -c "import json; from pathlib import Path; from tools.klean_preflight import check_generation; print(json.dumps(check_generation(Path('/reference/k-proof'), Path('/reference/lemma-discovery.json'), Path('/reference/klean-generation'), toolchain_lock=Path('/reference/klean-toolchain.lock.json')), indent=2, sort_keys=True))" \
  > /audit-output/evidence/preflight-result.json
```

## Confirm no-obligation structure

```sh
python3 - <<'PY'
import json
from pathlib import Path
fresh = json.loads(Path('/audit-output/evidence/preflight-result.json').read_text())
recorded = json.loads(Path('/reference/klean-generation/preflight.json').read_text())
print('fresh_equals_recorded=', fresh == recorded, sep='')
print('fresh_status=', fresh['status'], sep='')
print('lake_clean_exit=', fresh['diagnostics'][0]['exit_code'], sep='')
print('lake_build_exit=', fresh['diagnostics'][1]['exit_code'], sep='')
print('obligation_count=', fresh['obligation_count'], sep='')
print('target=', json.dumps(fresh['target']), sep='')
PY
rg -n --glob '*.lean' '^\s*def\s+targetStatement\b' \
  /reference/klean-generation/generated || true
if test -e /candidate; then
  printf 'candidate_exists=yes\n'
else
  printf 'candidate_exists=no\n'
fi
```
