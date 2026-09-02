# Audit command ledger

All paths below were invoked from `/audit-output` unless a different working
directory is shown. The numbered `.log` files contain the raw combined output
and `script(1)` exit code.

## Audit input and producer provenance

```sh
env | rg '^AUDIT_MODE='
sed -n '1,260p' /audit-input.json
sha256sum /reference/generation-tools/klean_export.py \
  /reference/generation-tools/klean.py \
  /reference/generation-tools/source-manifest.json \
  /reference/klean-generation/generator-manifest.json \
  /reference/klean-generation/input-manifest.json \
  /reference/lemma-discovery.json \
  /reference/k-proof/verification.k
PYTHONPATH=/reference python3 \
  /audit-output/evidence/provenance_hash_audit.py
```

Results: `00_audit_mode.log`, `01_audit_input.log`, `03_direct_hashes.log`,
`04_source_manifest.log`, `05_generator_manifest.log`,
`06_generation_input_manifest.log`, and `08_provenance_hash_audit.log`.

## Stage 3 reconstruction and K semantic checks

```sh
PYTHONPATH=/reference python3 \
  /audit-output/evidence/stage3_inventory_audit.py
```

Result: `07_stage3_inventory_audit.log`.

Fresh K workspace setup:

```sh
mkdir -p /tmp/audit-work/k-classification-check
cp /reference/k-proof/semantic.k \
  /tmp/audit-work/k-classification-check/semantic.k
cp /reference/k-proof/verification.k \
  /tmp/audit-work/k-classification-check/verification.k
cp /reference/k-proof/solution.mpy \
  /tmp/audit-work/k-classification-check/solution.mpy
```

From `/tmp/audit-work/k-classification-check`:

```sh
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw("")' --output pretty
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw(")")' --output pretty
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw("(()")' --output pretty
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw("())")' --output pretty
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw("( ) (( )) (( )( ))")' --output pretty
krun solution.mpy --definition verification-kompiled \
  -cINPUT='Raw(" (()) () ")' --output pretty
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --output pretty
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --output pretty
```

Results: `10_fresh_kompile.log` through `16_krun_spaced.log`,
`26_fresh_kprove.log`, and `27_false_postcondition_kprove.log`. The last
command is deliberately expected to exit 1 with a stuck implication.
`25_frozen_sources.log` preserves the numbered frozen source used for the
manual operational comparison.

## Stage 4 preflight and manifest checks

The initial exact call was:

```sh
PYTHONPATH=/reference python3 -c '
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
'
```

It reached `lake clean` but exposed the managed PID/procfs mismatch recorded in
`17_fresh_check_generation.log`. `18_environment.log` through
`21_pid_namespace_workaround.log` record the diagnosis. The workaround library
was built with:

```sh
cc -shared -fPIC /tmp/audit-work/hostpid_preload.c \
  -o /tmp/audit-work/libhostpid_preload.so
```

The exact source is preserved as `evidence/hostpid_preload.c`.

The unchanged trusted call was rerun with only the process-identity workaround
inherited by Lake/Lean:

```sh
PYTHONPATH=/reference \
LD_PRELOAD=/tmp/audit-work/libhostpid_preload.so \
python3 -c '
import json
from pathlib import Path
from tools.klean_preflight import check_generation
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
'
```

Result: `22_fresh_check_generation.log` (`KLEAN_NO_OBLIGATIONS`, exit 0).

The independent sidecar/target audit was:

```sh
PYTHONPATH=/reference python3 \
  /audit-output/evidence/stage4_manifest_audit.py
```

Results: `23_stage4_sidecars.log` and `24_stage4_manifest_audit.log`.
